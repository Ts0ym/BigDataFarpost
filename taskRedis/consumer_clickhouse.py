import redis
import json
from clickhouse_driver import Client

r = redis.Redis(host='localhost', port=6379, db=0)
client = Client(host='localhost', port=9000)

while True:
    message = r.brpop('messages', timeout=0)
    if message:
        message_data = json.loads(message[1])
        client.execute("INSERT INTO messages (message) VALUES", [(message_data['message'],)])
        print(f"Inserted: {message_data['message']}")
