from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import stripe

from api.models import Category, Product, Sale
from api.serializers import CategorySerializer, ProductSerializer, SaleSerializer


class CategoryList(APIView):
    '''Get all categories or create a category'''
    @csrf_exempt
    def get(self, request, format=None):
        cats = Category.object.all()
        if request.query_params.get('title'):
            cats = cats.filter(title__contains=request.query_params.get('title'))
        serializer = CategorySerializer(cats, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetail(APIView):
    '''Work with an individual Category object'''
    @csrf_exempt
    def get(self, request, pk, format=None):
        cat = Category.object.get(id=pk)
        serializer = CategorySerializer(cat)
        return Response(serializer.data)

    @csrf_exempt
    def put(self, request, pk, format=None):
        cat = Category.object.get(id=pk)
        serializer = CategorySerializer(cat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def delete(self, request, pk, format=None):
        cat = Category.object.get(id=pk)
        cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductList(APIView):
    '''Get all products or create a product'''
    @csrf_exempt
    def get(self, request, format=None):
        prods = Product.object.all()
        if request.query_params.get('name'):
            prods = prods.filter(name__contains=request.query_params.get('name'))
        if request.query_params.get('description'):
            prods = prods.filter(description__contains=request.query_params.get('description'))
        if request.query_params.get('filename'):
            prods = prods.filter(filename__contains=request.query_params.get('filename'))
        if request.query_params.get('price'):
            prods = prods.filter(price__contains=request.query_params.get('price'))
        if request.query_params.get('category'):
            prods = prods.filter(category__contains=request.query_params.get('category'))
        serializer = ProductSerializer(prods, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetail(APIView):
    '''Work with an individual Product object'''
    @csrf_exempt
    def get(self, request, pk, format=None):
        prod = Product.object.get(id=pk)
        serializer = ProductSerializer(prod)
        return Response(serializer.data)

    @csrf_exempt
    def put(self, request, pk, format=None):
        prod = Product.object.get(id=pk)
        serializer = ProductSerializer(prod, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def delete(self, request, pk, format=None):
        prod = Product.object.get(id=pk)
        prod.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CreateSale(APIView):
    '''View Sale'''
    @csrf_exempt
    def get(self, request, format=None):
        sales = Sale.object.all()
        if request.query_params.get('name'):
            sales = sales.filter(name__contains=request.query_params.get('name'))
        if request.query_params.get('address1'):
            sales = sales.filter(address1__contains=request.query_params.get('address1'))
        if request.query_params.get('address2'):
            sales = sales.filter(address2__contains=request.query_params.get('address2'))
        if request.query_params.get('city'):
            sales = sales.filter(city__contains=request.query_params.get('city'))
        if request.query_params.get('state'):
            sales = sales.filter(state__contains=request.query_params.get('state'))
        if request.query_params.get('zipcode'):
            sales = sales.filter(zipcode__contains=request.query_params.get('zipcode'))
        if request.query_params.get('total'):
            sales = sales.filter(total__contains=request.query_params.get('total'))
        if request.query_params.get('items'):
            sales = sales.filter(items__contains=request.query_params.get('items'))
        if request.query_params.get('payment_intent'):
            sales = sales.filter(payment_intent__contains=request.query_params.get('payment_intent'))
        serializer = SaleSerializer(sales, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request, format=None):
        body = json.loads(request.body)
        
        sale = Sale()
        sale.name = body['name']
        sale.address1 = body['address1']
        sale.address2 = body['address2']
        sale.city = body['city']
        sale.state = body['state']
        sale.zipcode = body['zipcode']
        sale.total = body['total']
        sale.items = body['items']
        sale.payment_intent = stripe.PaymentIntent.create(
            amount = int(sale.total * 100), # $10.00 is 1000s
            currency = 'usd',
        )
        sale.save()
        
        return Response({
            # pylint: disable=maybe-no-member
            'sale_id': sale.id,
            'client_secret': sale.payment_intent['client_secret'], 
        })
        # serializer = SaleSerializer(data=request.data)