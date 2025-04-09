import random
import csv
from datetime import datetime, timedelta

MIN_EVENTS_PER_ACTION = 5
MONTH_DAYS = 31
start_date = datetime(2023, 1, 1)

user_counter = 1
topic_counter = 1
message_counter = 1
log_counter = 1

users_data = []      # Поля: user_id, username, registration_date
topics_data = []     # Поля: topic_id, user_id, title, created_at
messages_data = []   # Поля: message_id, topic_id, user_id, content, created_at
logs_data = []       # Поля: log_id, user_id, action_type, reference_id, server_response, error_message, action_timestamp

registered_users = []
created_topics = []

def random_time_on_day(date_obj):
    return f"{date_obj.strftime('%Y-%m-%d')} {random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}"

for day in range(MONTH_DAYS):
    current_date = start_date + timedelta(days=day)
    for action in ['first_visit', 'registration', 'login', 'logout', 'create_topic', 'enter_topic', 'delete_topic', 'write_message']:
        count = random.randint(MIN_EVENTS_PER_ACTION, MIN_EVENTS_PER_ACTION + 5)
        
        if action == 'registration':
            for _ in range(count):
                reg_time = random_time_on_day(current_date)
                user_id = user_counter
                username = f"user{user_id}"
                users_data.append([user_id, username, reg_time])
                registered_users.append(user_id)
                logs_data.append([log_counter, user_id, 'registration', user_id, 'success', None, reg_time])
                log_counter += 1
                user_counter += 1
        
        elif action == 'first_visit':
            for _ in range(count):
                event_time = random_time_on_day(current_date)
                logs_data.append([log_counter, None, 'first_visit', None, 'success', None, event_time])
                log_counter += 1
        
        elif action in ['login', 'logout', 'enter_topic', 'delete_topic']:
            for _ in range(count):
                event_time = random_time_on_day(current_date)
                user_id = random.choice(registered_users) if registered_users else None
                logs_data.append([log_counter, user_id, action, None, 'success', None, event_time])
                log_counter += 1
        
        elif action == 'create_topic':
            error_events = 2 if count >= 2 else 0
            success_events = count - error_events
            for _ in range(success_events):
                event_time = random_time_on_day(current_date)
                if registered_users:
                    user_id = random.choice(registered_users)
                else:
                    user_id = user_counter
                    username = f"user{user_id}"
                    users_data.append([user_id, username, event_time])
                    registered_users.append(user_id)
                    user_counter += 1
                topic_id = topic_counter
                title = f"Topic {topic_id}"
                topics_data.append([topic_id, user_id, title, event_time])
                created_topics.append(topic_id)
                topic_counter += 1
                logs_data.append([log_counter, user_id, 'create_topic', topic_id, 'success', None, event_time])
                log_counter += 1
            for _ in range(error_events):
                event_time = random_time_on_day(current_date)
                logs_data.append([log_counter, None, 'create_topic', None, 'error', 'User not logged in', event_time])
                log_counter += 1
        
        elif action == 'write_message':
            for _ in range(count):
                event_time = random_time_on_day(current_date)
                user_id = random.choice(registered_users) if (registered_users and random.random() < 0.5) else None
                if created_topics:
                    topic_id = random.choice(created_topics)
                else:
                    if registered_users:
                        topic_user = random.choice(registered_users)
                    else:
                        topic_user = user_counter
                        username = f"user{topic_user}"
                        users_data.append([topic_user, username, event_time])
                        registered_users.append(topic_user)
                        user_counter += 1
                    topic_id = topic_counter
                    title = f"Topic {topic_id}"
                    topics_data.append([topic_id, topic_user, title, event_time])
                    created_topics.append(topic_id)
                    topic_counter += 1
                message_id = message_counter
                content = f"Message {message_id} content"
                messages_data.append([message_id, topic_id, user_id, content, event_time])
                message_counter += 1
                logs_data.append([log_counter, user_id, 'write_message', message_id, 'success', None, event_time])
                log_counter += 1

with open('users.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['user_id', 'username', 'registration_date'])
    writer.writerows(users_data)

with open('topics.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['topic_id', 'user_id', 'title', 'created_at'])
    writer.writerows(topics_data)

with open('messages.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['message_id', 'topic_id', 'user_id', 'content', 'created_at'])
    writer.writerows(messages_data)

with open('log_events.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['log_id', 'user_id', 'action_type', 'reference_id', 'server_response', 'error_message', 'action_timestamp'])
    writer.writerows(logs_data)

print("Датасет сгенерирован и сохранён в файлах: users.csv, topics.csv, messages.csv, log_events.csv")
