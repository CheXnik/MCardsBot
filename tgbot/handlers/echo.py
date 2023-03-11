from aiogram import Router
from aiogram.types import Message

from tgbot.keyboards import reply

echo_router = Router()


@echo_router.message()
async def echo_mesage(message: Message):
    await message.answer('Ну ти і опецьок, ти що мені скинув?\n'
                         'Пробуй ще раз🫥', reply_markup=reply.keyboard_home)
    await message.answer_sticker('CAACAgIAAxkBAAEIEe1kCnOPiqqfUemCPWRhiZHATrs0FQACAgEAAladvQpO4myBy0Dk_y8E')
