import config as cfg
import markups as nav
import logging
import openai
import asyncio
from aiogram import executor

from config import bot, dp, OPENAI_API_KEY
from db.db_operations import *
from handlers.handlers import register_handlers

import datetime
import os

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
register_handlers(dp)
 
async def on_startup(dispatcher):
    """
    Инициализация бота при запуске
    """
    task1 = asyncio.create_task(control_user_subscription())
    task2 = asyncio.create_task(upd_users_limit())
    
async def control_user_subscription():
    """
    Проверка и контроль подписок пользователей
    """
    while True:
        current_time = datetime.datetime.now()
        tg_id_list = await get_expired_subs(current_time)
        if len(tg_id_list) > 0:
            for tg_id in tg_id_list:
                await set_user_unsubdcribed(tg_id)
                print(f"USER {tg_id} IS UNSUBSCRIBED")
        await asyncio.sleep(3600)

async def upd_users_limit():
    """
    Обновление лимитов пользователей
    """
    old_date = datetime.datetime.now().date()
    while True:
        current_date = datetime.datetime.now().date()
        if current_date > old_date:
            print("LIMIT WAS UPDATED")
            await update_limit()
            old_date = current_date
        await asyncio.sleep(5)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
