from bs4 import BeautifulSoup
import uuid
import requests
import re
from common.database import Database
import models.items.constants as ItemConstants
from models.stores.store import Store


class Item:


    def __init__(self,name,url,price=None,_id=None):
        self.name = name
        self.url = url
        store = Store.find_by_url(url)
        self.tag_name = store.tag_name
        self.query = store.query
        self.price = None if price is None else price 
        self._id = uuid.uuid4().hex if _id is None else _id


    def __repr__(self):

        return f"<Item {self.name} with URL {self.url}>"




    def load_price(self):


        headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
                }
        content = requests.get(self.url,headers=headers)
        content = content.content
        soup = BeautifulSoup(content,"html.parser")
        element = soup.find(self.tag_name,self.query)

        string_price = element.text.strip()
        

        pattern = re.compile(r'(\d+.\d+)')

        
        match = pattern.search(string_price)

        self.price = float(match.group())
        return self.price


    def save_to_mongo(self):

        Database.update(ItemConstants.COLLECTION,{'_id': self._id},self.json())
    

    
    def json(self):

        return {
                '_id': self._id,
                'name': self.name,
                'url': self.url,
                "price": self.price


                }
        
    @classmethod
    def get_by_id(cls,item_id): 
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"_id": item_id}))
