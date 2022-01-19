from django.contrib import admin
from .models import Product, ProductImage,User, SavedProduct,ProductTag
# Register your models here.
from django.contrib.auth.admin import Group, UserAdmin as DjangoUserAdmin
# admin.site.register(Product)
# admin.site.register(ProductTag)
# admin.site.register(ProductImage)
# admin.site.register(User)
# admin.site.register(SavedProduct)

class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None,{"fields":("email","password")}),
        ("Personal info",{"fields":("first_name","last_name")}),
        ("Permission",{"fields":("is_active","is_staff","is_superuser","groups","user_permissions")}),
        ("Important dates",{"fields":("last_login","date_joined")}),
    )
    add_fieldsets = ((None,{"classes":("wide",),"fields":("email","password1","password2")}))

    list_display = ("email","phone_number","is_active","is_staff")
    search_fields = ("email","phone_number")
    ordering = ("email",)
    actions = ("make_active","make_inactive")
    def make_active(self,request,queryset):
        queryset.update(is_active = True)
    def make_inactive(self,request,queryset):
        queryset.update(is_active = False)
    make_active.short_description = 'Make Selected Users Active'
    make_inactive.short_description = 'Make Selected Users Inactive'


class CustomizedAdmin(admin.sites.AdminSite):
    site_header = "Shopping Den Admin"
    site_header_color = "black"
    module_caption_color = "#03500d"
    site_title = "Shopping Den Admin"
    def each_context(self,request):
        context = super().each_context(request)
        context['site_header_color'] = getattr(self,'site_header_color',None)
        context['module_caption_color'] = getattr(self,'module_caption_color',None)
        return context
    def has_permission(self, request):
        return (request.user.is_active and request.user.is_superuser)

class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ("user",'id',"name","location","price","active","negotiable","available")
    list_filter = ("active","available","negotiable","location")
    autocomplete_fields = ("tag",) 
    search_fields = ("user","name","id")
    
    actions = ("make_active","make_inactive")
    
    def make_active(self,request,queryset):
        queryset.update(active = True)
    def make_inactive(self,request,queryset):
        queryset.update(active = False)
    make_active.short_description = 'Make Selected Items Active'
    make_inactive.short_description = 'Make Selected Items Inactive'
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product_user','product_name','image_size')
    search_fields = ('product_user','product_name')

    def product_name(self,obj):
        return obj.product.name
    def product_user(self,obj):
        return obj.product.user.email
    def image_size(self,obj):
        image_size = obj.image.size
        if image_size/ 1048576 > 1:
            size = int(image_size/1048576)
            image_size = str(size)+'MB'
        elif image_size/1024 > 1:
            size = int(image_size/1024)
            image_size = str(size)+'KB'
        return image_size
class SavedProductAdmin(admin.ModelAdmin):
    list_display = ('user','product')
    search_fields = ('user','product')

main_admin = CustomizedAdmin()
main_admin.register(Product,ProductAdmin)
main_admin.register(ProductTag,ProductTagAdmin)
main_admin.register(ProductImage,ProductImageAdmin)
main_admin.register(User,UserAdmin)
main_admin.register(SavedProduct,SavedProductAdmin)
main_admin.register(Group)