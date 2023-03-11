from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

instruction_router = Router()


@instruction_router.callback_query()
async def next_slide(call: CallbackQuery, stete: FSMContext):
    ...


@instruction_router.callback_query()
async def previous_slide(call: CallbackQuery, stete: FSMContext):
    ...


@instruction_router.callback_query()
async def close_menu(call: CallbackQuery, stete: FSMContext):
    ...
