from api.models import Category, Product, Sale
from rest_framework import serializers

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'description', 'filename', 'price']

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['name', 'address1', 'address2', 'city', 'state', 'zipcode', 'total', 'items', 'payment_intent']