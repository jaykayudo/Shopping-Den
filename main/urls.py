from django.urls import path
from . import views
from . import admin
from django.views.generic import TemplateView

urlpatterns = [
    path("",views.home,name="index"),
    path("about/",TemplateView.as_view(template_name = "about.html"),name="about"),
    path("login/",views.LoginView.as_view(),name="login"),
    path("logout/",views.loguserout,name="logout"),
    path("signup/",views.SignUpView.as_view(),name="signup"),
    path("sell/",views.CreatePostView.as_view(),name="sell"),
    path("user-profile/",views.UserProfile.as_view(),name="profile"),
    path("user-profile/change-password/",views.UserPasswordChangeView.as_view(),name="password-change"),
    path("goods/",views.AllProductView.as_view(),name="goods"),
    path("goods/<int:id>/",views.details,name="details"),
    path("posts/<int:id>/delete/",views.DeletePostView.as_view(),name="delete-post"),
    path("posts/save-item/",views.SaveItemView.as_view(),name="save-item"),
    path("posts/<int:id>/save-item/delete/",views.DeleteSavedPostView.as_view(),name="delete-saved-item"),
    path("goods/search/",views.search,name="search"),
    path("404-test/",views.handler_404,name="404-handler"),

    #admin
    path("admin/", admin.main_admin.urls,name="admin"),
]
