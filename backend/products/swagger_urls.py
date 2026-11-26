from django.urls import path
from .views import swagger_ui, swagger_schema

urlpatterns = [
    path('', swagger_ui, name='swagger-ui'),
    path('openapi.json', swagger_schema, name='openapi-schema'),
]
