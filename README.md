## Test API

### MongoDB on Docker
1. docker exec -it test-db bash
2. mongo --port 131
3. use testdb
4. db.counters.insert({"_id": "chats", "seq": 1})
5. docker-compose logs -f -t