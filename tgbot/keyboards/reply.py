from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


button_back = KeyboardButton(text='Назад↩️')
keyboard_back = ReplyKeyboardBuilder().row(button_back).as_markup(resize_keyboard=True)

button_add_card = KeyboardButton(text='Додати💳')
button_edit_card = KeyboardButton(text='Редагувати📝')
button_check_card = KeyboardButton(text='Переглянути🗂')
# button_how_to_use = KeyboardButton(text='Як користуватися❓')
keyboard_home = ReplyKeyboardBuilder().row(button_add_card, button_edit_card,
                                           button_check_card,
                                           width=2).as_markup(resize_keyboard=True)
