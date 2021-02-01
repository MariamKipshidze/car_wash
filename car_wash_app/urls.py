from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views 
from .views import home, detail, profile
from .views import employee_profile, employee_register, company_register
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", user_views.home, name = "home" ),
    path("accounts/profile/", user_views.profile, name = "profile"),
    path("login/", auth_views.LoginView.as_view(template_name  = "car_wash_app/login.html"), name = "login"),
    path("logout/", auth_views.LogoutView.as_view(template_name = "car_wash_app/logout.html"), name = "logout"),
    path('detail/<int:pk>/', user_views.detail, name = "branch-detail"),
    path('employee/detail/<int:pk>/', user_views.employee_profile, name = "employee-detail"),
    path('employee/register/<int:pk>', user_views.employee_register, name = "employee-register"),
    path('company/register/', user_views.company_register, name = "company-register"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)