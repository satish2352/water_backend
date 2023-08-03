import json
import re
from datetime import datetime, timedelta
import threading

# from random import randint
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http.response import JsonResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
# from rest_framework.parsers import JSONParser
from rest_framework import status
from django.db import transaction
from django.db.models import Q
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
# from django.middleware.csrf import get_token
from rest_framework.authtoken.models import Token
import paho.mqtt.client as mqtt


from .models import Site, User, SitePermission, Device, Subscription, Company, Price
from init_water_app import settings
from init_water_app.settings import OTP_VALID_FOR, LOG_FILE_LOCATION
# from .serializers import SiteSerializer, UserSerializer

from .iw_logger import logger
# from .mqtt_service import Client

# @api_view(['GET'])
# def get_free_or_expired_trial_sites(request, pk):
#     available_site_ids = []
#     logger.info("Got request to list free or expired sites before site delete")
#     if request.method == 'GET':
#         try:
#             requested_site = Site.objects.get(id=pk)
#         except ObjectDoesNotExist:
#             return JsonResponse({"Response": {
#                     "Status": "error"},
#                     'message': 'The site does not exist'
#                 }, status=status.HTTP_200_OK)
#
#         # find site to be deleted
#         site_type = ""
#         site_obj = Site.objects.get(id=pk)
#         response_data = {}
#
#         # find site type
#         if site_obj.is_treatment_unit:
#             site_type = "treatment unit"
#             subs_obj = Subscription.objects.filter(site_id=site_obj.id, is_treatment_unit=True)
#         else:  # user_info["is_dispensing_unit"]:
#             site_type = "dispensing unit"
#             subs_obj = Subscription.objects.filter(site_id=site_obj.id, is_dispensing_unit=True)
#
#         print("About to delete site is {}".format(site_type))
#
#         # if site has active license
#         #   if found get free or expired licenses's sites
#         #   else
#         #   do not allow site delete
#         # if site has no active license give empty response and allow direct delete
#
#         for sub_info in subs_obj.values():
#             print(sub_info)
#             # if the "to be deleted site" has a valid active subscription then return valid sites else simple delete
#             # so return empty site ids
#             if sub_info["subscription_code"] is not None and not sub_info["expired"]:
#                 print("to be deleted site has active license")
#                 if site_type is "treatment unit":
#                     new_free_or_expired_site = Subscription.objects.filter(Q(expired=True) |
#                                                                            Q(subscription_code__isnull=True),
#                                                                            is_treatment_unit=True,
#                                                                            company_id=request.user.company_id)
#                 else:
#                     new_free_or_expired_site = Subscription.objects.filter(Q(expired=True) |
#                                                                            Q(subscription_code__isnull=True),
#                                                                            is_dispensing_unit=True,
#                                                                            company_id=request.user.company_id)
#                 for new_site in new_free_or_expired_site.values():
#                     site_data = {
#                         'site_id': new_site["site_id"]
#                     }
#                     available_site_ids.append(site_data)
#
#                 # Do not allow site deletion if there is no other free or expired sites available to allocate the
#                 # subscription of a "to be deleted site" with valid subscription
#                 if not available_site_ids:
#                     return JsonResponse({"Response": {
#                         "Status": "error"},
#                         "message": "Not able to delete the requested site as there is no other site to allocate the "
#                                    "existing subscription"
#                     }, safe=False, status=status.HTTP_200_OK)
#
#             response_data.update({"available_sites": available_site_ids})
#
#         logger.debug("available_sites {}".format(available_site_ids))
#         return JsonResponse({"Response": {
#                 "Status": "success"},
#                 "Data": response_data
#             }, safe=False, status=status.HTTP_200_OK)
#
#
# @api_view(['POST'])
# def delete_site(request, pk):
#     logger.info("Delete site request came for site id {}".format(pk))
#     if request.method == 'POST':
#
#         to_be_added_site_id = request.data['site_id'] if request.data else None
#         logger.info("To be added site id {}".format(to_be_added_site_id))
#
#         try:
#             logger.debug("Checking whether to be deleted site exists")
#             site_data = Site.objects.get(id=pk)
#         except ObjectDoesNotExist:
#             return JsonResponse({"Response": {"Status": "error"}, "message": "The requested site does not exist"},
#                                 status=status.HTTP_200_OK)
#         logger.debug("To be deleted site exists")
#
#         try:
#
#             logger.debug("Checking whether the new site exists")
#             new_site = Site.objects.get(id=to_be_added_site_id)
#             if new_site:
#                 with transaction.atomic():
#                     try:
#                         logger.info("Trying to allocate the existing subscription to new site")
#
#                         if site_data.is_treatment_unit:
#                             subscriptions = Subscription.objects.filter(site_id=pk, is_treatment_unit=True)
#                         else:  # user_info["is_dispensing_unit"]:
#                             subscriptions = Subscription.objects.filter(site_id=pk, is_dispensing_unit=True)
#
#                         for sub in subscriptions.values():
#                             # delete new sites old (free or expired) subscriptions
#                             Subscription.objects.filter(site_id=to_be_added_site_id).delete()
#                             new_sub = Subscription.objects.get(id=sub["id"])
#                             new_sub.site_id = to_be_added_site_id
#                             new_sub.save()
#                             logger.info("Allocated the subscription {} to new site {}".format(sub["id"],
#                                                                                               to_be_added_site_id))
#
#                     except Exception as err:
#                         transaction.set_rollback(True)
#                         logger.error("Error in allocating site subscription to new site. {}".format(err))
#                         return JsonResponse({"Response": {"Status": "error"}, "message": "Error in allocating site "
#                                                                                          "subscription to new site"},
#                                             status=status.HTTP_200_OK)
#         except ObjectDoesNotExist:
#             logger.info("To be deleted site has no valid license, hence simply deleting the site")
#         except Exception as err:
#             logger.error("Error in allocating site subscription. {}".format(err))
#             return JsonResponse({"Response": {"Status": "error"}, "message": "Error in allocating site "
#                                                                              "subscription"},
#                                 status=status.HTTP_200_OK)
#         logger.debug("New site to be assigned exists")
#
#         try:
#             logger.debug("Trying to delete the site")
#             Site.objects.filter(pk=pk).delete()
#             logger.debug("Deleted the site")
#         except Exception as err:
#             logger.error("Error in deleting site {}.{}".format(pk, err))
#         logger.debug("Site deleted successfully")
#         return JsonResponse({"Response": {"Status": "success"}, "message": "Site deleted successfully"},
#                             status=status.HTTP_200_OK)

# Create your views here.
class MqttClient:

    def __init__(self, company_id):
        # _data_mqtt = settings.settings_get_mqttSettings()
        _topic = "IW/V1/OTP"
        # _username = _data_mqtt['_username']
        # _password = _data_mqtt['_password']
        _hostname = "broker.mqttdashboard.com"
        _port = 1883
        self.company_id = company_id

        # logger.info("MQTT - Credentials: username: {}, hostname: {}, port: {}".format(_username, _hostname, _port))
        self.client = mqtt.Client()
        self.topic = _topic
        # if _clientID != "":
        # self.client = mqtt.Client(client_id="")

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # connect to HiveMQ Cloud on port
        self.client.connect(_hostname, _port, OTP_VALID_FOR)

        self.client.loop_start()

    def on_message(self, client, userdata, message):

        data = json.loads(str(message.payload.decode('utf-8')))
        logger.info("MQTT data {}".format(data))
        site_id = data["token"]
        # site_id = str(data["token"]).lstrip("0")

        device_id = data["deviceid"]
        panelid = data["panelid"] if data["panelid"] else None
        atmid = data["atmid"] if data["atmid"] else None

        logger.info("site_id {}".format(site_id))
        logger.info("company_id {}".format(self.company_id))
        logger.info("device_id {}".format(device_id))
        logger.info("panelid {}".format(panelid))
        logger.info("atmid {}".format(atmid))

        with transaction.atomic():
            try:
                if panelid and atmid:
                    logger.info("Got both panel and atm id from device")

                    subscription_data = Device()
                    subscription_data.device_name1 = device_id
                    subscription_data.device_name2 = panelid
                    subscription_data.device_name3 = atmid
                    subscription_data.site_id = site_id
                    subscription_data.save()
                    logger.info("Added device serial numbers")

                    subscription_data = Site.objects.get(id=site_id)
                    subscription_data.is_treatment_unit = True
                    subscription_data.save()
                    logger.info("Updated site details for treatment unit")

                    subscription_data = Subscription()
                    subscription_data.site_id = site_id
                    subscription_data.is_treatment_unit = True
                    subscription_data.company_id = self.company_id
                    subscription_data.save()
                    logger.info("Added subscription details for treatment unit")

                    subscription_data = Site.objects.get(id=site_id)
                    subscription_data.is_dispensing_unit = True
                    subscription_data.save()
                    logger.info("Updated site details for dispensing unit")

                    # subscription_data = Subscription.objects.get(site_id=site_id)
                    # subscription_data.is_treatment_unit = True
                    # subscription_data.save()

                    subscription_data = Subscription()
                    subscription_data.site_id = site_id
                    subscription_data.is_dispensing_unit = True
                    subscription_data.company_id = self.company_id
                    subscription_data.save()
                    logger.info("Added subscription details for dispensing unit")

                elif panelid:
                    logger.info("Got only panel id from device")

                    subscription_data = Device()
                    subscription_data.device_name1 = device_id
                    subscription_data.device_name2 = panelid
                    subscription_data.device_name3 = atmid
                    subscription_data.site_id = site_id
                    subscription_data.save()
                    logger.info("Added device serial numbers")

                    subscription_data = Site.objects.get(id=site_id)
                    subscription_data.is_treatment_unit = True
                    subscription_data.save()
                    logger.info("Updated site details for treatment unit")

                    subscription_data = Subscription()
                    subscription_data.site_id = site_id
                    subscription_data.is_treatment_unit = True
                    subscription_data.company_id = self.company_id
                    subscription_data.save()
                    logger.info("Added subscription details for treatment unit")

                elif atmid:
                    logger.info("Got only atm id from device")

                    subscription_data = Device()
                    subscription_data.device_name1 = device_id
                    subscription_data.device_name2 = panelid
                    subscription_data.device_name3 = atmid
                    subscription_data.site_id = site_id
                    subscription_data.save()

                    subscription_data = Site.objects.get(id=site_id)
                    subscription_data.is_dispensing_unit = True
                    subscription_data.save()
                    logger.info("Updated site details for dispensing unit")

                    subscription_data = Subscription()
                    subscription_data.site_id = site_id
                    subscription_data.is_dispensing_unit = True
                    subscription_data.company_id = self.company_id
                    subscription_data.save()
                    logger.info("Added subscription details for dispensing unit")

            except Exception as err:
                transaction.set_rollback(True)
                logger.error("MQTT - {}".format(err))
        logger.info("Successfully added data to db over mqtt")

    def on_connect(self, client, userdata, flags, rc):
        logger.info("MQTT - connected")
        self.subscribe(self.topic)

    def subscribe(self, topic):
        self.client.subscribe(topic)
        logger.info("MQTT - Subscribed to topic '" + topic)

    def publish(self, topic, payload):
        logger.info("MQTT - Published message '" + str(payload) + "' on topic '" + topic)
        self.client.publish(topic, payload=payload)
        # self.client.loop_stop()

    def stop(self):
        logger.info("MQTT - Disconnecting from mqtt broker and cleaning up")
        self.client.disconnect()


# @login_required
@api_view(['GET'])
# @user_email_verified
def dashboard(request):
    data = []
    total_sites = 0
    free_sites = 0
    assigned_sites = 0
    unassigned_sites = 0

    if request.method == 'GET':

        subscription = Subscription.objects.all()
        for subs in subscription.values():
                logger.info("\nsubscription - {}".format(subs["id"]))

                total_sites += 1

                logger.info("subscription_code - {}".format(subs["subscription_code"]))
                valid_till = datetime.strptime(str(subs["valid_till"]), "%Y-%m-%d")
                present_date = datetime.now()
                logger.info("present_date - {}".format(present_date))
                logger.info("valid_till - {}".format(valid_till))

                if subs["subscription_code"] is None:
                    free_sites += 1
                elif valid_till.date() > present_date.date():  # TODO check if and subs["subscription_code"] is not None
                    # is needed
                    assigned_sites += 1
                elif valid_till.date() < present_date.date():  # TODO and subs["subscription_code"] is not None
                    unassigned_sites += 1

        resp = {
            'no_of_sites': total_sites,
            'free_sites': free_sites,
            'assigned_sites': assigned_sites,
            'unassigned_sites': unassigned_sites,
        }
        data.append(resp)

        return JsonResponse(
            {"Response": {
                "Status": "success"
            },
                "Data": data
            }, safe=False, status=status.HTTP_200_OK)

    return JsonResponse({"Response": {
        "Status": "error"},
        "message": "Invalid request"
    }, safe=False, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        email = request.data['email']
        password = request.data['password']

        user = authenticate(request, email=email, password=password)
        logger.info("Logged in user is {}".format(user))
        if user is not None:
            if user.is_active:
                login(request, user)
                loggeduser = User.objects.get(email=email)

                role = ""
                if loggeduser.is_super_admin:
                    role = "super_admin"
                elif loggeduser.is_admin:
                    role = "admin"
                elif loggeduser.is_supervisor:
                    role = "supervisor"
                elif loggeduser.is_operator:
                    role = "operator"

                user_data = {
                    "user": {
                        'serial_no': loggeduser.id,
                        'creation_date': loggeduser.date_joined,
                        'username': loggeduser.username,
                        'user_role': role,
                        'email': loggeduser.email,
                        'contact_no': loggeduser.phone
                    }
                }
                logger.info(user_data)
                token, created = Token.objects.get_or_create(user=user)
                token = {'token': token.key}
                logger.info(token)
                user_data.update(token)
                return JsonResponse({"Response": {
                    "Status": "status"},
                    "Data": user_data
                }, safe=False, status=status.HTTP_200_OK)
                # next_param = request.POST.get('next')
                # if next_param:
                #     url = next_param
                # else:
                #     url = reverse('dashboard')

                # return redirect(url)
        else:
            return JsonResponse({"Response": {
                "Status": "error"},
                "message": "Invalid mail id or password"
            }, safe=False, status=status.HTTP_200_OK)

    #         redirect_url = request.GET.get('next', reverse('index')) if request.GET else reverse('index')
    #         response = {"logged_in": user.is_active, "redirect_url": redirect_url}
    #         return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
    #     else:
    #         response = {"logged_in": False, "redirect_url": None}
    #         return JsonResponse(response, safe=False, status=status.HTTP_403_FORBIDDEN)
    # elif request.user and request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('index'))
    # else:
    #     return render(request, 'login.html')


def user_logout(request):
    logger.info("Logged in user is {}".format(request.user))
    logout(request)
    logger.info("Logged out and now user is {}".format(request.user))

    return JsonResponse({"Response": {
        "Status": "success"},
        "message": "User logged out successfully"
    }, safe=False, status=status.HTTP_200_OK)


@api_view(['POST'])
def user_registration(request):
    if request.method == 'POST':
        try:
            username = request.data['username']
            email = request.data['email']
            phone_country = "+91"
            mob = re.sub(r"\D", "", request.data['phone'])
            phone = phone_country + str(mob)
            company_name = request.data['company']
            address1 = request.data['address1']
            address2 = request.data['address2']
            city = request.data['city']
            pincode = request.data['pincode']
            state = request.data['state']
            gst_no = request.data['gstno']

            # regex = "^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$"
            #
            # p = re.compile(regex)
            #
            # if not (re.search(p, gst_no)):
            #     logger.error("Signup: Invalid GST Number")
            #     response = {"Response": {"Status": "error"}, "message": "Invalid GST Number"}
            #     return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Signup: Error in getting user info: {}".format(e))
            response = {"Response": {"Status": "error"}, "message": "Error in getting user info; {}".format(e)}
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

        if username.startswith('__'):
            response = {"Response": {"Status": "error"}, "message": "Username not allowed"}
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

        try:
            User.objects.get(username=username)
            response = {"Response": {"Status": "error"}, "message": "The username is already taken"}
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            pass

        try:
            User.objects.get(email=email)
            response = {"Response": {"Status": "error"}, "message": "The email address is already used for registration"}
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            pass

        try:
            User.objects.get(phone=phone)
            response = {"Response": {"Status": "error"}, "message": "The phone number is already used for registration"}
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            pass

        with transaction.atomic():
            try:
                company = Company.objects.get(company_name=company_name, gst_no=gst_no, address1=address1)
                admin_count_in_company = User.objects.filter(company_id=company, is_super_admin=True).count()
                logger.info("Admin count in company is {}".format(admin_count_in_company))
                if admin_count_in_company > 0:
                    logger.info("Signup: Already a super admin is registered in the company \"{}\". "
                                "Only one super admin per company is allowed".format(company_name))
                    response = {"Response": {"Status": "error"}, "message": "Only one super admin per company is allowed"}
                    return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

            except Company.DoesNotExist:
                try:
                    company = Company()
                    company.company_name = company_name
                    company.address1 = address1
                    company.address2 = address2
                    company.city = city
                    company.pincode = pincode
                    company.state = state
                    company.gst_no = gst_no
                    company.save()
                    logger.info("Signup: successfully added company info to db")
                except Exception as err:
                    transaction.set_rollback(True)
                    logger.info("Signup: Error in adding company info to db: {}".format(err))
                    response = {"Response": {"Status": "error"}, "message": "Error in adding "
                                                                            "company info to db: {}".format(err)}
                    return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

            try:
                # Add admin user to database
                super_admin_user = User.objects.create_user(username, email=email)
                super_admin_user.phone = phone  # phone_country + phone
                super_admin_user.is_super_admin = True
                super_admin_user.company = company
                super_admin_user.save()

                # Send welcome and verification email
                super_admin_user.send_verification_email(get_current_site(request).domain)

                response = {"Response": {"Status": "success"}, "message": "User created successfully"}
                logger.info("Signup: successfully added user info to db")
            except Exception as e:
                transaction.set_rollback(True)
                logger.info("Signup: Error in adding user info to db: {}".format(e))
                response = {"Response": {"Status": "error"}, "message": "Error in adding user info to db: {}".format(e)}
                return JsonResponse(response, safe=False, status=status.HTTP_400_BAD_REQUEST)
            return JsonResponse(response, safe=False, status=status.HTTP_201_CREATED)
    elif request.user and request.user.is_authenticated:
        request.user.await_verification = True
        return HttpResponseRedirect(reverse('user_not_verified'))
    else:
        return render(request, 'signup.html')


@api_view(['GET'])
def get_user_to_verify(request, uidb64, token):
    logger.info("User is {}".format(request.user))
    logger.info("Verifying user")

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        logger.info(uid)
    except (TypeError, ValueError, OverflowError):
        logger.info("User verification: invalid user id")
        response = {"Response": {"Status": "error"}, "message": "Invalid verification link"}
        return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

    if request.method == 'GET':

        try:
            user = User.objects.get(pk=uid)
            if user is not None and not user.is_link_expired():
            # if user is not None:
                data = {"username": user.username, "email": user.email, "company_name": user.company.company_name}
                # logger.info("User verification: was success")
                response = {"Response": {"Status": "success"}, "Data": data}
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
            else:
                response = {"Response": {"Status": "error"}, "message": "Invalid verification link or link expired"}
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            logger.info("User verification: couldn't find the user")
            response = {"Response": {"Status": "error"}, "message": "Invalid verification link or link expired"}
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

    response = {"Response": {"Status": "error"}, "message": "Method {} not allowed".format(request.method)}
    return JsonResponse(response, safe=False, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def forgot_password(request,):
    logger.info("User is {}".format(request.user))
    logger.info("forgot password")

    if request.method == 'POST':
        username = request.data['username']
        email = request.data['email']
        # logger.info(username)
        # logger.info(type(username))
        # logger.info(email)
        try:
            user = User.objects.get(username=username)
            logger.info(user.email)
            if user is not None and user.email == email and user.email_verified is True:
                user.send_verification_email(get_current_site(request).domain)
                response = {"Response": {"Status": "success"}, "message": "Email sent to the user"}
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

            response = {"Response": {"Status": "error"}, "message": "Invalid user"}
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        except Exception as err:
            logger.info("Forgot password: couldn't find the user")
            response = {"Response": {"Status": "error"}, "message": "Invalid user"}
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)


@api_view(['POST'])
def change_password(request, uidb64, token):
    logger.info("User is {}".format(request.user))
    logger.info("Verifying user")

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
    except (TypeError, ValueError, OverflowError):
        logger.info("User verification: invalid user id")
        response = {"Response": {"Status": "error"}, "message": "Invalid verification link"}
        return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

    # TODO add expiry of link

    # try:
    #     user = User.objects.get(pk=uid)
    #     logger.info(user.date_joined)
    #     logger.info(user.email_verified)
    #     logger.info(datetime.now())
    #     uid = force_str(urlsafe_base64_decode(uidb64))
    # except Exception as err:
    #     logger.info("User verification: invalid user id")
    #     response = {"Response": {"Status": "error"}, "message": "Invalid verification link"}
    #     return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

    if request.method == 'POST':
        password = request.data['password']
        password2 = request.data['confirmpassword']

        if password != password2:
            response = {"Response": {"Status": "error"}, "message": "Password mismatch"}
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

        try:
            logger.info(uid)
            user = User.objects.get(pk=uid)
            logger.info(user)
            # if user is not None and user.email_verified is True:
            #     logger.info("User verification: User already verified")
            #     response = {"Response": {"Status": "error"}, "message": "User already verified"}
            #     return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

            if user is not None and user.verify_email(token):
                user.set_password(password)
                user.email_verified = True
                user.save()
            else:
                response = {"Response": {"Status": "error"}, "message": "Invalid verification link"}
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            logger.info("User verification: couldn't find the user")
            response = {"Response": {"Status": "error"}, "message": "Invalid verification link"}
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

        logger.info("User verification: was success")
        response = {"Response": {"Status": "success"}, "message": "User verification and password update done"}
        return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

    response = {"Response": {"Status": "error"}, "message": "Method {} not allowed".format(request.method)}
    return JsonResponse(response, safe=False, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# def my_scheduled_job():
#     logger.info("ran @ {}".format(datetime.today()))
#     pass

# @login_required
@api_view(['GET'])
def list_users(request):
    logger.info("User is {}".format(request.user))
    data = []

    all_users = User.objects.filter(email_verified=False)
    for single_user in all_users.values():
        user_obj = User.objects.get(id=single_user["id"])
        if user_obj.is_link_expired():
            user_obj.invite_link_expired = True
            user_obj.save()
        else:
            user_obj.invite_link_expired = False
            user_obj.save()

    # operators cannot see user managemente
    if request.user.is_operator:
        return JsonResponse({"Response": {"Status": "error"}, "message": "Requested user not authorized to see users"},
                            safe=False, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        company = Company.objects.get(id=request.user.company_id)
        # supervisors can only see their own added users
        if request.user.is_supervisor:
            users = User.objects.filter(company_id=company).filter(added_by_id=request.user)
        else:
            # admins can see all invitations
            users = User.objects.filter(company_id=company)

        # users = User.objects.all()

        for user_info in users.values():
            perm_obj = SitePermission.objects.filter(user_id=user_info["id"])
            count = 0
            for userid in perm_obj.values("user_id"):
                count += 1
            role = ""
            if not user_info["is_super_admin"]:
                if user_info["is_admin"]:
                    role = "admin"
                elif user_info["is_supervisor"]:
                    role = "supervisor"
                elif user_info["is_operator"]:
                    role = "operator"

                user_status = -1
                # user_status = 0 invite sent
                # user_status = 1 invite accepted and active
                # user_status = 2 invite expired
                if not user_info["email_verified"] and not user_info["invite_link_expired"]:
                    user_status = 0
                elif user_info["email_verified"]:
                    user_status = 1
                elif user_info["invite_link_expired"]:
                    user_status = 2

                response_data = {
                    'serial_no': user_info["id"],
                    'creation_date': user_info["date_joined"],
                    'username': user_info["username"],
                    'avatar': 'http://{}{}{}'
                    .format(get_current_site(request).domain, settings.MEDIA_URL, user_info["avatar"])
                    if user_info["avatar"] else "",
                    'user_role': role,
                    'email': user_info["email"],
                    'contact_no': user_info["phone"],
                    "status": user_status,
                    'no_of_sites': count

                }
                data.append(response_data)

        logger.debug("users array length {}".format(len(data)))
        return JsonResponse({"Response": {
            "Status": "success"},
            "Data": data
        }, safe=False, status=status.HTTP_200_OK)


# @login_required
@api_view(['GET'])
def user(request, pk):

    data = []
    if request.method == 'GET':
        user_dat = User.objects.filter(id=pk)
        if user_dat.count() < 1:
            return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_200_OK)

        for user_info in user_dat.values():
            perm_obj = SitePermission.objects.filter(user_id=user_info["id"])
            count = 0
            for userid in perm_obj.values("user_id"):
                count += 1
            role = ""
            if not user_info["is_super_admin"]:
                if user_info["is_admin"]:
                    role = "admin"
                elif user_info["is_supervisor"]:
                    role = "supervisor"
                elif user_info["is_operator"]:
                    role = "operator"

                user_status = -1
                # user_status = 0 invite sent
                # user_status = 1 invite accepted and active
                # user_status = 2 invite expired
                if not user_info["email_verified"] and not user_info["invite_link_expired"]:
                    user_status = 0
                elif user_info["email_verified"]:
                    user_status = 1
                elif user_info["invite_link_expired"]:
                    user_status = 2

                response_data = {
                    'serial_no': user_info["id"],
                    'creation_date': user_info["date_joined"],
                    'username': user_info["username"],
                    'avatar': 'http://{}{}{}'
                    .format(get_current_site(request).domain, settings.MEDIA_URL, user_info["avatar"])
                    if user_info["avatar"] else "",
                    'user_role': role,
                    'email': user_info["email"],
                    'contact_no': user_info["phone"],
                    # 'site_limit': user_info["site_limit"],
                    "status": user_status,
                    'no_of_sites': count

                }
                data.append(response_data)

        return JsonResponse({"Response": {
            "Status": "success"},
            "Data": data
        }, safe=False, status=status.HTTP_200_OK)


# TODO
# @login_required
@api_view(['POST'])
def add_user(request):

    if request.method == 'POST':
        logger.info("Current user is {}".format(request.user))

        username = request.POST.get('user_name')
        role = str(request.POST.get('user_role')).lower()
        email = request.POST.get('email_id')
        phone_country = "+91"
        mob = re.sub(r"\D", "", request.POST.get('contact_number'))
        phone = phone_country + str(mob)
        image = request.FILES.get("user_picture")
        # site_limit = request.POST.get("site_limit") if request.POST.get("site_limit") else 0

        company = Company.objects.get(id=request.user.company_id)

        if role not in ["admin", "supervisor", 'operator']:
            response = {"Response": {
                "Status": "error"},
                "message": "Invalid user role"
            }
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

        if request.user.is_operator or (request.user.is_supervisor and (role == "admin" or role == "supervisor")):
            # and role != "operator"): TODO check if condition
            response = {"Response": {
                "Status": "error"},
                "message": "You({user}) are not authorized to create any {role} account".format(user=request.user,
                                                                                              role=role)
            }
            return JsonResponse(response, safe=False, status=status.HTTP_403_FORBIDDEN)

        if username.startswith('__'):
            response = {"Response": {
                "Status": "error"},
                "message": "Username not allowed"
            }
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

        try:
            User.objects.get(username=username)
            response = {"Response": {
                "Status": "error"},
                "message": "The username is already taken"
            }
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            pass

        try:
            User.objects.get(email=email)
            response = {"Response": {
                "Status": "error"},
                "message": "The email address is already used for registration"
            }
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            pass

        try:
            User.objects.get(phone=phone)
            response = {"Response": {"Status": "error"}, "message": "The phone number is already used for registration"}
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            pass

        with transaction.atomic():

            try:
                # Add user to database
                user = User.objects.create_user(username, email=email)
                if role == "admin":
                    user.is_admin = True
                elif role == "supervisor":
                    user.is_supervisor = True
                elif role == "operator":
                    user.is_operator = True
                user.phone = phone  # phone_country + phone
                user.avatar = image
                # user.site_limit = site_limit
                user.company = company
                user.added_by = request.user
                user.save()

                # Send welcome and verification email
                user.send_verification_email(get_current_site(request).domain)

                response = {"Response": {
                    "Status": "success"},
                    "message": "User registered successfully.Please check the provided "
                               "email inbox for further instruction"
                }
            except Exception as e:
                transaction.set_rollback(True)
                response = {"Response": {
                    "Status": "error"},
                    "message": "Error in saving user data; {}".format(e)
                }
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        return JsonResponse(response, safe=False, status=status.HTTP_201_CREATED)
    elif request.user and request.user.is_authenticated:
        request.user.await_verification = True
        return HttpResponseRedirect(reverse('user_not_verified'))
    else:
        return render(request, 'signup.html')


@api_view(['GET'])
def resend_invite(request, pk):

    if request.method == 'GET':
        logger.info("Current user is {}".format(request.user))

        # user_id = request.data['user_id']

        user_obj = User.objects.get(id=pk)
        role = ""
        if user_obj.is_admin:
            role = "admin"
        elif user_obj.is_supervisor:
            role = "supervisor"
        elif user_obj.is_operator:
            role = "operator"

        if request.user.is_operator or (request.user.is_supervisor and (role == "admin" or role == "supervisor")):
            # TODO check if condition
            response = {"Response": {
                "Status": "error"},
                "message": "You({user}) are not authorized to create any {role} account".format(user=request.user,
                                                                                              role=role)
            }
            return JsonResponse(response, safe=False, status=status.HTTP_403_FORBIDDEN)

        try:
            # Send welcome and verification email
            user_obj.send_verification_email(get_current_site(request).domain)
            user_obj.invite_link_expired = False
            user_obj.save()

            response = {"Response": {
                "Status": "success"},
                "message": "User invitation resent"
            }
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            response = {"Response": {
                "Status": "error"},
                "message": "Error in sending user invite; {}".format(e)
            }
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

    return JsonResponse({"Response": {
                "Status": "error"},
                "message": "Invalid request"
            }, safe=False, status=status.HTTP_400_BAD_REQUEST)


# @login_required()
@api_view(['PUT'])
def edit_user(request, pk):

    if request.method == 'PUT':
        try:
            user_obj = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)

        username = request.POST.get('user_name')
        role = str(request.POST.get('user_role')).lower()
        image = request.FILES.get("user_picture")

        logger.info(request.user)

        if role not in ["admin", "supervisor", 'operator']:
            response = {"Response": {
                "Status": "error"},
                "message": "Invalid user role"
            }
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

        if request.user.is_operator or (request.user.is_supervisor and role != "operator"):
            response = {
                "created": False,
                "error": "You({user}) are not authorized to create any {role} account".format(user=request.user,
                                                                                              role=role)
            }
            return JsonResponse(response, safe=False, status=status.HTTP_403_FORBIDDEN)

        try:
            # edit user to database
            user_obj = User.objects.get(id=pk)
            user_obj.username = username
            if role == "admin":
                user.is_admin = True
            elif role == "supervisor":
                user_obj.is_supervisor = True
                # user_obj.is_operator = False
            elif role == "operator":
                user_obj.is_operator = True
                # user_obj.is_supervisor = False
            user_obj.avatar = image
            user_obj.save()

            response = {"Response": {
                "Status": "success"},
                "message": "User edited successfully"
            }
        except Exception as e:
            response = {"Response": {
                "Status": "error"},
                "message": "Error in saving user data; {}".format(e)
            }
            return JsonResponse(response, safe=False, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(response, safe=False, status=status.HTTP_201_CREATED)
    return JsonResponse({"Response": {
                "Status": "error"},
                "message": "Invalid request"
            }, safe=False, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def get_available_users(request, pk):
#     site_ids = []
#     available_users = []
#     logger.info("Got request to list available users before delete")
#     if request.method == 'GET':
#         try:
#             requested_user = User.objects.get(id=pk)
#         except ObjectDoesNotExist:
#             return JsonResponse({"Response": {
#                     "Status": "error"},
#                     'message': 'The user does not exist'
#                 }, status=status.HTTP_200_OK)
#
#         role = ""
#         user_obj = User.objects.filter(id=pk)
#         response_data = {}
#         for user_info in user_obj.values():
#             if not user_info["is_admin"]:
#                 logger.debug("About to delete user is not admin")
#                 if user_info["is_supervisor"]:
#                     role = "supervisor"
#                 elif user_info["is_operator"]:
#                     role = "operator"
#                 logger.debug("About to delete user is {}".format(role))
#
#         logger.debug("assigned_sites {}".format(site_ids))
#         logger.debug("About to delete user after loop is {}".format(role))
#         if role == "supervisor":
#             logger.debug("supervisor")
#             user_obj = User.objects.exclude(id=pk).filter(is_supervisor=True).\
#                 filter(company_id=request.user.company_id).filter(email_verified=True)
#             logger.debug(user_obj)
#         elif role == "operator":
#             logger.debug("operator")
#             user_obj = User.objects.filter(is_operator=True).filter(company_id=request.user.company_id).filter(email_verified=True).exclude(id=pk)
#             logger.debug(user_obj)
#
#         for user_dat in user_obj.values():
#             logger.info(user_dat)
#         # for site_id in site_ids:
#             assigned_site_count = 0
#             # logger.info("--------------")
#             # logger.info(user_dat)
#             # TODO exclude the users that are already assigned to the assigned_sites
#             perm_obj = SitePermission.objects.filter(user_id=user_dat["id"])  # .exclude(site_id=site_id["serial_no"])
#             for perm in perm_obj.values():
#                 assigned_site_count += 1
#                 # logger.info(perm)
#             if assigned_site_count < 4:
#                 dat = {
#                     'serial_no': user_dat["id"],
#                     'creation_date': user_dat["date_joined"],
#                     'username': user_dat["username"],
#                     'user_role': role,
#                     'email': user_dat["email"],
#                     'contact_no': user_dat["phone"],
#                     'site_limit': user_dat["site_limit"],
#                     'no_of_sites': assigned_site_count
#
#                 }
#                 available_users.append(dat)
#                 # logger.info(user_dat)
#                 # logger.info(assigned_site_count)
#
#         logger.debug("available_users {}".format(available_users))
#         response_data.update({"available_users": available_users})
#         return JsonResponse({"Response": {
#                 "Status": "success"},
#                 "Data": response_data
#             }, safe=False, status=status.HTTP_200_OK)
@api_view(['GET'])
def get_available_users(request, pk):
    site_ids = []
    available_users = []
    logger.info("Got request to list available users before delete")
    if request.method == 'GET':
        try:
            requested_user = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            return JsonResponse({"Response": {
                    "Status": "error"},
                    'message': 'The user does not exist'
                }, status=status.HTTP_200_OK)

        role = ""
        user_obj = User.objects.filter(id=pk)
        response_data = {}
        for user_info in user_obj.values():
            if not user_info["is_admin"]:
                logger.debug("About to delete user is not admin")
                if user_info["is_supervisor"]:
                    role = "supervisor"
                elif user_info["is_operator"]:
                    role = "operator"
                logger.debug("About to delete user is {}".format(role))
            perm_obj = SitePermission.objects.filter(user_id=user_info["id"])
            count = 0
            for perm_info in perm_obj.values():
                count += 1
                site_obj = Site.objects.filter(id=perm_info["site_id"])
                for site_info in site_obj.values():
                    site_data = {
                        'serial_no': site_info["id"],
                        'creation_date': site_info["created"],
                        'site_name': site_info["site_name"],
                        'address': site_info["address"],
                        'city': site_info["city"],
                        'state': site_info["state"],
                        'device_mobile_number': site_info["phone"],
                        'status': site_info["status"],
                        'no_of_alerts': site_info["alerts"]

                    }
                    site_ids.append(site_data)

            response_data = {
                "assigned_sites": site_ids,
            }

            # logger.info(response_data)
            # logger.info(role)
        logger.debug("assigned_sites {}".format(site_ids))
        logger.debug("About to delete user after loop is {}".format(role))
        if role == "supervisor":
            logger.debug("supervisor")
            user_obj = User.objects.exclude(id=pk).filter(is_supervisor=True).\
                filter(company_id=request.user.company_id).filter(email_verified=True)
            logger.debug(user_obj)
        elif role == "operator":
            logger.debug("operator")
            user_obj = User.objects.exclude(id=pk).filter(is_operator=True).\
                filter(company_id=request.user.company_id).filter(email_verified=True)
            logger.debug(user_obj)

        for user_dat in user_obj.values():
            logger.info(user_dat)
        # for site_id in site_ids:
            assigned_site_count = 0
            # logger.info("--------------")
            # logger.info(user_dat)
            # TODO exclude the users that are already assigned to the assigned_sites
            perm_obj = SitePermission.objects.filter(user_id=user_dat["id"])  # .exclude(site_id=site_id["serial_no"])
            for perm in perm_obj.values():
                assigned_site_count += 1
                # logger.info(perm)
            if assigned_site_count < 100:
                dat = {
                    'serial_no': user_dat["id"],
                    'creation_date': user_dat["date_joined"],
                    'username': user_dat["username"],
                    'user_role': role,
                    'email': user_dat["email"],
                    'contact_no': user_dat["phone"],
                    'site_limit': user_dat["site_limit"],
                    'no_of_sites': assigned_site_count

                }
                available_users.append(dat)
                # logger.info(user_dat)
                # logger.info(assigned_site_count)

        logger.debug("available_users {}".format(available_users))
        response_data.update({"available_users": available_users})
        return JsonResponse({"Response": {
                "Status": "success"},
                "Data": response_data
            }, safe=False, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def save_and_delete_user(request, pk):
    site_ids = []

    if request.method == 'DELETE':
        try:
            user_obj = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            return JsonResponse(
                {
                    "Response": {
                        "Status": "error"
                    },
                    'message': 'The user does not exist'
                }, status=status.HTTP_200_OK)

        # TODO get site id and users then add user to site_permission table
        request_data = request.data['assignsites']
        # logger.info(request_data)
        user_id = ""
        site_id = ""

        for site_user in request_data:
            supervisor_count_in_this_site = 0
            operator_count_in_this_site = 0

            site_data = Site.objects.filter(company_id=request.user.company_id, site_name=site_user["sitename"])

            for site_info in site_data.values():
                site_id = site_info["id"]

            for users in site_user["user"]:
                logger.info("{} {}".format(users, site_user["sitename"]))
                user_data = User.objects.filter(username=users)

            # for site_info in site_data.values():
            #     site_id = site_info["id"]

                for user_info in user_data.values():
                    user_id = user_info["id"]
                    role = ""
                    if user_info["is_supervisor"]:
                        role = "supervisor"
                    elif user_info["is_operator"]:
                        role = "operator"
                    logger.info(role)
                    # get no. of supervisors and operators in a given site(max 3 supervisors and 2 operators)
                    # if maximum reached before adding and deletion then return error with max count reached
                    site_obj_for_getting_count = SitePermission.objects.filter(site_id=site_id)
                    for site_dat in site_obj_for_getting_count.values():
                        logger.info(site_dat["user_id"])

                        user_dat_for_getting_user_role_count = User.objects.filter(id=site_dat["user_id"])
                        for user_dat in user_dat_for_getting_user_role_count.values():
                            if role == "supervisor" and user_dat["is_supervisor"]:
                                supervisor_count_in_this_site += 1
                                logger.info("Site {} has {} supervisors before deletion".format(
                                    site_user["sitename"],
                                    supervisor_count_in_this_site,
                                    ))
                            elif role == "operator" and user_dat["is_operator"]:
                                operator_count_in_this_site += 1

                    if role == "supervisor":
                        logger.info("Site {} has {} supervisors before deletion".format(
                            site_user["sitename"],
                            supervisor_count_in_this_site,
                        ))
                        if supervisor_count_in_this_site > 4:  # 3 plus 1 = 4 to add new user and delete old
                            return JsonResponse(
                                {
                                    "Response": {
                                        "Status": "error"
                                    },
                                    'message': 'Save and delete failed because only 3 supervisors are permitted for Site {}'
                                    .format(site_user["site_name"])
                                },
                                status=status.HTTP_200_OK)

                    elif role == "operator":
                        logger.info("Site {} has {} operators before deletion".format(site_user["sitename"],
                                                                                operator_count_in_this_site))
                        if operator_count_in_this_site > 3:  # 2 plus 1 = 3 to add new user and delete old
                            return JsonResponse(
                                {
                                    "Response": {
                                        "Status": "error"
                                    },
                                    'message': 'Save and delete failed because only 2 operators are permitted for Site {}'
                                    .format(site_user["site_name"])
                                },
                                status=status.HTTP_200_OK)

                existing_permission = SitePermission.objects.filter(user_id=user_id, site_id=site_id)
                if existing_permission:
                    logger.info("Skipping since, user {} already assigned to {} site".format(site_user["user"],
                                                                                       site_user["sitename"]))
                    continue
                else:
                    with transaction.atomic():
                        try:
                            perm_obj = SitePermission()
                            perm_obj.user_id = user_id
                            perm_obj.site_id = site_id
                            perm_obj.save()
                            # User.objects.filter(pk=pk).delete()
                        except Exception as err:
                            transaction.set_rollback(True)
                            return JsonResponse(
                                {
                                    "Response": {
                                        "Status": "error"
                                    },
                                    'message': 'Save and delete failed, {}'.format(err)
                                },
                                status=status.HTTP_200_OK)

                logger.info(site_user)

        try:
            User.objects.filter(pk=pk).delete()
        except Exception as err:
            return JsonResponse(
                {
                    "Response": {
                        "Status": "error"
                    },
                    'message': 'Save and delete failed, {}'.format(err)
                },
                status=status.HTTP_200_OK)

        return JsonResponse(
            {
                "Response": {
                    "Status": "success"
                },
                'message': 'user deleted successfully!'
            },
            status=status.HTTP_200_OK)


@api_view(['GET'])
def list_sites(request):
    city_state = []
    data = []
    unverified_data = []
    supervisors_data = []
    operators_data = []
    if request.method == 'GET':

        # unverified_site_obj = Site.objects.filter(company_id=request.user.company_id).filter(phone_verified=1)
        # for site_info in unverified_site_obj.values():
        #     devices = {}
        #     device_obj = Device.objects.filter(site_id=site_info["id"])
        #     for dev in device_obj.values():
        #         devices = {
        #             "device_name": [
        #                 dev["device_name1"],
        #                 dev["device_name2"],
        #                 dev["device_name3"]
        #             ],
        #             "device_serial_number": [
        #                 dev["serial_no1"],
        #                 dev["serial_no2"],
        #                 dev["serial_no3"]
        #             ],
        #         }
        #
        #     unverified_response_data = {
        #         'serial_no': site_info["id"],
        #         'creation_date': site_info["created"],
        #         'site_name': site_info["site_name"],
        #         'address': site_info["address"],
        #         'city': site_info["city"],
        #         'state': site_info["state"],
        #         'device_mobile_number': site_info["phone"],
        #         'status': site_info["status"],
        #         'no_of_alerts': site_info["alerts"]
        #
        #     }
        #     unverified_data.append(unverified_response_data)
        #     unverified_response_data.update(devices)

        if request.user.is_operator:
            response = {"Response": {
                "Status": "error"},
                "message": "You({user}) are not authorized to view this page".format(user=request.user)
            }
            return JsonResponse(response, safe=False, status=status.HTTP_403_FORBIDDEN)

        site_obj = Site.objects.filter(company_id=request.user.company_id).filter(phone_verified=1)
        for site_info in site_obj.values():
            perm_obj = SitePermission.objects.filter(site_id=site_info["id"])
            supervisor = []
            operator = []
            for userid in perm_obj.values("user_id"):
                user_obj = User.objects.filter(id=userid["user_id"]).filter(is_supervisor=True).\
                    filter(is_operator=False)
                # user_obj = user_obj.filter(is_supervisor=True).filter(is_operator=False)  # TODO Set to True
                if user_obj:
                    supervisor.append([i for i in user_obj.values("username")])

                user_obj = User.objects.filter(id=userid["user_id"]).filter(is_operator=True).\
                    filter(is_supervisor=False)
                # user_obj = user_obj.filter(is_operator=False).filter(is_supervisor=False)  # TODO Set operator to True
                if user_obj:
                    operator.append([i for i in user_obj.values("username")])

            supervisors = []
            for j in supervisor:
                for k in j:
                    supervisors.append(k["username"])
                    # supervisors_data.append(k)

            operators = []
            for n in operator:
                for m in n:
                    operators.append(m["username"])
                    # operators_data.append(m)

            # logger.info("----------------------")
            users = {
                "supervisors": supervisors,
                "operators": operators
            }
            # logger.info(users)

            devices = {}
            device_obj = Device.objects.filter(site_id=site_info["id"])
            for dev in device_obj.values():
                devices = {
                    "device_name": [
                        dev["device_name1"],
                        dev["device_name2"],
                        dev["device_name3"]
                    ],
                    "device_serial_number": [
                        dev["serial_no1"],
                        dev["serial_no2"],
                        dev["serial_no3"]
                    ],
                }
                # logger.info(devices)
            # logger.info("----------------------")
            response_data = {}
            if users["supervisors"] or users["operators"]:
                response_data = {
                    'serial_no': site_info["id"],
                    'creation_date': site_info["created"],
                    'site_name': site_info["site_name"],
                    'address': site_info["address"],
                    'city': site_info["city"],
                    'state': site_info["state"],
                    "supervisors": users["supervisors"],
                    "operators": users["operators"],
                    'device_mobile_number': site_info["phone"],
                    'status': site_info["status"],
                    'no_of_alerts': site_info["alerts"]

                }
                data.append(response_data)
                response_data.update(devices)
            else:
                unverified_response_data = {
                    'serial_no': site_info["id"],
                    'creation_date': site_info["created"],
                    'site_name': site_info["site_name"],
                    'address': site_info["address"],
                    'city': site_info["city"],
                    'state': site_info["state"],
                    'device_mobile_number': site_info["phone"],
                    'status': site_info["status"],
                    'no_of_alerts': site_info["alerts"]

                }
                unverified_data.append(unverified_response_data)
                unverified_response_data.update(devices)

            city_state.append(site_info["city"])
            city_state.append(site_info["state"])

        logger.info('Response:')
        supervisor = []
        supervisrs = User.objects.filter(is_supervisor=True).filter(is_operator=False).filter(email_verified=1)\
            .filter(company_id=request.user.company_id)
        for userid in supervisrs.values():
            perm_obj = SitePermission.objects.filter(user_id=userid["id"])
            count = 0
            for perm in perm_obj.values():
                count += 1
            supervisor.append({
                'serial_no': userid["id"],
                'creation_date': userid["date_joined"],
                'username': userid["username"],
                'avatar': 'http://{}{}{}'
                .format(get_current_site(request).domain, settings.MEDIA_URL, userid["avatar"])
                if userid["avatar"] else "",
                'user_role': "Supervisor",
                'email': userid["email"],
                'contact_no': userid["phone"],
                # 'site_limit': userid["site_limit"],
                'no_of_sites': count

            })
        logger.info("++++++++++++++===")
        # logger.info(supervisor)

        operator = []
        operatrs = User.objects.filter(is_supervisor=False).filter(is_operator=True).filter(email_verified=1).\
            filter(company_id=request.user.company_id)
        for userid in operatrs.values():
            perm_obj = SitePermission.objects.filter(user_id=userid["id"])
            count = 0
            for perm in perm_obj.values():
                count += 1
            operator.append({
                'serial_no': userid["id"],
                'creation_date': userid["date_joined"],
                'username': userid["username"],
                'avatar': 'http://{}{}{}'
                .format(get_current_site(request).domain, settings.MEDIA_URL, userid["avatar"])
                if userid["avatar"] else "",
                'user_role': "Operator",
                'email': userid["email"],
                'contact_no': userid["phone"],
                # 'site_limit': userid["site_limit"],
                'no_of_sites': count

            })

        context = {"sites": data, "unverified_sites": unverified_data, "city_state": list(set(city_state)), "supervisors": supervisor,
                   "operators": operator}
        # logger.info(context)

        # logger.info(len(data))

        return JsonResponse({"Response": {"Status": "success"}, "Data": context},
                            safe=False, status=status.HTTP_200_OK)

    return JsonResponse({"Response": {"Status": "success"}, "Data": "Bad request"},
                        safe=False, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def site(request, pk):

    if request.method == 'GET':

        site_dat = Site.objects.filter(id=pk)
        if site_dat.count() < 1:
            return JsonResponse({
                "Response":
                    {
                        "Status": "error"
                     },
                "Data": "The requested site does not exist"
            }, status=status.HTTP_404_NOT_FOUND)

        context = []
        site_obj = Site.objects.filter(id=pk)
        for site_info in site_obj.values():
            perm_obj = SitePermission.objects.filter(site_id=site_info["id"])
            supervisor = []
            operator = []
            for userid in perm_obj.values("user_id"):
                user_obj = User.objects.filter(id=userid["user_id"]).filter(is_supervisor=True). \
                    filter(is_operator=False)
                # user_obj = user_obj.filter(is_supervisor=True).filter(is_operator=False)  # TODO Set to True
                if user_obj:
                    supervisor.append([i for i in user_obj.values("username")])

                user_obj = User.objects.filter(id=userid["user_id"]).filter(is_operator=True). \
                    filter(is_supervisor=False)
                # user_obj = user_obj.filter(is_operator=False).filter(is_supervisor=False)  # TODO Set operator to True
                if user_obj:
                    operator.append([i for i in user_obj.values("username")])

            supervisors = []
            for j in supervisor:
                for k in j:
                    supervisors.append(k["username"])

            operators = []
            for n in operator:
                for m in n:
                    operators.append(m["username"])

            # logger.info("----------------------")
            users = {
                "supervisors": supervisors,
                "operators": operators
            }
            # logger.info(users)

            devices = {}
            device_obj = Device.objects.filter(site_id=site_info["id"])
            for dev in device_obj.values():
                devices = {
                    "device_name": [
                        dev["device_name1"],
                        dev["device_name2"],
                        dev["device_name3"]
                    ],
                    "device_serial_number": [
                        dev["serial_no1"],
                        dev["serial_no2"],
                        dev["serial_no3"]
                    ],
                }
                # logger.info(devices)
            # logger.info("----------------------")
            response_data = {
                'serial_no': site_info["id"],
                'creation_date': site_info["created"],
                'site_name': site_info["site_name"],
                'address': site_info["address"],
                'city': site_info["city"],
                'state': site_info["state"],
                "supervisors": users["supervisors"],
                "operators": users["operators"],
                'device_mobile_number': site_info["phone"],
                'status': site_info["status"],
                'no_of_alerts': site_info["alerts"]
            }
            response_data.update(devices)
            # logger.info(response_data)
            context.append(response_data)

        logger.info('Response:')
        logger.info(context)

        logger.info(len(context))
        return JsonResponse({"Response": {"Status": "success"}, "Data": context},
                            safe=False, status=status.HTTP_200_OK)
    return JsonResponse({"Response": {"Status": "success"}, "Data": "Bad request"},
                        safe=False, status=status.HTTP_400_BAD_REQUEST)


# @login_required
@api_view(['POST'])
def send_otp(request):

    # Request to send verification sms
    if request.method == 'POST':
        # phone = request.data['phone']
        # site_name = request.data['site_name']

        site_name = request.data['site_name']
        address = request.data['address']
        city = request.data['city']
        state = request.data['state']
        phone_country = "+91"
        mob = re.sub(r"\D", "", request.data['phone'])
        site_mob = phone_country + str(mob)

        try:
            Site.objects.get(company_id=request.user.company_id, site_name=site_name)
            response = {"Response": {
                "Status": "error"},
                "message": "The site name is already used for this company"
            }
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        except Site.DoesNotExist:
            pass

        try:
            Site.objects.get(phone=site_mob)
            response = {"Response": {
                "Status": "error"},
                "message": "The phone number is already used for site registration"
            }
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        except Site.DoesNotExist:
            pass

        with transaction.atomic():

            if not Site.objects.filter(company_id=request.user.company_id, site_name=site_name).exists():
                site_dat = Site()
                site_dat.site_name = site_name
                site_dat.address = address
                site_dat.city = city
                site_dat.state = state
                site_dat.phone = site_mob
                site_dat.company = request.user.company
                site_dat.save()
            else:
                transaction.set_rollback(True)
                return JsonResponse({"Response": {"Status": "error"},
                                     "message": "The site name is already taken"},
                                    safe=False, status=status.HTTP_409_CONFLICT)

        try:
            site_obj = Site.objects.get(company_id=request.user.company_id, site_name=site_name)

            # if str(TimestampSigner().unsign(code, max_age=7200)) == str(request.user.id):
            if not site_mob:
                return JsonResponse({"Response": {"Status": "error"}, "message": "No phone number is provided"},
                                    safe=False, status=status.HTTP_200_OK)
                # return HttpResponse('No phone number is provided', status=400)

            # if phone != site_obj.phone:
            #     site_obj.phone = phone
            #     site_obj.save()

            # token = "{:04d}".format(randint(0, 9999))
            if site_obj.phone_verified:
                return JsonResponse({"Response": {"Status": "error"},
                                     "message": "Site is already verified"},  # Site is already verified
                                    # Site name is already taken
                                    safe=False, status=status.HTTP_200_OK)

            threading.Thread(target=connect_mqtt_in_background, args=(request.user.company_id, )).start()
            sent = site_obj.send_verification_sms(site_obj.id)
            logger.info(sent)
            if sent["status"]:
                return JsonResponse({"Response": {"Status": "success"},
                                     "message": "OTP sent to the registered number",
                                     "valid_for": OTP_VALID_FOR,
                                     "otp": {"token": "{0:04}".format(site_obj.id), "otp": sent["otp"]}},
                                    safe=False, status=status.HTTP_200_OK)
                # return HttpResponse('', status=200)
            return JsonResponse({"Response": {"Status": "error"},
                                 "message": "Site name is already taken"},
                                safe=False, status=status.HTTP_200_OK)
            # return HttpResponse('Invalid phone number', status=400)
        except Exception as err:
            return JsonResponse({"Response": {"Status": "error"},
                                 "message": "Invalid verification request; {}".format(err)},
                                safe=False, status=status.HTTP_200_OK)


def connect_mqtt_in_background(company_id):

    # connect to MQTT
    client = MqttClient(company_id)
    client.publish("my/test/topic", "connected from iw backend app")
    # client.on_connect = client.on_connect
    # client.on_message = client.on_message


# @login_required
@api_view(['POST'])
def verify_otp(request):

    if request.method == 'POST':
        code = request.data['otpnumber']
        site_name = request.data['site_name']

        try:
            site_obj = Site.objects.get(company_id=request.user.company_id, site_name=site_name)
            if not site_obj.phone:
                return JsonResponse({"Response": {"Status": "error"},
                                     "message": "Verification failed. No phone number is provided"},
                                    safe=False, status=status.HTTP_200_OK)

            if site_obj.verify_phone(code)["status"]:
                while site_obj.verify_phone(code)["difference"] < OTP_VALID_FOR:
                    try:
                        sub_count = Subscription.objects.filter(site_id=site_obj.id).count()
                        logger.debug(sub_count)
                        if sub_count > 0:
                            dev_obj = Device.objects.get(site_id=site_obj.id)
                            response = {
                                'device_name1': dev_obj.device_name1,
                                "device_name2": dev_obj.device_name2,
                                "device_name3": dev_obj.device_name3
                            }
                            logger.info(response)
                            return JsonResponse({"Response": {"Status": "success"},
                                                 "message": "Verified both OTP and token"},
                                                safe=False, status=status.HTTP_200_OK)
                    except Exception as err:
                        pass
                        # logger.info("Didn't get the token yet from the device; {}".format(err))

                # return JsonResponse({"Response": {"Status": "success"},
                #                      "message": "Verified"},
                #                     safe=False, status=status.HTTP_200_OK)
            logger.info("Verification failed. Invalid otp or otp expired or didn't get the token from the device")
            return JsonResponse({"Response": {"Status": "error"},
                                 "message": "Verification failed. Invalid otp or token, or otp expired"
                                            "from the device"},
                                safe=False, status=status.HTTP_200_OK)
        except Site.DoesNotExist as err:
            return JsonResponse({"Response": {"Status": "error"},
                                 "message": "Couldn't find the requested site, {}".format(err)},
                                safe=False, status=status.HTTP_200_OK)


# @api_view(['POST'])
# def verify_token(request):
#
#     if request.method == 'POST':
#         site_name = request.data['site_name']
#
#         try:
#             site_obj = Site.objects.get(site_name=site_name, phone_verified=True)
#         except Exception as err:
#             return JsonResponse({"Response": {"Status": "error"},
#                                  "message": "Couldn't find the requested site or phone number not verified, {}"
#                                 .format(err)},
#                                 safe=False, status=status.HTTP_200_OK)
#         try:
#             sub_count = Subscription.objects.filter(site_id=site_obj.id).count()
#             logger.debug(sub_count)
#             if sub_count > 0:
#                 dev_obj = Device.objects.get(site_id=site_obj.id)
#                 response = {
#                     'device_name1': dev_obj.device_name1,
#                     "device_name2": dev_obj.device_name2,
#                     "device_name3": dev_obj.device_name3
#                 }
#                 return JsonResponse({"Response": {"Status": "success"},
#                                      "Data": response},
#                                     safe=False, status=status.HTTP_200_OK)
#             return JsonResponse({"Response": {"Status": "error"},
#                                  "message": "Token verification failed. Didn't get the token from device"},
#                                 safe=False, status=status.HTTP_200_OK)
#         except Exception as err:
#             return JsonResponse({"Response": {"Status": "error"},
#                                  "message": "Token verification failed, didn't get the device serial numbers over mqtt."
#                                             " {}".format(err)}, safe=False, status=status.HTTP_200_OK)


# @csrf_exempt
@api_view(['PUT'])
def add_site(request):
    # TODO add checking user permission
    if not request.user.is_admin:
        return JsonResponse({"Response": {"Status": "error"}, "message": "Requested user not authorized to add site"},
                            safe=False, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        try:
            site_name = request.data['site_name']
            supervisor = request.data['supervisor']
            operator = request.data['operator']

            supervisor_lst = []
            operator_lst = []

            for supervsr in supervisor:
                supervisor_lst.append(User.objects.get(username=str(supervsr)))

            for oprtr in operator:
                operator_lst.append(User.objects.get(username=oprtr))

            if len(supervisor_lst) > 2 or len(operator_lst) > 3:
                return JsonResponse({"Response": {"Status": "error"},
                                     "message": "Supervisors and/or Operators limit reached."
                                                "Maximum of 2 supervisors and 3 operators allowed per site"},
                                    safe=False, status=status.HTTP_400_BAD_REQUEST)
            with transaction.atomic():
                try:
                    try:
                        site_obj = Site.objects.get(company_id=request.user.company_id, site_name=site_name)
                    except Exception as err:
                        return JsonResponse({"Response": {"Status": "error"},
                                             "message": "Error in getting site details; {}".format(err)},
                                            safe=False, status=status.HTTP_200_OK)

                    try:
                        for suprvsr_usr in supervisor_lst:
                            site_per = SitePermission()
                            site_per.site = site_obj
                            site_per.user = suprvsr_usr
                            site_per.save()

                        for op_user in operator_lst:
                            site_per = SitePermission()
                            site_per.site = site_obj
                            site_per.user = op_user
                            site_per.save()
                    except Exception as err:
                        transaction.set_rollback(True)
                        return JsonResponse({"Response": {"Status": "error"},
                                             "message": "Error at adding user permission details; {}".format(err)},
                                            safe=False, status=status.HTTP_200_OK)
                except Exception as err:
                    transaction.set_rollback(True)
                    return JsonResponse({"Response": {"Status": "error"},
                                         "message": err},
                                        safe=False, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"Response": {"Status": "error"}, "message": "{}".format(e)},
                                safe=False, status=status.HTTP_200_OK)
        return JsonResponse({"Response": {"Status": "success"}, "message": "site {} added successfully"
                            .format(site_name)},
                            safe=False, status=status.HTTP_201_CREATED)
    return JsonResponse({"Response": {"Status": "error"}, "message": "Method not allowed"},
                        safe=False, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['PUT'])
def edit_site(request, pk):
    supervisor_lst = []
    operator_lst = []
    if request.method == 'PUT':

        try:
            site_obj = Site.objects.get(id=pk)
        except ObjectDoesNotExist:
            return JsonResponse({"Response": {"Status": "error"}, "Data": "The requested site does not exist"},
                                status=status.HTTP_404_NOT_FOUND)

        try:
            site_obj.site_name = request.data['site_name']
            site_obj.address = request.data['address']
            site_obj.city = request.data['city']
            site_obj.state = request.data['state']
            site_obj.save()

            supervisor = request.data['supervisors']
            operator = request.data['operators']
        except Exception as err:
            return JsonResponse({"Response": {"Status": "error"}, "message": "{}".format(err)},
                                safe=False, status=status.HTTP_400_BAD_REQUEST)

        for supervsr in supervisor:
            supervisor_lst.append(User.objects.get(username=str(supervsr)))

        for oprtr in operator:
            operator_lst.append(User.objects.get(username=oprtr))

        perm_obj = SitePermission.objects.filter(site_id=pk).delete()

        for suprvsr_usr in supervisor_lst:
            site_per = SitePermission()
            site_per.site = site_obj
            site_per.user = suprvsr_usr
            site_per.save()

        for op_user in operator_lst:
            site_per = SitePermission()
            site_per.site = site_obj
            site_per.user = op_user
            site_per.save()

        site_obj = Site.objects.filter(id=pk)
        context = [dict(i) for i in site_obj.values("id", "site_name", "address", "city", "state")]

        return JsonResponse({"Response": {"Status": "success"}, "message": "Site edited successfully"},
                            safe=False, status=status.HTTP_200_OK)

    return JsonResponse({"Response": {"Status": "error"}, "message": "Method not allowed"},
                        safe=False, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['DELETE'])
def delete_site(request, pk):
    logger.info("Delete site request")
    logger.info("Requested site id {}".format(pk))
    try:
        logger.debug("Checking whether the site exists")
        site_data = Site.objects.get(id=pk)
    except ObjectDoesNotExist:
        return JsonResponse({"Response": {"Status": "error"}, "message": "The requested site does not exist"},
                            status=status.HTTP_200_OK)
    logger.debug("The requested site exists")

    if request.method == 'DELETE':
        with transaction.atomic():
            try:
                logger.debug("Trying to unmap the subscriptions")
                subscriptions = Subscription.objects.filter(site_id=pk)
                for sub in subscriptions.values():
                    new_sub = Subscription.objects.get(id=sub["id"])
                    new_sub.site_id = None
                    new_sub.save()
                    logger.debug("Unmapped the subscription {}".format(sub["id"]))
                logger.debug("Trying to delete the site")
                count = Site.objects.filter(pk=pk).delete()
                logger.debug("Deleted the site")
            except Exception as err:
                transaction.set_rollback(True)
                return JsonResponse({"Response": {"Status": "error"}, "message": "{}".format(err)},
                                    status=status.HTTP_200_OK)

        logger.debug("Site deleted successfully")
        return JsonResponse({"Response": {"Status": "success"}, "message": "Site deleted successfully"},
                            status=status.HTTP_200_OK)


@api_view(['GET'])
def filter_sites_by_location(request, name):

    if request.method == 'GET':

        site_dat = Site.objects.filter(company_id=request.user.company_id, city=name)
        if site_dat.count() < 1:
            site_dat = Site.objects.filter(company_id=request.user.company_id, state=name)

        if site_dat.count() < 1:
            return JsonResponse({"Response": {"Status": "error"}, "Data": "The requested site(s) does not exist"},
                                status=status.HTTP_404_NOT_FOUND)

        context = []
        for site_info in site_dat.values():
            perm_obj = SitePermission.objects.filter(site_id=site_info["id"])
            supervisor = []
            operator = []
            for userid in perm_obj.values("user_id"):
                user_obj = User.objects.filter(id=userid["user_id"]).filter(is_supervisor=True). \
                    filter(is_operator=False)
                # user_obj = user_obj.filter(is_supervisor=True).filter(is_operator=False)  # TODO Set to True
                if user_obj:
                    supervisor.append([i for i in user_obj.values("username")])

                user_obj = User.objects.filter(id=userid["user_id"]).filter(is_operator=True). \
                    filter(is_supervisor=False)
                # user_obj = user_obj.filter(is_operator=False).filter(is_supervisor=False)  # TODO Set operator to True
                if user_obj:
                    operator.append([i for i in user_obj.values("username")])

            supervisors = []
            for j in supervisor:
                for k in j:
                    supervisors.append(k["username"])

            operators = []
            for n in operator:
                for m in n:
                    operators.append(m["username"])

            # logger.info("----------------------")
            users = {
                "supervisors": supervisors,
                "operators": operators
            }
            # logger.info(users)

            devices = {}
            device_obj = Device.objects.filter(site_id=site_info["id"])
            for dev in device_obj.values():
                devices = {
                    "device_name": [
                        dev["device_name1"],
                        dev["device_name2"],
                        dev["device_name3"]
                    ],
                    "device_serial_number": [
                        dev["serial_no1"],
                        dev["serial_no2"],
                        dev["serial_no3"]
                    ],
                }
                # logger.info(devices)
            # logger.info("----------------------")
            response_data = {
                'serial_no': site_info["id"],
                'creation_date': site_info["created"],
                'site_name': site_info["site_name"],
                'address': site_info["address"],
                'city': site_info["city"],
                'state': site_info["state"],
                "supervisors": users["supervisors"],
                "operators": users["operators"],
                'device_mobile_number': site_info["phone"],
                'status': site_info["status"],
                'no_of_alerts': site_info["alerts"]
            }
            response_data.update(devices)
            # logger.info(response_data)
            context.append(response_data)

        logger.info('Response:')
        logger.info(context)

        logger.info(len(context))
        return JsonResponse({"Response": {"Status": "success"}, "Data": context},
                            safe=False, status=status.HTTP_200_OK)

    return JsonResponse({"Response": {"Status": "error"}, "Data": "Bad request"},
                        safe=False, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_sub(request):
    summary_data = []

    total_treatment_sites = 0
    free_treatment_sites = 0
    assigned_treatment_sites = 0
    unassigned_treatment_sites = 0
    treatment_last_paid = 0
    treatment_total_paid = 0

    free_treatment_data = []
    active_treatment_data = []
    inactive_treatment_data = []

    total_dispensing_sites = 0
    free_dispensing_sites = 0
    assigned_dispensing_sites = 0
    unassigned_dispensing_sites = 0
    dispensing_last_paid = 0
    dispensing_total_paid = 0

    free_dispensing_data = []
    active_dispensing_data = []
    inactive_dispensing_data = []

    if request.method == 'GET':

        if request.user.is_supervisor or request.user.is_operator:
            response = {"Response": {
                "Status": "error"},
                "message": "You({user}) are not authorized to view this page".format(user=request.user)
            }
            return JsonResponse(response, safe=False, status=status.HTTP_403_FORBIDDEN)

        subscription = Subscription.objects.filter(company_id=request.user.company_id).order_by('-created')
        for subs in subscription.values():

            single_subscription = Subscription.objects.get(id=subs["id"])
            valid_till = datetime.strptime(str(subs["valid_till"]), "%Y-%m-%d")
            present_date = datetime.now()
            logger.info("present_date - {}".format(present_date))
            logger.info("valid_till - {}".format(valid_till))

            daysleft = (valid_till - present_date).days
            logger.info("days left {}".format(daysleft))
            single_subscription.days_to_expire = daysleft
            if daysleft <= 0:
                single_subscription.expired = True
            single_subscription.save()

            try:
                site_obj = Site.objects.get(id=subs["site_id"])
                site_name = site_obj.site_name
            except Exception as e:
                site_name = ""

            if subs["is_treatment_unit"]:
                logger.info("\nsubscription - {}".format(subs["id"]))

                total_treatment_sites += 1
                treatment_total_paid += subs["total_paid"]

                logger.info("subscription_code - {}".format(subs["subscription_code"]))
                valid_till = datetime.strptime(str(subs["valid_till"]), "%Y-%m-%d")
                present_date = datetime.now()
                logger.info("present_date - {}".format(present_date))
                logger.info("valid_till - {}".format(valid_till))

                # daysleft = (valid_till - present_date).days
                # logger.info("days left {}".format(daysleft))

                if subs["subscription_code"] is None and not subs["expired"]:
                    free_treatment_sites += 1
                    logger.info("subscription code is none and hence its free site")
                    free_treatment_resp = {
                        'subscription_id': subs["id"],
                        'site_id': subs["site_id"] if subs["site_id"] else None,
                        'site_name': site_name if site_name else "",
                        'subscription_type': "Treatment Unit",
                        'start_date': subs["created"],
                        "valid_till": subs["valid_till"],
                        "days_to_expire": subs["days_to_expire"],
                    }
                    free_treatment_data.append(free_treatment_resp)
                elif subs["subscription_code"] is not None and not subs["expired"]:
                    logger.info("subscription is valid and hence its assigned site")
                    assigned_treatment_sites += 1
                    active_treatment_resp = {
                        'subscription_id': subs["id"],
                        'site_id': subs["site_id"] if subs["site_id"] else None,
                        'site_name': site_name if site_name else "",
                        'subscription_type': "Treatment Unit",
                        'start_date': subs["created"],
                        "valid_till": subs["valid_till"],
                        "days_to_expire": subs["days_to_expire"],
                    }
                    active_treatment_data.append(active_treatment_resp)
                elif subs["expired"]:
                    logger.info("subscription is expired and hence its unassigned site")
                    unassigned_treatment_sites += 1
                    inactive_treatment_resp = {
                        'subscription_id': subs["id"],
                        'site_id': subs["site_id"] if subs["site_id"] else None,
                        'site_name': site_name if site_name else "",
                        'subscription_type': "Treatment Unit",
                        'start_date': subs["created"],
                        "valid_till": subs["valid_till"],
                        "days_to_expire": subs["days_to_expire"],
                    }
                    inactive_treatment_data.append(inactive_treatment_resp)

            elif subs["is_dispensing_unit"]:
                logger.info("subscription - {}".format(subs["id"]))

                total_dispensing_sites += 1
                dispensing_total_paid += subs["total_paid"]

                logger.info("subscription_code - {}".format(subs["subscription_code"]))
                valid_till = datetime.strptime(str(subs["valid_till"]), "%Y-%m-%d")
                present_date = datetime.now()
                logger.info("present_date - {}".format(present_date))
                logger.info("valid_till - {}".format(valid_till))

                if subs["subscription_code"] is None and not subs["expired"]:
                    free_dispensing_sites += 1
                    free_dispensing_resp = {
                        'subscription_id': subs["id"],
                        'site_id': subs["site_id"],
                        'site_name': site_name,
                        'subscription_type': "Dispensing Unit",
                        'start_date': subs["created"],
                        "valid_till": subs["valid_till"],
                        "days_to_expire": subs["days_to_expire"],
                    }
                    free_dispensing_data.append(free_dispensing_resp)
                elif subs["subscription_code"] is not None and not subs["expired"]:
                    logger.info("subscription is valid and hence its assigned site")
                    assigned_dispensing_sites += 1
                    active_dispensing_resp = {
                        'subscription_id': subs["id"],
                        'site_id': subs["site_id"],
                        'site_name': site_name,
                        'subscription_type': "Dispensing Unit",
                        'start_date': subs["created"],
                        "valid_till": subs["valid_till"],
                        "days_to_expire": subs["days_to_expire"],
                    }
                    active_dispensing_data.append(active_dispensing_resp)
                elif subs["expired"]:
                    logger.info("subscription is expired and hence its unassigned site")
                    unassigned_dispensing_sites += 1
                    inactive_dispensing_resp = {
                        'subscription_id': subs["id"],
                        'site_id': subs["site_id"],
                        'site_name': site_name,
                        'subscription_type': "Dispensing Unit",
                        'start_date': subs["created"],
                        "valid_till": subs["valid_till"],
                        "days_to_expire": subs["days_to_expire"],
                    }
                    inactive_dispensing_data.append(inactive_dispensing_resp)

        treatment_per_price = 0
        treatment_per_tax = 0
        dispensing_per_price = 0
        dispensing_per_tax = 0

        price = Price.objects.all()
        if price:
            for per_rate in price.values():
                treatment_per_price = per_rate["treatment_price"]
                treatment_per_tax = per_rate["treatment_tax"]
                dispensing_per_price = per_rate["dispensing_price"]
                dispensing_per_tax = per_rate["dispensing_tax"]

        resp = {
            'serial_no': 1,
            'subscription_category': "Treatment Unit",
            'no_of_sites': total_treatment_sites,
            'no_of_free_sites': free_treatment_sites,
            'no_of_active_sites': assigned_treatment_sites,
            'no_of_inactive_sites': unassigned_treatment_sites,
            "treatment_per_price": treatment_per_price,
            "treatment_per_tax": treatment_per_tax,
            'last_paid': treatment_last_paid,
            'total_paid': treatment_total_paid,
            "free_sites": free_treatment_data,
            "active_sites": active_treatment_data,
            "inactive_sites": inactive_treatment_data
        }
        summary_data.append(resp)
        resp = {
            'serial_no': 2,
            'subscription_category': "Dispensing Unit",
            'no_of_sites': total_dispensing_sites,
            'no_of_free_sites': free_dispensing_sites,
            'no_of_active_sites': assigned_dispensing_sites,
            'no_of_inactive_sites': unassigned_dispensing_sites,
            "dispensing_per_price": dispensing_per_price,
            "dispensing_per_tax": dispensing_per_tax,
            'last_paid': dispensing_last_paid,
            'total_paid': dispensing_total_paid,
            "free_sites": free_dispensing_data,
            "active_sites": active_dispensing_data,
            "inactive_sites": inactive_dispensing_data
        }
        summary_data.append(resp)

        logger.info("Data\n\n{}".format(summary_data))
        return JsonResponse(
            {"Response": {
                "Status": "success"
            },
                "Data": summary_data
            }, safe=False, status=status.HTTP_200_OK)


@api_view(['GET'])
def sites_under_subscription(request, id):
    data = []
    if request.method == 'GET':

        if id == 1:
            subscription = Subscription.objects.filter(company_id=request.user.company_id).\
                filter(is_treatment_unit=True)
        elif id == 2:
            subscription = Subscription.objects.filter(company_id=request.user.company_id).\
                filter(is_dispensing_unit=True)
        else:
            return JsonResponse(
                {"Response": {
                    "Status": "error"
                },
                    "message": "Invalid subscription type"
                }, safe=False, status=status.HTTP_200_OK)

        for subs in subscription.values():

            single_subscription = Subscription.objects.get(id=subs["id"])
            valid_till = datetime.strptime(str(subs["valid_till"]), "%Y-%m-%d")
            present_date = datetime.now()
            logger.info("present_date - {}".format(present_date))
            logger.info("valid_till - {}".format(valid_till))

            daysleft = (valid_till - present_date).days
            logger.info("days left {}".format(daysleft))
            single_subscription.days_to_expire = daysleft
            single_subscription.save()

            site_dat = Site.objects.get(id=subs["site_id"])
            subscription_status = ""
            if subs["subscription_code"] is None and not subs["expired"]:
                subscription_status = "free"
            elif subs["subscription_code"] is not None and not subs["expired"]:
                subscription_status = "active"
            elif subs["expired"]:
                subscription_status = "inactive"

            subscription_type = ""
            per_price = 0
            per_tax = 0
            if subs["is_treatment_unit"]:
                subscription_type = "Treatment Unit"
                price = Price.objects.all()
                if price:
                    for per_rate in price.values():
                        per_price = per_rate["treatment_price"]
                        per_tax = per_rate["treatment_tax"]
            elif subs["is_dispensing_unit"]:
                subscription_type = "Dispensing Unit"
                price = Price.objects.all()
                if price:
                    for per_rate in price.values():
                        per_price = per_rate["dispensing_price"]
                        per_tax = per_rate["dispensing_tax"]

            resp = {"site_license": {
                'serial_no': subs["id"],
                "subscription_type": subscription_type,
                'site_name': site_dat.site_name,
                'start_date': subs["created"],
                "valid_till": subs["valid_till"],
                "days_to_expire": daysleft,
                "data_transfer_volume": subs["data_transfer_volume"],
                "no_of_actions": subs["no_of_actions"],
                "status": subscription_status,
                "per_price": per_price,
                "per_tax": per_tax
            },
                "payment_details": {
                    "date_time": datetime.now(),
                    "amount": subs["total_paid"],
                    "subscription_confirmation": "success"
                }
            }

            logger.info(resp)
            data.append(resp)

        # # sites_list = {"site_licenses": da}
        # treatment_per_price = 0
        # treatment_per_tax = 0
        # dispensing_per_price = 0
        # dispensing_per_tax = 0
        #
        # price = Price.objects.all()
        # if price:
        #     for per_rate in price.values():
        #         treatment_per_price = per_rate["treatment_price"]
        #         treatment_per_tax = per_rate["treatment_tax"]
        #         dispensing_per_price = per_rate["dispensing_price"]
        #         dispensing_per_tax = per_rate["dispensing_tax"]
        #
        # price_details = {
        #     "treatment_per_price": treatment_per_price,
        #     "treatment_per_tax": treatment_per_tax,
        #     "dispensing_per_price": dispensing_per_price,
        #     "dispensing_per_tax": dispensing_per_tax
        #
        # }
        # data.append(price_details)

        return JsonResponse(
            {"Response": {
                "Status": "success"
            },
                "Data": data
            }, safe=False, status=status.HTTP_200_OK)


# TODO list sites and subscriptions that has free subscription or unassigned subscriptions inorder to assign from
#  frontend
@api_view(['GET'])
def list_free_or_unassigned_sites(request):
    data = []
    if request.method == 'GET':
        # TODO if null subs available & not have any free subs then create new subs to null subs with
        #  expiry date set to 365 days
        #  if null subs available & found 1 ore more free subs then ask for transfer of subs and return a flag

        if Subscription.objects.filter(subscription_code__isnull=True).count() >= 1:
            if Subscription.objects.filter(subscription_code__isnull=False).filter(days_to_expire__gte=1).count() >= 1:
                logger.info("Found one ore more valid(available) subscriptions so ask user for subscription transfer "
                      "and send null subscription list and valid subscription list")
                single_subscription = Subscription.objects.filter(Q(days_to_expire__lt=0) | Q(subscription_code__isnull=True))
                for subs in single_subscription.values():
                    # single_subscription = Subscription.objects.get(id=subs["id"])
                    site_dat = Site.objects.get(id=subs["site_id"])
                    subscription_type = "Treatment unit" if site_dat.is_treatment_unit else "Dispensing unit"
                    resp = {
                        'subscription_serial_no': subs["id"],
                        'site_serial_no': site_dat.id,
                        'site_name': site_dat.site_name,
                        'subscription_type': subscription_type,
                        'start_date': subs["created"],
                        "valid_till": subs["valid_till"],
                        "days_to_expire": subs["days_to_expire"],
                    }
                    logger.info(resp)
                    data.append(resp)
                # TODO add list of valid subs
                # single_subscription = Subscription.objects.filter(Q(days_to_expire__lt=0) | Q(subscription_code__isnull=True))
                # for subs in single_subscription.values():
                #     # single_subscription = Subscription.objects.get(id=subs["id"])
                #     site_dat = Site.objects.get(id=subs["site_id"])
                #     subscription_type = "Treatment unit" if site_dat.is_treatment_unit else "Dispensing unit"
                #     resp = {
                #         'subscription_serial_no': subs["id"],
                #         'site_serial_no': site_dat.id,
                #         'site_name': site_dat.site_name,
                #         'subscription_type': subscription_type,
                #         'start_date': subs["created"],
                #         "valid_till": subs["valid_till"],
                #         "days_to_expire": subs["days_to_expire"],
                #     }
                #     logger.info(resp)
                #     data.append(resp)
                #  set transfer flag true
                context = {"free_sites": data, "transfer": True}
                return JsonResponse(
                    {"Response": {
                        "Status": "success"
                    },
                        "Data": context
                    }, safe=False, status=status.HTTP_200_OK)
            else:
                logger.info("Couldn't find any valid(available) subscription so create new subscription for "
                      "the given free sites")
                single_subscription = Subscription.objects.filter(
                    Q(days_to_expire__lt=0) | Q(subscription_code__isnull=True))
                for subs in single_subscription.values():
                    # single_subscription = Subscription.objects.get(id=subs["id"])
                    site_dat = Site.objects.get(id=subs["site_id"])
                    subscription_type = "Treatment unit" if site_dat.is_treatment_unit else "Dispensing unit"
                    resp = {
                        'subscription_serial_no': subs["id"],
                        'site_serial_no': site_dat.id,
                        'site_name': site_dat.site_name,
                        'subscription_type': subscription_type,
                        'start_date': subs["created"],
                        "valid_till": subs["valid_till"],
                        "days_to_expire": subs["days_to_expire"],
                    }
                    # logger.info(resp)
                    data.append(resp)
                logger.info(data)
                # TODO set transfer flag false
                context = {"free_sites": data, "transfer": False}
                return JsonResponse(
                    {"Response": {
                        "Status": "success"
                    },
                        "Data": context
                    }, safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse(
                {"Response": {
                    "Status": "error"
                },
                    "message": "Couldn't find any free sites"
                }, safe=False, status=status.HTTP_200_OK)

    else:
        return JsonResponse(
            {"Response": {"Status": "error"}, "message": "Invalid request"},
            safe=False, status=status.HTTP_400_BAD_REQUEST)


# {"free_subs": [
#                 {
#                     "subscription_serial_no": 20,
#                     "site_serial_no": 14,
#                     "site_name": "Site5",
#                     "subscription_type": "Dispensing unit",
#                     "start_date": "2022-09-05",
#                     "valid_till": "2022-10-05",
#                     "days_to_expire": 28
#                 },
#                 {
#                     "subscription_serial_no": 21,
#                     "site_serial_no": 15,
#                     "site_name": "Site6",
#                     "subscription_type": "Treatment unit",
#                     "start_date": "2022-09-05",
#                     "valid_till": "2022-10-05",
#                     "days_to_expire": 28
#                 }
#             ]}

@api_view(['POST'])
def add_sub(request):
    if request.method == 'POST':
        no_of_sites = request.data['no_of_sites']
        sub_sites = request.data['sub_sites']
        subscription_type = request.data['subscription_type']
        total_cost = request.data['total_cost']
        tax_amount = request.data['tax_amount']
        total_amount = request.data['total_amount']

        logger.info(no_of_sites)
        logger.info(sub_sites)
        logger.info(subscription_type)
        for sub_site in sub_sites:
            sub_detail = sub_site.split(",")
            logger.info(sub_detail)
            existing_sub = Subscription.objects.get(id=sub_detail[1])
            # print(existing_sub)
            start_date = datetime.today().date()
            end_date = start_date + timedelta(days=365)
            subscription_code = "{}_{}_{}_{}".format(request.user.company.id, sub_detail[1],
                                                     start_date, end_date)
            logger.info(subscription_code)
            existing_sub.subscription_code = subscription_code
            existing_sub.created = start_date
            existing_sub.valid_till = end_date
            existing_sub.days_to_expire = 365
            existing_sub.site_id = sub_detail[0]
            existing_sub.total_paid = total_cost/no_of_sites
            existing_sub.save()

                # existing_sub.subscription_code = "{}_{}_{}".format(request.user.company.id, start_date, end_date)
            # no_of_sites = request.data['no_of_sites']
            # total_cost = request.data['total_cost']
            # tax_amount = request.data['tax_amount']
            # total_amount = request.data['total_amount']
            #
            # subscription = Subscription()
            # if str(subscription_type).lower() == "treatment unit":
            #     subscription.is_treatment_unit = True
            # elif str(subscription_type).lower() == "dispensing unit":
            #     subscription.is_dispensing_unit = True
            #
            # subscription.no_of_sites = no_of_sites
            # subscription.total_cost = total_cost
            # # subscription.tax_amount = tax_amount
            # subscription.total_paid = total_amount
            # subscription.save()

            # TODO get site type from mqtt after authentication
            # site_type = "Treatment"
            # subscription_type = site_type
            #
            # if site_type == "Dispensing":
            #     site_dat.is_dispensing_unit = True
            # elif site_type == "Treatment":
            #     site_dat.is_treatment_unit = True
            #
            # site_dat.save()
            #
            # site_obj = Site.objects.get(site_name=site_name)
            #
            # subscription_data = Subscription()
            # subscription_data.site = site_obj
            # if str(subscription_type).lower() == "treatment":
            #     subscription_data.is_treatment_unit = True
            # elif str(subscription_type).lower() == "dispensing":
            #     subscription_data.is_dispensing_unit = True
            #
            # subscription_data.save()

        # no_of_sites = request.data['no_of_sites']
        # no_of_sites = request.data['no_of_sites']

        # TODO check no of sites == no of subs else return cannot add subs more than sites
        # TODO check if the subscription category and sites types match
        # TODO if true then add a unique subscription code with format companyname_startdate_enddate
        # free_subscription = request.data['free_subs']
        # for subs in free_subscription:
        #     logger.info(subs)
        #     existing_sub = Subscription.objects.get(id=subs["subscription_serial_no"])
        #     start_date = datetime.today().date()
        #     end_date = start_date + timedelta(days=365)
        #     subscription_code = "{}_{}_{}_{}".format(request.user.company.id, subs["subscription_serial_no"],
        #                                              start_date, end_date)
        #     logger.info(subscription_code)
        #     existing_sub.subscription_code = subscription_code
        #     existing_sub.created = start_date
        #     existing_sub.valid_till = end_date
        #     existing_sub.days_to_expire = 365
        #     # existing_sub.site_id = site_id
        #     existing_sub.save()
        #     # existing_sub.subscription_code = "{}_{}_{}".format(request.user.company.id, start_date, end_date)
        # # no_of_sites = request.data['no_of_sites']
        # # total_cost = request.data['total_cost']
        # # tax_amount = request.data['tax_amount']
        # # total_amount = request.data['total_amount']
        # #
        # # subscription = Subscription()
        # # if str(subscription_type).lower() == "treatment unit":
        # #     subscription.is_treatment_unit = True
        # # elif str(subscription_type).lower() == "dispensing unit":
        # #     subscription.is_dispensing_unit = True
        # #
        # # subscription.no_of_sites = no_of_sites
        # # subscription.total_cost = total_cost
        # # # subscription.tax_amount = tax_amount
        # # subscription.total_paid = total_amount
        # # subscription.save()
        #
        # # TODO get site type from mqtt after authentication
        # # site_type = "Treatment"
        # # subscription_type = site_type
        # #
        # # if site_type == "Dispensing":
        # #     site_dat.is_dispensing_unit = True
        # # elif site_type == "Treatment":
        # #     site_dat.is_treatment_unit = True
        # #
        # # site_dat.save()
        # #
        # # site_obj = Site.objects.get(site_name=site_name)
        # #
        # # subscription_data = Subscription()
        # # subscription_data.site = site_obj
        # # if str(subscription_type).lower() == "treatment":
        # #     subscription_data.is_treatment_unit = True
        # # elif str(subscription_type).lower() == "dispensing":
        # #     subscription_data.is_dispensing_unit = True
        # #
        # # subscription_data.save()

        return JsonResponse(
                            {"Response": {
                                "Status": "success"
                            },
                                "message": "added subscription details"
                            }, safe=False, status=status.HTTP_200_OK)
    return JsonResponse(
        {"Response": {
            "Status": "error"
        },
            "message": "Invalid request"
        }, safe=False, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def renew_sub(request, sub_id):
    logger.info("Subscription renew request came for subscription id {}".format(sub_id))
    if request.method == 'POST':
        no_of_sites = request.data['no_of_sites']
        site_name = request.data['site_name']
        subscription_type = request.data['sub_type']
        total_cost = request.data['total_cost']
        tax_amount = request.data['tax_amount']
        total_amount = request.data['total_amount']

        logger.info("no_of_sites {}".format(no_of_sites))
        logger.info("site_name {}".format(site_name))
        logger.info("subscription_type {}".format(subscription_type))

        existing_sub = Subscription.objects.get(id=sub_id)
        if existing_sub.expired:
            logger.info("Selected subscription expired hence renewing")
            # print(existing_sub)
            start_date = datetime.today().date()
            end_date = start_date + timedelta(days=365)
            subscription_code = "{}_{}_{}_{}".format(request.user.company.id, sub_id,
                                                     start_date, end_date)
            logger.info("New subscription code {}".format(subscription_code))
            existing_sub.subscription_code = subscription_code
            existing_sub.created = start_date
            existing_sub.valid_till = end_date
            existing_sub.days_to_expire = 365
            existing_sub.expired = False
            existing_sub.site_id = Site.objects.get(company_id=request.user.company_id, site_name=site_name)
            existing_sub.total_paid = total_amount
            existing_sub.save()

            return JsonResponse(
                                {"Response": {
                                    "Status": "success"
                                },
                                    "message": "Subscription renewed successfully"
                                }, safe=False, status=status.HTTP_200_OK)
        else:
            logger.info("Selected subscription didn't expire hence not renewing")
            return JsonResponse(
                {"Response": {
                    "Status": "error"
                },
                    "message": "Selected subscription didn't expire"
                }, safe=False, status=status.HTTP_200_OK)
    return JsonResponse(
        {"Response": {
            "Status": "error"
        },
            "message": "Invalid request"
        }, safe=False, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def add_sub(request):
#     if request.method == 'POST':
#         # TODO check if the subscription category and sites types match
#         # TODO if true then add a unique subscription code with format companyname_startdate_enddate
#         subscription_type = request.data['subscription_type']
#         no_of_sites = request.data['no_of_sites']
#         total_cost = request.data['total_cost']
#         tax_amount = request.data['tax_amount']
#         total_amount = request.data['total_amount']
#
#         subscription = Subscription()
#         if str(subscription_type).lower() == "treatment unit":
#             subscription.is_treatment_unit = True
#         elif str(subscription_type).lower() == "dispensing unit":
#             subscription.is_dispensing_unit = True
#
#         subscription.no_of_sites = no_of_sites
#         subscription.total_cost = total_cost
#         # subscription.tax_amount = tax_amount
#         subscription.total_paid = total_amount
#         subscription.save()
#
#         # TODO get site type from mqtt after authentication
#         # site_type = "Treatment"
#         # subscription_type = site_type
#         #
#         # if site_type == "Dispensing":
#         #     site_dat.is_dispensing_unit = True
#         # elif site_type == "Treatment":
#         #     site_dat.is_treatment_unit = True
#         #
#         # site_dat.save()
#         #
#         # site_obj = Site.objects.get(site_name=site_name)
#         #
#         # subscription_data = Subscription()
#         # subscription_data.site = site_obj
#         # if str(subscription_type).lower() == "treatment":
#         #     subscription_data.is_treatment_unit = True
#         # elif str(subscription_type).lower() == "dispensing":
#         #     subscription_data.is_dispensing_unit = True
#         #
#         # subscription_data.save()
#
#         return JsonResponse(
#                             {"Response": {
#                                 "Status": "success"
#                             },
#                                 "message": "added subscription details"
#                             }, safe=False, status=status.HTTP_200_OK)
#     return JsonResponse(
#         {"Response": {
#             "Status": "error"
#         },
#             "message": "Invalid request"
#         }, safe=False, status=status.HTTP_400_BAD_REQUEST)

# TODO
# @api_view(['GET'])
# def filter_sites_by_name(request, site_name):
#     logger.info(site_name)
#     site_dat = Site.objects.filter(id=site_name)
#     if site_dat.count() < 1:
#         return JsonResponse({'message': 'The site does not exist'}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         tutorials = Site.objects.all()
#
#         title = request.GET.get('title', None)
#         if title is not None:
#             tutorials = tutorials.filter(title__icontains=title)
#
#         tutorials_serializer = SiteSerializer(tutorials, many=True)
#         return JsonResponse(tutorials_serializer.data, safe=False)
#
#
#
#
# @api_view(['GET'])
# def filter_sites_by_date(request, created_date):
#     if request.method == 'GET':
#         tutorials = Site.objects.all()
#
#         title = request.GET.get('title', None)
#         if title is not None:
#             tutorials = tutorials.filter(title__icontains=title)
#
#         tutorials_serializer = SiteSerializer(tutorials, many=True)
#         return JsonResponse(tutorials_serializer.data, safe=False)


def get_logfile_data(filename, lines, count, n):
    with open(filename) as file:
        for line in file:
            line = line.strip()  # or some other preprocessing
            lines.append(line)  # storing everything in memory!
            if "continued from:" in line:
                oldfile = line.split(':')[2]
                get_logfile_data(oldfile, lines, count, n)
            count += 1
            if count > n:
                lines.append("...")
                return lines
    return lines


def get_logfile(n=1000):
    lines = []
    count = 0
    return get_logfile_data(LOG_FILE_LOCATION, lines, count, n)


@api_view(['GET'])
def get_log(request, n):
    return JsonResponse(get_logfile(n), safe=False)
