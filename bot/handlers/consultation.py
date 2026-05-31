from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from bot.keyboards.main_menu import main_menu_keyboard
from bot.services.consultation_service import create_consultation_request
from bot.services.admin_notify_service import notify_admins_about_consultation

from bot.config import ADMIN_IDS

router = Router()


class ConsultationForm(StatesGroup):
    full_name = State()
    age = State()
    education_level = State()
    interested_field = State()
    residence_country = State()
    phone_number = State()
    budget = State()
    language_certificate = State()
    extra_description = State()


def cancel_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ لغو فرم")]
        ],
        resize_keyboard=True
    )


@router.message(F.text == "📝 مشاوره رایگان")
async def consultation_start(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        """
📝 فرم مشاوره رایگان پروما ویزا

در این بخش شرایط اولیه شما برای ویزای تحصیلی رومانی بررسی می‌شود.

لطفاً مرحله‌به‌مرحله به سوالات پاسخ دهید.

سوال ۱ از ۹:
نام و نام خانوادگی خود را وارد کنید:
""",
        reply_markup=cancel_keyboard()
    )

    await state.set_state(ConsultationForm.full_name)


@router.message(F.text == "❌ لغو فرم")
async def cancel_form(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "فرم مشاوره لغو شد.",
        reply_markup=main_menu_keyboard(is_admin=message.from_user.id in ADMIN_IDS)
    )


@router.message(ConsultationForm.full_name)
async def process_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)

    await message.answer(
        """
سوال ۲ از ۹:
سن خود را وارد کنید:

مثال:
۲۴
"""
    )

    await state.set_state(ConsultationForm.age)


@router.message(ConsultationForm.age)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)

    await message.answer(
        """
سوال ۳ از ۹:
آخرین مدرک تحصیلی شما چیست؟

مثال:
دیپلم تجربی
کارشناسی پرستاری
کارشناسی ارشد مدیریت
"""
    )

    await state.set_state(ConsultationForm.education_level)


@router.message(ConsultationForm.education_level)
async def process_education_level(message: Message, state: FSMContext):
    await state.update_data(education_level=message.text)

    await message.answer(
        """
سوال ۴ از ۹:
به چه رشته‌ای در رومانی علاقه دارید؟

مثال:
پزشکی
دندانپزشکی
داروسازی
کامپیوتر
مدیریت
"""
    )

    await state.set_state(ConsultationForm.interested_field)


@router.message(ConsultationForm.interested_field)
async def process_interested_field(message: Message, state: FSMContext):
    await state.update_data(interested_field=message.text)

    await message.answer(
        """
سوال ۵ از ۹:
در حال حاضر در کدام کشور زندگی می‌کنید؟

مثال:
ایران
رومانی
ترکیه
امارات
"""
    )

    await state.set_state(ConsultationForm.residence_country)


@router.message(ConsultationForm.residence_country)
async def process_residence_country(message: Message, state: FSMContext):
    await state.update_data(residence_country=message.text)

    await message.answer(
        """
سوال ۶ از ۹:
شماره تماس خود را وارد کنید:

مثال:
+98912...
یا
+40730...
"""
    )

    await state.set_state(ConsultationForm.phone_number)


@router.message(ConsultationForm.phone_number)
async def process_phone_number(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)

    await message.answer(
        """
سوال ۷ از ۹:
بودجه تقریبی شما برای تحصیل چقدر است؟

مثال:
سالی ۸۰۰۰ یورو
سالی ۵۰۰۰ یورو
هنوز دقیق نمی‌دانم
"""
    )

    await state.set_state(ConsultationForm.budget)


@router.message(ConsultationForm.budget)
async def process_budget(message: Message, state: FSMContext):
    await state.update_data(budget=message.text)

    await message.answer(
        """
سوال ۸ از ۹:
آیا مدرک زبان دارید؟

مثال:
آیلتس دارم
مدرک زبان ندارم
زبان انگلیسی متوسط
زبان رومانیایی ندارم
"""
    )

    await state.set_state(ConsultationForm.language_certificate)


@router.message(ConsultationForm.language_certificate)
async def process_language_certificate(message: Message, state: FSMContext):
    await state.update_data(language_certificate=message.text)

    await message.answer(
        """
سوال ۹ از ۹:
اگر توضیح اضافه‌ای دارید بنویسید.

مثلاً:
قبلاً ویزا ریجکت شدم
می‌خواهم با خانواده اقدام کنم
عجله دارم برای ترم بعد
اگر توضیحی ندارید بنویسید: ندارم
"""
    )

    await state.set_state(ConsultationForm.extra_description)


@router.message(ConsultationForm.extra_description)
async def process_extra_description(message: Message, state: FSMContext):
    await state.update_data(extra_description=message.text)

    data = await state.get_data()

    request = await create_consultation_request(
        telegram_id=message.from_user.id,
        data=data
    )

    await notify_admins_about_consultation(
        bot=message.bot,
        request=request,
        data=data
    )

    await state.clear()

    summary = f"""
✅ درخواست مشاوره شما با موفقیت ثبت شد.

کد درخواست شما:
#{request.id}

خلاصه اطلاعات ثبت‌شده:

نام:
{data.get("full_name")}

سن:
{data.get("age")}

مدرک تحصیلی:
{data.get("education_level")}

رشته مورد علاقه:
{data.get("interested_field")}

کشور محل اقامت:
{data.get("residence_country")}

شماره تماس:
{data.get("phone_number")}

بودجه:
{data.get("budget")}

مدرک زبان:
{data.get("language_certificate")}

توضیحات:
{data.get("extra_description")}

مشاوران پروما ویزا اطلاعات شما را بررسی می‌کنند.

📞 واتساپ / تلگرام:
+40730480000
"""

    await message.answer(
        summary,
        reply_markup=main_menu_keyboard(is_admin=message.from_user.id in ADMIN_IDS)
    )


@router.message(F.text == "📞 ارتباط با مشاور")
async def contact_consultant(message: Message):
    text = """
📞 ارتباط با مشاور پروما ویزا

🇷🇴 مهاجرت تحصیلی رومانی | پروما ویزا 🇮🇷
Peroma ; drumul de succes

خدمت اصلی:
ویزای تحصیلی رومانی

جهت مشاوره از طریق واتساپ یا تلگرام:

+40730480000
"""

    await message.answer(text)
