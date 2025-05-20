from yoomoney import Authorize, Client
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

def check_token():
    """
    Проверяет работоспособность текущего токена ЮMoney
    """
    token = os.getenv('PAYMENT_TOKEN')
    if not token:
        return False
    
    try:
        client = Client(token)
        client.account_info()
        return True
    except Exception:
        return False

def get_yoomoney_token():
    """
    Функция для получения токена ЮMoney.
    Запускается один раз для получения токена, который затем нужно сохранить в .env файл.
    
    Инструкция:
    1. Создайте приложение в ЮMoney: https://yoomoney.ru/myservices/new
    2. Получите client_id в настройках приложения
    3. Запустите эту функцию
    4. Перейдите по URL, который появится в консоли
    5. Подтвердите доступ в браузере
    6. Скопируйте полученный токен
    7. Добавьте токен в .env файл:
       PAYMENT_TOKEN=полученный_токен
    
    Примечание: токен действителен бессрочно, пока вы его не отзовете
    в настройках своего ЮMoney кошелька
    """
    auth = Authorize(
        client_id="Ваш client_id",
        redirect_uri="https://t.me/[BOT_NAME]",
        scope=[
            "account-info",      # Информация о счете
            "operation-history", # История операций
            "operation-details", # Детали операций
            "incoming-transfers", # Входящие переводы
            "payment-p2p",       # Переводы между пользователями
            "payment-shop",      # Платежи в магазины
        ]
    )
    
    print("\n=== Получение токена ЮMoney ===")
    print("1. Перейдите по следующей ссылке:")
    print(auth.url)
    print("\n2. Подтвердите доступ в браузере")
    print("3. Скопируйте полученный токен")
    print("4. Добавьте токен в .env файл как PAYMENT_TOKEN=полученный_токен")
    print("\nПримечание: если токен не отображается, проверьте настройки приложения в ЮMoney")

if __name__ == "__main__":
    if check_token():
        print("\n✅ Текущий токен ЮMoney работает корректно")
        print("Если вы хотите получить новый токен, удалите PAYMENT_TOKEN из .env файла и запустите скрипт снова")
    else:
        print("\n❌ Токен ЮMoney отсутствует или недействителен")
        get_yoomoney_token()

