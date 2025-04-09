import json
import csv

def load_data():
    # Читаем преобразованные данные
    with open("transformed_data.json", "r", encoding="utf-8") as f:
        transformed = json.load(f)

    # Определяем имена колонок для CSV
    fieldnames = ["day", "new_accounts", "total_messages", "anon_message_percentage", "topic_change_percentage"]

    # Записываем данные в CSV
    with open("aggregated_data.csv", "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transformed)
    print("Load: данные записаны в aggregated_data.csv.")

if __name__ == '__main__':
    load_data()
