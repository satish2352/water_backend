# Create your models here.

import os

from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import plivo

from init_water_app.settings import BRAND_NAME, SUPPORT_EMAIL, SUPPORT_PHONE, OTP_VALID_FOR, AUTH_LINK_VALID_FOR
from .utilities.tokens import account_verification_token, SmsPinGenerator
from .utilities.sms.message import SmsMessage

# auth_id = "MAZJK4ZTC4ZWM3Y2U0ZW"  # TODO tony's
# auth_token = "MjE5ZGRlNTY1Mzc4MzFkOGQ0MDkzOTE2MTUwYjll"
# auth_id = "MAZWZKNZMXZJCYODI3OT"  # TODO daliya's           #metric tree commented by bhart
# auth_token = "MGJhZWQ4MTdlZTBmN2IwMDQ0MzQzZDc1MmU1ZmJj"     #metric tree commented by bharti

auth_id = "MAMDAWZWNMOTJKNJCZNJ"  # Ini id updated by Sourabh ref: mail from Bharati ma'am
# auth_token = "YTAxZDM4ZDBlNzFkNmM3NDAzZjUwOWExMTNmOWIz" # Ini id updated by Sourabh ref: mail from Bharati ma'am
auth_token = "NDIyNDk5NDJjMDNiYjkxY2E0MmQ0ZTJmZjlmMTgw" # Ini id updated by Sourabh ref: mail from Bharati ma'am

#auth_id = "MAMDAWZWNMOTJKNJCZNJ"                           #initiative added by bharti
#auth_token = "MDM3OGQ3OTFiNDQ5MmM2ZTYyNjU0MjU1MjMyNzk0"    #initiative added by bharti

class Company(models.Model):
    company_name = models.CharField(blank=True, max_length=50, verbose_name='company_name')
    gst_no = models.CharField(blank=True, max_length=20, verbose_name='gstno')
    address1 = models.CharField(blank=True, max_length=200, verbose_name='address1')
    address2 = models.CharField(blank=True, max_length=200, verbose_name='address2')
    city = models.CharField(blank=True, max_length=200, verbose_name='city')
    state = models.CharField(blank=True, max_length=200, verbose_name='state')
    pincode = models.CharField(blank=True, max_length=6, verbose_name='pincode')

    def __str__(self):
        return self.company_name

    class Meta:
        unique_together = ('company_name', 'pincode', 'gst_no')


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.username = username
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            email=email,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser, PermissionsMixin):

    first_name = None
    last_name = None
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # phone = models.CharField(unique=True, blank=True, max_length=15, verbose_name='phone',null=True)
    # email = models.EmailField(unique=True, verbose_name='email')
    phone = models.CharField(unique=True, blank=True, null=True, max_length=15, verbose_name='phone')
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name='email')
    email_verified = models.BooleanField(default=0, verbose_name='email_verified')
    avatar = models.ImageField(upload_to="media/", null=True)
    # avatar = models.ImageField(upload_to="images/", null=True)
    site_limit = models.SmallIntegerField(default=0)
    date_joined = models.DateField(auto_now_add=True)

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_id',  null=True,
                                verbose_name='company_id')

    is_super_admin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_supervisor = models.BooleanField('Is supervisor', default=False)
    is_operator = models.BooleanField('Is operator', default=False)
    is_active = models.BooleanField(default=True)
   

    # added by Sourabh to enable block unblock
    is_blocked = models.BooleanField(default=False)
    # change ends here



    token = models.CharField(max_length=255, null=True, blank=True)
    token_created = models.DateTimeField(auto_now_add=True, null=True)
    invite_link_expired = models.BooleanField(default=False)

    added_by = models.ForeignKey('self', null=True, on_delete=models.CASCADE)

    invite_rejected = models.BooleanField(default=0, verbose_name='invite_rejected')
    phone_verified = models.BooleanField(default=0, verbose_name='phone_verified')
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created = models.DateTimeField(auto_now_add=True, null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def is_link_expired(self,):

        token_cache_time = self.token_created.replace(tzinfo=None)
        current_time = datetime.today().replace(tzinfo=None)
        difference = (current_time - token_cache_time).total_seconds()
        # print(difference)
        if difference > AUTH_LINK_VALID_FOR:
            return True

        return False

    def verify_email(self, token):

        # token_cache_time = self.token_created.replace(tzinfo=None)
        # current_time = datetime.today().replace(tzinfo=None)
        # difference = (current_time - token_cache_time).total_seconds()
        # print(difference)
        # if difference > OTP_VALID_FOR:
        #     return False

        if account_verification_token.check_token(self, token):
            # self.email_verified = True
            # self.save()
            return True
        return False

    def set_password_email(self, site_domain, brand_name, support_email, support_phone):
        print(site_domain)
        print('sending email')
        token = account_verification_token.make_token(self)
        mail_subject = "Set Password for Initiative Water Account"
        text_content = render_to_string('set-password.txt', {
            'user': self,
            # 'domain': "{}/invitation/".format(site_domain),  
            'domain': "{}/change_pass/".format(site_domain), 
            'uid': urlsafe_base64_encode(force_bytes(self.pk)),
            'token': token,
            'brand_name': brand_name,
            'support_email': support_email,
            'support_phone': support_phone,
        })
        self.token = token
        self.token_created = datetime.today()
        self.save()


        email = EmailMultiAlternatives(
            mail_subject, text_content, to=[self.email]
        )
        # print(text_content)
        email.mixed_subtype = 'related'
        email.send()

    # def send_verification_email(self, site_domain, brand_name, support_email, support_phone, inviter=None):
    #     token = account_verification_token.make_token(self)
    #     mail_subject = "Invite for Initiative Water Account"
    #     mail_content = render_to_string('set-password.txt', {
    #         'user': self,
    #         # 'domain': "{}/invitation/".format(site_domain),  # TODO site_domain,
    #         'domain': "{}/changepassword/".format(site_domain),  # TODO site_domain,
    #         'uid': urlsafe_base64_encode(force_bytes(self.pk)),
    #         'token': token,
    #         'brand_name': brand_name,
    #         'support_email': support_email,
    #         'support_phone': support_phone,
    #         'invite_message': "You are invited by {} as a user in {} company.".format(inviter, brand_name) if inviter else ""
    #     })
    #
    #     email = EmailMultiAlternatives(
    #         mail_subject, mail_content, to=[self.email]
    #     )
    #     # print(text_content)
    #     email.mixed_subtype = 'related'
    #     email.send()
    #
    #     text_content = render_to_string('account-verification.txt', {
    #         'user': self,
    #         'domain': "{}/invitation/".format(site_domain),  # TODO site_domain,
    #         # 'domain': "{}/changepassword/".format(site_domain),  # TODO site_domain,
    #         'uid': urlsafe_base64_encode(force_bytes(self.pk)),
    #         'token': token,
    #         'brand_name': brand_name,
    #         'support_email': support_email,
    #         'support_phone': support_phone,
    #         'invite_message': "You are invited by {} as a user in {} company.".format(inviter, brand_name) if inviter else ""
    #     })
    #     self.token = token
    #     self.token_created = datetime.today()
    #     self.save()
    #
    #     if not self.phone:
    #         return False
    #
    #     # TODO comment for trial testings
    #     auth_id = "MAZJK4ZTC4ZWM3Y2U0ZW"
    #     auth_token = "MjE5ZGRlNTY1Mzc4MzFkOGQ0MDkzOTE2MTUwYjll"
    #
    #    import plivo
    #
    #     client = plivo.RestClient(auth_id, auth_token)
    #     message_created = client.messages.create(
    #         src="+919645578992",
    #         dst=self.phone,
    #         text=text_content)
    #
    #     return True
    def send_set_password_email(self, site_domain, brand_name, support_email, support_phone, inviter=None):
        print(site_domain)
        print('reached here')
        token = account_verification_token.make_token(self)
        mail_subject = "Invite for Initiative Water Account"
        mail_content = render_to_string('set-password.txt', {
            'user': self,
            # 'domain': "{}/invitation/".format(site_domain),  
            #'domain': "{}/changepassword/".format(site_domain),     #commented by bharti
            'domain': "{}/change_pass/".format(site_domain.strip()),     #added by bharti 
            'uid': urlsafe_base64_encode(force_bytes(self.pk)),
            'token': token,
            'brand_name': brand_name,
            'support_email': support_email,
            'support_phone': support_phone,
            'invite_message': "You are invited by {} as a user in {} company.".format(inviter, brand_name) if inviter else ""
        })

        email = EmailMultiAlternatives(
            mail_subject, mail_content, to=[self.email]
        )
        # print(text_content)
        email.mixed_subtype = 'related'
        email.send()

    def send_invite_sms(self, site_domain, brand_name, support_email, support_phone, inviter=None):
        token = account_verification_token.make_token(self)

        text_content = render_to_string('account-verification.txt', {
            'user': self,
            # 'domain': "{}/invitation/".format(site_domain),  # TODO site_domain, old code
            'domain': "{}/invitation/".format(os.environ.get("SITE_DOMAIN")),  # TODO site_domain,
            # 'domain': "{}/changepassword/".format(site_domain),  # TODO site_domain,
            'uid': urlsafe_base64_encode(force_bytes(self.pk)),
            'token': token,
            'brand_name': brand_name,
            'support_email': support_email,
            'support_phone': support_phone,
            'invite_message': "You are invited by {} as a user in {} company.".format(inviter, brand_name) if inviter else ""
        })

        # Hi {#var#} ,\r\n\r\nWelcome to {#var#} !\r\n\r\nYour action is required\r\n\r\n{#var#}\r\nPlease navigate to the link below to accept or reject the invite.\r\n\r\nhttps://{#var#} {#var#} /{#var#} /\r\n\r\nIf you have issues with your account, please contact our Support Team at {#var#} or {#var#}.\r\n\r\nRegards,\r\n{#var#} Team\r\n


        self.token = token
        self.token_created = datetime.today()
        self.save()

        if not self.phone:
            return False

        # TODO comment for trial testings


        # client = plivo.RestClient("MAMDAWZWNMOTJKNJCZNJ", "MDM3OGQ3OTFiNDQ5MmM2ZTYyNjU0MjU1MjMyNzk0")
        client = plivo.RestClient("MAMDAWZWNMOTJKNJCZNJ", "ODBkZmM2OWU0NGM1ZjBmY2ExZDMyODFjZTY5N2Q5")
        message_created = client.messages.create(
            #src="+919645578992",                #9645578992 changed to 9607007015 by bharti
            src="+919607007015",                #Number updated by Sourabh ref: call with Bharati Ma'am
            dst=self.phone,
            text=text_content)
        
       

        return True

    def verify_phone(self, code):

        otp_cache_time = self.otp_created.replace(tzinfo=None)
        current_time = datetime.today().replace(tzinfo=None)
        difference = (current_time - otp_cache_time).total_seconds()
        # print(difference)

        if not self.phone:
            # print("no phone")
            return {"status": False}
        if self.phone_verified:
            # print(self.phone_verified)
            # print("phone_verified")
            return {"status": False, "difference": difference}

        # otp_cache_time = self.otp_created.replace(tzinfo=None)
        # current_time = datetime.today().replace(tzinfo=None)
        # difference = (current_time - otp_cache_time).total_seconds()
        # print(difference)
        if difference > OTP_VALID_FOR:
            return {"status": False, "difference": difference}

        pin = code
        cached_pin = self.otp
        pin_matches = pin is not None and pin == cached_pin
        if pin_matches:
            self.otp = None
            self.phone_verified = True
            self.save()
            return {"status": True, "difference": difference}
            # cache.delete('pin({phone_number})'.format(phone_number=site.phone))
        # return pin_matches
        # if SmsPinGenerator().consume_pin(self, code):
        #     self.phone_verified = True
        #     self.save()
        #     return True

        # if self.phone_verified:
        #     return False
        return {"status": False, "difference": difference}

    def send_verification_sms(self, ):
        if self.phone_verified:
            return {"status": False}

        # Generate verification code
        code = SmsPinGenerator().make_6_pin(self)
        self.otp = code
        self.otp_created = datetime.today()
        self.save()

        # TODO comment for trial testings
        # auth_id = "MAZJK4ZTC4ZWM3Y2U0ZW"
        # auth_token = "MjE5ZGRlNTY1Mzc4MzFkOGQ0MDkzOTE2MTUwYjll"
        #
        # import plivo

        BRAND_NAME = "Initiative Water"
        client = plivo.RestClient(auth_id, auth_token)
        message_created = client.messages.create(
            #src_old="+919645578992",                          #9645578992 changed to 9607007015 by bharti
            src="+919607007015",                #Number updated by Sourabh ref: call with Bharati Ma'am
            dst=self.phone,
            text="Your OTP for accepting user invitation in {} account is {}".format(BRAND_NAME, code)
        )

        return {"otp": code, "status": True}

    def verify_otp(self, code):

        otp_cache_time = self.otp_created.replace(tzinfo=None)
        current_time = datetime.today().replace(tzinfo=None)
        difference = (current_time - otp_cache_time).total_seconds()

        if not self.phone:
            return {"status": False}

        if difference > OTP_VALID_FOR:
            return {"status": False, "difference": difference}

        pin = code
        cached_pin = self.otp
        pin_matches = pin is not None and pin == cached_pin
        if pin_matches:
            self.otp = None
            self.phone_verified = True
            self.save()
            return {"status": True, "difference": difference}

        return {"status": False, "difference": difference}

    def send_login_sms(self, ):
        if self.phone_verified:
            # Generate verification code
            code = SmsPinGenerator().make_6_pin(self)
            self.otp = code
            self.otp_created = datetime.today()
            self.save()

            # TODO comment for trial testings
            # auth_id = "MAZJK4ZTC4ZWM3Y2U0ZW"
            # auth_token = "MjE5ZGRlNTY1Mzc4MzFkOGQ0MDkzOTE2MTUwYjll"
            #
            # import plivo

            BRAND_NAME = "Initiative Water"
            client = plivo.RestClient(auth_id, auth_token)
            message_created = client.messages.create(
               #src="+919645578992",     #commented by bharti
               src="+919607007015",                #Number updated by Sourabh ref: call with Bharati Ma'am
                dst=self.phone,
                text="Your OTP for logging in to {} account is {}".format(BRAND_NAME, code)
            )

            return {"otp": code, "status": True}
        return {"status": False}

    # def send_subaccount_creation_email(self, site_domain):
    #     mail_subject = 'Access Granted for {} CityConnect Account'.format(
    #         BRAND_NAME)
    #     text_content = render_to_string('subaccount-created.txt', {
    #         'user': self,
    #         'domain': site_domain,
    #         'brand_name': BRAND_NAME,
    #         'support_email': SUPPORT_EMAIL,
    #         'support_phone': SUPPORT_PHONE,
    #     })
    #     html_content = render_to_string('subaccount-created.html', {
    #         'user': self,
    #         'domain': site_domain,
    #         'brand_name': BRAND_NAME,
    #         'brand_website': BRAND_WEBSITE,
    #         'support_email': SUPPORT_EMAIL,
    #         'support_phone': SUPPORT_PHONE,
    #     })
    #     email = EmailMultiAlternatives(
    #         mail_subject, text_content, to=[self.email]
    #     )
    #     email.attach_alternative(html_content, "text/html")
    #     email.mixed_subtype = 'related'
    #     for f in [('logo', 'logo.png'), ('banner', 'banner.png')]:
    #         with open(os.path.join(STATICFILES_DIRS[0], 'images', f[1]), 'rb') as fp:
    #             img = MIMEImage(fp.read())
    #             img.add_header('Content-ID', '<{}>'.format(f[0]))
    #             email.attach(img)
    #     email.send()

    # TODO
    # def send_termination_email(self, site_domain):
    #     mail_subject = 'Your Access to {} CityConnect Service Has Been' \
    #                    ' Revoked'.format(BRAND_NAME)
    #     text_content = render_to_string('account-termination.txt', {
    #         'user': self,
    #         'domain': site_domain,
    #         'uid': urlsafe_base64_encode(force_bytes(self.pk)),
    #         'token': account_verification_token.make_token(self),
    #         'brand_name': BRAND_NAME,
    #         'support_email': SUPPORT_EMAIL,
    #         'support_phone': SUPPORT_PHONE,
    #     })
    #     html_content = render_to_string('account-termination.html', {
    #         'user': self,
    #         'domain': site_domain,
    #         'uid': urlsafe_base64_encode(force_bytes(self.pk)),
    #         'token': account_verification_token.make_token(self),
    #         'brand_name': BRAND_NAME,
    #         'brand_website': BRAND_WEBSITE,
    #         'support_email': SUPPORT_EMAIL,
    #         'support_phone': SUPPORT_PHONE,
    #     })
    #     email = EmailMultiAlternatives(
    #         mail_subject, text_content, to=[self.email]
    #     )
    #     email.attach_alternative(html_content, "text/html")
    #     email.mixed_subtype = 'related'
    #     for f in [('logo', 'logo.png'), ('banner', 'banner.png')]:
    #         with open(os.path.join(STATICFILES_DIRS[0], 'images', f[1]), 'rb') as fp:
    #             img = MIMEImage(fp.read())
    #             img.add_header('Content-ID', '<{}>'.format(f[0]))
    #             email.attach(img)
    #
    #     email.send()

    # def verify_phone(self, code):
    #     if not self.phone:
    #         return False
    #     if self.phone_verified:
    #         return True
    #     if SmsPinGenerator().consume_pin(self, code):
    #         self.phone_verified = True
    #         self.save()
    #         return True
    #     return False
    #
    # def send_verification_sms(self):
    #     if not self.phone or self.phone_verified:
    #         return False
    #
    #     # Generate verification code
    #     code = SmsPinGenerator().make_pin(self)
    #
    #     # Send sms to user
    #     text_message = SmsMessage.template['verification'].format(code=code)
    #     SmsMessage(message=text_message).send(to_number=self.phone)
    #     return True

# Added is_blocked = models.BooleanField(default=False) to add block unblock functionality

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_blocked = models.BooleanField(default=False)

# Created calss to generate blocks tables

class Site(models.Model):
    site_name = models.CharField(max_length=255)

    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    phone = models.CharField(max_length=60, null=True, blank=True)
    token = models.CharField(max_length=60, null=True, blank=True)
    phone_verified = models.BooleanField(default=0, verbose_name='phone_verified')
    token_verified = models.BooleanField(default=0, verbose_name='token_verified')

    status = models.BooleanField(default=True)
    alerts = models.SmallIntegerField(default=0)
    created = models.DateField(auto_now_add=True)

    is_treatment_unit = models.BooleanField('Is treatment', default=False)
    is_dispensing_unit = models.BooleanField('Is dispensing', default=False)

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='site_company', null=True,
                                verbose_name='site_company')
    
    otp = models.CharField(max_length=4, null=True, blank=True)
    otp_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.site_name

    class Meta:
        db_table = 'iwater_site'
        unique_together = ('site_name', 'company',)

    def verify_phone(self, code):

        otp_cache_time = self.otp_created.replace(tzinfo=None)
        current_time = datetime.today().replace(tzinfo=None)
        difference = (current_time - otp_cache_time).total_seconds()
        # print(difference)

        if not self.phone:
            # print("no phone")
            return {"status": False}
        # if self.phone_verified:  # TODO commented for re-auth
        #     # print(self.phone_verified)
        #     # print("phone_verified")
        #     return {"status": False, "difference": difference}

        # otp_cache_time = self.otp_created.replace(tzinfo=None)
        # current_time = datetime.today().replace(tzinfo=None)
        # difference = (current_time - otp_cache_time).total_seconds()
        # print(difference)
        if difference > OTP_VALID_FOR:
            return {"status": False, "difference": difference}

        pin = code
        cached_pin = self.otp
        pin_matches = pin is not None and pin == cached_pin
        if pin_matches:
            self.otp = None
            self.phone_verified = True
            self.save()
            return {"status": True, "difference": difference}
            # cache.delete('pin({phone_number})'.format(phone_number=site.phone))
        # return pin_matches
        # if SmsPinGenerator().consume_pin(self, code):
        #     self.phone_verified = True
        #     self.save()
        #     return True

        # if self.phone_verified:
        #     return False
        return {"status": False, "difference": difference}

    def send_verification_sms(self,token):
        # ! Sends message for device verification
        # if self.phone_verified:  # TODO commented for re-auth
        # # if not self.phone or self.phone_verified:
        #     return {"status": False}

        # Generate verification code
        code = SmsPinGenerator().make_pin(self)
        self.otp = code
        self.otp_created = datetime.today()
        self.token=token  #store token in site
        self.save()

        # Send sms to user
        # text_message2 = "Your verification code for adding site in {brand} account:{token:{{otp_token}},otp:{{code}} } " \
        #                 ". It expires in {valid_for} seconds".format(brand=BRAND_NAME, otp_token=token, code=code,
        #                                                                                             valid_for=OTP_VALID_FOR)

        # text_message = SmsMessage.template['verification'].format(code=code)
        # SmsMessage(message=text_message).send(to_number=self.phone)

        # TODO comment for trial testings
        # auth_id = "MAZJK4ZTC4ZWM3Y2U0ZW"
        # auth_token = "MjE5ZGRlNTY1Mzc4MzFkOGQ0MDkzOTE2MTUwYjll"
        #
        # import plivo

        client = plivo.RestClient(auth_id, auth_token)
        message_created = client.messages.create(
           # src="+919645578992",                       #9645578992 changed to 9607007015 by bharti
            src="+919607007015",                #Number updated by Sourabh ref: call with Bharati Ma'am
            dst=self.phone,
            # text=str({"token":'{0:04}'.format(token),"otp": code +",app:wc, The Secret OTP for initiative Device"}),
            text="Your verification code for adding site in account" + str({"token": '{0:04}'.format(token), "otp": code}) + " for your Initiative Product",
            # text="Your verification code for adding site in account"+str({"token": '{0:04}'.format(token),"otp": code})+" for your Initiative Product",
            # dlt_entity_id='1201159178492032504',
            # dlt_template_category='service_implicit',
            # dlt_template_id='1007493130372339254'  
            # Your verification code for adding site in account{'token': '{#var#}', 'otp': '{#var#}'} for your Initiative Product 
            # Your verification code for adding site in account{'token': '{#var#}', 'otp': '{#var#}'} for your Initiative Product 
        )

        # Your verification code for adding site in account{'token': '{#var#}', 'otp': '{#var#}'}

        return {"otp":code, "status":True}


class SiteCopy(models.Model):
    site_name = models.CharField(unique=True, max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    phone = models.CharField(max_length=60, null=True, blank=True)
    phone_verified = models.BooleanField(default=0, verbose_name='phone_verified')
    status = models.BooleanField(default=True)
    alerts = models.SmallIntegerField(default=0)
    created = models.DateField(auto_now_add=True)
    is_treatment_unit = models.BooleanField('Is treatment', default=False)
    is_dispensing_unit = models.BooleanField('Is dispensing', default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='sitecopy_company', null=True,
                                verbose_name='sitecopy_company')
    otp = models.CharField(max_length=4, null=True, blank=True)
    otp_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.site_name

    def verify_phone(self, code):
        if not self.phone:
            # print("no phone")
            return False
        if self.phone_verified:
            # print(self.phone_verified)
            # print("phone_verified")
            return False

        otp_cache_time = self.otp_created.replace(tzinfo=None)
        current_time = datetime.today().replace(tzinfo=None)
        difference = (current_time - otp_cache_time).total_seconds()
        # print(difference)
        if difference > OTP_VALID_FOR:
            return False

        pin = code
        cached_pin = self.otp
        pin_matches = pin is not None and pin == cached_pin
        if pin_matches:
            self.otp = None
            self.phone_verified = True
            self.save()
            return True
            # cache.delete('pin({phone_number})'.format(phone_number=site.phone))
        # return pin_matches
        # if SmsPinGenerator().consume_pin(self, code):
        #     self.phone_verified = True
        #     self.save()
        #     return True

        # if self.phone_verified:
        #     return False
        return False

    def send_verification_sms(self,):
        if self.phone_verified:
        # if not self.phone or self.phone_verified:
            return {"status": False}

        # Generate verification code
        code = SmsPinGenerator().make_pin(self)
        self.otp = code
        self.otp_created = datetime.today()
        self.save()

        # Send sms to user
        # text_message2 = "Your verification code for adding site in {brand} account:{token:{{otp_token}},otp:{{code}} } " \
        #                 ". It expires in {valid_for} seconds".format(brand=BRAND_NAME, otp_token=token, code=code,
        #                                                                                             valid_for=OTP_VALID_FOR)

        # text_message = SmsMessage.template['verification'].format(code=code)
        # SmsMessage(message=text_message).send(to_number=self.phone)

        # auth_id = "MAZJK4ZTC4ZWM3Y2U0ZW"
        # auth_token = "MjE5ZGRlNTY1Mzc4MzFkOGQ0MDkzOTE2MTUwYjll"
        #
        # import plivo

        client = plivo.RestClient(auth_id, auth_token)
        message_created = client.messages.create(
            #src="+919645578992",                        #9645578992 changed to 9607007015 by bharti
            src="+919607007015",                #Number updated by Sourabh ref: call with Bharati Ma'am
            dst=self.phone,
            text="Verification sms"
        )

        return {"otp": code, "status": True}


class SitePermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userid',  null=True, verbose_name='userid')
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='siteid',  null=True, verbose_name='siteid')
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'iwater_site_permissions'
        unique_together = ('user', 'site',)

# class siteandpermision(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
#     title= models.CharField(max_length=300, null=True)
#     SitePermission=models.ForeignKey(SitePermission, on_delete=models.CASCADE, null=True)
#     Site=models.ForeignKey(Site, on_delete=models.CASCADE, null=True)
#     # city=models.ForeignKey(city, on_delete=models.CASCADE, null=True)

#     def __str__(self):
#         return self.title
class Device(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE,  null=True)
    # site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='site',  null=True, verbose_name='site')
    device_name1 = models.CharField(max_length=255, null=True, unique=True)
    serial_no1 = models.CharField(max_length=255, null=True, unique=True)
    device_name2 = models.CharField(max_length=255, null=True, unique=True)
    serial_no2 = models.CharField(max_length=255, null=True, unique=True)
    device_name3 = models.CharField(max_length=255, null=True, unique=True) # ! iot module  
    serial_no3 = models.CharField(max_length=255, null=True, unique=True)   # ! iot module
    device1_sub_status = models.CharField(max_length=255, null=True)
    device2_sub_status = models.CharField(max_length=255, null=True)
    device3_sub_status = models.CharField(max_length=255, null=True)

    
    def __str__(self):
        return self.pk
  

class PaymentStatus:
    SUCCESS = "Success"
    FAILURE = "Failure"
    PENDING = "Pending"


# ! Razorpay order table
class Order(models.Model):

    # ! assigning user who paid
    paid_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paid_user',
                                        null=True, verbose_name='paid_user')

    # ! assigning company account                                         
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='paid_company', null=True,
                                verbose_name='paid_company')

                               
    paid_on = models.DateTimeField(auto_now_add=True, null=True)

    amount = models.FloatField(null=False, blank=False)

    # ! razorpay paymetn response status
    payment_status = models.CharField(verbose_name='payment_status', default=PaymentStatus.PENDING, max_length=254,
                                      blank=False, null=False)
    
    # ! razorpay paymetn id
    provider_order_id = models.CharField(verbose_name='provider_order_id', max_length=40, null=False, blank=False)
    

    payment_id = models.CharField(verbose_name='payment_id', max_length=36, null=False, blank=False)
    
    # ! razorpay signature
    signature_id = models.CharField(verbose_name='signature_id', max_length=128, null=False, blank=False)

    def __str__(self):
        # resp = ("{}-{}".format(self.subscription, self.payment_status))
        # print(resp)
        # f"{self.pk}-{self.subscription}-{self.payment_status}"
        return str(self.pk) + "--" + str(self.provider_order_id)


def get_deadline():
    return datetime.today() + timedelta(days=1)  # TODO should change to 30 days

# ! Site subscriptions table  
class Subscription(models.Model):

    # ! assigns site via foreign key
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='site_id',  null=True, verbose_name='site_id')

    is_treatment_unit = models.BooleanField('Is treatment', default=False)
    is_dispensing_unit = models.BooleanField('Is dispensing', default=False) # Make a seprate table for unit type
    
    created = models.DateField(auto_now_add=True)
    valid_till = models.DateField(default=get_deadline)
    days_to_expire = models.SmallIntegerField(default=1)  # TODO should change to 30 days
    expired = models.BooleanField(default=0, verbose_name='expired')
   
    no_of_sites = models.SmallIntegerField(default=0)
    
    assigned_sites = models.SmallIntegerField(default=0)
    unassigned_sites = models.SmallIntegerField(default=0)
    
    last_paid = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    total_paid = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    
    data_transfer_volume = models.BigIntegerField(default=0)
    
    no_of_actions = models.BigIntegerField(default=0)
    
    subscription_code = models.CharField(max_length=255, null=True)
    # ! this is subscription code

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='subscription_company', null=True,
                                verbose_name='subscription_company')
    
    # ! assigns order_id from orde table which is smae as provider_order_id
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_id',  null=True,
                              verbose_name='order_id')

    def __str__(self):
        return self.pk


class Price(models.Model): # ! change when pushed to production
    dispensing_price = models.CharField(max_length=255, default=1000)
    treatment_price = models.CharField(max_length=255, default=1200)
    dispensing_tax = models.CharField(max_length=255, default=5)
    treatment_tax = models.CharField(max_length=255, default=5)


class ArchiveSite(models.Model):
    site_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    phone = models.CharField(max_length=60, unique=True, null=True, blank=True)
    phone_verified = models.BooleanField(default=0, verbose_name='phone_verified')
    token_verified = models.BooleanField(default=0, verbose_name='token_verified')
    status = models.BooleanField(default=True)
    alerts = models.SmallIntegerField(default=0)
    created = models.DateField(auto_now_add=True)
    is_treatment_unit = models.BooleanField('Is treatment', default=False)
    is_dispensing_unit = models.BooleanField('Is dispensing', default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='archive_site_company', null=True,
                                verbose_name='site_company')
    otp = models.CharField(max_length=4, null=True, blank=True)
    otp_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.site_name

    class Meta:
        db_table = 'iwater_archive_site'
        unique_together = ('site_name', 'company',)


class ArchiveSitePermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='archive_site_user',  null=True, verbose_name='userid')
    site = models.ForeignKey(ArchiveSite, on_delete=models.CASCADE, related_name='archive_siteid',  null=True, verbose_name='siteid')
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'iwater_archive_site_permissions'
        unique_together = ('user', 'site',)


class ArchiveDevice(models.Model):
    site = models.OneToOneField(ArchiveSite, on_delete=models.CASCADE,  null=True)
    # site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='site',  null=True, verbose_name='site')
    device_name1 = models.CharField(max_length=255, null=True, unique=True)
    serial_no1 = models.CharField(max_length=255, null=True, unique=True)
    device_name2 = models.CharField(max_length=255, null=True, unique=True)
    serial_no2 = models.CharField(max_length=255, null=True, unique=True)
    device_name3 = models.CharField(max_length=255, null=True, unique=True)
    serial_no3 = models.CharField(max_length=255, null=True, unique=True)

    def __str__(self):
        return self.pk

    class Meta:
        db_table = 'iwater_archive_device'



'''
-- archive_device
-- archive_site
-- archive_site_permission
-- company
-- device
-- order
-- price
-- site
-- site_permission
-- sitecopy
-- subscription
-- user
user_groups
user_user_permissions
-- userProfile

xx paymentStatus

'''