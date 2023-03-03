from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from keyboards.inline.reg_buttons import end_reg
from loader import dp
from states.registration import registration as reg
from aiogram.dispatcher import FSMContext
from keyboards.default import cancel
from keyboards.default import menu
from data.config import location as loc
import re
import mariadb
#import sys
try:
    conn = mariadb.connect(
        user="root",
        password="1202",
        host="127.0.0.1",
        port=3306,
        database="users"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")

# Get Cursor
cur = conn.cursor()

#cur.execute("CREATE TABLE users (name VARCHAR(255), phone VARCHAR(255), address VARCHAR(255))")

sql = "INSERT INTO users (name, phone, address) VALUES (%s, %s, %s)"
@dp.message_handler(text="Регистрация", state=None)
async def enter_reg(message: Message):
    await message.answer(f"Вы выбрали {message.text}", reply_markup=ReplyKeyboardRemove())
    await message.answer("При желании вы всегда можете выйти в главное меню, нажав кнопку отмена", reply_markup=cancel)
    await message.answer("Введите ФИО")
    await reg.fio.set()


@dp.message_handler(state=reg.fio)
async def reg_fio(message: Message, state: FSMContext):
    fio = message.text
    await message.answer("Введите номер телефона")
    await state.update_data(fio=fio)
    await reg.phone.set()



@dp.message_handler(state=reg.phone)
async def reg_phone(message: Message, state: FSMContext):
    r = message.text
    pattern = r'\b\+?[7,8](\s*\d{3}\s*\d{3}\s*\d{2}\s*\d{2})\b'
    if re.match(pattern, r):
        phone = message.text
        await message.answer("Введите адрес")
        await state.update_data(phone=phone)
        await reg.address.set()
    else:
        await message.answer("Неверный формат номера телефона")
        await message.answer("Пожалуйста, введите номер правильно")
        await reg.phone.set()


@dp.message_handler(state=reg.address)
async def reg_address(message: Message, state: FSMContext):
    address = message.text
    await message.answer("Отправьте главную страницу паспорта")
    await state.update_data(address=address)
    await reg.passport.set()


@dp.message_handler(state=reg.passport, content_types=['photo'])
async def reg_passport(message, state: FSMContext):
    passport = message.photo[-1]
    await passport.download(destination=loc + r"\\photos\\" + "pasport_" + str(message.from_user.id) + ".jpg")
    data = await state.get_data()
    await message.answer("Пожалуйста, проверте верна ли введеная информация\n"\
                        "ФИО: " + data.get("fio") + "\n"
                        "Номер телефона: " + data.get("phone") + "\n"\
                        "Адрес: " + data.get("address") + "\n", reply_markup=end_reg)
    await reg.check.set()


@dp.callback_query_handler(text_contains="reg", state=reg.check)
async def reg_check(call: CallbackQuery, state: FSMContext):
    callback_data = call.data
    mas = []
    data = await state.get_data()
    if callback_data == "reg:True":
        mis = ""
        cur.execute("SELECT name FROM users;")
        mis = cur.fetchall()
        await call.message.answer(mis)
        await call.message.answer("Ваша заявка отправленна на рассмотрение оператором", reply_markup=menu)
        mas.append(data.get("fio"))
        mas.append(data.get("phone"))
        mas.append(data.get("address"))
        cur.execute(sql, mas)
        conn.commit()
        await state.finish()
    else:
        await call.message.answer("Ничего страшного.\nНачнём сначала!")
        await call.message.answer("Введите ФИО")
        await reg.fio.set()
