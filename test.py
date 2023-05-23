import logging
import asyncio
import aiogram
from aiogram import Bot, Dispatcher, types

# Инициализация бота
bot = Bot(token='2134371626:AAGRlCgKhU4IW47IeQa8tYt9_6VarKdDzyI')
dp = Dispatcher(bot)

# Функция для пересылки сообщений из главной группы в другие
@dp.message_handler()
async def forward_message(message: types.Message):
    # Получаем id чата из которого пришло сообщение
    chat_id = message.chat.id
    print(chat_id)
    # Список id чатов, куда нужно переслать сообщение
    forward_chat_ids = [-824233113, -948554253]

    # Пересылаем сообщение во все чаты из списка
    for forward_chat_id in forward_chat_ids:
        if forward_chat_id != chat_id:
            await message.forward(chat_id=forward_chat_id)

# Запуск бота
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(dp.start_polling())
