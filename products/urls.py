from django.urls import path, include
from .views import CategoryViewSet, ProductViewSet, UserViewSet, MyProfileView
from rest_framework.routers import DefaultRouter
from .views import precio_final

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet, basename='categories')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('products/<int:pk>/precio-final/', precio_final),
    path('me/', MyProfileView.as_view(), name='my-profile'),
]
