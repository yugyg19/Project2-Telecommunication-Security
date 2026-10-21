from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from appsite import views

urlpatterns = [
    path("", views.home, name="home"),
    path("health/", views.health, name="health"),
    path("api/status/", views.api_status, name="api_status"),
    path("search/", views.search, name="search"),
    path("accounts/login/", auth_views.LoginView.as_view(
        template_name="appsite/login.html"
    ), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", views.profile, name="profile"),
    path("feedback/", views.feedback, name="feedback"),
    path("admin/", admin.site.urls),
]
