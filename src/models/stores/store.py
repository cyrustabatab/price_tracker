import uuid
from common.database import Database
import models.stores.constants as StoreConstants
import models.stores.errors as StoreErrors



class Store:


    def __init__(self,name,url_prefix,tag_name,query,_id=None):
        self.name = name
        self.url_prefix =url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = uuid.uuid4().hex if _id is None else _id


    def __repr__(self):
        return f"<Store {self.name}>"



    def json(self):

        return {
                '_id': self._id,
                'name': self.name,
                'url_prefix': self.url_prefix,
                'tag_name': self.tag_name,
                'query': self.query
                }


    @classmethod
    def get_by_id(cls,store_id): 
        return cls(**Database.find_one(StoreConstants.COLLECTION,{"_id": id}))
    


    def save_to_mongo(self):
        Database.update(StoreConstants.COLLECTION,{"_id": self._id},self.json())


    @classmethod
    def get_by_name(cls,store_name):
        return cls(**Database.find_one(StoreConstants.COLLECTION,{'name': store_name}))


    @classmethod
    def get_by_url_prefix(cls,url_prefix):
        """
        htt
        """

        return cls(**Database.find_one(StoreConstants.COLLECTION,{'url_prefix': {'$regex': '^{}'.format(url_prefix)}}))




    @classmethod
    def find_by_url(cls,url):
        """
        Returns a store from a url like "http://www.johnlewis.com/item/
        :param url: The item's URL
        :return a Store
        """
        # pattern = re.compile(r"www.(\w+).")

        # match = pattern.search(url)

        # term = match.group(1)

        # store = cls.get_by_url_prefix(term)
        for i in range(0,len(url) + 1):
            try:
                store = cls.get_by_url_prefix(url[:i])
            except:
                raise StoreErrors.StoreNotFoundException("The URL Prefix used to find the store didn't give us any results!")
            else:
                return store


    @classmethod
    def get_by_id(cls,store_id):
        return cls(**Database.find_one(StoreConstants.COLLECTION,{'_id': store_id}))

    @classmethod
    def all(cls):
        return [cls(**s) for s in Database.find(StoreConstants.COLLECTION,{})]





    def delete(self):

        Database.remove(StoreConstants.COLLECTION,{"_id": self._id})