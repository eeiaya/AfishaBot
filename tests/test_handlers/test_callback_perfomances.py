import json
import pytest

from unittest.mock import AsyncMock, MagicMock, patch, mock_open

from aiogram.types import CallbackQuery, User, Message, Chat
from aiogram import Bot

from datetime import datetime

# Импортируем модули
from app.handlers import callback_performances
from utils.states import user_states


@pytest.fixture
def mock_dependencies():
    with patch("services.CollectData.CollectData.collect_data_perfomances", new=MagicMock()) as mock_collect_data, \
            patch("builtins.open", mock_open(read_data=json.dumps([{
                "name": "Test Event 3",
                "link": "https://test.link",
                "priceMin": 100,
                "author": "Test Author 3",
                "place": "Test Venue 3"
            }]))) as mock_file, \
            patch("app.handlers.send_event_card", new=AsyncMock()) as mock_send_event_card:
        yield mock_collect_data, mock_file, mock_send_event_card


@pytest.fixture
def mock_bot():
    # Мок для экземпляра Bot
    return AsyncMock(spec=Bot)


@pytest.mark.asyncio
async def test_callback_performances(mock_dependencies, mock_bot):
    mock_collect_data, mock_file, mock_send_event_card = mock_dependencies

    # создаем фейковые данные
    user_id = 123456789
    chat_id = 987654321
    message_id = 5555

    # Подготовка объекта CallbackQuery
    callback = CallbackQuery(
        id="1",
        from_user=User(
            id=user_id,
            is_bot=False,
            first_name="Test User"
        ),
        message=Message(
            message_id=message_id,
            chat=Chat(
                id=chat_id,
                type="private"
            ),
            text="Callback query test",
            date=datetime.now()
        ),
        data="performances",
        chat_instance="test_instance"
    )

    with patch.dict(user_states, {}, clear=True):
        # Патчим переданный бот в аргументы callback_performances
        with patch("app.handlers.bot", new=mock_bot):
            # Вызов тестируемого обработчика
            await callback_performances(callback)

        # Проверяем, что collect_data_perfomances была вызвана
        mock_collect_data.assert_called_once()

        # Проверяем, что open был вызван с правильным путем
        mock_file.assert_called_once_with("storage/spektakli.json")

        # Проверяем, что user_states обновлен корректно
        assert user_id in user_states
        assert user_states[user_id] == {
            "index": 0,
            "storage": [{
                "name": "Test Event 3",
                "link": "https://test.link",
                "priceMin": 100,
                "author": "Test Author 3",
                "place": "Test Venue 3"
            }],
            "message_id": message_id
        }

        # Проверяем вызов send_event_card с правильными аргументами
        mock_send_event_card.assert_called_once_with(
            user_id,
            chat_id,
            message_id,
            mock_bot  # Здесь проверяем, что передали замоканный объект бота
        )
