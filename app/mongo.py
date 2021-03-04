# setup mongo
from flask import request, json, Response
from pymongo import MongoClient
from bson.objectid import ObjectId


class MongoAPI:
    def __init__(self, data):
        self.client = MongoClient(data['url'])
        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data

    def read(self):
        documents = self.collection.find()
        output = [{item: data[item] for item in data} for data in documents]
        return output

    def readOne(self, obj_id_to_find):
        documents = self.collection.find({"_id": ObjectId(obj_id_to_find)})
        output = [{item: data[item] for item in data} for data in documents]
        return output

    def insertOne(self, data):
        response = self.collection.insert_one(data)
        output = {'Status': 'Successfully Insert',
                  'Document_ID': str(response.inserted_id)}
        return output


    def updateOne(self, filt, dUpdated):
        updated_data = {"$set": dUpdated}
        response = self.collection.update_one({"_id": ObjectId(filt)}, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else 'Update error'}
        return output


    def deleteOne(self, filt):
        response = self.collection.delete_one({"_id": ObjectId(filt)})
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else 'Delete error'}
        return output
