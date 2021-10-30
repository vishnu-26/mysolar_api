import requests
import json
import os
from . import checksum
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

def verify_payment_response(response):
    transaction_dict = {}
    data_dict = {}

#    print(request.POST.items)
    for key in response.POST:
#        print(key,end=" ")
        data_dict[key]= response.POST[key]

    verify = checksum.verify_checksum(
                        data_dict,
                        os.getenv('PAYTM_MERCHANT_KEY'),
                        data_dict['CHECKSUMHASH']
                      )

    
    if verify:
        headers = {
            'Content-Type': 'application/json',
        }

        data = '{"MID":"%s","ORDERID":"%s"}'%(data_dict['MID'],data_dict['ORDERID'])
        transaction_dict = requests.post(
                        'https://securegw-stage.paytm.in/order/status',
                         data = data,
                         headers=headers

                    ).json()

#        print(transaction_dict)
        if 'STATUS' in transaction_dict and transaction_dict['STATUS'] == 'TXN_SUCCESS':
            transaction_dict['verified'] = True
            
        else:
            transaction_dict['verified'] = False
            print(transaction_dict)
    else:
        transaction_dict['verified']=False

    return transaction_dict
