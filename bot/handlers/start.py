from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from bot.keyboards.main_menu import main_menu_keyboard
from bot.services.user_service import register_or_update_user, update_user_phone

router = Router()


def request_contact_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📱 ارسال شماره تلگرام",
                    request_contact=True
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def start_text(full_name: str, premium_status: str):
    return f"""
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


@router.message(CommandStart())
async def start_command(message: Message):
    user = await register_or_update_user(message.from_user)

    if not user.contact_shared or not user.phone_number:
        await message.answer(
            """
برای شروع استفاده از بات پروما ویزا، لطفاً شماره تلگرام خود را ارسال کنید.

این شماره فقط برای ثبت اطلاعات اولیه، پیگیری مشاوره و ارتباط با شما استفاده می‌شود.

برای ادامه روی دکمه زیر بزنید:
""",
            reply_markup=request_contact_keyboard()
        )
        return

    full_name = message.from_user.full_name
    premium_status = "فعال ✅" if user.is_premium else "غیرفعال 🔒"

    await message.answer(
        text=start_text(full_name, premium_status),
        reply_markup=main_menu_keyboard(is_admin=user.is_admin)
    )


@router.message(F.contact)
async def receive_contact(message: Message):
    contact = message.contact

    if contact.user_id != message.from_user.id:
        await message.answer(
            "لطفاً شماره تلگرام خودتان را با دکمه ارسال شماره تلگرام بفرستید.",
            reply_markup=request_contact_keyboard()
        )
        return

    user = await update_user_phone(
        telegram_id=message.from_user.id,
        phone_number=contact.phone_number
    )

    if not user:
        await message.answer("خطا در ثبت شماره. لطفاً دوباره /start را بزنید.")
        return

    full_name = message.from_user.full_name
    premium_status = "فعال ✅" if user.is_premium else "غیرفعال 🔒"

    await message.answer(
        "✅ شماره تلگرام شما با موفقیت ثبت شد.",
        reply_markup=main_menu_keyboard(is_admin=user.is_admin)
    )

    await message.answer(
        text=start_text(full_name, premium_status),
        reply_markup=main_menu_keyboard(is_admin=user.is_admin)
    )
