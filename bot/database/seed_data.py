import asyncio

from sqlalchemy import select

from bot.database.models import City, University
from bot.database.session import AsyncSessionLocal


INITIAL_DATA = [
    {
        "name_en": "Bucharest",
        "name_fa": "بخارست",
        "slug": "bucharest",
        "short_description": "پایتخت رومانی و یکی از مهم‌ترین شهرهای دانشجویی این کشور.",
        "full_description": """
بخارست پایتخت رومانی و بزرگ‌ترین شهر این کشور است. این شهر برای دانشجویان خارجی، مخصوصاً دانشجویان رشته‌های پزشکی، دندانپزشکی، داروسازی، اقتصاد، مدیریت و IT یکی از گزینه‌های مهم محسوب می‌شود.

مزایای بخارست:
✅ دانشگاه‌های معتبر
✅ امکانات شهری کامل
✅ فرصت‌های کاری بیشتر
✅ دسترسی بهتر به سفارت‌ها، شرکت‌ها و مراکز اداری
✅ جامعه بین‌المللی بزرگ‌تر
""",
        "cost_of_living": "هزینه زندگی در بخارست نسبت به بسیاری از پایتخت‌های اروپایی مناسب‌تر است، اما نسبت به شهرهای کوچک‌تر رومانی کمی بالاتر است.",
        "student_life": "بخارست فضای دانشجویی فعال، مراکز خرید، کافه‌ها، خوابگاه‌ها و امکانات شهری متنوعی دارد.",
        "universities": [
            {
                "name_en": "Carol Davila University of Medicine and Pharmacy",
                "name_fa": "دانشگاه پزشکی و داروسازی کارول داویلا",
                "slug": "carol-davila",
                "description": """
دانشگاه Carol Davila یکی از معروف‌ترین دانشگاه‌های پزشکی رومانی است و در شهر بخارست قرار دارد. این دانشگاه برای رشته‌های پزشکی، دندانپزشکی و داروسازی میان دانشجویان خارجی شناخته‌شده است.
""",
                "website": "https://umfcd.ro",
                "admission_requirements": "مدارک تحصیلی، ریزنمرات، پاسپورت، عکس، فرم درخواست و سایر مدارک بسته به رشته و سال پذیرش.",
                "tuition_fee": "شهریه دقیق باید هر سال از سایت دانشگاه بررسی شود. معمولاً رشته‌های پزشکی شهریه بالاتری نسبت به رشته‌های غیرپزشکی دارند.",
                "is_premium": False,
            },
            {
                "name_en": "University of Bucharest",
                "name_fa": "دانشگاه بخارست",
                "slug": "university-of-bucharest",
                "description": "یکی از دانشگاه‌های مهم رومانی با رشته‌های متنوع در علوم انسانی، علوم اجتماعی، زبان، حقوق، مدیریت و رشته‌های دیگر.",
                "website": "https://unibuc.ro",
                "admission_requirements": "بسته به رشته متفاوت است.",
                "tuition_fee": "شهریه بسته به رشته متفاوت است.",
                "is_premium": False,
            },
        ],
    },
    {
        "name_en": "Cluj-Napoca",
        "name_fa": "کلوژ ناپوکا",
        "slug": "cluj-napoca",
        "short_description": "یکی از معروف‌ترین شهرهای دانشجویی رومانی.",
        "full_description": """
کلوژ ناپوکا یکی از شهرهای مهم دانشگاهی رومانی است. این شهر فضای دانشجویی قوی، کیفیت زندگی مناسب و دانشگاه‌های معتبر دارد.

مزایا:
✅ شهر دانشجویی شناخته‌شده
✅ مناسب برای پزشکی و رشته‌های IT
✅ کیفیت زندگی خوب
✅ محیط آرام‌تر نسبت به بخارست
""",
        "cost_of_living": "هزینه زندگی در کلوژ معمولاً از شهرهای کوچک‌تر بیشتر است، اما کیفیت زندگی بالایی دارد.",
        "student_life": "کلوژ یکی از فعال‌ترین شهرهای دانشجویی رومانی است.",
        "universities": [
            {
                "name_en": "Iuliu Hațieganu University of Medicine and Pharmacy",
                "name_fa": "دانشگاه پزشکی و داروسازی یولیو هاتسیگانو",
                "slug": "iuliu-hatieganu",
                "description": "یکی از دانشگاه‌های شناخته‌شده پزشکی رومانی در شهر کلوژ.",
                "website": "https://umfcluj.ro",
                "admission_requirements": "مدارک تحصیلی، ریزنمرات، پاسپورت و مدارک مورد نیاز دانشگاه.",
                "tuition_fee": "شهریه باید بر اساس سال پذیرش از سایت رسمی بررسی شود.",
                "is_premium": False,
            },
            {
                "name_en": "Babeș-Bolyai University",
                "name_fa": "دانشگاه بابش بولیای",
                "slug": "babes-bolyai",
                "description": "یکی از بزرگ‌ترین و معتبرترین دانشگاه‌های رومانی با رشته‌های متنوع.",
                "website": "https://ubbcluj.ro",
                "admission_requirements": "بسته به رشته متفاوت است.",
                "tuition_fee": "شهریه بسته به رشته متفاوت است.",
                "is_premium": False,
            },
        ],
    },
    {
        "name_en": "Timișoara",
        "name_fa": "تیمیشوارا",
        "slug": "timisoara",
        "short_description": "شهر مهم غرب رومانی و یکی از گزینه‌های محبوب دانشجویان خارجی.",
        "full_description": """
تیمیشوارا در غرب رومانی قرار دارد و یکی از شهرهای مهم دانشگاهی و اقتصادی کشور است. این شهر برای دانشجویان پزشکی، فنی و رشته‌های مختلف گزینه مناسبی است.

مزایا:
✅ موقعیت خوب در غرب رومانی
✅ فضای اروپایی و آرام
✅ دانشگاه‌های معتبر
✅ مناسب برای زندگی دانشجویی
""",
        "cost_of_living": "هزینه زندگی در تیمیشوارا معمولاً مناسب‌تر از بخارست و کلوژ است.",
        "student_life": "تیمیشوارا فضای دانشجویی خوب و محیطی آرام‌تر دارد.",
        "universities": [
            {
                "name_en": "Victor Babeș University of Medicine and Pharmacy",
                "name_fa": "دانشگاه پزشکی و داروسازی ویکتور بابش",
                "slug": "victor-babes-timisoara",
                "description": "یکی از دانشگاه‌های پزشکی معروف رومانی در شهر تیمیشوارا.",
                "website": "https://umft.ro",
                "admission_requirements": "مدارک تحصیلی، ریزنمرات، پاسپورت و مدارک تکمیلی.",
                "tuition_fee": "شهریه بسته به رشته و سال پذیرش متفاوت است.",
                "is_premium": False,
            },
            {
                "name_en": "West University of Timișoara",
                "name_fa": "دانشگاه غرب تیمیشوارا",
                "slug": "west-university-timisoara",
                "description": "دانشگاهی با رشته‌های متنوع در علوم انسانی، اقتصاد، هنر، IT و رشته‌های دیگر.",
                "website": "https://uvt.ro",
                "admission_requirements": "بسته به رشته متفاوت است.",
                "tuition_fee": "شهریه بسته به رشته متفاوت است.",
                "is_premium": False,
            },
        ],
    },
    {
        "name_en": "Iași",
        "name_fa": "یاش",
        "slug": "iasi",
        "short_description": "یکی از شهرهای قدیمی، فرهنگی و دانشگاهی رومانی.",
        "full_description": """
یاش یکی از شهرهای قدیمی و مهم دانشگاهی رومانی است. این شهر فضای علمی و فرهنگی قوی دارد و برای دانشجویان خارجی مخصوصاً در رشته‌های پزشکی شناخته‌شده است.

مزایا:
✅ شهر دانشگاهی قدیمی
✅ هزینه زندگی مناسب‌تر
✅ فضای فرهنگی و دانشجویی
✅ دانشگاه‌های معتبر
""",
        "cost_of_living": "هزینه زندگی در یاش معمولاً مناسب‌تر از بخارست و کلوژ است.",
        "student_life": "یاش فضای دانشجویی خوبی دارد و برای زندگی دانشجویی گزینه مناسبی است.",
        "universities": [
            {
                "name_en": "Grigore T. Popa University of Medicine and Pharmacy",
                "name_fa": "دانشگاه پزشکی و داروسازی گریگوره تی پوپا",
                "slug": "grigore-t-popa",
                "description": "یکی از دانشگاه‌های شناخته‌شده پزشکی رومانی در شهر یاش.",
                "website": "https://umfiasi.ro",
                "admission_requirements": "مدارک تحصیلی، ریزنمرات، پاسپورت و مدارک تکمیلی.",
                "tuition_fee": "شهریه بسته به رشته و سال پذیرش متفاوت است.",
                "is_premium": False,
            },
            {
                "name_en": "Alexandru Ioan Cuza University",
                "name_fa": "دانشگاه الکساندرو ایوان کوزا",
                "slug": "alexandru-ioan-cuza",
                "description": "یکی از قدیمی‌ترین دانشگاه‌های رومانی با رشته‌های متنوع.",
                "website": "https://uaic.ro",
                "admission_requirements": "بسته به رشته متفاوت است.",
                "tuition_fee": "شهریه بسته به رشته متفاوت است.",
                "is_premium": False,
            },
        ],
    },
]


async def seed_data():
    async with AsyncSessionLocal() as session:
        for city_data in INITIAL_DATA:
            existing_city_result = await session.execute(
                select(City).where(City.slug == city_data["slug"])
            )
            existing_city = existing_city_result.scalar_one_or_none()

            if existing_city:
                print(f"City already exists: {city_data['name_en']}")
                continue

            universities_data = city_data.pop("universities")

            city = City(**city_data)
            session.add(city)
            await session.flush()

            for university_data in universities_data:
                university = University(
                    city_id=city.id,
                    **university_data
                )
                session.add(university)

            print(f"Added city and universities: {city.name_en}")

        await session.commit()

    print("Initial data inserted successfully.")


if __name__ == "__main__":
    asyncio.run(seed_data())
