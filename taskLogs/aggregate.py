import mysql.connector
import csv
import argparse
from datetime import datetime

def aggregate_data(start_date, end_date):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="rootpass",
        database="forum_logs"
    )
    cursor = conn.cursor(dictionary=True)

    # Запрос агрегации по дням:
    query = """
    SELECT DATE(action_timestamp) AS day,
           SUM(CASE WHEN action_type = 'registration' AND server_response = 'success' THEN 1 ELSE 0 END) AS new_accounts,
           SUM(CASE WHEN action_type = 'write_message' AND user_id IS NULL THEN 1 ELSE 0 END) AS anon_messages,
           SUM(CASE WHEN action_type = 'write_message' THEN 1 ELSE 0 END) AS total_messages,
           SUM(CASE WHEN action_type = 'create_topic' AND server_response = 'success' THEN 1 ELSE 0 END) AS new_topics
    FROM log_events
    WHERE action_timestamp BETWEEN %s AND %s
    GROUP BY DATE(action_timestamp)
    ORDER BY day;
    """
    cursor.execute(query, (start_date, end_date))
    results = cursor.fetchall()
    
    aggregated = []
    prev_topics = None
    for row in results:
        day = row['day']
        new_accounts = row['new_accounts']
        total_messages = row['total_messages']
        anon_messages = row['anon_messages']
        topics = row['new_topics']
        
        # Вычисляем процент анонимных сообщений
        if total_messages > 0:
            anon_percentage = (anon_messages / total_messages) * 100
        else:
            anon_percentage = 0
        
        # Вычисляем процентное изменение количества тем относительно предыдущего дня.
        # Для первого дня (prev_topics is None) прирост считаем 0.
        if prev_topics is None or prev_topics == 0:
            topic_change = 0
        else:
            topic_change = ((topics - prev_topics) / prev_topics) * 100
        
        aggregated.append({
            'day': day,
            'new_accounts': new_accounts,
            'anon_message_percentage': round(anon_percentage, 2),
            'total_messages': total_messages,
            'topic_change_percentage': round(topic_change, 2)
        })
        prev_topics = topics

    cursor.close()
    conn.close()
    return aggregated

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Агрегация логов форума и экспорт в CSV")
    parser.add_argument('--start_date', type=str, required=True, help="Начальная дата периода в формате YYYY-MM-DD")
    parser.add_argument('--end_date', type=str, required=True, help="Конечная дата периода в формате YYYY-MM-DD")
    args = parser.parse_args()
    
    aggregated_data = aggregate_data(args.start_date, args.end_date)
    
    if aggregated_data:
        fieldnames = aggregated_data[0].keys()
    else:
        fieldnames = ['day', 'new_accounts', 'anon_message_percentage', 'total_messages', 'topic_change_percentage']
    
    with open('aggregated_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(aggregated_data)
    
    print("CSV файл 'aggregated_data.csv' создан успешно.")
