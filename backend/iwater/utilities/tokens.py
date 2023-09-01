from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.cache import cache

from random import randint

from init_water_app.settings import OTP_VALID_FOR


class VerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(user.is_active) + str(user.email)
        )


class SmsPinGenerator:
    """
    4-digit number verification code generator, used for sms verification
    """
    def __init__(self):
        self.valid_for = OTP_VALID_FOR  # seconds

    def make_pin(self, site):
        pin = "{:04d}".format(randint(0, 9999))
        # cache.set('pin({phone_number})'.format(phone_number=site.phone), pin, self.valid_for)
        return pin

    def make_6_pin(self, site):
        pin = "{:06d}".format(randint(0, 999999))
        # cache.set('pin({phone_number})'.format(phone_number=site.phone), pin, self.valid_for)
        return pin

    def consume_pin(self, site, pin):
        cached_pin = cache.get('pin({phone_number})'.format(phone_number=site.phone))
        pin_matches = pin is not None and pin == cached_pin
        if pin_matches:
            cache.delete('pin({phone_number})'.format(phone_number=site.phone))
        return pin_matches


account_verification_token = VerificationTokenGenerator()
