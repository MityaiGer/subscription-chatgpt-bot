# ChatGPT Telegram Bot с системой подписки

Telegram бот с интеграцией ChatGPT и системой платной подписки через ЮMoney. Бот предоставляет доступ к возможностям ChatGPT по подписке с гибкой системой тарификации.

## Возможности подписки

- **Тарифные планы**:
  - 1 день - 100 рублей
  - 7 дней - 350 рублей
  - 30 дней - 700 рублей

- **Функции системы подписки**:
  - Автоматическая проверка статуса подписки
  - Безопасная оплата через ЮMoney
  - Мгновенная активация после оплаты
  - Уведомления о скором окончании подписки
  - Проверка подписки на обязательные каналы

## Основные функции

- Интеграция с ChatGPT API для обработки сообщений
- Система платных подписок с разными тарифными планами
- Автоматическая проверка подписки на канал
- Безопасная обработка платежей через ЮMoney
- Хранение данных пользователей и подписок в PostgreSQL

## Установка и настройка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/subscription-chatgpt-bot.git
cd subscription-chatgpt-bot
```

2. Создайте виртуальное окружение и установите зависимости:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows
pip install -r requirements.txt
```

3. Создайте файл `.env` в корневой директории проекта и заполните его следующими данными:
```env
# Токены
BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
PAYMENT_TOKEN=your_yoomoney_payment_token

# База данных
DB_HOST=localhost
DB_PORT=5432
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name

# Цены (в копейках)
PRICE_DAY=10000
PRICE_WEEK=35000
PRICE_MONTH=70000

# ID каналов
CHANNEL_ID=your_channel_id
```

4. Настройка платежной системы:
   - Создайте приложение в [ЮMoney](https://yoomoney.ru/myservices/new)
   - Получите `client_id` в настройках приложения
   - Запустите `YoumoneyAuth.py` для получения токена
   - Добавьте полученный токен в `.env` файл

5. Создайте базу данных PostgreSQL с указанными в .env параметрами

6. Запустите бота:
```bash
python main.py
```

## Необходимые токены и ключи

- Telegram Bot Token: Получите у [@BotFather](https://t.me/BotFather)
- OpenAI API Key: [OpenAI API](https://platform.openai.com/)
- ЮMoney Payment Token: Получите через `YoumoneyAuth.py`

## Структура проекта

- `main.py` - основной файл бота
- `config.py` - конфигурация и настройки
- `markups.py` - клавиатуры и кнопки для подписок
- `YoumoneyAuth.py` - настройка платежной системы
- `handlers/` - обработчики команд и платежей
- `db/` - работа с базой данных

## Зависимости

- Python 3.8+
- aiogram - для работы с Telegram API
- openai - для интеграции с ChatGPT
- yoomoney - для обработки платежей
- python-dotenv - для работы с переменными окружения
- psycopg2-binary - для работы с PostgreSQL

## Безопасность

- Все чувствительные данные хранятся в `.env` файле
- Платежи обрабатываются через защищенный API ЮMoney
- Токены и ключи не хранятся в коде
- База данных защищена паролем

## Лицензия

MIT 