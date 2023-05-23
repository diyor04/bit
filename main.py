import asyncio
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentTypes
import keyboards as kb
from keyboards import cb
from config import token, payment_token
import sqlite3
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

class UserState(StatesGroup):
    product_name = State()
    product_amount = State()


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
@dp.message_handler(Text(equals="Заказать"), state=None)
async def order(message: types.Message):
    await message.answer("Выберите товар", reply_markup=kb.inline_drink_kb_full)
    await UserState.product_name.set()


@dp.message_handler(state=UserState.product_name)
async def shop(message: types.Message, state: FSMContext):

    await state.update_data(product_name=message.text)
    await message.answer('Выберите количество', reply_markup=kb.inline_count_kb_full)
    await UserState.product_amount.set()


@dp.message_handler(state=UserState.product_amount)
async def count(message: types.Message, state: FSMContext):

    data = await state.get_data()  # Получаем словарь с данными в хранилище
    product_name = data["product_name"]
    if message.text.isnumeric():
        product_amount = message.text
        connect = sqlite3.connect('cards.db')
        cursor = connect.cursor()
        user_id = message.chat.id

        cursor.execute("""INSERT INTO cards (user_id,product_name,product_amount) VALUES (?,?,?)""",
                       [user_id, product_name, product_amount])
        cursor.close()
        connect.commit()
        await message.answer('Добавлено в корзину!')
        connect.close()
    else:
        await bot.send_message(message.chat.id, "Это не число")


    await state.finish()  # Выходим из состояния, оно становится None, а все данные из хранилища стираются

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
        new.append(cursor.execute("""SELECT * FROM products WHERE id=(?)""", ([data[i][1]],)).fetchall())
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

#@dp.message_handler(Text(equals='Оплатить'))
#async def buy(mess: types.Message):
#    connect = sqlite3.connect('cards.db')
#    cursor = connect.cursor()
#    data = cursor.execute("""SELECT * FROM cards WHERE user_id=(?)""", [mess.chat.id]).fetchall()
#    #cursor.close()
#    #connect.commit()
#    print(data)
#    res = []
#    #cursor = connect.cursor()
#    for y in data:
#        for x in y:
#            res.append(x)
#
#    for i in range(len(data)):
#        res.append(cursor.execute("""SELECT * FROM products WHERE id=(?)""", [data[i][1]]).fetchall())
#    print(res)

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


