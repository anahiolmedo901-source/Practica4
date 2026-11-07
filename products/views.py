from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from django.http import JsonResponse
from django.shortcuts import render

from .models import Category, Product, User
from .serializers import CategorySerializer, ProductSerializer, UserSerializer
from .services import obtener_estrategia  # Importamos la lógica de descuentos
                                            # Agregada en services.py
from .openapi import SCHEMA


def swagger_schema(request):
    return JsonResponse(SCHEMA)


def swagger_ui(request):
    return render(request, 'products/swagger.html')


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']
    permission_classes = [IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer

    def get_permissions(self):
        # El registro es público; la gestión completa de cuentas es solo para staff.
        return [AllowAny()] if self.action == 'create' else [IsAdminUser()]


class MyProfileView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# Endpoint Facade: precio final con descuento
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def precio_final(request, pk):
    producto = Product.objects.get(pk=pk)
    estrategia = obtener_estrategia(producto.category.name)
    precio_con_descuento = estrategia.calcular(float(producto.price))
    return Response({
        'producto': producto.name,
        'precio_original': producto.price,
        'precio_final': round(precio_con_descuento, 2)
    })
