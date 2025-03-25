import random
import string
import time
import redis
import json  # Добавим импорт

# Подключение к Redis
r = redis.Redis(host='localhost', port=6379, db=0)

while True:
    # Генерация случайного сообщения
    message = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    
    # Сериализация словаря в JSON-строку
    string_message = (str)({'message': message})
    
    r.lpush('messages', string_message)  # Отправка строки, а не словаря
    print(f"Sent: {message}")
    time.sleep(60)  # Ждать 1 минуту