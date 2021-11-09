import pymongo
import os
import dns
from dotenv import load_dotenv

load_dotenv()

def connect(db_name="mysolar"):
    try:
        client = pymongo.MongoClient(os.getenv('MONGODB_URI'))

        db = client[db_name]
        print('Mongodb Connected: ',db)
        
    except:
        db =None
    
    return db
    


if __name__=='__main__':
    connect()



