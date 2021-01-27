from django.urls import path
from . import views as user_views
from .views import home, detail
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", user_views.home, name = "home" ),
    path('detail/<int:pk>/', user_views.detail, name = "branch-detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)