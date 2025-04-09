import mysql.connector
import json
import argparse

def extract_data(start_date, end_date):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="rootpass",
        database="forum_logs"
    )
    cursor = conn.cursor(dictionary=True)

    # Запрос для пользователей (новые регистрации)
    cursor.execute("""
      SELECT DATE(registration_date) AS day, COUNT(*) AS new_accounts
      FROM users
      WHERE registration_date BETWEEN %s AND %s
      GROUP BY DATE(registration_date)
      ORDER BY day;
    """, (start_date, end_date))
    users_data = cursor.fetchall()

    # Запрос для сообщений
    cursor.execute("""
      SELECT DATE(created_at) AS day,
             COUNT(*) AS total_messages,
             SUM(CASE WHEN user_id IS NULL THEN 1 ELSE 0 END) AS anon_messages
      FROM messages
      WHERE created_at BETWEEN %s AND %s
      GROUP BY DATE(created_at)
      ORDER BY day;
    """, (start_date, end_date))
    messages_data = cursor.fetchall()

    # Запрос для тем
    cursor.execute("""
      SELECT DATE(created_at) AS day, COUNT(*) AS new_topics
      FROM topics
      WHERE created_at BETWEEN %s AND %s
      GROUP BY DATE(created_at)
      ORDER BY day;
    """, (start_date, end_date))
    topics_data = cursor.fetchall()

    cursor.close()
    conn.close()

    # Собираем результаты в один словарь
    extracted = {
        "users": users_data,
        "messages": messages_data,
        "topics": topics_data
    }
    # Сохраняем данные в файл extracted_data.json
    with open("extracted_data.json", "w", encoding="utf-8") as f:
        json.dump(extracted, f, ensure_ascii=False, indent=2, default=str)
    print("Extract: данные сохранены в extracted_data.json.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Извлечение данных из MySQL")
    parser.add_argument('--start_date', type=str, default="2023-01-01", help="Начальная дата (YYYY-MM-DD)")
    parser.add_argument('--end_date', type=str, default="2023-01-31", help="Конечная дата (YYYY-MM-DD)")
    args = parser.parse_args()
    extract_data(args.start_date, args.end_date)
