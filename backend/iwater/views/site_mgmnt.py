import json
import re
import threading
from connection.alpn_mqtt import *
from datetime import datetime

import random
from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework import status
from django.db import transaction
from django.db.models import Q

from django.contrib.sites.shortcuts import get_current_site
import paho.mqtt.client as mqtt

from .signup_mgmnt import user_login
from iwater.models import Site, User, SitePermission, Device, Subscription, ArchiveSite, ArchiveDevice, ArchiveSitePermission,Company
from init_water_app import settings
from init_water_app.settings import OTP_VALID_FOR
from iwater.iw_logger import logger
from connection.models import device_info
from connection.views import MqttClient,mqttc
token_=0
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
        #                 "Device 1",
        #                 "Device 2",
        #                 "Device 3"
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
            # ! access permission check 
            response = {"Response": {
                "Status": "error"},
                "message": "You({user}) are not authorized to view this page".format(user=request.user)
            }
            return JsonResponse(response, safe=False, status=status.HTTP_403_FORBIDDEN)

        authenticated_devices = {}

        site_obj = Site.objects.filter(company_id=request.user.company_id).filter(phone_verified=1).order_by('-id')
        # ! collects model instance of site object where phone 

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

            users = {
                "supervisors": supervisors,
                "operators": operators
            }

            devices = {}
            device_obj = Device.objects.filter(site_id=site_info["id"])
            for dev in device_obj.values():
                devices = {
                    "device_name": [
                        "Device 1",
                        "Device 2",
                        "Device 3"
                    ],
                    "device_serial_number": [
                        dev["serial_no1"],
                        dev["serial_no2"],
                        dev["serial_no3"]
                    ],
                }
                if dev["serial_no2"] and dev["serial_no3"]:
                    authenticated_devices = {"authenticated_devices": {
                        "treatment_unit": dev["serial_no2"],
                        "dispensing_unit": dev["serial_no3"]}
                    }
                elif dev["serial_no2"]:
                    authenticated_devices = {"authenticated_devices": {
                        "treatment_unit": dev["serial_no2"]}
                    }
                elif dev["serial_no3"]:
                    authenticated_devices = {"authenticated_devices": {
                        "dispensing_unit": dev["serial_no3"]}
                    }
            response_data = {}
            # if users["supervisors"] or users["operators"]:
            if True: #change by bharti ma'am
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
                response_data.update(authenticated_devices)
            else:
                # ! if users are not added to the site site goes to unverified

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
                response_data.update(authenticated_devices)

            city_state.append(site_info["city"])
            city_state.append(site_info["state"])

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
            # ! sets site permission
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

            users = {
                "supervisors": supervisors,
                "operators": operators
            }

            devices = {}
            device_obj = Device.objects.filter(site_id=site_info["id"])
            for dev in device_obj.values():
                devices = {
                    "device_name": [
                        "Device 1",
                        "Device 2",
                        "Device 3"
                    ],
                    "device_serial_number": [
                        dev["serial_no1"],
                        dev["serial_no2"],
                        dev["serial_no3"]
                    ],
                }

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
            context.append(response_data)

      
        return JsonResponse({"Response": {"Status": "success"}, "Data": context},
                            safe=False, status=status.HTTP_200_OK)
    return JsonResponse({"Response": {"Status": "success"}, "Data": "Bad request"},
                        safe=False, status=status.HTTP_400_BAD_REQUEST)


# @login_required
@api_view(['POST'])
def send_otp(request):

    not_verified_sites = Site.objects.filter(token_verified=False)
    not_verified_sites_phone = Site.objects.filter(phone_verified=False)
    # ! defination of unverified sites collects model instance

    for not_verified_site in not_verified_sites.values():
        logger.debug("unverified site {}: {}".format(not_verified_site["id"], not_verified_site["site_name"]))
        otp_cache_time = not_verified_site["otp_created"].replace(tzinfo=None)
        current_time = datetime.today().replace(tzinfo=None)
        difference = (current_time - otp_cache_time).total_seconds()
        if difference > OTP_VALID_FOR:
            logger.info("Deleting timed out unverified site {}: {}".format(not_verified_site["id"],
                                                                           not_verified_site["site_name"]))
            Site.objects.filter(id=not_verified_site["id"]).delete()
            logger.info("Deleted timed out unverified site {}: {}".format(not_verified_site["id"],
                                                                          not_verified_site["site_name"]))


    for not_verified_site_p in not_verified_sites_phone.values():
        logger.debug("unverified site {}: {}".format(not_verified_site_p["id"], not_verified_site_p["site_name"]))
        otp_cache_time_p = not_verified_site_p["otp_created"].replace(tzinfo=None)
        current_time_p = datetime.today().replace(tzinfo=None)
        difference_p = (current_time_p - otp_cache_time_p).total_seconds()
        if difference_p > 1800:
            logger.info("Deleting timed out unverified site {}: {}".format(not_verified_site_p["id"],
                                                                           not_verified_site_p["site_name"]))
            Site.objects.filter(id=not_verified_site_p["id"]).delete()
            logger.info("Deleted timed out unverified site {}: {}".format(not_verified_site_p["id"],
                                                                          not_verified_site_p["site_name"]))


    # Request to send verification sms
    if request.method == 'POST':
        # phone = request.data['phone']
        # site_name = request.data['site_name']
        print("send_otp request", request)
        print("send_otp request data", request.data)
        site_name = request.data['site_name']
        address = request.data['address']
        city = request.data['city']
        state = request.data['state']
        user_obj = request.data['user']
        
        phone_country = "+91"
        mob = re.sub(r"\D", "", request.data['phone'])
        site_mob = phone_country + str(mob)
        try:
            existing_site = Site.objects.get(company_id=int(user_obj['company_id']), site_name=site_name)
            # ! checks for duplication of site name
            if existing_site.token_verified and existing_site.phone_verified and existing_site.is_dispensing_unit and existing_site.is_treatment_unit:
                response = {"Response": {
                    "Status": "error"},
                    "message": "The site name is already used"
                }
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
         
        except Exception as e :
            print("Exception at line 387",e)  

        with transaction.atomic():
            try:
                site_obj = Site.objects.filter(company_id=int(user_obj['company_id']), site_name=site_name)
                site_obj_count = site_obj.count()
                if site_obj_count > 0:
                    site_obj.site_name = site_name
                    site_obj.address = address
                    site_obj.city = city
                    site_obj.state = state
                    site_obj.phone = site_mob
                    site_obj.company = request.user.company
                    site_obj.save()
                    logger.error("site {} already exists".format(site_name))

                else:  
                    site_data = Site()
                    site_data.site_name = site_name
                    site_data.address = address
                    site_data.city = city
                    site_data.state = state
                    site_data.phone = site_mob
                    site_data.company = request.user.company
                    site_data.save()
            
            except Exception as err:
                transaction.set_rollback(True)
                logger.error("Error in adding site details; {}".format(err))
                return JsonResponse({"Response": {"Status": "error"},
                                     "message": "Data base write error for site details"},
                                    safe=False, status=status.HTTP_200_OK)

        try:
            site_obj = Site.objects.get(company_id=request.user.company_id, site_name=site_name)

            # if str(TimestampSigner().unsign(code, max_age=7200)) == str(request.user.id):
            if not site_mob:
                return JsonResponse({"Response": {"Status": "error"}, "message": "No phone number is provided"},
                                    safe=False, status=status.HTTP_200_OK)
                # return HttpResponse('No phone number is provided', status=400)

        
            if site_obj.phone_verified and site_obj.token_verified and site_obj.is_treatment_unit and site_obj.is_dispensing_unit:
                return JsonResponse({"Response": {"Status": "error"},
                                     "message": "Site is already verified"},  # Site is already verified
                                    # Site name is already taken
                                    safe=False, status=status.HTTP_200_OK)
            else:
                site_obj.phone_verified = False
                logger.info("Both OTP and token are not verified hence resending the otp")
                sent = site_obj.send_verification_sms(random.randint(1000, 9999))
                logger.info("otp sent")
            if sent["status"]:
                return JsonResponse({"Response": {"Status": "success"},
                                     "message": "OTP sent to the registered number",
                                     "valid_for": OTP_VALID_FOR,
                                     "otp": {"token": site_obj.token, "otp": sent["otp"]}  # TODO remove
                                     },
                                    safe=False, status=status.HTTP_200_OK)
            return JsonResponse({"Response": {"Status": "error"},
                                 "message": "SMS sendings failed"},
                                safe=False, status=status.HTTP_200_OK)
        except Exception as err:
            return JsonResponse({"Response": {"Status": "error"},
                                 "message": "Invalid verification request; {}".format(err)},
                                safe=False, status=status.HTTP_200_OK)


# client = MqttClient()
def connect_mqtt_in_background(company_id):

    # connect to MQTT
    # client = MqttClient(company_id)
    client = MqttClient(company_id)
    client.publish("my/test/topic", "connected from iw backend app")
    # client.publish("wc/v1/OTP", "connected from iw backend app")
    # client.on_connect = client.on_connect
    # client.on_message = client.on_message
    # mqttc.on_connect = mqttc.on_connect
    # mqttc.on_message = mqttc.on_message



@api_view(['POST'])
def verify_otp(request):

    if request.method == 'POST':
        code = request.data['otpnumber']
        site_name = request.data['site_name']
        user_obj = request.data['user']
        try:
            site_obj = Site.objects.get(company_id=user_obj['company_id'], site_name=site_name)
            if not site_obj.phone:
                return JsonResponse({"Response": {"Status": "error"},
                                     "message": "Verification failed. No phone number is provided"},
                                    safe=False, status=status.HTTP_200_OK)

            if site_obj.verify_phone(code)["status"]:
                return JsonResponse({"Response": {"Status": "success"},
                                     "message": "OTP verified successfully"},
                                    safe=False, status=status.HTTP_200_OK)
                # while site_obj.verify_phone(code)["difference"] < OTP_VALID_FOR:
                #     try:
                #         sub_count = Subscription.objects.filter(site_id=site_obj.id).count()
                #         logger.debug(sub_count)
                #         if sub_count > 0:
                #             dev_obj = Device.objects.get(site_id=site_obj.id)
                #             response = {
                #                 'device_name1': dev_obj.device_name1,
                #                 "device_name2": dev_obj.device_name2,
                #                 "device_name3": dev_obj.device_name3
                #             }
                #             logger.info(response)
                #             return JsonResponse({"Response": {"Status": "success"},
                #                                  "message": "Verified both OTP and token"},
                #                                 safe=False, status=status.HTTP_200_OK)
                #     except Exception as err:
                #         pass

            logger.info("Verification failed. Invalid otp or otp expired or didn't get the token from the device")
            return JsonResponse({"Response": {"Status": "error"},
                                 "message": "Verification failed. Invalid or expired OTP"},
                                safe=False, status=status.HTTP_200_OK)
        except Site.DoesNotExist as err:
            return JsonResponse({"Response": {"Status": "error"},
                                 "message": "Couldn't find the requested site, {}".format(err)},
                                safe=False, status=status.HTTP_200_OK)


@api_view(['POST'])
def verify_token(request):

    if request.method == 'POST':
        site_name = request.data['site_name']
        user_obj = request.data['user']
        # try:
        #     authenticate_device = request.data['authenticate_device']
        # except Exception as err:
        #     authenticate_device = None

        # if authenticate_device is None:
    
        try:
            site_obj = Site.objects.get(company_id=user_obj['company_id'], site_name=site_name, phone_verified=True)

        except Exception as err:
            logger.error("Verify token error , {}".format(err))
            return JsonResponse({"Response": {"Status": "error"},
                                    "message": "OTP is not verified"},
                                safe=False, status=status.HTTP_200_OK)
        try:
            sub_count = Subscription.objects.filter(site_id=site_obj.id).count()
            if sub_count > 0:
                dev_obj = Device.objects.get(site_id=site_obj.id)
                response = {
                    'device_name1': dev_obj.serial_no1,
                    "device_name2": dev_obj.serial_no2,
                    "device_name3": dev_obj.serial_no3
                }
                site_obj.token_verified = True
                site_obj.otp = None
                site_obj.save()

                #mongodb device information
                try:

                    records_panel = [
                    {
                    "Device_id": dev_obj.serial_no2,
                    "Device_name": "wc",
                    "unit_type": "water_treatment",
                    "company_id": user_obj['company_id'],
                    "site_name": site_name
                    }
                    ]
                
                    record_atm=[
                    {
                    "Device_id": dev_obj.serial_no3,
                    "Device_name": "wc",
                    "unit_type": "water_dispense",
                    "company_id": user_obj['company_id'],
                    "site_name": site_name
                    }
                    ]
                    records_panel_exist =device_info.objects.find(records_panel)
                    print("records_panel_exist ",records_panel_exist)
                    record_atm_exist =device_info.objects.find(record_atm)
                    print("record_atm_exist ",record_atm_exist)
                    if dev_obj.serial_no2 and dev_obj.serial_no3:
                        
                        if records_panel_exist is None:
                            info=device_info.objects.create(records_panel)
                            info.save()

                        if record_atm_exist is None:
                            info=device_info.objects.create(record_atm)
                            info.save()
                            logger.info("atm records Added")
                        
                    elif dev_obj.serial_no2:
                        if records_panel_exist is None:
                            info=device_info.objects.create(records_panel)
                            info.save()
                            logger.info("panel records Added")
                       
                    elif dev_obj.serial_no3:
                        if record_atm_exist is None:
                            info=device_info.objects.create(record_atm)
                            info.save()
                            logger.info("atm records Added")

                except Exception as err:
                    return JsonResponse({"Response": {"Status": "error"},
                                    "message": "Mongodb Device information write error"
                                            " {}".format(err)}, safe=False, status=status.HTTP_200_OK)
        
                if dev_obj.serial_no2 and dev_obj.serial_no3:

                    return JsonResponse({"Response": {"Status": "success"},
                                            "message": "Both treatment and dispensing units verified successfully!"},
                                        safe=False, status=status.HTTP_200_OK)
                elif dev_obj.serial_no2:
                    return JsonResponse({"Response": {"Status": "success"},
                                            "message": "Treatment unit verified successfully!"},
                                        safe=False, status=status.HTTP_200_OK)
                elif dev_obj.serial_no3:
                    return JsonResponse({"Response": {"Status": "success"},
                                            "message": "Dispensing unit verified successfully!"},
                                        safe=False, status=status.HTTP_200_OK)
            else:
                site_obj.otp = None
                site_obj.save()
                return JsonResponse({"Response": {"Status": "error"},
                                    "message": "1Token verification failed. Didn't get the token from device1"},
                                safe=False, status=status.HTTP_200_OK)
            
        except Exception as err:
            return JsonResponse({"Response": {"Status": "error"},
                                    "message": "Token verification failed, didn't get the device serial numbers over mqtt."
                                            " {}".format(err)}, safe=False, status=status.HTTP_200_OK)
        # else:

        #     try:
        #         site_obj = Site.objects.get(company_id=request.user.company_id, site_name=site_name,
        #                                     phone_verified=True)
        #     except Exception as err:
        #         logger.error("Verify token error , {}".format(err))
        #         return JsonResponse({"Response": {"Status": "error"},
        #                              "message": "OTP is not verified"},
        #                             safe=False, status=status.HTTP_200_OK)
        #     try:
        #         sub_count = Subscription.objects.filter(site_id=site_obj.id).count()
        #         logger.debug(sub_count)
        #         if sub_count > 0:
        #             dev_obj = Device.objects.get(site_id=site_obj.id)
        #             response = {
        #                 'device_name1': dev_obj.serial_no1,
        #                 "device_name2": dev_obj.serial_no2,
        #                 "device_name3": dev_obj.serial_no3
        #             }
        #             site_obj.token_verified = True
        #             site_obj.token = False
        #             site_obj.save()
        #             len_authenticate_device = len(authenticate_device)

        #             if (len_authenticate_device == 2) and (dev_obj.serial_no2 and dev_obj.serial_no3):
        #             # if dev_obj.serial_no2 and dev_obj.serial_no3:
        #                 return JsonResponse({"Response": {"Status": "success"},
        #                                      "message": "Both treatment and dispensing units verified successfully!"},
        #                                     safe=False, status=status.HTTP_200_OK)

        #             elif len_authenticate_device == 1 and authenticate_device[0] == "treatment_unit" and dev_obj.serial_no2:
        #                 return JsonResponse({"Response": {"Status": "success"},
        #                                      "message": "Treatment unit verified successfully!"},
        #                                     safe=False, status=status.HTTP_200_OK)
        #             elif len_authenticate_device == 1 and authenticate_device[0] == "dispensing_unit" and dev_obj.serial_no3:
        #                 return JsonResponse({"Response": {"Status": "success"},
        #                                      "message": "Dispensing unit verified successfully!"},
        #                                     safe=False, status=status.HTTP_200_OK)
        #         return JsonResponse({"Response": {"Status": "error"},
        #                              "message": "2Token verification failed. Didn't get the token from device2"},
        #                             safe=False, status=status.HTTP_200_OK)
        #     except Exception as err:
        #         return JsonResponse({"Response": {"Status": "error"},
        #                              "message": "Token verification failed, didn't get the device serial numbers over mqtt."
        #                                         " {}".format(err)}, safe=False, status=status.HTTP_200_OK)


# @csrf_exempt
@api_view(['PUT'])
def add_site(request):
    # * TODO add checking user permission
    logger.info("requested user is {}".format(request.user))
    if request.user.is_supervisor or request.user.is_operator:

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
                            # ! saving in site_permissions

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


@api_view(['GET'])
def get_device(request, pk):
    logger.info("Got device get for site {}".format(pk))

    # Request to send verification sms
    if request.method == 'GET':

        try:
            device = Device.objects.get(site_id=pk)
            context = {
                "device_id": device.serial_no1,
                "paneld_id": device.serial_no2,
                "atm_id": device.serial_no3
            }

            response = {"Response": {
                "Status": "success"},
                "Data": context
            }
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        except Exception as err:
            logger.error("Error in getting device details {}".format(err))
            return JsonResponse({"Response": {"Status": "error"},
                                 "message": "Error in getting device details"},
                                safe=False, status=status.HTTP_200_OK)
    return JsonResponse({"Response": {"Status": "error"}, "message": "Invalid method"}, safe=False, status=status.HTTP_200_OK)


@api_view(['POST'])
def re_auth_device(request):
    logger.info("Got re_auth_device")
    if request.method == 'POST':
        site_name = request.data['site_name']

        try:
            site_obj = Site.objects.get(company_id=request.user.company_id, site_name=site_name)

            logger.info("Re-auth request for device added")
            # threading.Thread(target=connect_mqtt_in_background, args=(request.user.company_id, )).start()
            sent = site_obj.send_verification_sms(random.randint(1000, 9999))
            logger.info(sent)
            if sent["status"]:
                return JsonResponse({"Response": {"Status": "success"},
                                     "message": "OTP sent to the registered number",
                                     "valid_for": OTP_VALID_FOR,
                                     "otp": {"token": "{0:04}".format(site_obj.id), "otp": sent["otp"]}  # TODO remove
                                     },
                                    safe=False, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"Response": {"Status": "error"},
                                 "message": "phone already verified verified"},
                                safe=False, status=status.HTTP_200_OK)
            # return HttpResponse('Invalid phone number', status=400)
        except Exception as err:
            logger.error("Error in sending re-auth request for device add {}".format(err))
            return JsonResponse({"Response": {"Status": "error"},
                                 "message": "Error in sending re-auth request for device add"},
                                safe=False, status=status.HTTP_200_OK)


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


# @api_view(['GET'])
# def get_free_or_expired_trial_sites(request, pk):
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
#         if site_obj.is_treatment_unit and site_obj.is_dispensing_unit:
#             site_type = "both"
#             logger.info("About to delete site has both units")
#             subs_obj = Subscription.objects.filter(site_id=site_obj.id)
#         elif site_obj.is_treatment_unit:
#             site_type = "treatment unit"
#             subs_obj = Subscription.objects.filter(site_id=site_obj.id, is_treatment_unit=True)
#         else:  # user_info["is_dispensing_unit"]:
#             site_type = "dispensing unit"
#             subs_obj = Subscription.objects.filter(site_id=site_obj.id, is_dispensing_unit=True)
#
#         logger.info("About to delete site is {}".format(site_type))
#
#         # if site has active license
#         #   if found get free or expired licenses sites
#         #   else
#         #   do not allow site delete
#         # if site has no active license give empty response and allow direct delete
#
#         for sub_info in subs_obj.values():
#             # logger.info(sub_info)
#             # if the "to be deleted site" has a valid active subscription then return valid sites else simple delete
#             # so return empty site ids
#             # available_site_ids = []
#
#             if sub_info["subscription_code"] is not None and not sub_info["expired"]:
#                 logger.info("to be deleted site has active license")
#                 if site_type == "treatment unit":
#                     available_treatment_site_ids = []
#                     new_free_or_expired_site = Subscription.objects.filter(Q(expired=True) |
#                                                                            Q(subscription_code__isnull=True),
#                                                                            is_treatment_unit=True,
#                                                                            company_id=request.user.company_id)
#                     for new_site in new_free_or_expired_site.values():
#                         available_treatment_site_ids.append(new_site["site_id"])
#                     treatment_site_data = {"treatment_sites": available_treatment_site_ids}
#
#                     if not available_treatment_site_ids:
#                         return JsonResponse({"Response": {
#                             "Status": "error"},
#                             "message": "Not able to delete the requested site as there is no other site to allocate "
#                                        "the existing subscription"
#                         }, safe=False, status=status.HTTP_200_OK)
#
#                     response_data.update(treatment_site_data)
#
#                 elif site_type == "dispensing unit":
#                     available_dispensing_site_ids = []
#                     new_free_or_expired_site = Subscription.objects.filter(Q(expired=True) |
#                                                                            Q(subscription_code__isnull=True),
#                                                                            is_dispensing_unit=True,
#                                                                            company_id=request.user.company_id)
#                     for new_site in new_free_or_expired_site.values():
#                         available_dispensing_site_ids.append(new_site["site_id"])
#                     dispensing_site_data = {"dispensing_sites": available_dispensing_site_ids}
#                     if not available_dispensing_site_ids:
#                         return JsonResponse({"Response": {
#                             "Status": "error"},
#                             "message": "Not able to delete the requested site as there is no other site to allocate "
#                                        "the existing subscription"
#                         }, safe=False, status=status.HTTP_200_OK)
#                     response_data.update(dispensing_site_data)
#                 else:
#                     available_treatment_site_ids = []
#                     new_free_or_expired_treatment__site = Subscription.objects.filter(Q(expired=True) |
#                                                                            Q(subscription_code__isnull=True),
#                                                                            is_treatment_unit=True,
#                                                                            company_id=request.user.company_id)
#                     for new_site in new_free_or_expired_treatment__site.values():
#                         available_treatment_site_ids.append(new_site["site_id"])
#
#                     treatment_site_data = {"treatment_sites": available_treatment_site_ids}
#                     logger.info(treatment_site_data)
#
#                     available_dispensing_site_ids = []
#                     new_free_or_expired_dispensing_site = Subscription.objects.filter(Q(expired=True) |
#                                                                            Q(subscription_code__isnull=True),
#                                                                            is_dispensing_unit=True,
#                                                                            company_id=request.user.company_id)
#                     for new_site in new_free_or_expired_dispensing_site.values():
#                         available_dispensing_site_ids.append(new_site["site_id"])
#                     dispensing_site_data = {"dispensing_sites": available_dispensing_site_ids}
#                     logger.info(dispensing_site_data)
#                     # Do not allow site deletion if there is no other free or expired sites available to allocate the
#                     # subscription of a "to be deleted site" with valid subscription
#                     if not available_treatment_site_ids or not available_dispensing_site_ids:
#                         return JsonResponse({"Response": {
#                             "Status": "error"},
#                             "message": "Not able to delete the requested site as there is no other site to allocate "
#                                        "the existing subscription"
#                         }, safe=False, status=status.HTTP_200_OK)
#
#                     response_data.update(treatment_site_data)
#                     response_data.update(dispensing_site_data)
#
#         logger.debug("response_data {}".format(response_data))
#         return JsonResponse({"Response": {
#                 "Status": "success"},
#                 "Data": response_data
#             }, safe=False, status=status.HTTP_200_OK)
#
#
# @api_view(['POST'])
# def delete_site(request, pk):
#     # delete free sites subscription
#     # get to be deleted sites subscriptions
#     # add free sites id to "to be deleted" subscription details
#     logger.info("Delete site request came for site id {}".format(pk))
#     if request.method == 'POST':
#
#         expired_treatment_site_id = request.data['treatment_site'] if request.data['treatment_site'] else None
#         expired_dispensing_site_id = request.data['dispensing_site'] if request.data['dispensing_site'] else None
#
#         logger.info("Free treatment site is {}".format(expired_treatment_site_id))
#         logger.info("Free dispensing site is {}".format(expired_dispensing_site_id))
#
#         try:
#             logger.info("Checking whether the site exists for deletion")
#             site_data = Site.objects.get(id=pk)
#             logger.info("Site exists for deletion")
#         except ObjectDoesNotExist:
#             return JsonResponse({"Response": {"Status": "error"}, "message": "The requested site does not exist"},
#                                 status=status.HTTP_200_OK)
#
#         try:
#             logger.info("Checking whether the new site exists")
#             new_treatment_site = Site.objects.get(id=expired_treatment_site_id)
#             new_dispensing_site = Site.objects.get(id=expired_dispensing_site_id)
#             logger.info("New site(s) exists for deletion")
#         except ObjectDoesNotExist:
#             logger.info("Couldn't find the new site")
#             pass
#             # return JsonResponse({"Response": {"Status": "error"}, "message": "Couldn't find the new site"},
#             #                     status=status.HTTP_200_OK)
#
#         # validate if the corresponding list of new site is empty for an active subscription; then don't allow delete
#         if site_data.is_treatment_unit:
#             free_treatment_subscription = Subscription.objects.get(site_id=pk, is_treatment_unit=True)
#             if (not free_treatment_subscription.expired and free_treatment_subscription.subscription_code is not None) \
#                     and (expired_treatment_site_id is None):
#                 logger.error("Error in allocating site subscription to new site. Didn't get the new site list")
#                 return JsonResponse({"Response": {"Status": "error"}, "message": "Didn't get the new site list"},
#                                     status=status.HTTP_200_OK)
#
#         if site_data.is_dispensing_unit:
#             free_dispensing_subscription = Subscription.objects.get(site_id=pk, is_dispensing_unit=True)
#             if (not free_dispensing_subscription.expired and free_dispensing_subscription.subscription_code is not None)\
#                     and (expired_dispensing_site_id is None):
#                 logger.error("Error in allocating site subscription to new site. Didn't get the new site list")
#                 return JsonResponse({"Response": {"Status": "error"}, "message": "Didn't get the new site list"},
#                                     status=status.HTTP_200_OK)
#
#         if expired_treatment_site_id is not None or expired_dispensing_site_id is not None:
#             with transaction.atomic():
#                 try:
#                     # delete new sites old (free or expired) subscriptions
#                     if expired_treatment_site_id == expired_dispensing_site_id:
#                         Subscription.objects.filter(site_id=expired_treatment_site_id).delete()
#                         logger.info("deleting both subscriptions of expired site")
#                     else:
#                         if expired_treatment_site_id is not None:
#                             Subscription.objects.filter(site_id=expired_treatment_site_id).delete()
#                             logger.info("deleting treatment subscription of free site {}"
#                                         .format(expired_treatment_site_id))
#                         if expired_dispensing_site_id is not None:
#                             Subscription.objects.filter(site_id=expired_dispensing_site_id).delete()
#                             logger.info("deleting dispensing subscription of free site {}"
#                                         .format(expired_dispensing_site_id))
#
#                     # get available subscriptions of deleting site and add site ids of new sites(s) to it
#                     if site_data.is_treatment_unit and site_data.is_dispensing_unit:
#                         logger.info("to be deleted site has both subscriptions")
#                         treatment_subscription = Subscription.objects.get(site_id=pk, is_treatment_unit=True)
#                         treatment_subscription.site_id = expired_treatment_site_id
#                         treatment_subscription.save()
#
#                         dispensing_subscription = Subscription.objects.get(site_id=pk, is_dispensing_unit=True)
#                         dispensing_subscription.site_id = expired_dispensing_site_id
#                         dispensing_subscription.save()
#
#                     elif site_data.is_treatment_unit:
#                         logger.info("to be deleted site has only treatment unit")
#                         treatment_subscription = Subscription.objects.get(site_id=pk, is_treatment_unit=True)
#                         treatment_subscription.site_id = expired_treatment_site_id
#                         treatment_subscription.save()
#                     else:  # user_info["is_dispensing_unit"]:
#                         logger.info("to be deleted site has only dispensing unit")
#                         dispensing_subscription = Subscription.objects.filter(site_id=pk, is_dispensing_unit=True)
#                         dispensing_subscription.site_id = expired_dispensing_site_id
#                         dispensing_subscription.save()
#
#                     logger.info("Allocated the subscription(s) to new site(s)")
#                 except Exception as err:
#                     transaction.set_rollback(True)
#                     logger.error("Error in allocating site subscription to new site. {}".format(err))
#                     return JsonResponse({"Response": {"Status": "error"}, "message": "Error in allocating site's "
#                                                                                      "subscription(s) to new site(s)"},
#                                         status=status.HTTP_200_OK)
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
@api_view(['GET'])
def get_free_or_expired_trial_sites(request, pk):
    logger.info("Got request to list free or expired sites before site delete")
    if request.method == 'GET':
        try:
            requested_site = Site.objects.get(id=pk)
        except ObjectDoesNotExist:                                          
            # ! if the site doesn't exists controller stops here

            return JsonResponse({"Response": {
                    "Status": "error"},
                    'message': 'The site does not exist'
                }, status=status.HTTP_200_OK)

       
        site_type = ""
        site_obj = Site.objects.get(id=pk)                                  
        # ! finds site to be deleted and sotres in site_obj

        response_data = {}
        # ! Creates response data variable which is returned as a response

    
        if site_obj.is_treatment_unit and site_obj.is_dispensing_unit:
            site_type = "both"
            logger.info("About to delete site has both units")              
            # ! finds and sets site type. Deletes both if type is both

            subs_obj = Subscription.objects.filter(site_id=site_obj.id)     
            # ! subscription object is fetched and stored inside subs_obj

        elif site_obj.is_treatment_unit:
            site_type = "treatment unit"
            subs_obj = Subscription.objects.filter(site_id=site_obj.id, is_treatment_unit=True)  

        else:  
            site_type = "dispensing unit"
            subs_obj = Subscription.objects.filter(site_id=site_obj.id, is_dispensing_unit=True)

        logger.info("About to delete site is {}".format(site_type))

        # if site has active license
        #   if found get free or expired licenses sites
        #   else
        #   do not allow site delete
        # if site has no active license give empty response and allow direct delete

        for sub_info in subs_obj.values():                                 
            # ! fetches subscription informaiton form subscription object value

            # logger.info(sub_info)
            # if the "to be deleted site" has a valid active subscription then return valid sites else simple delete
            # so return empty site ids
            # available_site_ids = []

            if sub_info["subscription_code"] is not None and not sub_info["expired"]:
                # ! subscription_code = "{}_{}_{}_{}".format(request.user.company.id, site_id, start_date, end_date)
                # ! checks for value of expired table in the subscription table for that particular row/id

                logger.info("to be deleted site has active license")

                if site_type == "treatment unit":
                    available_treatment_site_ids = []
                    # ! list abailable or free treatment sites
                    
                    new_free_or_expired_site = Subscription.objects.filter(Q(expired=True) | Q(subscription_code__isnull=True),is_treatment_unit=True, company_id=request.user.company_id)
                    # ! retrives from database free or expired site for a particular company account | retrieves as a model instacce 

                    for new_site in new_free_or_expired_site.values():
                        site_name = Site.objects.get(id=new_site["site_id"]).site_name
                        available_treatment_site_ids.append(site_name)
                    treatment_site_data = {"site_names": available_treatment_site_ids}
                    # ! build treatement site data object

                    if not available_treatment_site_ids:
                    # ! does not allow to delete the site if there are no other sites to allocat the exiting subscription to 
                        return JsonResponse({"Response": {
                            "Status": "error"},
                            "message": "Not able to delete the requested site as there is no other site to allocate "
                                       "the existing subscription"
                        }, safe=False, status=status.HTTP_200_OK)

                    response_data.update(treatment_site_data)
                    # ! Updates repsonse data

                elif site_type == "dispensing unit":
                    # ! applies same logic for dispensig sites and updates respons data

                    available_dispensing_site_ids = []
                    new_free_or_expired_site = Subscription.objects.filter(Q(expired=True) | Q(subscription_code__isnull=True), is_dispensing_unit=True, company_id=request.user.company_id)
                    for new_site in new_free_or_expired_site.values():
                        site_name = Site.objects.get(id=new_site["site_id"]).site_name
                        available_dispensing_site_ids.append(site_name)
                    dispensing_site_data = {"site_names": available_dispensing_site_ids}
                    if not available_dispensing_site_ids:
                        return JsonResponse({"Response": {
                            "Status": "error"},
                            "message": "Not able to delete the requested site as there is no other site to allocate "
                                       "the existing subscription"
                        }, safe=False, status=status.HTTP_200_OK)
                    response_data.update(dispensing_site_data)
                
                else:
                    # ! if site type is both, then search for available sites where sites are either expired or 
                    available_site_ids = []
                    new_free_or_expired_site = Subscription.objects.filter(Q(expired=True) |
                                                                                      Q(subscription_code__isnull=True),
                                                                                      is_treatment_unit=True,
                                                                                      is_dispensing_unit=True,
                                                                                      company_id=
                                                                                      request.user.company_id)
                    for new_site in new_free_or_expired_site.values():
                        site_name = Site.objects.get(id=new_site["site_id"]).site_name
                        available_site_ids.append(site_name)

                    treatment_site_data = {"site_names": available_site_ids}
                    logger.info(treatment_site_data)

                    # ! Does not allow site deletion if there is no other free or expired sites available to allocate the subscription of a "to be deleted site" with valid subscription
                    if not available_site_ids:
                        return JsonResponse({"Response": {
                            "Status": "error"},
                            "message": "Not able to delete the requested site as there is no other site to allocate "
                                       "the existing subscription"
                        }, safe=False, status=status.HTTP_200_OK)

                    response_data.update(treatment_site_data)

        logger.debug("response_data {}".format(response_data))
        return JsonResponse({"Response": {
                "Status": "success"},
                "Data": response_data
            }, safe=False, status=status.HTTP_200_OK)


@api_view(['POST'])
def delete_site(request, pk):
    # delete free sites subscription
    # get to be deleted sites subscriptions
    # add free sites id to "to be deleted" subscription details
    logger.info("Delete site request came for site id {}".format(pk))
    if request.method == 'POST':

        expired_site_id = request.data['site_name'] if request.data['site_name'] else None
        # ! fetches expired site id A TERRIBLE MISTAKE OF NAMING A VARIBLE. IT SHOULD BE EXPIRED_SITE_NAME. 

        # expired_dispensing_site_id = request.data['dispensing_site'] if request.data['dispensing_site'] else None

        logger.info("Free treatment site is {}".format(expired_site_id))
        # logger.info("Free dispensing site is {}".format(expired_dispensing_site_id))

        try:
            logger.info("Checking whether the site exists for deletion")
            site_data = Site.objects.get(id=pk)
            # ! collects site data from Sites
            logger.info("Site exists for deletion")
        except ObjectDoesNotExist:
            return JsonResponse({"Response": {"Status": "error"}, "message": "The requested site does not exist"},
                                status=status.HTTP_200_OK)

        try:
            logger.info("Checking whether the new site exists")
            new_site = Site.objects.get(site_name=expired_site_id)
            # new_dispensing_site = Site.objects.get(id=expired_dispensing_site_id)
            logger.info("New site(s) exists for deletion")
        except ObjectDoesNotExist:
            logger.info("Couldn't find the new site")
            pass
            # return JsonResponse({"Response": {"Status": "error"}, "message": "Couldn't find the new site"},
            #                     status=status.HTTP_200_OK)

        # validate if the corresponding list of new site is empty for an active subscription; then don't allow delete
        if site_data.is_treatment_unit:
            free_treatment_subscription = Subscription.objects.get(site_id=pk, is_treatment_unit=True)
            # ! site allocatgion logic for treatment unit
            if (not free_treatment_subscription.expired and free_treatment_subscription.subscription_code is not None) \
                    and (expired_site_id is None): # ! Expried iste id is the name of the site to be deleted
                logger.error("Error in allocating site subscription to new site. Didn't get the new site list")
                return JsonResponse({"Response": {"Status": "error"}, "message": "Didn't get the new site list"},
                                    status=status.HTTP_200_OK)

        if site_data.is_dispensing_unit:
            free_dispensing_subscription = Subscription.objects.get(site_id=pk, is_dispensing_unit=True)
             # ! site allocation logic for treatment unit
            if (not free_dispensing_subscription.expired and free_dispensing_subscription.subscription_code is not None)\
                    and (expired_site_id is None):
                logger.error("Error in allocating site subscription to new site. Didn't get the new site list")
                return JsonResponse({"Response": {"Status": "error"}, "message": "Didn't get the new site list"},
                                    status=status.HTTP_200_OK)

        if expired_site_id is not None:
            with transaction.atomic():
                try:
                    # delete new sites old (free or expired) subscriptions
                    expired_site = Site.objects.get(site_name=expired_site_id, company_id=request.user.company_id)
                    # ! Fetches details of expired site

                    site_id = expired_site.id
                    # ! stored site id of the expired site 

                    Subscription.objects.filter(site_id=site_id).delete()
                    # ! Deletes the site 

                    logger.info("deleting subscription of free site {}"
                                .format(expired_site_id))

                    # get available subscriptions of deleting site and add site ids of new sites(s) to it

                    if site_data.is_treatment_unit and site_data.is_dispensing_unit:
                        logger.info("to be deleted site has both subscriptions")
                        treatment_subscription = Subscription.objects.get(site_id=pk, is_treatment_unit=True)
                        treatment_subscription.site_id = site_id
                        # ! changes site id of treatment unit and matches it with the site id of deleted site
                        treatment_subscription.save()

                        dispensing_subscription = Subscription.objects.get(site_id=pk, is_dispensing_unit=True)
                        dispensing_subscription.site_id = site_id
                        # ! changes site id of treatment unit and matches it with the site id of deleted site
                        dispensing_subscription.save()

                    elif site_data.is_treatment_unit:
                        logger.info("to be deleted site has only treatment unit")
                        treatment_subscription = Subscription.objects.get(site_id=pk, is_treatment_unit=True)
                        treatment_subscription.site_id = site_id
                        treatment_subscription.save()

                    else:  # user_info["is_dispensing_unit"]:
                        logger.info("to be deleted site has only dispensing unit")
                        dispensing_subscription = Subscription.objects.get(site_id=pk, is_dispensing_unit=True)
                        dispensing_subscription.site_id = site_id
                        dispensing_subscription.save()

                    logger.info("Allocated the subscription(s) to new site(s)")
                    expired_site.status = True
                    expired_site.save()
                    logger.info("Updated the new site(s) status to active")
                except Exception as err:
                    transaction.set_rollback(True)
                    logger.error("Error in allocating site subscription to new site. {}".format(err))
                    return JsonResponse({"Response": {"Status": "error"}, "message": "Error in allocating site's "
                                                                                     "subscription(s) to new site(s)"},
                                        status=status.HTTP_200_OK)
        with transaction.atomic():
            # ! archives the site
            try:
                logger.debug("Trying to delete the site")
                site_details = Site.objects.get(pk=pk)
                archive_site = ArchiveSite()
                archive_site.site_name = site_details.site_name
                archive_site.address = site_details.address
                archive_site.city = site_details.city
                archive_site.state = site_details.state
                archive_site.phone = site_details.phone
                archive_site.phone_verified = site_details.phone_verified
                archive_site.token_verified = site_details.token_verified
                archive_site.status = site_details.status
                archive_site.alerts = site_details.alerts
                archive_site.created = site_details.created
                archive_site.is_treatment_unit = site_details.is_treatment_unit
                archive_site.is_dispensing_unit = site_details.is_dispensing_unit
                archive_site.company = site_details.company
                archive_site.save()

                device_details = Device.objects.get(site_id=pk)
                archive_device = ArchiveDevice()
                archive_device.device_name1 = device_details.device_name1
                archive_device.serial_no1 = device_details.serial_no1
                archive_device.device_name2 = device_details.device_name2
                archive_device.serial_no2 = device_details.serial_no2
                archive_device.device_name3 = device_details.device_name3
                archive_device.serial_no3 = device_details.serial_no3
                archive_device.site_id = archive_site.id
                archive_device.save()

                site_permission = SitePermission.objects.filter(site_id=pk)
                for permission in site_permission.values():
                    archive_site_permission = ArchiveSitePermission()
                    archive_site_permission.created = permission["created"]
                    archive_site_permission.site_id = archive_site.id
                    archive_site_permission.user_id = permission["user_id"]
                    archive_site_permission.save()

                Site.objects.filter(pk=pk).delete()

                logger.debug("Deleted the site")
            except Exception as err:
                transaction.set_rollback(True)
                logger.error("Error in deleting site {}.{}".format(pk, err))
                return JsonResponse({"Response": {"Status": "error"}, "message": "Error in site delete"},
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
                        "Device 1",
                        "Device 2",
                        "Device 3"
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


# @login_required
# @api_view(['POST'])
# def verify_otp(request):
#
#     if request.method == 'POST':
#         code = request.data['otpnumber']
#         site_name = request.data['site_name']
#
#         try:
#             site_obj = Site.objects.get(company_id=request.user.company_id, site_name=site_name)
#             if not site_obj.phone:
#                 return JsonResponse({"Response": {"Status": "error"},
#                                      "message": "Verification failed. No phone number is provided"},
#                                     safe=False, status=status.HTTP_200_OK)
#
#             if site_obj.verify_phone(code)["status"]:
#                 while site_obj.verify_phone(code)["difference"] < OTP_VALID_FOR:
#                     try:
#                         sub_count = Subscription.objects.filter(site_id=site_obj.id).count()
#                         logger.debug(sub_count)
#                         if sub_count > 0:
#                             dev_obj = Device.objects.get(site_id=site_obj.id)
#                             response = {
#                                 'device_name1': dev_obj.device_name1,
#                                 "device_name2": dev_obj.device_name2,
#                                 "device_name3": dev_obj.device_name3
#                             }
#                             logger.info(response)
#                             return JsonResponse({"Response": {"Status": "success"},
#                                                  "message": "Verified both OTP and token"},
#                                                 safe=False, status=status.HTTP_200_OK)
#                     except Exception as err:
#                         pass
#                         # logger.info("Didn't get the token yet from the device; {}".format(err))
#
#                 # return JsonResponse({"Response": {"Status": "success"},
#                 #                      "message": "Verified"},
#                 #                     safe=False, status=status.HTTP_200_OK)
#             logger.info("Verification failed. Invalid otp or otp expired or didn't get the token from the device")
#             return JsonResponse({"Response": {"Status": "error"},
#                                  "message": "Verification failed. Invalid or expired otp or token"},
#                                 safe=False, status=status.HTTP_200_OK)
#         except Site.DoesNotExist as err:
#             return JsonResponse({"Response": {"Status": "error"},
#                                  "message": "Couldn't find the requested site, {}".format(err)},
#                                 safe=False, status=status.HTTP_200_OK)
