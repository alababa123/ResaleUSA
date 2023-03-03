from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Условия"),
        ],
        [
            KeyboardButton(text="Как заказать"), 
        ],
        [
            KeyboardButton(text="Все о доставке"), 
        ],
    ],
    resize_keyboard=True
)

