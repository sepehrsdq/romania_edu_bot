from aiogram import Bot

from bot.config import ADMIN_IDS


async def notify_admins_about_consultation(bot: Bot, request, data: dict):
    if not ADMIN_IDS:
        return

    text = f"""
🔔 درخواست مشاوره جدید ثبت شد

کد درخواست:
#{request.id}

👤 نام:
{data.get("full_name")}

🎂 سن:
{data.get("age")}

🎓 آخرین مدرک:
{data.get("education_level")}

📚 رشته مورد علاقه:
{data.get("interested_field")}

🌍 کشور محل اقامت:
{data.get("residence_country")}

📞 شماره تماس:
{data.get("phone_number")}

💶 بودجه:
{data.get("budget")}

🗣 مدرک زبان:
{data.get("language_certificate")}

📝 توضیحات:
{data.get("extra_description")}

برای مشاهده و مدیریت کامل درخواست، وارد پنل ادمین شوید.
"""

    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=text
            )
        except Exception as e:
            print(f"Failed to send admin notification to {admin_id}: {e}")
