from django.urls import path
from . import views as user_views 
from .views import home, detail, profile, BranchCreateView, order_create, car_type_create
from .views import employee_profile, employee_register, BranchDeleteView, car_create
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", user_views.home, name="home"),
    path("company/profile/", user_views.profile, name="profile"),
    path('detail/<int:pk>/', user_views.detail, name="branch-detail"),
    path('employee/detail/', user_views.employee_profile, name="employee-detail"),
    path('employee/register/<int:pk>', user_views.employee_register, name="employee-register"),
    path("branch/new/", BranchCreateView.as_view(), name="branch-create"),
    path("order/new/", user_views.order_create, name="order-create"),
    path("branch/<int:pk>/delete/", BranchDeleteView.as_view(), name="branch-delete"),
    path('car/new/', user_views.car_create, name="car-register"),
    path('car/type/new/', user_views.car_type_create, name="car-type-register"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + \
                   static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
