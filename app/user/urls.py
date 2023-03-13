"""
URLS for user API
"""
from django.urls import path

from . import views

app_name = "user"

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create-user"),
    path("token/", views.CreateTokenView.as_view(), name="token"),
    path("current-user/", views.ManageUserView.as_view(), name="current-user"),
]
