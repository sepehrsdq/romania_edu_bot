# 🇷🇴 Romania Education Migration Telegram Bot | Peroma Visa

A professional Telegram bot and admin panel for managing Romania education migration services.

Brand:

**🇷🇴 مهاجرت تحصیلی رومانی | پروما ویزا 🇮🇷**  
**Peroma ; drumul de succes**  
رومانی؛ کشوری امن، ارزان و زیبا، عضو اتحادیه اروپا

Main service:

**ویزای تحصیلی رومانی**

Contact:

**WhatsApp / Telegram:** +40730480000

---

## Project Features

- Telegram bot built with Python and aiogram
- PostgreSQL database
- Django Admin panel
- Modern admin interface with Django Unfold
- Dynamic cities and universities
- Premium user system
- Consultation form with step-by-step questions
- Consultation requests stored in database
- Admin notifications on Telegram
- Broadcast message system for admins
- Persistent deployment with systemd
- Nginx reverse proxy for admin panel

---

## Tech Stack

- Python 3
- aiogram
- Django
- Django Unfold
- PostgreSQL
- SQLAlchemy
- asyncpg
- Gunicorn
- Nginx
- systemd

---

## Project Structure

```
romania_edu_bot/
├── admin_panel/              # Django project settings
├── bot/                      # Telegram bot source code
│   ├── database/             # SQLAlchemy models and DB session
│   ├── handlers/             # Bot handlers
│   ├── keyboards/            # Telegram keyboards
│   └── services/             # Business logic services
├── core/                     # Django models/admin integration
├── manage.py                 # Django management file
├── requirements.txt          # Python dependencies
├── .env.example              # Example environment variables
├── .gitignore
└── README.md
