from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from init_water_app.settings import BRAND_NAME, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_DEFAULT_SENDER, \
    OTP_VALID_FOR


class SmsMessage:
    template = {
        'verification': 'Your verification code for adding site in {} account:'
                        ' {{code}}. It expires in {} seconds'.format(BRAND_NAME, OTP_VALID_FOR)
    }

    # template2 = {
    #     "verification": "Your verification code for adding site in {} account:"
    #                     "{token:{{otp_token}},otp:{{code}} } . It expires in {} seconds".format(BRAND_NAME, OTP_VALID_FOR)
    # }

    def __init__(self, message=None):
        self._account_sid = TWILIO_ACCOUNT_SID
        self._auth_token = TWILIO_AUTH_TOKEN
        self.message = message

    def send(self, to_number, from_number=None):
        if from_number is None:
            from_number = TWILIO_DEFAULT_SENDER
        try:
            client = Client(self._account_sid, self._auth_token)
            client.api.account.messages.create(to=to_number, from_=from_number, body=self.message or 'Please ignore this message.')
        except TwilioRestException as e:
            print(e)
            pass
