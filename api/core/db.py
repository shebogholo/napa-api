from typing import Dict
from pymongo import MongoClient

client = MongoClient("mongodb://napa-mongodb:161/napa", connect=False)


db = client["napa"]
queries_collection = db["queries"]


def create_query(data: Dict):
    queries_collection.insert_one(data)

def get_all_queries():
    return list(queries_collection.find({}, {'_id':0}))