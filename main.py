import asyncio
import logging

print("STEP 1: importing aiogram...")

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

print("STEP 2: importing project config...")

from bot.config import BOT_TOKEN
from bot.handlers import start, cities, premium, consultation

print("STEP 3: imports completed.")


async def main():
    logging.basicConfig(level=logging.INFO)

    print("STEP 4: creating bot...")

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    print("STEP 5: creating dispatcher...")

    dp = Dispatcher()

    print("STEP 6: including routers...")

    dp.include_router(start.router)
    dp.include_router(cities.router)
    dp.include_router(premium.router)
    dp.include_router(consultation.router)

    print("STEP 7: bot polling started.")
    print("Now go to Telegram and send /start")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
