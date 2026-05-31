from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu_keyboard(is_admin: bool = False):
    keyboard = [
        [
            KeyboardButton(text="🎓 تحصیل در رومانی"),
            KeyboardButton(text="💼 مهاجرت کاری"),
        ],
        [
            KeyboardButton(text="🏙 شهرها و دانشگاه‌ها"),
            KeyboardButton(text="⭐ بخش پرمیوم"),
        ],
        [
            KeyboardButton(text="📝 مشاوره رایگان"),
            KeyboardButton(text="📞 ارتباط با مشاور"),
        ],
    ]

    if is_admin:
        keyboard.append(
            [
                KeyboardButton(text="🛠 پنل ادمین")
            ]
        )

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
