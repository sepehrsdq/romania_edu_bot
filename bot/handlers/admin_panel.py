import asyncio

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from bot.config import ADMIN_IDS
from bot.keyboards.main_menu import main_menu_keyboard
from bot.services.user_service import get_all_active_users

router = Router()


class BroadcastForm(StatesGroup):
    waiting_for_message = State()
    waiting_for_confirm = State()


def is_admin_user(telegram_id: int) -> bool:
    return telegram_id in ADMIN_IDS


def admin_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📢 ارسال پیام همگانی")],
            [KeyboardButton(text="🔙 بازگشت به منوی اصلی")],
        ],
        resize_keyboard=True
    )


def broadcast_confirm_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="✅ تایید و ارسال"),
                KeyboardButton(text="❌ لغو ارسال"),
            ]
        ],
        resize_keyboard=True
    )


@router.message(F.text == "🛠 پنل ادمین")
async def admin_panel(message: Message):
    if not is_admin_user(message.from_user.id):
        await message.answer("شما دسترسی ادمین ندارید.")
        return

    await message.answer(
        """
🛠 پنل ادمین پروما ویزا

از این بخش می‌توانید عملیات مدیریتی بات را انجام دهید.

گزینه‌های فعلی:
📢 ارسال پیام همگانی به کاربران
""",
        reply_markup=admin_keyboard()
    )


@router.message(F.text == "🔙 بازگشت به منوی اصلی")
async def back_to_main_menu(message: Message, state: FSMContext):
    await state.clear()

    is_admin = is_admin_user(message.from_user.id)

    await message.answer(
        "به منوی اصلی برگشتید.",
        reply_markup=main_menu_keyboard(is_admin=is_admin)
    )


@router.message(F.text == "📢 ارسال پیام همگانی")
async def broadcast_start(message: Message, state: FSMContext):
    if not is_admin_user(message.from_user.id):
        await message.answer("شما دسترسی ادمین ندارید.")
        return

    await state.clear()

    await message.answer(
        """
📢 ارسال پیام همگانی

متنی که می‌خواهید برای همه کاربران ارسال شود را بفرستید.

مثال:

🇷🇴 ثبت‌نام ترم جدید دانشگاه‌های رومانی شروع شد.

برای بررسی شرایط خود با پروما ویزا در ارتباط باشید:
+40730480000
"""
    )

    await state.set_state(BroadcastForm.waiting_for_message)


@router.message(BroadcastForm.waiting_for_message)
async def broadcast_get_message(message: Message, state: FSMContext):
    if not is_admin_user(message.from_user.id):
        await message.answer("شما دسترسی ادمین ندارید.")
        await state.clear()
        return

    broadcast_text = message.text

    if not broadcast_text or len(broadcast_text.strip()) < 2:
        await message.answer("متن پیام خیلی کوتاه است. لطفاً پیام کامل‌تری وارد کنید.")
        return

    await state.update_data(broadcast_text=broadcast_text)

    preview = f"""
📢 پیش‌نمایش پیام همگانی:

{broadcast_text}

آیا این پیام برای همه کاربران ارسال شود؟
"""

    await message.answer(
        preview,
        reply_markup=broadcast_confirm_keyboard()
    )

    await state.set_state(BroadcastForm.waiting_for_confirm)


@router.message(BroadcastForm.waiting_for_confirm)
async def broadcast_confirm(message: Message, state: FSMContext):
    if not is_admin_user(message.from_user.id):
        await message.answer("شما دسترسی ادمین ندارید.")
        await state.clear()
        return

    if message.text == "❌ لغو ارسال":
        await state.clear()
        await message.answer(
            "ارسال پیام همگانی لغو شد.",
            reply_markup=admin_keyboard()
        )
        return

    if message.text != "✅ تایید و ارسال":
        await message.answer("لطفاً یکی از گزینه‌های تایید یا لغو را انتخاب کنید.")
        return

    data = await state.get_data()
    broadcast_text = data.get("broadcast_text")

    if not broadcast_text:
        await state.clear()
        await message.answer(
            "متن پیام پیدا نشد. لطفاً دوباره تلاش کنید.",
            reply_markup=admin_keyboard()
        )
        return

    users = await get_all_active_users()

    total_users = len(users)
    success_count = 0
    failed_count = 0

    await message.answer(
        f"ارسال پیام شروع شد.\nتعداد کاربران هدف: {total_users}"
    )

    for user in users:
        try:
            await message.bot.send_message(
                chat_id=user.telegram_id,
                text=broadcast_text
            )
            success_count += 1

            # برای جلوگیری از محدودیت تلگرام
            await asyncio.sleep(0.05)

        except Exception as e:
            failed_count += 1
            print(f"Broadcast failed for {user.telegram_id}: {e}")

    await state.clear()

    result_text = f"""
✅ ارسال پیام همگانی تمام شد.

تعداد کل کاربران:
{total_users}

ارسال موفق:
{success_count}

ارسال ناموفق:
{failed_count}
"""

    await message.answer(
        result_text,
        reply_markup=admin_keyboard()
    )
