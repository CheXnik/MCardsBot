from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

# -------------------------------------------------------------------------------------------------------- keyboard back
button_back = InlineKeyboardButton(text='Повернутись↩️', callback_data='back')
keyboard_back = InlineKeyboardBuilder().row(button_back, width=1).as_markup()

# --------------------------------------------------------------------------------------------------- keyboard yes or no
button_yes = InlineKeyboardButton(text='Так✅', callback_data='yes')
button_no = InlineKeyboardButton(text='Ні❌', callback_data='no')
keyboard_yes_or_no = InlineKeyboardBuilder().row(button_yes, button_no, width=2).as_markup()

# ------------------------------------------------------------------------------------------------- keyboard choice logo
butoon_choice_logo = InlineKeyboardButton(text='Обрати логотип✨', switch_inline_query_current_chat='логотипи')
keyboard_choice_logo = InlineKeyboardBuilder().row(butoon_choice_logo).as_markup()
keyboard_choice_logo_and_back = InlineKeyboardBuilder().row(butoon_choice_logo, button_back, width=1).as_markup()

# ----------------------------------------------------------------------------------------------- keyboard test new card
butoon_test_in_chat = InlineKeyboardButton(text='Спробувати в чаті📄', switch_inline_query_current_chat='')
butoon_send_card = InlineKeyboardButton(text='Відправити комусь📨', switch_inline_query='')

keyboard_test_new_card = InlineKeyboardBuilder().row(butoon_test_in_chat, butoon_send_card, width=1).as_markup()

# --------------------------------------------------------------------------------------------------- keyboard edit menu
button_edit_title = InlineKeyboardButton(text='Редагувати назву📝', callback_data='edit_title')
button_edit_number = InlineKeyboardButton(text='Редагувати номер/гаманець📝', callback_data='edit_number')
button_edit_logo = InlineKeyboardButton(text='Редагувати логотип🖼', callback_data='edit_logo')
button_delete_card = InlineKeyboardButton(text='Видалити🗑', callback_data='delete')

keyboard_edit_menu = InlineKeyboardBuilder().row(button_edit_title, button_edit_number, button_edit_logo,
                                                 button_delete_card, button_back, width=1).as_markup()


# ----------------------------------------------------------------------------------------------- keyboard get all cards
def keyboard_get_cards(cards: tuple[tuple[...]]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for card_id, card_title, *_ in cards:
        keyboard.row(InlineKeyboardButton(text=card_title, callback_data=card_id))

    return keyboard.as_markup()
