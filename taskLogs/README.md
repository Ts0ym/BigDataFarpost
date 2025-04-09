Файлы проекта:

docker-compose.yml
Docker‑Compose конфигурация для запуска MySQL базы данных.

generate_data.py
Скрипт для генерации тестовых данных. Создаёт CSV-файлы:
    users.csv
    topics.csv
    messages.csv
    log_events.csv

init_db.py
Скрипт для создания нормализованной схемы БД (таблицы: users, topics, messages, log_events) и импорта данных из CSV.

aggregate.py
Скрипт для агрегации данных из базы (новые регистрации, сообщения, процент анонимных сообщений, изменение тем по дням) с сохранением результата в aggregated_data.csv.