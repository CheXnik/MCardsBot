from  .user import user_router
from .echo import echo_router
from .admin import admin_router
from .inline_mode import inline_router
from .edit_cards import edit_cards_router
from .add_card import add_card_router
from .instruction import instruction_router

__all__ = [
    'user_router',
    'echo_router',
    'admin_router',
    'inline_router',
    'edit_cards_router',
    'add_card_router',
]
