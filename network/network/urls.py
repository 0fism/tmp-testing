from django.urls import path, include

from . import views
from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("following", views.following, name="following"),   
    path("profile/<str:username>", views.profile, name="profile"),
    path("post_message", views.post_message, name="post_message"),
    
    path("like/<int:id>", views.like, name="like"),
    path("follow/<int:id>", views.follow, name="follow"),
    path("edit_post/<int:id>", views.edit_post, name="edit_post")

]
