import pytest
from unittest.mock import AsyncMock, patch

from app.handlers import start_com
from app.Keyboards import Keyboards

from utils.states import user_states

# импортируем нашу клавиатуру
start_keyboard = Keyboards()

@pytest.mark.asyncio
async def test_start_com():
    # мокаем сообщение
    message = AsyncMock()
    message.from_user.id = 123  # тестовый id пользователя
    message.from_user.username = "vodka_medvedi"  # тестовое имя пользователя

    # мокаем ответ бота на сообщение
    sent_message = AsyncMock()
    sent_message.message_id = 228  # тестовый id отправленного сообщения
    message.answer.return_value = sent_message

    # временно очищаем наш глобальный словарь чтобы быть уверенным что тест не зависит от старых данных
    # так же все изменения со словарем внутри теста будут локальными
    with patch.dict(user_states, {}, clear=True):
        await start_com(message)

        # проверка вызова message.answer
        message.answer.assert_called_with(
            text=(
                f"Привет, <b>vodka_medvedi</b>, это бот-помощник "
                f"в нахождении культурных мероприятий в городе Владимир!\n <em>Выбери категорию нужного тебе события!</em>"
            ),
            reply_markup=start_keyboard.keyboard_categories(),
            parse_mode='HTML'
        )

        # проверка, что глобальный словарь обновился
        assert user_states[123] == {"message_id": 228}

        # проверка вызова удаления предыдущего сообщения
        message.delete.assert_called_once()