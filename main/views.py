from django.shortcuts import render,get_object_or_404, redirect
from django.views.generic import FormView, View, ListView, DetailView
from .forms import LoginForm, SignUpForm, ProductCreateForm
from django.contrib.auth import login, logout, update_session_auth_hash,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ProductImage, User,ProductTag,Product, SavedProduct
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordResetView,PasswordResetConfirmView,PasswordChangeView
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseBadRequest
from django.db.models import Q
from django.core import paginator
from datetime import datetime,timedelta



# Create your views here.
def home(request):
    tags = ProductTag.objects.all().order_by('name')
    recent_product = Product.objects.recent()
    location = request.GET.get('location')
    if location and (location == "unn" or location == "unec" or location == "all"):
        request.session['location'] = location
        if location == "all":
            recent_product = Product.objects.recent()
        else:
            recent_product = Product.objects.recent(location)
    content = {
        "products":recent_product,
        "tags":tags
    }
    
    return render(request,"index.html",content)

def details(request,id):
    objectdetail = get_object_or_404(Product,id = id)
    return render(request,"details.html",{"object":objectdetail})
class UserProfile(LoginRequiredMixin,View):
    def get(self,request):
        content = {}
        posts = Product.objects.filter(user=request.user).order_by("-date_uploaded")
        user = User.objects.get(id = request.user.id)
        saved_product = user.savedproduct_set.all()
        form = PasswordChangeForm(user= request.user)
        content['posts'] = posts
        content['saved_products'] = saved_product
        content['form'] = form
        return render(request,"main/profile.html",content)
    def post(self,request):
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request,_("Password Changed"))
            return redirect(reverse('profile'))
        content = {}
        posts = Product.objects.filter(user=request.user).order_by("-date_uploaded")
        user = User.objects.get(id = request.user.id)
        saved_product = user.savedproduct_set.all()
        content['posts'] = posts
        content['saved_products'] = saved_product
        content['form'] = form
        return render(request,"main/profile.html",content)

"""
    Authentications 
"""

class LoginView(FormView):
    form_class = LoginForm
    template_name = "login.html"
    def get_success_url(self):
        url = self.request.GET.get("next",reverse('profile'))
        return url
    def form_valid(self,form):
        response = super().form_valid(form)
        user = form.get_user()
        login(self.request,user)
        messages.success(self.request,"Login Successful")
        return response

class SignUpView(FormView):
    form_class = SignUpForm
    template_name = "signup.html"
    def get_success_url(self):
        url = self.request.GET.get("next",reverse('profile'))
        return url
    def form_valid(self,form):
        response = super().form_valid(form)
        user = form.save()
        auth_user = authenticate(self.request,email = user.email,password=user.password)
        if auth_user:
            login(self.request,auth_user)
        messages.success(self.request,"Account Registered Successfully")
        return response


"""
    Product Related
"""
class CreatePostView(LoginRequiredMixin,FormView):
    form_class = ProductCreateForm
    template_name = "main/product-create-form.html"
    
    def get_success_url(self):
        id = None
        url = '/'
        if "recent_post_id" in self.request.session:
            id = self.request.session['recent_post_id']
            del self.request.session['recent_post_id']
        if id:
            url = reverse("details",kwargs={"id":id})
        return url
    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        tags = ProductTag.objects.all()
        context['tags'] = tags
        return context
    def form_valid(self,form):
        response = super().form_valid(form)
        obj = form.save(commit = False)
        obj.user = self.request.user
        if not form.cleaned_data.get('phone_number') and not self.request.user.is_superuser:
            obj.phone_number = self.request.user.phone_number
        obj.save()
        category = form.cleaned_data.get('category')
        if category:
            category_list = category.split(',')
            category_list = set(category_list)
            for y in category_list:
                product_tag = ProductTag.objects.get(id = int(y))
                obj.tag.add(product_tag)
        obj.save()
        files = self.request.FILES.getlist('file')
        for x in files:
            image = ProductImage.objects.create(product=obj, image = x)
            image.save()
        self.request.session['recent_post_id'] = obj.id
        messages.success(self.request,"Sucessfully Uploaded an Item")
        return response
class AllProductView(ListView):
    paginate_by = 24
    template_name = "product.html"
    def get_queryset(self):
        products = ""
        tag = self.request.GET.get('tag')
        self.request.session['filter'] = self.request.GET.get('filter')
        if self.request.GET.get("filter"):
            if self.request.GET.get("filter") == "asc":
                products = Product.objects.filter(active=True).order_by("name")
            elif self.request.GET.get("filter") == "desc":
                products = Product.objects.filter(active=True).order_by("-name")
            elif self.request.GET.get("filter") == "latest":
                products = Product.objects.filter(active=True).order_by("-date_uploaded")
            elif self.request.GET.get("filter") == "oldest":
                products = Product.objects.filter(active=True).order_by("date_uploaded")
        else:
            products = Product.objects.filter(active= True).order_by("-date_uploaded")
        location = self.request.session.get("location")
        if tag:
            products = products.filter(tag__name = tag)
        if location and location != "all" and products:
            products = products.filter(location = location.upper())
        return products
class DeletePostView(LoginRequiredMixin,View):
    def get(self,request,id):
        post = get_object_or_404(Product,id = id)
        if post.user != request.user:
            return HttpResponseForbidden()
        post.delete()
        return redirect(reverse("profile"))
class DeleteSavedPostView(LoginRequiredMixin,View):
    def get(self,request,id):
        post = get_object_or_404(SavedProduct,id = id)
        if post.user != request.user:
            return HttpResponseForbidden()
        post.delete()
        messages.success(request,_('Item unsaved'))
        return redirect(reverse("profile"))

class MakeAvailablePostView(LoginRequiredMixin,View):
    def get(self,request,id):
        post = get_object_or_404(Product,id = id)
        if post.user != request.user:
            return HttpResponseForbidden()
        if post.available:
            post.available = True
        else:
            post.available = False
        post.save()
        return redirect(reverse('profile'))

class SaveItemView(View):
    def get(self,request):
        id = request.GET.get('id')
        context ={'saved':False,'auth':True,'max':False,'id':id}
        
        if request.is_ajax() and id:
            if not request.user.is_authenticated:
                context['auth'] = False
                return JsonResponse(context,safe=False)
            product = get_object_or_404(Product,id = int(id))
            if SavedProduct.objects.filter(user = request.user,product = product).count() == 10:
                context['max'] = True
                return JsonResponse(context,safe=False)
            if SavedProduct.objects.filter(user = request.user,product = product):
                saved_item = SavedProduct.objects.get(user = request.user,product = product)
                saved_item.delete()
                context['saved'] = False
                return JsonResponse(context,safe=False)
            else:
                saved_item = SavedProduct.objects.create(user = request.user,product = product)
                saved_item.save()
                context['saved'] = True
                return JsonResponse(context,safe = True)
        else:
            messages.error(request,_("Could not save item"))
            return redirect(reverse("goods"))
            

# class Search(View):
#     """
#     A Search Algorithm that searches with price value or goods name or categories
#     """
#     def get(self,request):
#         search = request.GET.get("q")
#         all_search = []
#         a = ""
#         productsearch= None
#         tagsearch = None
#         if search is not None:
#             if search.isalpha:
#                 tagsearch = ProductTag.objects.filter(name__istartswith= search)
#                 if tagsearch:
#                     for _ in tagsearch:
#                         all_search.append(tagsearch)
#                 else:
                    
#                     productsearch = Product.objects.filter(name__icontains = search)

#                 if productsearch:
#                     for _ in productsearch:
#                         all_search.append(productsearch)
#             elif search.isnumeric:
#                 productsearch = Product.objects.filter(price__lte = int(search))
#                 for _ in productsearch:
#                     all_search.append(productsearch)
#             elif search.isalnum:
#                 search_array = search.split(" ")
#                 numeric_value = None
#                 alpha_value = None
#                 if search_array:
#                     for x in search_array:
#                         if x.isnumeric:
#                             numeric_value = x
#                             break
#                     for y in search_array:
#                         if y.isalpha:
#                             alpha_value = y
#                             break
#                     if alpha_value and numeric_value:
#                         tagsearch = ProductTag.objects.filter(name__istartwith = alpha_value)
#                         if tagsearch:
#                             for x in tagsearch:
#                                 product = Product.objects.filter(tag= x,price__lte = int(numeric_value)).order_by("-date_uploaded")
#                                 for y in product:
#                                     all_search.append(y)
#                         productsearch = Product.objects.filter(name = alpha_value,price__lte = int(numeric_value))
#                         if productsearch:
#                             for x in productsearch:
#                                 all_search.append(x)
#         return render(request,"search.html",{"result":all_search,'search_query':q})
def search(request):
    search = request.GET.get("q")
    if not search:
        return redirect(reverse('goods'))
    result = None
    page_num = request.GET.get("page")
    if page_num and page_num.isnumeric():
        page_num = int(page_num)
    else:
        page_num = 1
    result = Product.objects.filter(Q(tag__name__istartswith = search)|Q(name__icontains = search)|Q(location__istartswith = search )|Q(price = int(search)if search.isnumeric() else None ) )
    if result:
        page = paginator.Paginator(result,24)
        page_obj = page.page(page_num)
    else:
        page_obj = None
    return render(request,'search.html',{'page_obj': page_obj,'search':search})
class UserPasswordResetView(PasswordResetView):
    template_name = "account/passwordtemps/password-reset.html"
    success_url = reverse_lazy("login")
    email_template_name = "account/passwordtemps/password-reset-email.html"
    def form_valid(self,form):
        messages.success(self.request,_("Password reset email sent."))
        return super().form_valid(form)
class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "account/passwordtemps/password-reset-confirm.html"
    success_url = reverse_lazy("login")
    
    def form_valid(self,form):
        messages.success(self.request,_("Password reset successfully."))
        return super().form_valid(form)

class UserPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy("profile")
    def get(self,request,*args,**kwargs):
        return redirect(reverse('profile'))
    def form_valid(self,form):
        messages.success(self.request,_("Password changed."))
        return super().form_valid(form)
            
def loguserout(request):
    logout(request)
    return redirect(reverse('login'))



#hidden app function
def expire_posts():
    expired_posts = Product.objects.filter(active = True,expiring_date__gte = datetime.now())
    if expired_posts:
        for post in expired_posts:
            post.active = False
            post.save()

def delete_inactive_post():
    timeframe = timedelta(month=1)
    inactive_posts = Product.objects.filter(active = False,expiring_date__gte = datetime.now() - timeframe)
    if inactive_posts:
        for post in inactive_posts:
            post.delete()
    


"""
Error Handlers
"""

def handler_500(request):
    return render(request,"500.html")

def handler_404(request):
    return render(request,"404.html")
def handler_403(request,exception):
    return render(request,"403.html")