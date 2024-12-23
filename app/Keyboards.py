from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Keyboards:
    # создаем функцию для создания клавиатуры с навигацией по карточкам
    def keyboard_navigation(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[

            [InlineKeyboardButton(text="⬅️ Назад", callback_data="previous"),
             InlineKeyboardButton(text="Вперед ➡️", callback_data="next")],

            [InlineKeyboardButton(text='🏠 Меню', callback_data='back')]
        ])
    # создаем функцию с клавиуатурой для выбора категории мероприятия

    def keyboard_categories(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[

            [InlineKeyboardButton(text='Спектакли', callback_data='performances'),
             InlineKeyboardButton(text='Концерты', callback_data='concerts')],

            [InlineKeyboardButton(text='Выставки', callback_data='exhibitions')]
        ])
