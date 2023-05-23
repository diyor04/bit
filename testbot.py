import asyncio
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentTypes
import aw as kb
from aw import cb
from config import token, payment_token
import sqlite3
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

class UserState(StatesGroup):
    state1 = State()
    state2 = State()

storage = MemoryStorage()

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)


#------Запуск бота---------
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer("Tilni tanlang\n"
                         "Выберите язык", reply_markup=kb.markup2)
    connect = sqlite3.connect('cards.db')
    cursor = connect.cursor()
    cursor.execute("""INSERT INTO users (user_id, name) VALUES(?, ?)""", [message.chat.id, message.chat.first_name])
    cursor.close()
    connect.commit()
    connect.close()





#------Кнопки с напитками------
@dp.message_handler(Text(equals="Заказать"))
async def order(message: types.Message):
    await message.answer("Здесь представлены все напитки", reply_markup=kb.inline_buy_kb_full)


@dp.callback_query_handler(cb.filter(id='1'))
async def water(callback: CallbackQuery, callback_data: dict):
    await callback.answer(cache_time=10)

    product_id = callback_data.get('id')
    user_id = callback.message.chat.id


    connect = sqlite3.connect('cards.db')
    cursor = connect.cursor()
    cursor.execute("""INSERT INTO cards (user_id,product_id) VALUES (?,?)""", [user_id,product_id])
    cursor.close()
    connect.commit()
    await callback.answer('Добавлено в корзину!')
    connect.close()



@dp.message_handler(Text(equals='Оплатить'))
async def buy(mess: types.Message):
    connect = sqlite3.connect('cards.db')
    cursor = connect.cursor()
    data = cursor.execute("""SELECT * FROM cards WHERE user_id=(?)""", [mess.chat.id]).fetchall()
    #cursor.close()
    #connect.commit()
    #cursor = connect.cursor()

    new = []

    for i in range(len(data)):
        new.append(cursor.execute("""SELECT * FROM products WHERE id=(?)""", [data[i][1]]).fetchall())
    #cursor.close()
    #connect.commit()
    #connect.close()
    print(new)
    new_data = [new[i][0] for i in range(len(new))]
    price = [LabeledPrice(label=i[1], amount=i[2]) for i in new_data]
    print(new_data)
    print(price)
    await bot.send_invoice(mess.chat.id,
                           title='Cart',
                           description='It is carts',
                           provider_token=payment_token,
                           currency='UZS',
                           need_email=False,
                           prices=price,
                           start_parameter='example',
                           payload='some_invoice')

@dp.pre_checkout_query_handler(lambda q: True)
async def chek(pre_checkout: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)

@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def s_pay(message: types.Message):

    connect = sqlite3.connect('cards.db')
    cursor = connect.cursor()
    sql_update_query = """DELETE from cards where user_id = ?"""
    cursor.execute(sql_update_query, [message.chat.id])
    #cursor.execute("""DELETE FROM cards WHERE user_id=(?)""", [message.chat.id])
    cursor.close()
    connect.commit()
    await message.answer("SUCCESSFUL!")
    connect.close()


#---Go_Out----
@dp.message_handler(Text(equals="Назад"))
async def process_command_1(message: types.Message):
    await message.reply("Главное меню", reply_markup=kb.markup2)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    executor.start_polling(dp)


