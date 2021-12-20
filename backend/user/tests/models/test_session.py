from django.test import TestCase
from user.models import (
    User,
    Session,
    session_expiration_datetime
)
from django.utils import timezone


class TestSessionModel(TestCase):

    def test_session(self):
        user = User.objects.create_user(
            'webdeveloperpr@gmail.com',
            'password',
        )

        self.assertEqual(User.objects.count(), 1)

        time_zone = timezone.now()

        session = Session.objects.create(
            session_token='session_token',
            expires=session_expiration_datetime(time_zone),
            userId=user
        )

        minutes = ((session.expires - time_zone)).total_seconds() / 60
        self.assertEqual(minutes, 15)
        self.assertEqual(session.session_token, 'session_token')
        self.assertEqual(session.userId, user)
