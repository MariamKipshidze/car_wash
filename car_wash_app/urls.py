from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views 
from .views import home, detail, profile
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", user_views.home, name = "home" ),
    path("profile/", user_views.profile, name = "profile"),
    path("login/", auth_views.LoginView.as_view(template_name  = "car_wash_app/login.html"), name = "login"),
    path("logout/", auth_views.LogoutView.as_view(template_name = "car_wash_app/logout.html"), name = "logout"),
    path('detail/<int:pk>/', user_views.detail, name = "branch-detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)