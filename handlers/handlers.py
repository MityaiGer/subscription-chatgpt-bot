import openai
import config as cfg
import markups as nav
import datetime
import time
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.types import ContentType
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from openai.error import InvalidRequestError
from aiogram.types import ChatActions
from aiogram.utils.exceptions import CantInitiateConversation, Unauthorized, BotBlocked

from config import  bot, dp, PAYMENT_TOKEN2, PRICE_DAY, PRICE_WEEK, PRICE_MONTH, PAYMENT_TOKEN2, OPENAI_API_KEY
from db.db_operations import *

from yoomoney import Quickpay, Client
import string
import random

openai.api_key = OPENAI_API_KEY

messages={}
pinned_message_sent = {}
def update(messages,role,content):
    messages.append({"role":role, "content":content})
    return messages

async def check_sub_channels(channels, user_id):
    for channel in channels:
        chat_member = await bot.get_chat_member(chat_id=channel[1], user_id=user_id)
        if chat_member['status'] == 'left':
            return False
    return True
    
'''async def check_payment(payment, user_id):
    for payment in payment:
        pay_log= await get_payment_status(chat_id=payment[1], user_id=user_id)
        if pay_log['status'] == 'left':
            return False
    return True'''


def check_subscr_decorator(func):
    async def wrapper(*args, **kwargs):
        message: types.Message = args[0]
        if not await check_sub_channels(cfg.CHANNELS, message.from_user.id):
            try:
                await bot.send_message(message.from_user.id, cfg.NOT_SUB_MESSAGE, parse_mode = 'html', reply_markup=nav.showChannels())
            except (CantInitiateConversation, Unauthorized, BotBlocked) as ex:
                print(f"{ex} USER_ID:{message.from_user.id}")
                await update_user_active(message.from_user.id, False)
        else:
            await func(*args, **kwargs)
    return wrapper


@dp.message_handler(commands=["start"])
@check_subscr_decorator
async def start_handler(message: types.Message, **kwargs):
    id = message.from_user.id
    messages[id] = []
    if not await user_exists(message.from_user.id):
        await add_user(telegram_id=message.from_user.id, first_name=message.from_user.first_name, 
                        last_name=message.from_user.last_name, username=message.from_user.username)
    else:
        await update_user_active(message.from_user.id, True)
    await bot.send_message(message.from_user.id, text=f"Привет, <b>дорогой друг</b>!\n\nБот <b>Chat GPT</b> рад приветствовать тебя!\n\nТут ты сможешь узнать обо всем на свете, стоит лишь спросить.\n\n"\
            f"<b>Мои достижения:</b>\n\n🔘 C моей помощью была написана дипломная работа, которая оценена на высший балл;\n"\
            f"\n🔘 Я с легкостью прошла собеседование в Google на должность младшего инженера-программиста с зарплатой в $180 тыс. в год. Неплохо, да?\n"\
            f"\n🔘 Ну, и конечно же, я без проблем сдала экзамены на МБА в престижнейшей Уортонской школе бизнеса при университете Пенсильвании, а еще получила лицензию врача и юриста!\n\n"\
            f"<b>А теперь попробуй сам!</b> Задай мне любой интересующий тебя вопрос или попроси меня сделать что-нибудь!\n\n"\
            f"P.S. Или можем просто поболтать. Начнем?", parse_mode="html", reply_markup=nav.main_keyboard)
    

@dp.callback_query_handler(text="subchannelsdone")
async def subchannelsdone(call: types.CallbackQuery, **kwargs):
    if await check_sub_channels(cfg.CHANNELS,call.message.chat.id):
        await start_handler(call)
        print ('1')
    else:
        await bot.send_message(call.from_user.id, cfg.NOT_SUB_MESSAGE, parse_mode="html", reply_markup=nav.showChannels())
        print ('2')

@dp.message_handler(Text('ПОДПИСКА'))
@check_subscr_decorator
async def subscr_handler(message: types.message, **kwargs):
    if message.chat.type == 'private':
        if not await user_subscribed(message.from_user.id):
            await bot.send_message(message.from_user.id, text=f"У Вас есть <b>2 тестовых запроса</b> для ознакомления с функционалом бота. Если Вы хотите получить неограниченное колличество запросов в день, Вы можете приобрести <b>платную подписку</b>.", parse_mode='html')
            await bot.send_message(message.from_user.id, text="<b>ВАРИАНТЫ ПОДПИСКИ</b>", reply_markup=nav.subscr_inline_keyboard,parse_mode='html')
        else:
            subscr_expiration = await get_user_subscr_exp(message.from_user.id)
            time_delta = subscr_expiration - datetime.datetime.now()
            days = time_delta.days
            hours = int((time_delta.total_seconds() - (days * 24 * 3600)) // 3600)
            minutes = int((time_delta.total_seconds() -  (days * 24 * 3600) - (hours * 3600 )) // 60)
            await bot.send_message(message.from_user.id, text=f"У Вас уже имеется активная подписка. До конца  осталось:\n{days}дн. {hours}ч. {minutes}мин.")



@dp.callback_query_handler(Text("subbotsdone"))
async def subbotpay(call: types.CallbackQuery, **kwargs):
    data = await get_payment_status(call.message.chat.id)
    is_subscribed = data[0][0] if data else None
    label = data[0][1] if data else None
    period = data[0][2] if data else None
    print ('7')
    if not is_subscribed:
        client = Client(cfg.PAYMENT_TOKEN2)
        history = client.operation_history(label=label)
        current_date = datetime.datetime.now()
        print ('8')
        try:
            operation = history.operations[-1]
            if operation.status == 'success':
                if period == 'day':
                    exp_date = current_date + datetime.timedelta(days=1)
                    description ="Вам доступно неограниченное колличество запросов на 1 день"
                elif period == 'week':
                    exp_date = current_date + datetime.timedelta(days=7)
                    description ="Вам доступн неограниченное колличество запросов на 7 дней"
                elif period == 'month':
                    exp_date = current_date + datetime.timedelta(days=30)
                    description ="Вам доступно неограниченное колличество запросов 30 дней"
                await set_user_subscribed(exp_date, call.message.chat.id)
                await bot.send_message(call.message.chat.id, text=f'Спасибо за приобретение подписки! {description}')
                print ('9')
        except Exception as e:
            print(e)
            await bot.send_message(call.message.chat.id, text=f"Вы не оплатили подписку или оплата еще в пути!. При возникновении проблем с оплатой обращайтесь к админу бота ", reply_markup=call.message.reply_markup)      
            print ('10')                            
    else:
        subscr_expiration = await get_user_subscr_exp(call.from_user.id)
        time_delta = subscr_expiration - datetime.datetime.now()
        days = time_delta.days
        hours = int((time_delta.total_seconds() % (days * 24 * 3600)) // 3600)
        minutes = int((time_delta.total_seconds() % 3600) // 60)
        await bot.send_message(call.from_user.id, text=f"У Вас уже имеется активная подписка. До конца  осталось:\n{days}дн. {hours}ч. {minutes}мин.")


@dp.callback_query_handler(lambda call: True,)
@check_subscr_decorator
async def subscr_callback_handler(call: types.callback_query, **kwargs):
    letters_and_digits = string.ascii_lowercase + string.digits
    if call.data == 'subscr_month':
        payment_sum = 700             
        period='month' 
    elif call.data == 'subscr_week':
        payment_sum = 350 
        period = 'week'
    elif call.data == 'subscr_day':
        payment_sum = 100
        period = 'day'
        #await bot.delete_message(call.from_user.id, call.message.message_id
    
    rand_string = ''.join(random.sample(letters_and_digits, 10))
    
    
    quickpay = Quickpay(
        receiver='0000000000000',
        quickpay_form='shop',
        targets='ChatGPT',
        paymentType='SB',
        sum=payment_sum,
        label=rand_string
    )

    await update_label_period(rand_string, period, call.message.chat.id) 
    pay_keyboard = InlineKeyboardMarkup(row_width=1)
    btnPaySub = InlineKeyboardButton(text="ОПЛАТИТЬ", url=quickpay.redirected_url)
    btnDonePay = InlineKeyboardButton(text="Я ОПЛАТИЛ", callback_data="subbotsdone")  
    pay_keyboard.add(btnPaySub,btnDonePay)  
    await bot.send_message(call.message.chat.id, cfg.NOT_PAY_MESSAGE, parse_mode='html', reply_markup=pay_keyboard)
    print ('11')


''' if await check_payment(nav.subscr_inline_keyboard,call.chat.id):
        await start_handler(call.message)
    else:
        await bot.send_message(call.message.chat.id, cfg.NOT_PAY_MESSAGE, parse_mode="html", reply_markup=nav.showChannels())'''


"""@dp.pre_checkout_query_handler()
async def proccess_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)"""


"""@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_payment(message: types.Message):
    if message.successful_payment.invoice_payload == "month_sub":
        await bot.send_message(message.from_user.id, "Вы оформили подписку на 30 дней")
        current_date = datetime.datetime.now()
        exp_date = current_date + datetime.timedelta(days=30)
    elif message.successful_payment.invoice_payload == "week_sub":
        await bot.send_message(message.from_user.id, "Вы оформили подписку на 7 дней")
        current_date = datetime.datetime.now()
        exp_date = current_date + datetime.timedelta(days=7)  
    elif message.successful_payment.invoice_payload == "day_sub":
        await bot.send_message(message.from_user.id, "Вы оформили подписку на 1 день")
        current_date = datetime.datetime.now()
        exp_date = current_date + datetime.timedelta(days=1)
    await set_user_subscribed(exp_date,message.from_user.id)"""

@dp.message_handler()
@check_subscr_decorator
async def send(message: types.Message, **kwargs):
    user_message = message.text
    id = message.from_user.id
    if id not in pinned_message_sent:
        # Отправить закрепленное сообщение
        msg = await bot.send_message(message.from_user.id, text=f"<b>Уважаемые пользователи</b> нашего бота!\nДля <b>Вас</b> важное объявление!\n\n"\
               f"Бот перешел на версию <b>GPT-4</b>, и в связи с этим цены на подписки повысились!\n"\
               f"Подробности смотрите в разделе <b>'ПОДПИСКА'</b>\n\n"\
               f"<b>GPT-4</b> может решать сложные задачи с большей точностью благодаря более широким общим знаниям и способностям к решению задач.\n\n"\
               f"<b>Спеши попропобать!</b>",parse_mode="html")
        # Установить флаг, что сообщение отправлено
        await bot.pin_chat_message(message.chat.id, msg.message_id, disable_notification=True)
        pinned_message_sent[id] = True

    if not await user_exists(message.from_user.id):
        await add_user(telegram_id=message.from_user.id, first_name=message.from_user.first_name, 
                        last_name=message.from_user.last_name, username=message.from_user.username)
    else:
        await update_user_active(message.from_user.id, True)
    if await user_subscribed(message.from_user.id) or (await get_user_limit(message.from_user.id) > 0):
        await bot.send_message(message.from_user.id, text="<b>Ожидайте</b> ⏳", parse_mode="html")
        await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
        try:
            if id not in messages:
                messages[id] = []
            if len(messages[id]) >= 6:
                messages[id] = messages[id][-5:]
            messages[id].append({"role": "user", "content": user_message})
            messages[id].append({"role": "system", "content": "Ты чат-бот способный активно участвовать в дискуссиях и генерировать соответствующие ответы на запросы, как человек.  При приветствии, вы обязательно должны упоминать его по имени не используя юзернейм."})
            messages[id].append({"role": "user", "content": f"chat: {message.chat} user: {message.from_user.first_name} message: {message.text}"})
            messages[id].append({"role": "user", "content": f"chat: {message.chat} Сейчас время {time.strftime('%d/%m/%Y %H:%M:%S')} user: {message.from_user.first_name} message: {message.text}"})
            should_respond = not message.reply_to_message or message.reply_to_message.from_user.id == bot.id
            if should_respond:
                response = await openai.ChatCompletion.acreate(
                    #update(messages, "user", message.text)
                    model="gpt-3.5-turbo",
                    temperature=1,
                    messages=messages[id]
                #    user=id
                )
            """response = await openai.Completion.acreate(
                model="text-davinci-003", 
                prompt=message.text,
                temperature=0.9,
                max_tokens=4000,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.6,
                stop=[" Human:", " AI:"]"""
         
            await message.answer(response['choices'][0]['message']['content'])     
            #await bot.send_message(message.from_user.id, reply_markup = nav.main_keyboard)
            #await message.answer(response['choices'][0]['text'],reply_markup = nav.main_keyboard)
            
            if not await user_subscribed(message.from_user.id):
                await reduce_user_limit(message.from_user.id)
                user_limit = await get_user_limit(message.from_user.id)
                await bot.send_message(message.from_user.id, text="У Вас осталось <b>{0} запросов(а)</b>.".format(user_limit), parse_mode="html")

        except (CantInitiateConversation, Unauthorized, BotBlocked) as ex:
            print(f"EXCEPTION {ex} USER_ID:{message.from_user.id}")
            await update_user_active(message.from_user.id, False)
        
        except InvalidRequestError as ex:
            print(ex)
            await bot.send_message(message.from_user.id, text="Слишком длинный запрос! Запрос должен содержать не более 4тыс. символов, включая пробелы!")
    else:
        await bot.send_message(message.from_user.id, text="<b>Вы исчерпали лимит запросов!</b> Лимит автоматически обновляется каждые сутки.", parse_mode="html")
        

def register_handlers(dp:Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'])
    dp.register_message_handler(subscr_handler, Text("Подписка"))
    #dp.register_message_handler(process_payment, content_types=ContentType.SUCCESSFUL_PAYMENT)
    dp.register_message_handler(send)
    dp.register_callback_query_handler(subbotpay, text="subbotsdone")
    dp.register_callback_query_handler(subchannelsdone, Text("subchannelsdone"))
    dp.register_callback_query_handler(subscr_callback_handler)
    #dp.register_pre_checkout_query_handler(proccess_pre_checkout_query)
    
