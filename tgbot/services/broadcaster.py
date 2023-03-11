import asyncio
import logging

from aiogram import Bot
from aiogram import exceptions


async def send_message(bot: Bot, user_id, text: str, disable_notification: bool = False, keyboard=None) -> bool:
    try:
        await bot.send_message(user_id, text, disable_notification=disable_notification, reply_markup=keyboard)
    except exceptions.TelegramForbiddenError:
        logging.error(f"Target [ID:{user_id}]: got TelegramForbiddenError")
    except exceptions.TelegramRetryAfter as e:
        logging.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds.")
        await asyncio.sleep(e.retry_after)
        return await send_message(bot, user_id, text)
    except exceptions.TelegramAPIError:
        logging.exception(f"Target [ID:{user_id}]: failed")
    else:
        logging.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def broadcast(bot, users, text, keyboard=None) -> int:
    """
    Simple broadcaster
    :return: Count of messages
    """
    count = 0
    try:
        for user_id in users:
            if await send_message(bot, user_id, text, keyboard=keyboard):
                count += 1
            await asyncio.sleep(0.05)
    finally:
        logging.info(f"{count} messages successful sent.")

    return count
