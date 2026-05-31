import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from bot.config import BOT_TOKEN
from bot.handlers import start, cities, premium, consultation, admin_panel


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(cities.router)
    dp.include_router(premium.router)
    dp.include_router(consultation.router)
    dp.include_router(admin_panel.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
