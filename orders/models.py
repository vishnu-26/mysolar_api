import os
import json
import time
from django.db import models
from db_connection import connect
from bson.json_util import dumps,loads

# Create your models here.

class Order:
    def __init__(self):
        self.db = connect()
        self.collection = self.db['orders']
#        self.id = kwargs['_id']
#        self.document = kwargs

       
    def create(self, **kwargs):
        self.collection.insert_one(kwargs)
        return self.collection.find_one({"_id": kwargs['_id']})


    def get(self, **kwargs):
        return self.collection.find_one({"_id": kwargs['_id']})

    #here l is the list of tuple
    def update(self,query,_update):

        for update in _update:
            self.collection.update(
                { query['field_name'] : query['value'] },
                {'$set': { update['field_name'] : update['new_value'] }},
                upsert=False
            )


    
