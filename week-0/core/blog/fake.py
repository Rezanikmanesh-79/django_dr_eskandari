# save this as fake_data.py or run inside django shell
import random
from django.contrib.auth.models import User
from blog.models import Post, Ticket, Comment 
from faker import Faker
from django.utils import timezone

fake = Faker("fa_IR")  # برای داده‌های فارسی

# تعداد داده‌ها
NUM_POSTS = 15
NUM_TICKETS = 10
NUM_COMMENTS = 15

# اطمینان از اینکه حداقل یک کاربر وجود دارد
if not User.objects.exists():
    user = User.objects.create_user(username='reza', password='123456')
else:
    user = User.objects.first()

# ساخت پست‌های فیک
posts = []
for _ in range(NUM_POSTS):
    title = fake.sentence(nb_words=5)
    post = Post.objects.create(
        title=title,
        content=fake.paragraph(nb_sentences=5),
        slug=fake.unique.slug(),
        reading_time=random.randint(3, 15),
        publish=timezone.now(),
        author=user,
        status=random.choice([Post.Status.DRAFT, Post.Status.PUBLISHED, Post.Status.REJECTED])
    )
    posts.append(post)

# ساخت تیکت‌های فیک
for _ in range(NUM_TICKETS):
    Ticket.objects.create(
        message=fake.paragraph(nb_sentences=3),
        name=fake.name(),
        email=fake.email(),
        phone=fake.random_number(digits=11, fix_len=True),
        subject=fake.sentence(nb_words=4)
    )

# ساخت کامنت‌های فیک
for _ in range(NUM_COMMENTS):
    Comment.objects.create(
        post=random.choice(posts),
        name=fake.name(),
        email=fake.email(),
        content=fake.paragraph(nb_sentences=2),
        is_active=random.choice([True, False])
    )

print("Fake data created successfully!")
