"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from custom_auth import views as custom_auth_views
from sales import views as sales_views

router = DefaultRouter(trailing_slash=False)
router.register(r'auth-code', custom_auth_views.AuthCodeViewSet, basename='auth-code')
router.register(r'user', custom_auth_views.UserViewSet, basename='user')
router.register(r'products', sales_views.ProductViewSet, basename='products')
router.register(r'wallet', sales_views.WalletViewSet, basename='wallet')
router.register(r'orders', sales_views.OrderViewSet, basename='orders')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
