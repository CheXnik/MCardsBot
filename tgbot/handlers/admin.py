from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message

from tgbot.filters.admin import AdminFilter

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(StateFilter(None), F.document)
async def admin_start(message: Message):
    await message.answer(message.document.file_id)


@admin_router.message(StateFilter(None), F.photo)
async def admin_start(message: Message):
    await message.answer(message.photo[-1].file_id)
