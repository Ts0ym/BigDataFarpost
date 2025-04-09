import json

def transform_data():
    # Загружаем данные, извлечённые на этапе Extract
    with open("extracted_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Преобразуем данные для пользователей, сообщений и тем, приводя числовые значения к int
    users_dict = {}
    for entry in data.get("users", []):
        day = entry["day"]
        # Если значение new_accounts является строкой, преобразуем его в int
        users_dict[day] = int(entry["new_accounts"]) if isinstance(entry["new_accounts"], str) else entry["new_accounts"]

    messages_dict = {}
    for entry in data.get("messages", []):
        day = entry["day"]
        total_messages = entry["total_messages"]
        anon_messages = entry["anon_messages"]
        # Приводим значения к int, если они строковые
        messages_dict[day] = {
            "total_messages": int(total_messages) if isinstance(total_messages, str) else total_messages,
            "anon_messages": int(anon_messages) if isinstance(anon_messages, str) else anon_messages
        }

    topics_dict = {}
    for entry in data.get("topics", []):
        day = entry["day"]
        new_topics = entry["new_topics"]
        topics_dict[day] = int(new_topics) if isinstance(new_topics, str) else new_topics

    # Объединяем все дни
    all_days = set(users_dict.keys()).union(set(messages_dict.keys())).union(set(topics_dict.keys()))
    
    aggregated = []
    prev_topics = None
    for day in sorted(all_days):
        new_accounts = users_dict.get(day, 0)
        message_info = messages_dict.get(day, {"total_messages": 0, "anon_messages": 0})
        total_messages = int(message_info.get("total_messages", 0))
        anon_messages = int(message_info.get("anon_messages", 0))
        # Вычисляем процент анонимных сообщений
        anon_percentage = (anon_messages / total_messages * 100) if total_messages > 0 else 0
        new_topics = topics_dict.get(day, 0)
        # Вычисляем процентное изменение количества тем относительно предыдущего дня
        if prev_topics is None or prev_topics == 0:
            topic_change = 0
        else:
            topic_change = ((new_topics - prev_topics) / prev_topics * 100)
        aggregated.append({
            "day": day,
            "new_accounts": new_accounts,
            "total_messages": total_messages,
            "anon_message_percentage": round(anon_percentage, 2),
            "topic_change_percentage": round(topic_change, 2)
        })
        prev_topics = new_topics

    # Сохраняем преобразованные данные в файл transformed_data.json
    with open("transformed_data.json", "w", encoding="utf-8") as f:
        json.dump(aggregated, f, ensure_ascii=False, indent=2)
    
    print("Transform: данные сохранены в transformed_data.json.")

if __name__ == '__main__':
    transform_data()
