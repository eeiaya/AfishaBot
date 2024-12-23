from aiogram import types, Router
from aiogram.filters import CommandStart

from app.Keyboards import Keyboards

from utils.states import user_states
from utils.card import send_event_card
from utils.bot import bot

from services.CollectData import CollectData

import json


router = Router()

# создаем экземлпяр нашего класса со скриптами для сбора данных
collectData = CollectData()

# создаем экземпляр нашего класса с клавиатурами
start_keyboard = Keyboards()

# обработчик начальной команды
@router.message(CommandStart())
async def start_com(message: types.Message):
    sent_message = await message.answer(
        text=(
            f"Привет, <b>{message.from_user.username}</b>, это бот-помощник "
            f"в нахождении культурных мероприятий в городе Владимир!\n <em>Выбери категорию нужного тебе события!</em>"
        ),
        reply_markup=start_keyboard.keyboard_categories(),
        parse_mode='HTML',
    )
    user_states[message.from_user.id] = {"message_id": sent_message.message_id}
    await message.delete()

# обрабатываем нажатие на кнопку Спектакли
@router.callback_query(lambda callback: callback.data == 'performances')
async def callback_performances(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    collectData.collect_data_perfomances()
    with open("storage/spektakli.json") as file:
        data = json.load(file)

    user_states[user_id] = {"index": 0, "storage": data, "message_id": callback.message.message_id}

    await send_event_card(user_id, callback.message.chat.id, callback.message.message_id, bot)

# обрабатываем нажатие на кнопку Концерты
@router.callback_query(lambda callback: callback.data == 'concerts')
async def callback_concerts(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    collectData.collect_data_concerts()
    with open("storage/kontserti.json") as file:
        data = json.load(file)

    user_states[user_id] = {"index": 0, "storage": data, "message_id": callback.message.message_id}

    await send_event_card(user_id, callback.message.chat.id, callback.message.message_id, bot)

# обрабатываем нажатие на кнопку Выставки
@router.callback_query(lambda callback: callback.data == 'exhibitions')
async def callback_exhibitions(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    collectData.collect_data_exhibitions()
    with open("storage/vistavki.json") as file:
        data = json.load(file)
    user_states[user_id] = {"index": 0, "storage": data, "message_id": callback.message.message_id}

    await send_event_card(user_id, callback.message.chat.id, callback.message.message_id, bot)

# обрабатываем нажатия на кнопки назад, вперед, меню
@router.callback_query()
async def inline_callback(callback: types.CallbackQuery) -> None:
    user_id = callback.from_user.id
    user_state = user_states.get(user_id)

    if not user_state:
        await callback.answer("Ошибка: Состояние пользователя не найдено.")
        return

    message_id = user_state["message_id"]

    if callback.data == "next":
        # если это не последяняя карточка, то листаем дальше
        if user_state["index"] < len(user_state["storage"]) - 1:
            user_state["index"] += 1
            await send_event_card(user_id, callback.message.chat.id, message_id, bot)
    elif callback.data == "previous":
        # если это не первая карточка, то листаем назад
        if user_state["index"] > 0:
            user_state["index"] -= 1
            await send_event_card(user_id, callback.message.chat.id, message_id, bot)
    elif callback.data == 'back':

        # удаляем состояния пользователя, чтобы заново выбирать категории
        del user_states[user_id]
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=message_id,
            text=(
                f"Привет, <b>{callback.from_user.username}</b>, это бот-помощник "
                f"в нахождении мероприятий в городе Владимир!\n <em>Выбери категорию нужного тебе события!</em>"
            ),
            reply_markup=start_keyboard.keyboard_categories(),
            parse_mode='HTML'
            )
    # даем ответ серверу о нажатии
    await callback.answer()