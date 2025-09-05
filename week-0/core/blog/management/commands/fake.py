import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post, Ticket, Comment
from faker import Faker
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the database with fake data (posts, tickets, comments)'

    def handle(self, *args, **kwargs):
        fake = Faker("fa_IR")  # For Persian data

        NUM_POSTS = 15
        NUM_TICKETS = 10
        NUM_COMMENTS = 15

        # Ensure at least one user exists
        if not User.objects.exists():
            user = User.objects.create_user(username='reza', password='123456')
        else:
            user = User.objects.first()

        # Create fake posts
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

        # Create fake tickets
        for _ in range(NUM_TICKETS):
            Ticket.objects.create(
                message=fake.paragraph(nb_sentences=3),
                name=fake.name(),
                email=fake.email(),
                phone=fake.random_number(digits=11, fix_len=True),
                subject=fake.sentence(nb_words=4)
            )

        # Create fake comments
        for _ in range(NUM_COMMENTS):
            Comment.objects.create(
                post=random.choice(posts),
                name=fake.name(),
                email=fake.email(),
                content=fake.paragraph(nb_sentences=2),
                is_active=random.choice([True, False])
            )

        self.stdout.write(self.style.SUCCESS("Fake data created successfully!"))
