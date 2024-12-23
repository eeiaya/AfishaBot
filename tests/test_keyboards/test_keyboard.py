import pytest
from aiogram.types import InlineKeyboardMarkup
from app.Keyboards import Keyboards



def test_keyboard_navigation():

    # создаем экземпляр класса клавиатуры
    keyboards = Keyboards()

    keyboard_navigation = keyboards.keyboard_navigation()

    # проверяем что вернулся объект класса InlineKeyboardMarkup
    assert isinstance(keyboard_navigation, InlineKeyboardMarkup)
    # проверяем что клавиатура содержит две строки кнопок
    assert len(keyboard_navigation.inline_keyboard) == 2
    # проверяем что в первой строке кнопок находится две кнопки
    first_row = keyboard_navigation.inline_keyboard[0]
    assert len(first_row) == 2
    #проверяем содержимое кнопок
    assert first_row[0].text == '⬅️ Назад'
    assert first_row[0].callback_data == 'previous'
    # проверяем содержимое кнопок
    assert first_row[1].text == 'Вперед ➡️'
    assert first_row[1].callback_data == 'next'

    # проверяем что во второй строке одна кнопка
    second_row = keyboard_navigation.inline_keyboard[1]
    assert len(second_row) == 1

    assert second_row[0].text == '🏠 Меню'
    assert second_row[0].callback_data == 'back'

def test_keyboard_categories():

    keyboard = Keyboards()

    keyboard_categories = keyboard.keyboard_categories()

    assert isinstance(keyboard_categories, InlineKeyboardMarkup)

    assert len(keyboard_categories.inline_keyboard) == 2

    first_row = keyboard_categories.inline_keyboard[0]
    assert len(first_row) == 2

    assert first_row[0].text == 'Спектакли'
    assert first_row[0].callback_data == 'performances'

    assert first_row[1].text == 'Концерты'
    assert first_row[1].callback_data == 'concerts'

    second_row = keyboard_categories.inline_keyboard[1]
    assert len(second_row) == 1

    assert second_row[0].text == 'Выставки'
    assert second_row[0].callback_data == 'exhibitions'

