"""
URL configuration for diceandtiles project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as views2
from .drf import views
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="REST APIs",
        default_version='v1',
        description="API documentation for DiceAndTiles",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(
    r'products', views.ProductViewSet, basename="all products with jpg images")
router.register(
    r'productsweb', views.ProductwebViewSet, basename="all products with webp images")
router.register(
    r'fetchedproducts', views.Fetched_ProductViewSet, basename="fetched products")
router.register(
    r'register', views.RegisterViewSet, basename="register new user")
router.register(
    r'comment', views.CommentViewSet, basename="user comments")
router.register(
    r'vote', views.VoteViewSet, basename="cast a vote")
router.register(
    r'ownedproduct', views.OwnedProductViewSet, basename="list of owned games for user")




urlpatterns = [
    path('api/admin/', admin.site.urls),
    # path('api/register/', views.RegisterView, name='register'),
    path('api/login/', views2.obtain_auth_token),
    path("api/", include(router.urls)),


    ####swagger
    path('api/swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
