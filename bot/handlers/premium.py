from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "⭐ بخش پرمیوم")
async def premium_section(message: Message):
    text = """
⭐ بخش پرمیوم

در این بخش کاربران ویژه می‌توانند به اطلاعات کامل‌تر دسترسی داشته باشند:

🔒 لیست کامل دانشگاه‌ها
🔒 شهریه‌های دقیق
🔒 چک‌لیست مدارک
🔒 نمونه فایل‌ها
🔒 راهنمای ویزای تحصیلی
🔒 راهنمای مصاحبه سفارت
🔒 بررسی اولیه پرونده

برای فعال‌سازی دسترسی پرمیوم، با مشاور ارتباط بگیرید.
"""

    await message.answer(text)
