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


#    def get_products(self):
#        try:
#            cursor = self.collection.find({})
#
#            ## Converting pymongo cursor to list of dict
#            products = list(cursor)
#
#            for product in products:
#                product['image'] = 'http://mysolar.tech/media/'+product['image']
#        
#            ## converting list to json 
#            return loads(dumps(products))
#        except:
#            return None


    def get_products(self):
        cursor = self.collection.find()
    
         ## Converting pymongo cursor to list of dict
        products = list(cursor)


        for product in products:
           product['image'] = 'http://3.20.236.62/media/'+ product['image']
         ## converting list to json 
        return loads(dumps(products))
        
        

        




