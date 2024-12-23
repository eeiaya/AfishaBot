import pytest

from unittest.mock import AsyncMock, patch, MagicMock

from aiogram import Bot

from utils.states import user_states
from utils.card import send_event_card


# мокаем бота
@pytest.fixture
def mock_bot():
    return AsyncMock(spec=Bot)

# достаем клавиатуру которая лежит непосредственно в card.py, если взять клавиатуру не из простаранства имен
# utils.card... то она не замокается
@pytest.fixture
def mock_keyboard():
    with patch("utils.card.nav_keyboard.keyboard_navigation", new=MagicMock()) as mock_keyboard:
        mock_keyboard.return_value = "Test keyboard"
        yield mock_keyboard

@pytest.mark.asyncio
async def test_send_event_card(mock_bot, mock_keyboard):

    # создаем фейковые данные
    user_id = 123456789
    chat_id = 987654321
    message_id = 1111

    # открываем user_states . Это позваоляет очистить состояния перед тестом, чтобы вдруг другие данные не повлияли
    # на тест и patch.dict локально запишет данные а потом вернет все в прежнее состояние
    with patch.dict(user_states, {}, clear=True):

        # заполняем состояние фейковыми данными
        user_states[user_id] = {
            "index": 0,
            "storage": [{
                "name": "Test Event 4",
                "link": "https://test.link",
                "priceMin": 100,
                "author": "Test Author 4",
                "place": "Test place 4"
            }],
            "message": message_id
        }
        # вызываем функцию
        await send_event_card(user_id, chat_id, message_id, mock_bot)

        # тестим что функция вызвалась с нужными параметрами
        mock_bot.edit_message_text.assert_called_once_with(
            chat_id=chat_id,
            message_id=message_id,
            text=(
                '<a href="https://test.link">Test Event 4</a>\n'
                '<b>Стоимость от: </b>100₽\n'
                '<b>Автор: </b>Test Author 4\n'
                '<b>Место проведения: </b>Test place 4\n'
            ),
            reply_markup="Test keyboard",
            parse_mode="HTML"
        )
        # тестим что клавиатура вызвалась
        mock_keyboard.assert_called_once()
