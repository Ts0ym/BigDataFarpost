import mysql.connector
import csv

def initialize_database():
    conn = mysql.connector.connect(
        host="db",
        user="root",
        password="rootpass",
        database="forum_logs"
    )
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
      user_id INT AUTO_INCREMENT PRIMARY KEY,
      username VARCHAR(255) NOT NULL,
      registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS topics (
      topic_id INT AUTO_INCREMENT PRIMARY KEY,
      user_id INT NOT NULL,
      title VARCHAR(255),
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
      message_id INT AUTO_INCREMENT PRIMARY KEY,
      topic_id INT NOT NULL,
      user_id INT DEFAULT NULL,
      content TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (topic_id) REFERENCES topics(topic_id),
      FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS log_events (
      log_id INT AUTO_INCREMENT PRIMARY KEY,
      user_id INT DEFAULT NULL,
      action_type ENUM('first_visit','registration','login','logout','create_topic','enter_topic','delete_topic','write_message') NOT NULL,
      reference_id INT DEFAULT NULL,
      server_response ENUM('success','error') NOT NULL,
      error_message VARCHAR(255) DEFAULT NULL,
      action_timestamp DATETIME NOT NULL,
      FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)
    conn.commit()
    print("Таблицы созданы.")

    try:
        with open('users.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            users = []
            for row in reader:
                users.append((row['user_id'], row['username'], row['registration_date']))
            if users:
                cursor.executemany("""
                INSERT INTO users (user_id, username, registration_date) VALUES (%s, %s, %s)
                """, users)
                conn.commit()
                print(f"Импортировано {cursor.rowcount} строк в таблицу users.")
    except FileNotFoundError:
        print("Файл users.csv не найден.")
    
    try:
        with open('topics.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            topics = []
            for row in reader:
                topics.append((row['topic_id'], row['user_id'], row['title'], row['created_at']))
            if topics:
                cursor.executemany("""
                INSERT INTO topics (topic_id, user_id, title, created_at) VALUES (%s, %s, %s, %s)
                """, topics)
                conn.commit()
                print(f"Импортировано {cursor.rowcount} строк в таблицу topics.")
    except FileNotFoundError:
        print("Файл topics.csv не найден.")
    
    try:
        with open('messages.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            messages = []
            for row in reader:

                raw_user_id = row['user_id'].strip() if ('user_id' in row and row['user_id'] is not None) else ''
                if raw_user_id == '':
                    user_id = None
                else:
                    user_id = int(raw_user_id)

                message_id = int(row['message_id'].strip()) if row['message_id'].strip() != '' else None
                topic_id = int(row['topic_id'].strip()) if row['topic_id'].strip() != '' else None

                messages.append((message_id, topic_id, user_id, row['content'], row['created_at']))
            if messages:
                cursor.executemany("""
                INSERT INTO messages (message_id, topic_id, user_id, content, created_at) 
                VALUES (%s, %s, %s, %s, %s)
                """, messages)
                conn.commit()
                print(f"Импортировано {cursor.rowcount} строк в таблицу messages.")
    except FileNotFoundError:
        print("Файл messages.csv не найден.")


    try:
        with open('log_events.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            logs = []
            for row in reader:
                logs.append((row['log_id'], row['user_id'] if row['user_id'] != '' else None,
                             row['action_type'], row['reference_id'] if row['reference_id'] != '' else None,
                             row['server_response'], row['error_message'] if row['error_message'] != '' else None,
                             row['action_timestamp']))
            if logs:
                cursor.executemany("""
                INSERT INTO log_events (log_id, user_id, action_type, reference_id, server_response, error_message, action_timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, logs)
                conn.commit()
                print(f"Импортировано {cursor.rowcount} строк в таблицу log_events.")
    except FileNotFoundError:
        print("Файл log_events.csv не найден.")
    
    cursor.close()
    conn.close()
    print("Инициализация базы данных завершена.")

if __name__ == '__main__':
    initialize_database()
