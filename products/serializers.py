from rest_framework import serializers
from .models import Category, Product, User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'password')
        read_only_fields = ('id',)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if not password:
            raise serializers.ValidationError({'password': 'La contraseña es obligatoria.'})
        return User.objects.create_user(password=password, **validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attribute, value in validated_data.items():
            setattr(instance, attribute, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

""" class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()  # Muestra el nombre, no el ID

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'category') """
class ProductSerializer(serializers.ModelSerializer):
    # Campo de solo lectura para mostrar el nombre
    category_name = serializers.StringRelatedField(source='category', read_only=True)
    # Campo de escritura para aceptar el ID
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'category', 'category_name')
