import os
import json
import time
import random
import string
import requests
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
from bson.json_util import dumps,loads
from dotenv import load_dotenv
from . import checksum
from orders.models import Order
from .utils import verify_payment_response


load_dotenv()

# Create your views here.


@api_view(['POST'])
def payment(request):
    order_document= {}
    order_document['_id'] = checksum.__id_generator__()
#    print(order_id)

    for key in request.data:
        order_document[key] = request.data[key]
#    order_document['_id']
#    print(order_document)

#    order_document={
#        "_id": _id,
#        "customer": {
#            "name":"xyz@",
#            "email_id":"xyz@gmail.com",
#            "mobile_no":"7777777777"
#
#        },
#        "delivery_address":{
#            "line1":"abc@",
#            "line2":"def@",
#            "pincode":"121",
#            "city":"Mumbai",
#            "state":"Maharashtra"
#
#        },
#        "items":[
#            {"product_id":1,"quantity":2,"amount":600},
#            {"product_id":2,"quantity":1,"amount":400}
#        ],
#        "total_amount":"1000",
#        "order_status":"created",
#        "payment_status":"pending"
#        
#
#    }

    o = Order()
    order = o.create(**order_document)
#    return JsonResponse({
#       'order':order
#    })

    MERCHANT_KEY = os.getenv('PAYTM_MERCHANT_KEY')

    params_dict = {
        "MID": os.getenv('PAYTM_MERCHANT_ID'),
        "ORDER_ID": order['_id'],
        "CUST_ID": order['customer']['email_id'],
        "TXN_AMOUNT": order['total_amount'],
        "CHANNEL_ID": "WEB",
        "INDUSTRY_TYPE_ID": "Retail",
        "WEBSITE": "WEBSTAGING",
        "CALLBACK_URL": os.getenv('PAYTM_CALLBACK_URL')
    }

    params_dict['CHECKSUMHASH'] = checksum.generate_checksum(params_dict, MERCHANT_KEY)

    context = {
        'company_name': 'My Solar',
        'payment_url': os.getenv('PAYTM_TXN_URL'),
        'params_dict': params_dict
    }

    return render(request,'payment/payment.html',context)



@csrf_exempt
@api_view(['POST'])
def response(request):
    transaction  = verify_payment_response(request)
    print(transaction)

    order_id = transaction['ORDERID']
    o = Order()
    
    if transaction['verified']==True:
        o.update(
            {'field_name': '_id' , 'value': order_id},
            [{
                'field_name': 'order_status' , 
                'new_value': 'placed'
             },
             {
                'field_name': 'payment_status' , 
                'new_value': 'done'
            
             }
            ]
             
        )

    order = o.get(**{'_id': order_id})
    return JsonResponse({
        'order': order

    },status=201)    
    
        

#    o = Order()
#    if transaction['RESPMSG'] == 'Txn Success':
#        o.update(
#            {'field_name': '_id', 'value': transaction['ORDERID']},        
#            {'field_name': 'status' , 'new_value': 'placed'}
#        )
#        return HttpResponse('Done!!')


    
    
