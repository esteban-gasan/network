
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new_post, name="new-post"),
    path("profile/<int:pk>/", views.profile, name="profile"),
    path("following/", views.following, name="following"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),

    path("api/follow/<int:user_id>/", views.follow, name="follow"),
]
