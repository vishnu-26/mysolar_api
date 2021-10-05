import json,time
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Product
from .utils import upload_file

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
    start = time.time()

    products = Product().get_products()
#    print(type(products))

    end=time.time()
    print(end-start)

    if products:
        return JsonResponse({
            'Products': products
        },status=200)


    return JsonResponse({
        'Error': 'Something Went Wrong!!,Please try again'
    },status=501)


    








