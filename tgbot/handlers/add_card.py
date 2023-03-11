from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hitalic

from tgbot.keyboards import reply, inline
from tgbot.misc.states import Card
from tgbot.services.database import DataBase

add_card_router = Router()


@add_card_router.message(Card.get_number)
async def get_card_number(message: Message, state: FSMContext):
    if message.text == reply.button_back.text:
        await message.answer('Ти повернувся до головного меню↩️', reply_markup=reply.keyboard_home)
        await state.clear()
    else:
        await state.update_data(card_number=''.join(message.text.split()))
        await message.answer('Надійшли назву картки:')
        await state.set_state(Card.get_title)


@add_card_router.message(Card.get_title)
async def get_card_number(message: Message, state: FSMContext):
    if message.text == reply.button_back.text:
        await message.answer('Надійшли номер картки або адресу крипто гаманця:')
        await state.set_state(Card.get_number)
    else:
        choice_msg = await message.answer(f'Обери логотип(тисни на кнопку: {hitalic(inline.butoon_choice_logo.text)}), '
                                          f'або пропускай цей крок', reply_markup=inline.keyboard_choice_logo)
        await state.update_data(card_title=message.text)
        await state.update_data(choice_msg=choice_msg)
        await state.set_state(Card.get_logo)


@add_card_router.message(Card.get_logo, F.text == reply.button_back.text)
async def back_menu(message: Message, state: FSMContext):
    await message.answer('Надійшли назву картки:')
    await state.set_state(Card.get_title)


@add_card_router.message(Card.get_logo, F.photo)
async def get_card_number(message: Message, state: FSMContext, db: DataBase):
    data = await state.get_data()

    choice_msg: Message = data.get('choice_msg')
    card_number = data.get('card_number')
    card_title = data.get('card_title')
    logo_name = message.caption if message.caption is not None else 'auto'

    await choice_msg.edit_text(choice_msg.text)

    status = db.add_card(message.from_user.id, card_title, card_number, logo_name)

    if not status:
        await message.answer('Ну ти і опецьок, ти що мені скинув?\n'
                             'Пробуй ще раз🫥', reply_markup=reply.keyboard_home)
        await message.answer_sticker('CAACAgIAAxkBAAEICPJkBn-Xc0jqxaqUApw8WZ80Y_4NLwAC-wADVp29ClYO2zPbysnmLgQ')
    else:
        await message.answer('Успішний успіх, можеш користуватися', reply_markup=inline.keyboard_test_new_card)
        await message.answer_sticker('CAACAgIAAxkBAAEIBJ9kBRy_dTSRQUYZO65FPCJkMj-VjQACSAIAAladvQoc9XL43CkU0C4E',
                                     reply_markup=reply.keyboard_home)
    await state.clear()
