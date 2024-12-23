from utils.states import user_states

from aiogram.utils.markdown import hlink, hbold
from aiogram import Bot

from app.Keyboards import Keyboards

# также создаем экземлпяр нашего класса с клавиатурами и используем его методы
nav_keyboard = Keyboards()


async def send_event_card(user_id: int, chat_id: int, message_id: int, bot: Bot) -> None:
    user_state = user_states[user_id]
    index = user_state["index"]
    event = user_state["storage"][index]

    event_name = event.get("name")
    event_link = event.get("link")
    event_price = f'{event.get("priceMin")}'
    event_author = event.get("author")
    event_place = event.get("place")

    # собираем карточку о событии
    card = (
        f'{hlink(event_name, event_link)}\n'
        f'{hbold("Стоимость от: ")}{event_price}₽\n'
        f'{hbold("Автор: ")}{event_author}\n'
        f'{hbold("Место проведения: ")}{event_place}\n'
    )

    # изменяем сообщение при пролистывании
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=card,
                                reply_markup=nav_keyboard.keyboard_navigation(),
                                parse_mode='HTML')
