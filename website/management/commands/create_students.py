from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from website import models
from faker import Faker
import random
import string
from django.db import transaction


def _get_random_code():
    return ''.join(random.choice(string.digits) for _ in range(20))


class Command(BaseCommand):
    help = 'Creates students'

    @transaction.atomic
    def handle(self, *args, **options):
        user = None
        fake = Faker('pt_BR')

        years = models.Year.objects.all()
        # campi = models.Campus.objects.prefetch_related('courses').all()
        campi = models.Campus.objects.all()
        courses = models.Course.objects.all()
        students_per_course = 20

        users = []
        participants = []

        for campus in campi:
            # courses = campus.courses.all()
            for course in courses:
                for year in years:
                    for _ in range(students_per_course):
                        code = _get_random_code()
                        user = User(
                            username=code,
                            email=fake.email(),
                        )
                        participant = models.Participant(
                            id=code,
                            user=user,
                            name=fake.name(),
                            valid=True,
                            year=year,
                            course=course,
                            campus=campus,
                        )
                        users.append(user)
                        participants.append(participant)

        User.objects.bulk_create(users)
        models.Participant.objects.bulk_create(participants)
