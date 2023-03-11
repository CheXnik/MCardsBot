from aiogram import Router, F
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultCachedPhoto
from aiogram.utils.markdown import hcode

from tgbot.services.database import DataBase
from tgbot.services.utils import card_formated

inline_router = Router()


@inline_router.inline_query(F.query == 'логотипи')
async def show_user_images(inline_query: InlineQuery, db: DataBase):
    results = []
    logos = db.get_all_logos()

    for logo_id, caption, file_id in logos:
        results.append(InlineQueryResultCachedPhoto(
            id=str(logo_id),
            photo_file_id=file_id,
            caption=caption
        ))

    await inline_query.answer(
        results, is_personal=True
    )


@inline_router.inline_query()
async def show_user_images(inline_query: InlineQuery, db: DataBase):
    user_cards = db.get_all_cards(user_tg_id=inline_query.from_user.id)
    results = []

    for card_id, card_ttitle, card_number, thumb_url in user_cards:
        results.append(InlineQueryResultArticle(
            id=str(card_id),
            title=card_ttitle,
            description=f'{card_formated(card_number)}',
            input_message_content=InputTextMessageContent(
                message_text=f'Мій {card_ttitle}:\n{hcode(card_number)}',
                parse_mode="HTML"
            ),
            thumb_url=thumb_url if thumb_url != 'None' else None
        ))

    await inline_query.answer(
        results, is_personal=True,
        switch_pm_text="Додати ще 💳",
        switch_pm_parameter="add",
        cache_time=10
    )
