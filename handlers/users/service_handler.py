import re
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from keyboards.inline.service_buttons import service_buttons
from loader import dp
from states.service_state import choice_service as c_s
from states.login_state import log_in
from aiogram.dispatcher import FSMContext
from keyboards.default import cancel


@dp.message_handler(text="Сделать запрос", state=None)
async def enter_service(message: Message):

    if (False):
        await message.answer(text=f"Вы выбрали {message.text}", reply_markup=cancel)
        await message.answer(text="Пожалуйста, выберете один из пунктов", reply_markup=service_buttons)
        await c_s.choice.set()
    else:
        await message.answer(text="Пожалуйста, введите номер телефона для авторизации", reply_markup=cancel)
        await log_in.auth.set()

@dp.message_handler(state=log_in.auth)
async def auth(message: Message, state: FSMContext):
    r = message.text
    pattern = r'\b\+?[7,8](\s*\d{3}\s*\d{3}\s*\d{2}\s*\d{2})\b'
    if re.match(pattern, r):

        await message.answer(text="Пожалуйста, выберете один из пунктов", reply_markup=service_buttons)
        await c_s.choice.set()
    else:
        await message.answer(text="Неверный формат\nПожалуйста введите номер телефона правильно")
        await log_in.auth.set()