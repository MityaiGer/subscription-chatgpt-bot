import os
from dotenv import load_dotenv
from aiogram.types import LabeledPrice
from aiogram import Bot, Dispatcher
from yoomoney import Quickpay, Client

# Загрузка переменных окружения
load_dotenv()

# Токены
BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PAYMENT_TOKEN = os.getenv('PAYMENT_TOKEN')

# Каналы
CHANNELS = [
    ["CHANNEL_NAME", os.getenv('CHANNEL_ID'), "https://t.me/username"],
]

# Цены подписок
PRICE_DAY = LabeledPrice(label="Подписка на 1 день", amount=int(os.getenv('PRICE_DAY')))
PRICE_WEEK = LabeledPrice(label="Подписка на 7 дней", amount=int(os.getenv('PRICE_WEEK')))
PRICE_MONTH = LabeledPrice(label="Подписка на 30 дней", amount=int(os.getenv('PRICE_MONTH')))

# Сообщения
NOT_SUB_MESSAGE = "<b>Для доступа к боту, необходимо подписаться на канал:</b>"
NOT_PAY_MESSAGE = "<b>Для дальнейшнго использования бота, необходимо приобрести подписку:</b>"

# Настройки базы данных
DB = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# Инициализация бота
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

#client = Client(token=TOKEN)
