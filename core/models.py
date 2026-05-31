from django.db import models


class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True, db_index=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    language_code = models.CharField(max_length=20, null=True, blank=True)

    is_premium = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "telegram_users"
        verbose_name = "کاربر تلگرام"
        verbose_name_plural = "کاربران تلگرام"

    def __str__(self):
        return self.full_name or self.username or str(self.telegram_id)


class City(models.Model):
    name_en = models.CharField(max_length=255)
    name_fa = models.CharField(max_length=255, null=True, blank=True)
    slug = models.CharField(max_length=255, unique=True, db_index=True)

    short_description = models.TextField(null=True, blank=True)
    full_description = models.TextField(null=True, blank=True)
    cost_of_living = models.TextField(null=True, blank=True)
    student_life = models.TextField(null=True, blank=True)
    image_path = models.CharField(max_length=500, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "cities"
        verbose_name = "شهر"
        verbose_name_plural = "شهرها"

    def __str__(self):
        if self.name_fa:
            return f"{self.name_fa} / {self.name_en}"
        return self.name_en


class University(models.Model):
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="django_universities"
    )

    name_en = models.CharField(max_length=255)
    name_fa = models.CharField(max_length=255, null=True, blank=True)
    slug = models.CharField(max_length=255, unique=True, db_index=True)

    description = models.TextField(null=True, blank=True)
    website = models.CharField(max_length=500, null=True, blank=True)
    admission_requirements = models.TextField(null=True, blank=True)
    tuition_fee = models.TextField(null=True, blank=True)
    image_path = models.CharField(max_length=500, null=True, blank=True)

    is_premium = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "universities"
        verbose_name = "دانشگاه"
        verbose_name_plural = "دانشگاه‌ها"

    def __str__(self):
        if self.name_fa:
            return f"{self.name_fa} / {self.name_en}"
        return self.name_en

class ConsultationRequest(models.Model):
    telegram_user = models.ForeignKey(
        TelegramUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="consultation_requests"
    )

    full_name = models.CharField(max_length=255, null=True, blank=True)
    age = models.CharField(max_length=50, null=True, blank=True)
    education_level = models.CharField(max_length=255, null=True, blank=True)
    interested_field = models.CharField(max_length=255, null=True, blank=True)
    residence_country = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    budget = models.CharField(max_length=255, null=True, blank=True)
    language_certificate = models.CharField(max_length=255, null=True, blank=True)
    extra_description = models.TextField(null=True, blank=True)

    status = models.CharField(max_length=50, default="new")
    admin_note = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "consultation_requests"
        verbose_name = "درخواست مشاوره"
        verbose_name_plural = "درخواست‌های مشاوره"

    def __str__(self):
        return f"{self.full_name or 'بدون نام'} - {self.phone_number or 'بدون شماره'}"
