import pymongo

MONGODB_PORT = 27017


class MongoDB():

    def __init__(self, collection, database='root'):
        mongo_url = 'mongodb://{0}:{1}@{2}:{3}/root'.format("root", "123456", '114.116.25.73', MONGODB_PORT)
        self.client = pymongo.MongoClient(mongo_url)
        # self.client = pymongo.MongoClient(host='114.116.25.73', port=MONGODB_PORT,username="root", password="123456")
        self.database = self.client[database]
        self.col = self.database[collection]

    def get_valid_item_ids(self):
        return set([item['buff_id'] for item in self.col.find()])

    def get_item(self, buff_id):
        res_count = self.col.count_documents({'buff_id': buff_id})
        res = self.col.find({'buff_id': buff_id})
        if res_count:
            return res[0]
        else:
            return None

    def insert_item(self, item):
        res = self.col.insert_one(item)
        return res.acknowledged

    def delete_item(self, buff_id):
        res = self.col.delete_one({'buff_id': buff_id})
        return res.acknowledged

    def update_item(self, item):
        res = self.col.replace_one({'buff_id': item['buff_id']}, item)
        return res.acknowledged

    def get_all_items(self, rule=None):
        if rule is None:
            rule = {}
        return self.col.find(rule)

    def get_sorted_items(self, sort, rule=None, limit=0):
        if rule is None:
            rule = {}
        return self.col.find(rule).sort(sort, pymongo.ASCENDING).limit(limit)

    def close(self):
        self.client.close()

    def _clear(self):
        return self.col.delete_many({})

    def get_size(self):
        return self.col.estimated_document_count()
