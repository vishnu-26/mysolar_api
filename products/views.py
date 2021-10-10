import json,time
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Product
from .utils import upload_file
from rest_framework import viewsets,status,generics,mixins
from api.pagination import CustomPagination
from bson.json_util import dumps,loads

# Create your views here.

@api_view(['POST'])
def upload_product(request):
    
    image = request.data['image']
    request.data['image'] = image.name
    request.data['name'] = image.name
    
    product = Product()
    data = product.create(**request.data)

    upload_file(image)
    
    return JsonResponse({
        'Product': data
    },status=201)




@api_view(['GET'])
def products(request):

    products = Product().get_products()
    print(type(products))

    if products:
        paginator = CustomPagination()
        paginated_data_of_products = paginator.paginate_queryset(products,request)

        paginated_json_data_of_products = loads(dumps(paginated_data_of_products))
        print(type(paginated_json_data_of_products[0]))
        return paginator.get_paginated_response(('Products',paginated_json_data_of_products))


    return JsonResponse({
        'Error': 'Something Went Wrong!!,Please try again'
    },status=501)



    





    


    








