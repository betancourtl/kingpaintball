from django.test import TestCase
from django.utils import timezone
from user.models import (
    VerificationToken,
    verification_token_expiration_datetime
)


class TestVerificationTokenModel(TestCase):

    def test_verification_token(self):
        time_zone = timezone.now()

        vt = VerificationToken.objects.create(
            token='vt',
            expires=verification_token_expiration_datetime(time_zone),
            identifier='identifier'
        )

        minutes = ((vt.expires - time_zone)).total_seconds() / 60
        self.assertEqual(minutes, 15)
        self.assertEqual(vt.token, 'vt')
        self.assertEqual(vt.identifier, 'identifier')
