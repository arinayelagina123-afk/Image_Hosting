# Сервер картинок

Веб-приложение для загрузки, хранения и просмотра изображений.  
Бэкенд на Flask + PostgreSQL, раздача статики через Nginx, всё в Docker-контейнерах.

## Требования к окружению

- Docker
- Docker Compose

## Быстрый старт

```bash
docker compose up -d --build
```

После запуска:

- **Веб-интерфейс (Nginx):** http://localhost:8080
- **Бэкенд (Flask):** http://localhost:8000

## Остановка

```bash
docker compose down
```

Остановка с удалением томов БД:
```bash
docker compose down -v
```

## Структура проекта

```
├── app.py                 # Flask-бэкенд
├── requirements.txt       # Зависимости Python
├── Dockerfile             # Dockerfile для бэкенда
├── docker-compose.yaml    # Конфигурация Docker Compose
├── nginx.conf             # Конфигурация Nginx
├── database/
│   ├── db.py              # Подключение к PostgreSQL
│   ├── models.py          # Создание таблиц БД
│   └── repository.py      # CRUD-операции с БД
├── scripts/
│   ├── backup.sh          # Скрипт резервного копирования БД
│   ├── Dockerfile         # Dockerfile для контейнера бэкапов
│   └── crontab            # Расписание cron для бэкапов
├── images/                # Загруженные изображения (volume)
├── logs/                  # Логи приложения (volume)
├── backups/               # Резервные копии БД
├── templates/             # HTML-шаблоны
├── static/                # CSS, JS, изображения
│   ├── css/
│   ├── js/
│   └── img/
```

## Маршруты API

| Маршрут | Метод | Описание |
|---|---|---|
| `/` | GET | Главная страница |
| `/upload` | GET | Страница загрузки изображений |
| `/upload` | POST | Загрузка изображения (form-data, поле `image`) |
| `/images-list` | GET | Список всех загруженных изображений с пагинацией |
| `/images-list/<filename>` | DELETE | Удаление изображения по имени файла |
| `/images/<filename>` | GET | Просмотр/скачивание изображения |

### Параметры запросов

**Загрузка изображения:**
```
POST /upload
Content-Type: multipart/form-data
Поле: image (файл)
```

**Пагинация списка:**
```
GET /images-list?page=2
```

### Поддерживаемые форматы

- `.jpg`
- `.png`
- `.gif`

Максимальный размер файла: **5 МБ**.

## Резервное копирование

### Автоматический бэкап

Бэкапы создаются автоматически по расписанию cron (каждые 3 дня в 3:00) через отдельный сервис `backup`.

Файлы сохраняются в папку `backups/` с именем:
```
backup_YYYYMMDD_HHMMSS.sql
```

### Ручной бэкап

```bash
docker exec -t image_server_backup /backup.sh
```

Или напрямую через PostgreSQL:
```bash
docker exec -t image_serverdb pg_dump -U postgres images_db > backups/backup_$(date +%Y%m%d_%H%M%S).sql
```

### Восстановление из бэкапа

```bash
docker exec -i image_serverdb psql -U postgres images_db < backups/backup_YYYYMMDD_HHMMSS.sql
```

## Логирование

Все действия записываются в `logs/app.log` в формате:
```
[2025-01-24 14:00:00] INFO: Успех: изображение cat.jpg загружено
[2025-01-24 14:01:00] WARNING: Ошибка: неподдерживаемый формат файла
```
