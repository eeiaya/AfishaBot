from aiogram import Dispatcher
from aiogram.methods import DeleteWebhook

from utils.bot import bot
from app.handlers import router

import asyncio
# import logging

#создаем экземпляр класса диспетчер
dp = Dispatcher()

# подключаем к диспетчеру все обработчики, которые используют роутеры
dp.include_router(router)

async def main():

    # это нужно чтобы не обрабатывать команды, которые были написаны, покабот был выключен
    await bot(DeleteWebhook(drop_pending_updates=True))
    # запускаем бота
    await dp.start_polling(bot)

#Точка входа нашего приложения
if __name__ == "__main__":
    # смотрим логи отработки функций(не для прода)
    # logging.basicConfig(level=logging.INFO)
    #перехватываем ошибку с KeyboardInterrupt
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
