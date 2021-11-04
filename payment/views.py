import os
import json
import time
import random
import string
import requests
import urllib
#import urllib2
import webbrowser
from django.shortcuts import render,redirect
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

payment_action = None
@api_view(['POST'])
def payment(request):
    order_document= {}
    order_document['_id'] = checksum.__id_generator__()
#    print(order_id)

    for key in request.data:
        order_document[key] = request.data[key]
#    order_document['_id']
#    print(order_document)

#    {
#        "customer": {
#            "name":"xyz@",
#            "email_id":"xyz@gmail.com",
#            "mobile_no":"7777777777"
#
#        },
#        "delivery_address":"dummy",
#        "total_amount":"1000",
#        "order_status":"created",
#        "payment_status":"pending"
#        
#
#    }

    o = Order()
    order = o.create(**order_document)
#    print(order)
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

    
#    context={
#        'payment_url': os.getenv('PAYTM_TXN_URL'),
#        'params_dict': params_dict
#        
#    }

#    return render(request,'payment/payment.html',context)

    payment_url = os.getenv('PAYTM_TXN_URL')
#    print(os.getenv('PAYTM_CALLBACK_URL'))

    f = open(os.getcwd()+'/templates/payment/payment.html','w')
    
    form_fields=""
    for key,value in params_dict.items():
        form_fields+="<input type='hidden' name={} value={} >".format(key,value)
    
    html="""<html><head><title>Merchant Checkout Page</title></head><body><center><h1>Please do not refresh this page...</h1></center><form method="post" action={} name="f1"> {} </form><script type="text/javascript">document.f1.submit();</script></body></html>"""


    html_template = html.format(payment_url,form_fields)
#    print(html_template)
    
    f.write(html_template)
    f.close()
    

    webbrowser.open('file://'+os.path.realpath('templates/payment/payment.html'),new=2)
    
    while True:
        order=o.get(**{'_id':order['_id']})
        
        if order['transaction_status']!='pending':
            break
        time.sleep(5)

    
    print(order)
#    post_data = json.dumps(params_dict)
#    resp = requests.post(payment_url,data=post_data,headers = {"Content-type": "application/json"}).json()
#    print(resp)
#
   
#
#    return HttpResponse('<html><head><title>Merchant Checkout Page</title></head><body><center><h1>Please do not refresh this page...</h1></center><form method="post" action="' + payment_url + '" name="f1">' + form_fields + '</form><script type="text/javascript">document.f1.submit();</script></body></html>')
    
#    print('Params Dict',params_dict)
#    print('Payment Url',payment_url)
    return JsonResponse({
        'order':order
    },status=201)

#    resp = requests.post(payment_url,params_dict).text
#    
#    print(resp)



@csrf_exempt
@api_view(['POST'])
def response(request):
    transaction  = verify_payment_response(request)
#    print(transaction)

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
            
             },
             {
                'field_name': 'transaction_status' , 
                'new_value': 'success'
             }
            ]
             
        )
        
        order = o.get(**{'_id': order_id})
        
#        return render(request,'public/index.html')
        
    else:
        o.update(
            {'field_name': '_id' , 'value': order_id},
            [{
                'field_name': 'transaction_status' , 
                'new_value': 'failed'
             }]
             
        )
        order = o.get(**{'_id': order_id})
        
        
    
       
    return JsonResponse({
            'order': order

        },status=201)    
    
        




    
    
