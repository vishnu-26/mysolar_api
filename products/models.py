import os
import json
import time
from django.db import models
from db_connection import connect
from bson.json_util import dumps,loads

# Create your models here.


class Product:
    def __init__(self):
        self.db = connect()
        self.collection = self.db['products']
        
#        print(kwargs,type(kwargs))
#        self.price = kwargs['price']
#        self.name = kwargs['image']
#        self.image= kwargs['image']
#        self.id = kwargs['id']
#        self.details = kwargs['details']
#        print(self.details)
#        self.category = kwargs['category']
#        self.quantity = kwargs['quantity']
        


    def create(self,**kwargs):
        product_document= {
            
            'name':kwargs['name'],
            'image':kwargs['image'],
            'category':kwargs['category'],
            'brand':kwargs['brand'],
            'details':{
                        'output_power': kwargs['details'],
                        
                      },
            'quantity':kwargs['quantity']

        }

        

#        product_document = json.dumps(kwargs)
        
        
        self.collection.insert_one(product_document)


    def get_products(self):
        try:
            cursor = self.collection.find().sort('_id',1)
            
            ## Converting pymongo cursor to list of dict
            products = list(cursor)

            for product in products:
                product['image'] = os.getenv('MEDIA_URI') + product['image']
        

            
            return products
        except:
            return None




        

        




