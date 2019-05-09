import pymongo
import config


class Store:
    def __init__(self, database, collection, conn_str=config.MONGO_URI):
        self.client = pymongo.MongoClient(conn_str)
        self.db = self.client[database]
        self.collection = self.db[collection]

    def insert(self, data):
        c = self.collection
        result = c.insert_one(data)
        return result

    def get(self, query):
        c = self.collection
        result = c.find_one(query)
        return result


if __name__ == '__main__':
    store = Store("heroku_ptxs6mmt", "notifications", config.MONGO_URI)
    # result = store.insert({
    #     'test': 'test data',
    #     'name': 'John'
    #     })
    result = store.get({'name': 'test'})
    print(result)