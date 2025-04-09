## Описание файлов:

- **JenkinsETLPipeline/Jenkinsfile**
Этот файл содержит описание Pipeline, который определяет последовательные этапы ETL-процесса (Extract, Transform, Load) в Jenkins. Он управляет запуском Python‑скриптов и архивированием артефактов сборки.

- **JenkinsETLPipeline/DockerDatabase/docker-compose.yml**
Файл для развертывания Docker‑контейнеров. Он поднимает два сервиса:

- db – MySQL‑базу данных, в которую происходит наполнение.

- init – Python‑контейнер, который после короткого ожидания устанавливает зависимости (из requirements.txt) и запускает скрипты для генерации данных (generate_data.py) и инициализации базы (init_db.py).

- **JenkinsETLPipeline/requirements.txt**
Список зависимостей Python, которые необходимы для работы ETL‑скриптов (mysql-connector-python).

- **JenkinsETLPipeline/generate_data.py**
Скрипт для генерации тестовых данных. Он создаёт CSV-файлы (users.csv, topics.csv, messages.csv, log_events.csv), которые позже используются для наполнения базы данных.

- **JenkinsETLPipeline/init_db.py**
Скрипт, который создаёт схему базы данных (таблицы пользователей, тем, сообщений и логов) и импортирует сгенерированные данные из CSV-файлов в MySQL.

- **JenkinsETLPipeline/extract.py**
Скрипт для этапа Extract, который подключается к базе данных, извлекает нужные данные и сохраняет их во временный файл (extracted_data.json).

- **JenkinsETLPipeline/transform.py**
Скрипт для этапа Transform, который считывает извлечённые данные, агрегирует их и сохраняет преобразованные данные в transformed_data.json.

- **JenkinsETLPipeline/load.py**
Скрипт для этапа Load, который читает преобразованные данные из файла transformed_data.json и записывает итоговый результат в CSV‑файл (aggregated_data.csv).


## 1. Запуск базы данных через Docker Compose

- Перейдите в директорию, где находится docker-compose для базы данных:

**cd JenkinsETLPipeline/DockerDatabase**

- Запустите контейнеры:

**docker-compose up -d**

Это поднимет MySQL и автоматически выполнит скрипты наполнения базы (generate_data.py и init_db.py).

## 2. Импорт Pipeline в Jenkins

- Клонирование репозитория и выбор ветки:

- Откройте веб-интерфейс Jenkins (http://localhost:8080).

- Создайте новый проект типа Pipeline.

- В настройках проекта в разделе "Source Code Management" выберите Git и укажите:

URL репозитория: https://github.com/Ts0ym/BigDataFarpost.git

Ветка: 08-04-2025

- В разделе "Script Path" укажите путь JenkinsETLPipeline/Jenkinsfile

- Сохраните настройки и запустите сборку, чтобы Jenkins клонировал репозиторий и выполнил Pipeline.

## 3. Результат работы

После успешного прохождения всех этапов Pipeline, итоговый CSV-файл будет сохранён и архивирован как артефакт сборки.
