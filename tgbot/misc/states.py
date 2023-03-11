from aiogram.fsm.state import StatesGroup, State


class Card(StatesGroup):
    get_number = State()
    get_title = State()
    get_logo = State()


class EditMenu(StatesGroup):
    check_card = State()
    edit = State()
    get_title = State()
    get_number = State()
    get_logo = State()
    delete = State()
