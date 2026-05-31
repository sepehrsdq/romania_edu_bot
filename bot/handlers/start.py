from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.keyboards.main_menu import main_menu_keyboard
from bot.services.user_service import register_or_update_user

router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    user = await register_or_update_user(message.from_user)

    full_name = message.from_user.full_name
    premium_status = "فعال ✅" if user.is_premium else "غیرفعال 🔒"

    text = f"""
سلام {full_name} عزیز 👋

به بات رسمی پروما ویزا خوش آمدید 🇷🇴🇮🇷

🇷🇴 مهاجرت تحصیلی رومانی | پروما ویزا 🇮🇷
Peroma ; drumul de succes

رومانی کشوری امن، ارزان و زیبا و عضو اتحادیه اروپا است.

در این بات می‌توانید:

🎓 اطلاعات تحصیل در رومانی را ببینید
🏙 شهرها و دانشگاه‌های رومانی را بررسی کنید
📄 با مدارک و مراحل ویزای تحصیلی آشنا شوید
⭐ از بخش پرمیوم استفاده کنید
📝 فرم مشاوره اولیه را تکمیل کنید

وضعیت پرمیوم شما: {premium_status}

جهت مشاوره:
واتساپ / تلگرام
+40730480000

لطفاً یکی از گزینه‌های زیر را انتخاب کنید:
"""

    await message.answer(
        text=text,
        reply_markup=main_menu_keyboard(is_admin=user.is_admin)
    )
