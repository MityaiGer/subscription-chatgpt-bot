from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from config import CHANNELS

def showChannels():
    keyboard = InlineKeyboardMarkup(row_width=1)
    for channel in CHANNELS:
        btn  = InlineKeyboardButton(text=channel[0], url=channel[2])
        keyboard.insert(btn)
    btnDoneSub = InlineKeyboardButton(text='Я ПОДПИСАЛСЯ', callback_data="subchannelsdone")
    keyboard.add(btnDoneSub)
    return keyboard


main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
subscr_btn = KeyboardButton(text="ПОДПИСКА")
main_keyboard.add(subscr_btn)

subscr_inline_keyboard = InlineKeyboardMarkup(row_width=1)
subscr_month_btn = InlineKeyboardButton(text="На 30 дней - 700 рублей", callback_data="subscr_month")
subscr_week_btn = InlineKeyboardButton(text="На 7 дней - 350 рублей", callback_data="subscr_week")
subscr_day_btn = InlineKeyboardButton(text="На 1 день - 100 рублей", callback_data="subscr_day")
subscr_inline_keyboard.add(subscr_month_btn,subscr_week_btn,subscr_day_btn )
