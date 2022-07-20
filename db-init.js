db = db.getSiblingDB('testdb');
db.createCollection('counters');
db.counters.insert({"_id": "tablets", "seq": 1});
// db.counters.insert({"_id": "chats", "seq": 1});