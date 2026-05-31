from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import TelegramUser, City, University, ConsultationRequest


@admin.register(TelegramUser)
class TelegramUserAdmin(ModelAdmin):
    list_display = (
        "id",
        "telegram_id",
        "full_name",
        "username",
        "is_premium",
        "is_admin",
        "is_blocked",
        "created_at",
    )

    list_filter = (
        "is_premium",
        "is_admin",
        "is_blocked",
    )

    search_fields = (
        "telegram_id",
        "full_name",
        "username",
    )

    list_editable = (
        "is_premium",
        "is_blocked",
    )

    readonly_fields = (
        "telegram_id",
        "full_name",
        "username",
        "language_code",
        "created_at",
        "updated_at",
    )


class UniversityInline(TabularInline):
    model = University
    extra = 0

    fields = (
        "name_fa",
        "name_en",
        "slug",
        "is_active",
        "is_premium",
    )


@admin.register(City)
class CityAdmin(ModelAdmin):
    list_display = (
        "id",
        "name_fa",
        "name_en",
        "slug",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name_fa",
        "name_en",
        "slug",
    )

    prepopulated_fields = {
        "slug": ("name_en",)
    }

    inlines = [UniversityInline]


@admin.register(University)
class UniversityAdmin(ModelAdmin):
    list_display = (
        "id",
        "name_fa",
        "name_en",
        "city",
        "is_active",
        "is_premium",
        "created_at",
    )

    list_filter = (
        "city",
        "is_active",
        "is_premium",
    )

    search_fields = (
        "name_fa",
        "name_en",
        "slug",
        "description",
    )

    prepopulated_fields = {
        "slug": ("name_en",)
    }


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "phone_number",
        "interested_field",
        "residence_country",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "interested_field",
        "residence_country",
        "created_at",
    )

    search_fields = (
        "full_name",
        "phone_number",
        "interested_field",
        "education_level",
    )

    readonly_fields = (
        "telegram_user",
        "full_name",
        "age",
        "education_level",
        "interested_field",
        "residence_country",
        "phone_number",
        "budget",
        "language_certificate",
        "extra_description",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "اطلاعات کاربر",
            {
                "fields": (
                    "telegram_user",
                    "full_name",
                    "age",
                    "education_level",
                    "interested_field",
                    "residence_country",
                    "phone_number",
                )
            },
        ),
        (
            "اطلاعات پرونده",
            {
                "fields": (
                    "budget",
                    "language_certificate",
                    "extra_description",
                )
            },
        ),
        (
            "مدیریت ادمین",
            {
                "fields": (
                    "status",
                    "admin_note",
                )
            },
        ),
        (
            "زمان ثبت",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
