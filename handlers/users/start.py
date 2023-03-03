from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.default import menu, cancel
from aiogram.dispatcher.filters import Command
from loader import dp
from aiogram.dispatcher.filters.state import StatesGroup, State
from settings import ROOT_FOR_SAVE_IMAGES, URL_DJANGO
import requests

uslovia_description = """
Мы рады делать Ваши покупки комфортными 🛍и просим ознакомиться с условиями/
👉Мы заботимся о выкупе по лучшей цене и доставке без сюрпризов и не отвечаем за то, как ведут себя вещи в носке – не отвечаем за скрип подошвы и образование катышков
👉Мы поможем вам определить свой размер и предоставим размерную сетку, но решение о том, какой размер заказать, Вы должны принимать самостоятельно!
👉Про возврат
Мы сервис по выкупу и доставке товаров, возврата и обмена нет и не будет.
Если вещь не подошла Вы можете пристроить ее на авито/юла
"""

how_buy_description = """
Пришлите в этот чат:
- фото вещи
- нужный размер
"""

about_delivery_desctiption = """
Мы работаем с  самыми надёжными транспортными компаниями и выбираем для вас лучшие тарифы!
Средний срок доставки из США 5/7 недель с момента заказа! 
Стоимость доставки - 180/100гр
Вес товара, а также стоимость доставки определяется по факту поступления заказов на склад в РФ.
Существует возможность доставки ваших товаров напрямую сразу до вас, условия обсуждаются в индивидуальном порядке.
Всю обувь мы отправляем без коробок, если индивидуально не оговорено иное.
В связи с ситуацией в мире, перевозчики не гарантируют доставку в срок, это никак не компенсируется и мы за это ответственность не несём! 
Будьте готовы ждать и до 5 мес! Возврата за долгое ожидания нет!
Мы гарантируем вам доставку товара либо возврат денежных средств, в случае, если товар не пришёл в течении 6 месяцев!

"""


@dp.message_handler(CommandStart())
async def show_menu(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!\nЗадайте вопрос или узнайте о нас больше, выбрав нужный раздел👇")
    await message.answer("Пожалуйста, выберите пункт из меню", reply_markup=menu)

@dp.message_handler(text='Условия')
async def uslovia(message: Message):
    await message.answer(uslovia_description)

@dp.message_handler(text='Как заказать')
async def how_buy(message: Message):
    await message.answer(how_buy_description)

@dp.message_handler(text='Все о доставке')
async def about_delivery(message: Message):
    await message.answer(about_delivery_desctiption)


@dp.message_handler(text="отмена", state="*")
async def back_from_reg(message: Message, state=FSMContext):
    await state.finish()
    await message.answer("Вы вернулись в главное меню", reply_markup=menu)


class MakeOrder(StatesGroup):
    input_size = State()


@dp.message_handler(content_types=['photo'])
async def get_photo(message: types.Message, state=FSMContext):
    try:
        file_name = f'{message.message_id}.png'
        await message.photo[-1].download(destination_file= ROOT_FOR_SAVE_IMAGES + file_name)
        await message.answer('Введите размер выбранного товара')
        await MakeOrder.input_size.set()
        await state.update_data(order_image=file_name)
    except Exception as e:
        print(e)


@dp.message_handler(state=MakeOrder.input_size)
async def get_photo(message: types.Message, state=FSMContext):
    state_data = await state.get_data()
    order_image = state_data['order_image']

    data_req = {
        'size': message.text,
        'contact': message.from_user.url,
        'image': order_image,
    }

    req_add_order = requests.post(URL_DJANGO + 'create/order/', json=data_req)

    if req_add_order.status_code == 200:
        await message.answer('Заказ успешно отправлен, с вами свяжется менеджер')
        await state.finish()
    else:
        await message.answer('Ошибка на сервере, повторите попытку позже!')
        await state.finish()
