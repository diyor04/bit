from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData


#-------MainMenu-------
reply_btn_1 = KeyboardButton('Заказать')
reply_btn_4 = KeyboardButton('Оплатить')

markup2 = ReplyKeyboardMarkup(resize_keyboard=True)
markup2.row(reply_btn_1, reply_btn_4)


#

#-------Drinks--------
drink_kb_full = ReplyKeyboardMarkup(resize_keyboard=True)
btn_1 = KeyboardButton('Cola')
btn_2 = KeyboardButton('Fanta')

drink_kb_full.add(btn_1, btn_2)


#-------Кнопки с выбором количества товара----------
count_kb_full = ReplyKeyboardMarkup(resize_keyboard=True)
count_btn_1 = KeyboardButton('1')
count_btn_2 = KeyboardButton('5')
count_btn_3 = KeyboardButton('10')

count_kb_full.add(count_btn_1, count_btn_2, count_btn_3)

#----------Кнопка заказать
inline_bb_kb_full = InlineKeyboardMarkup(row_width=3)
inline_bb_btn_1 = InlineKeyboardButton('Заказать', callback_data='order')

inline_bb_kb_full.add(inline_bb_btn_1)

