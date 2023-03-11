from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hcode, hide_link

from tgbot.keyboards import inline
from tgbot.misc.states import EditMenu
from tgbot.services.database import DataBase

edit_cards_router = Router()


async def get_formated_card_text(bot: Bot,
                                 user_tg_id: int | str,
                                 db: DataBase,
                                 card_id: int | str,
                                 message_id: int | str) -> int:

    card_id, card_title, card_number, card_logo = db.get_card(user_tg_id, card_id)
    await bot.edit_message_text(chat_id=user_tg_id, message_id=message_id,
                                text=f'Назва: {hcode(card_title)}\n'
                                     f'Номер/адреса: {hcode(card_number)}\n'
                                     f'Логотип: {hide_link(card_logo)}',
                                reply_markup=inline.keyboard_edit_menu)

    return card_id


@edit_cards_router.callback_query(EditMenu.check_card)
async def check_card(call: CallbackQuery, state: FSMContext, db: DataBase, bot: Bot):
    if call.data == 'back':
        await call.answer('Меню закрите❌')
        await call.message.delete()
        await state.clear()
    else:
        card_id = await get_formated_card_text(bot, call.from_user.id, db, call.data, call.message.message_id)
        await state.update_data(card_id=card_id)
        await state.set_state(EditMenu.edit)


@edit_cards_router.callback_query(EditMenu.edit)
async def edit_card_menu(call: CallbackQuery, state: FSMContext, db: DataBase):
    if call.data == inline.button_back.callback_data:
        cards = db.get_all_cards(call.from_user.id)
        await call.message.edit_text('Обери картку:', reply_markup=inline.keyboard_get_cards(cards))
        await state.set_state(EditMenu.check_card)

    elif call.data == inline.button_edit_title.callback_data:
        await call.message.edit_text('Відправ нову назву картки/гаманця', reply_markup=inline.keyboard_back)
        await state.set_state(EditMenu.get_title)

    elif call.data == inline.button_edit_number.callback_data:
        await call.message.edit_text('Відправ новий номер картки або крипто гаманець',
                                     reply_markup=inline.keyboard_back)
        await state.set_state(EditMenu.get_number)

    elif call.data == inline.button_edit_logo.callback_data:
        await call.message.edit_text('Обери новий логотип:', reply_markup=inline.keyboard_choice_logo_and_back)
        await state.set_state(EditMenu.get_logo)
        print(await state.get_state())

    elif call.data == inline.button_delete_card.callback_data:
        await call.message.edit_text('Ти впевнений(на), що хочеш:', reply_markup=inline.keyboard_yes_or_no)
        await state.set_state(EditMenu.delete)
        print(await state.get_state())


@edit_cards_router.callback_query(F.data == inline.button_back.callback_data)
async def bcak_to_edit_card_menu(call: CallbackQuery, state: FSMContext, db: DataBase, bot: Bot):
    data = await state.get_data()
    card_id = data.get('card_id')
    message_id = data.get('message_id')
    await get_formated_card_text(bot, call.from_user.id, db, card_id, message_id)

    await state.set_state(EditMenu.edit)


@edit_cards_router.message(EditMenu.get_title, F.text)
async def get_card_title(message: Message, state: FSMContext, db: DataBase, bot: Bot):
    data = await state.get_data()
    card_id = data.get('card_id')
    message_id = data.get('message_id')

    db.update_card_title(card_id, message.text)
    await message.delete()

    await get_formated_card_text(bot, message.from_user.id, db, card_id, message_id)
    await state.set_state(EditMenu.edit)


@edit_cards_router.message(EditMenu.get_number, F.text)
async def get_card_title(message: Message, state: FSMContext, db: DataBase, bot: Bot):
    data = await state.get_data()
    card_id = data.get('card_id')
    message_id = data.get('message_id')

    db.update_card_number(card_id, message.text)
    await message.delete()

    await get_formated_card_text(bot, message.from_user.id, db, card_id, message_id)
    await state.set_state(EditMenu.edit)


@edit_cards_router.callback_query(EditMenu.delete)
async def get_card_title(call: CallbackQuery, state: FSMContext, db: DataBase, bot: Bot):
    data = await state.get_data()
    card_id = data.get('card_id')
    message_id = data.get('message_id')

    if call.data == inline.button_no.callback_data:
        await call.answer()
        await get_formated_card_text(bot, call.from_user.id, db, card_id, message_id)
        await state.set_state(EditMenu.edit)
    else:
        db.delete_card(card_id)
        cards = db.get_all_cards(call.from_user.id)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=message_id, text='Обери картку:',
                                    reply_markup=inline.keyboard_get_cards(cards))
        await state.set_state(EditMenu.check_card)
