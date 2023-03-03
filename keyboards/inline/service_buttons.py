from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_service import service_callback

service_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Добавить гостя", callback_data=service_callback.new(
                name="guests"
            ))
        ],
    ]
)
