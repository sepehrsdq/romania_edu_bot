from sqlalchemy import select

from bot.database.models import ConsultationRequest, TelegramUser
from bot.database.session import AsyncSessionLocal


async def create_consultation_request(telegram_id: int, data: dict):
    async with AsyncSessionLocal() as session:
        user_result = await session.execute(
            select(TelegramUser).where(TelegramUser.telegram_id == telegram_id)
        )
        user = user_result.scalar_one_or_none()

        request = ConsultationRequest(
            telegram_user_id=user.id if user else None,
            full_name=data.get("full_name"),
            age=data.get("age"),
            education_level=data.get("education_level"),
            interested_field=data.get("interested_field"),
            residence_country=data.get("residence_country"),
            phone_number=data.get("phone_number"),
            budget=data.get("budget"),
            language_certificate=data.get("language_certificate"),
            extra_description=data.get("extra_description"),
            status="new",
        )

        session.add(request)
        await session.commit()
        await session.refresh(request)

        return request
