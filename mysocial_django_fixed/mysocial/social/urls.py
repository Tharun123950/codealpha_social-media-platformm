
from django.urls import path
from . import views

urlpatterns = [
    path("", views.feed, name="feed"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("post/<int:pk>/like/", views.toggle_like, name="toggle_like"),
    path("u/<str:username>/", views.profile, name="profile"),
    path("u/<str:username>/follow/", views.follow_toggle, name="follow_toggle"),
    path("settings/profile/", views.edit_profile, name="edit_profile"),
]
