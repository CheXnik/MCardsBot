from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tgbot.keyboards import reply, inline
from tgbot.misc.states import Card, EditMenu
from tgbot.services.database import DataBase

user_router = Router()


@user_router.message(CommandStart(F.args == 'add'))
@user_router.message(Command(commands=['add']))
@user_router.message(F.text == reply.button_add_card.text)
async def add_card(message: Message, state: FSMContext):
    await message.reply('Надійшли номер картки або адресу крипто гаманця:', reply_markup=reply.keyboard_back)
    await state.set_state(Card.get_number)


@user_router.message(CommandStart())
async def user_start(message: Message, db: DataBase):
    db.add_user(message.from_user.id)
    await message.answer_sticker('CAACAgIAAxkBAAEIBKFkBR0-qtfzLbIn1KM6YpLwAXP0BAACAQEAAladvQoivp8OuMLmNC4E')
    await message.reply('Привіт, я допоможу тобі зручно зберігати та відправляти твої номера карток та адреси крипто '
                        'гаманців.', reply_markup=reply.keyboard_home)


@user_router.message(Command(commands=['check']))
@user_router.message(F.text == reply.button_check_card.text)
async def check_card_numbers(message: Message):
    await message.answer(f'Обирай де подивитися:', reply_markup=inline.keyboard_test_new_card)


@user_router.message(Command(commands=['edit']))
@user_router.message(F.text == reply.button_edit_card.text)
async def edit_card_numbers(message: Message, state: FSMContext, db: DataBase):
    cards = db.get_all_cards(message.from_user.id)
    msg = await message.answer('Обери картку:', reply_markup=inline.keyboard_get_cards(cards))
    await state.update_data(message_id=msg.message_id)
    await state.set_state(EditMenu.check_card)


# @user_router.message(Command(commands=['how_to_use']))
# @user_router.message(F.text == reply.button_how_to_use.text)
# async def edit_card_numbers(message: Message, state: FSMContext):
#     ...
