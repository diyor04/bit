from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData

cb = CallbackData('buy', 'id')


#------Спрашивает язык--------
inline_kb_full = InlineKeyboardMarkup(row_width=3)
inline_btn_1 = InlineKeyboardButton('RU', callback_data='btn1')
inline_btn_2 = InlineKeyboardButton('UZ', callback_data='btn2')

inline_kb_full.add(inline_btn_1, inline_btn_2)


# запрос у пользователя его контакт или локацию
markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
)

#-------MainMenu-------
reply_btn_1 = KeyboardButton('Заказать')
reply_btn_4 = KeyboardButton('Оплатить')

markup2 = ReplyKeyboardMarkup(resize_keyboard=True)
markup2.row(reply_btn_1, reply_btn_4)


#-----BuyOrder-----
inline_buy_kb_full = InlineKeyboardMarkup()
inline_buy_btn_1 = InlineKeyboardButton('Cola: 10000', callback_data='cola_btn')
inline_buy_kb_full.add(inline_buy_btn_1)


#------OrderButtons---------
reply_orderbtn_1 = KeyboardButton('Напитки')
reply_orderbtn_2 = KeyboardButton('Молочные продукты')
reply_orderbtn_3 = KeyboardButton('Колбысные изделия')
reply_orderbtn_4 = KeyboardButton('Масла')
reply_orderbtn_5 = KeyboardButton('Назад')

markup3 = ReplyKeyboardMarkup(resize_keyboard=True)
markup3.row(reply_orderbtn_1, reply_orderbtn_2)
markup3.add(reply_orderbtn_3, reply_orderbtn_4)
markup3.add(reply_orderbtn_5)

#-------Drinks--------
inline_drink_kb_full = ReplyKeyboardMarkup(resize_keyboard=True)
inline_btn_1 = KeyboardButton('Cola')
inline_btn_2 = KeyboardButton('Fanta')
#inline_btn_3 = InlineKeyboardButton('Cola-0.5', callback_data='drinks3')
#inline_btn_4 = InlineKeyboardButton('Pepsi-1.5',callback_data='drinks4')
#inline_btn_5 = InlineKeyboardButton('Pepsi-1',  callback_data='drinks5')
#inline_btn_6 = InlineKeyboardButton('Pepsi-0.5',callback_data='drinks6')
#inline_btn_7 = InlineKeyboardButton('Fanta-1.5',callback_data='drinks7')
#inline_btn_8 = InlineKeyboardButton('Fanta-1',  callback_data='drinks8')
#inline_btn_9 = InlineKeyboardButton('Fanta-0.5',callback_data='drinks9')

inline_drink_kb_full.add(inline_btn_1, inline_btn_2)


#-------Кнопки с выбором количества товара----------
inline_count_kb_full = ReplyKeyboardMarkup(resize_keyboard=True)
inline_count_btn_1 = KeyboardButton('1')
inline_count_btn_2 = KeyboardButton('5')
inline_count_btn_3 = KeyboardButton('10')
#inline_count_btn_4 = InlineKeyboardButton('15', callback_data='count4')
#inline_count_btn_5 = InlineKeyboardButton('20', callback_data='count5')
#inline_count_kb_full.add(inline_count_btn_1, inline_count_btn_2, inline_count_btn_3,
#                         inline_count_btn_4, inline_count_btn_5)
inline_count_kb_full.add(inline_count_btn_1, inline_count_btn_2, inline_count_btn_3)

#----------Кнопка заказать
inline_bb_kb_full = InlineKeyboardMarkup(row_width=3)
inline_bb_btn_1 = InlineKeyboardButton('Заказать', callback_data='order')

inline_bb_kb_full.add(inline_bb_btn_1)

