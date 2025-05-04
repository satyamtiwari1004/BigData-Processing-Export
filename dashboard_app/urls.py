from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'accounts', views.AccountViewSet)
router.register(r'locations', views.LocationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('export/', views.export_data, name='export_data'),
] 