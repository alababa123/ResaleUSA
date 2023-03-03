from aiogram.dispatcher.filters.state import StatesGroup, State


class choice_service(StatesGroup):
    choice: State = State()