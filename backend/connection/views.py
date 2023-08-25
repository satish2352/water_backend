from django.shortcuts import render
from django.db.models.expressions import RawSQL
from django.db import transaction, DatabaseError
# Create your views here.
from django.db import connection
from django.shortcuts import render
import sys
import ssl
import time
import datetime
import logging, traceback
import paho.mqtt.client as mqtt
from django.shortcuts import render
from django.http import HttpResponse
from .alpn_mqtt import *
import requests
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
# Create your views here.
from django.shortcuts import render
from .models import *
from django.utils import timezone
# from dateutil.relativedelta import relativedelta
import datetime
import pytz
from json import JSONDecodeError
import ast
from rest_framework import viewsets,permissions
# from tzlocal import get_localzone # $ pip install tzlocal
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponse,Http404
from channels.generic.websocket import WebsocketConsumer
import json
from rest_framework import generics
import os
from django.http import HttpResponse
from datetime import datetime

# get local timezone    
# local_tz = get_localzone()

from .serializers import *
msgo="hello"

from django.http import JsonResponse
# from .mqttconn import client as mqttc
from channels.consumer import SyncConsumer
# from devices.views import msgo
import json

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.consumer import StopConsumer

import traceback
from django.shortcuts import render
from channels.generic.websocket import AsyncWebsocketConsumer

from django.core.serializers import serialize

from iwater import models as mo
channel_layer = get_channel_layer()
eg=''
# set DJANGO_SETTINGS_MODULE=waterinn.settings
# from django_init import *

# Now you can access Django settings and models
from django.conf import settings
from django.contrib.auth.models import User

#jwt setting
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.serializers import serialize
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

import json
import re
import threading
from connection.alpn_mqtt import *
from datetime import datetime

from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework import status
from django.db import transaction
from django.db.models import Q

from django.contrib.sites.shortcuts import get_current_site
import paho.mqtt.client as mqtt

# from iwater.views.signup_mgmnt import user_login,email
from iwater.models import Site, User, SitePermission, Device, Subscription, ArchiveSite, ArchiveDevice, ArchiveSitePermission,Company
from init_water_app import settings
from init_water_app.settings import OTP_VALID_FOR
from iwater.iw_logger import logger
import random
site_ids=0
panelid=None
atmid=None
company_ids=0
# mqttc = mqtt.Client()
# client = mqtt.Client()
# client.subscribe('wc1/v1/OTP',1)
# mqttc.subscribe('wc1/#',1)
# try:
#     info_data=device_info.objects.all()
#     print("device_info is:",info_data)
#     for zzz in info_data:
#         print("first record:",zzz.Device_name)
# except Exception as e:
#     print("data not found in device_info",e.args)
# logging.info("****************************************************************vikas")
# print("****************************************************************vikas")
# client.message_callback_add("wc/v1/OTP", on_message)
# client.message_callback_add("wc/#", on_message)
class MqttClient:
    def __init__(self, company_id):
        # _data_mqtt = settings.settings_get_mqttSettings()
        # _topic = "IW/V1/OTP"
        _topic = "wc1/v1/OTP"
        # _username = _data_mqtt['_username']
        # _password = _data_mqtt['_password']
        # _hostname = "broker.mqttdashboard.com"
        # _port = 443
        _port = 8883
        self.company_id = company_id

        # logger.info("MQTT - Credentials: username: {}, hostname: {}, port: {}".format(_username, _hostname, _port))
        self.client = mqtt.Client()
        self.client = self.client 
        self.topic = _topic
        # if _clientID != "":
        # self.client = mqtt.Client(client_id="")

        # self.client.on_connect = self.on_connect
        # self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect_1
        self.client.on_message = self.on_message_1

        # connect to HiveMQ Cloud on port
        # self.client.connect(_hostname, _port, OTP_VALID_FOR)
        ssl_context= ssl_alpn()
        self.client.tls_set_context(context=ssl_context)
        self.client.connect(aws_iot_endpoint, _port, OTP_VALID_FOR)
        

        self.client.loop_start()

    def on_message_1(self, client, userdata, message):
        global token_,company_ids
        print("Data received1!!!",message.payload)
        jstr=message.payload
        if isinstance(jstr, bytes):
            data1 = jstr.decode("utf-8")
            # print("data:",data,type(data))
        # if data.startswith("{'") and data.endswith("'}"):
            # dict_str = jstring.decode("UTF-8")
        # data = json.loads(str(message.payload.decode('utf-8')))
        print("Data received!!!",data1)

        logger.info("MQTT data {}".format(data1))

        data=eval(data1)
        print("new data is:",data,type(data))
        # site_id = data["token"]

        token_ = data["token"]
        # site_id= Site.objects.filter(token=token_).latest()
        # site_id = str(data["token"]).lstrip("0")
        # site_id = site_id['id']
        device_id = data["deviceid"]
        if "panelid" in data1:
            global panelid
            panelid = data["panelid"] if data["panelid"] else None
            if panelid:
                logger.info("panelid {}".format(panelid))

        if "atmid" in data1:
            global atmid
            atmid = data["atmid"] if data["atmid"] else None
            if atmid:
                logger.info("atmid {}".format(atmid))


        logger.info("site_id {}".format(token_))
        logger.info("company_id {}".format(self.company_id))
        company_ids=self.company_id
        logger.info("device_id {}".format(device_id))
        get_siteid=Site.objects.filter(token=token_,company_id=self.company_id)
        
        if get_siteid: 
            for qq in get_siteid:
                global site_ids
                site_ids=qq.id
                # company_ids=qq.company_id
                print("qq:", qq.id)
        # device_data=Device.objects.create()
        
        # doublicate_device_id=Device.objects.filter(Q(serial_no2 =panelid) | Q(serial_no3=atmid)).filter(~Q(site_id = site_ids))
        if panelid is not None:
            doublicate_panel_id=Device.objects.filter(serial_no2 =panelid).filter(~Q(site_id = site_ids))
        if atmid is not None:
            doublicate_atm_id=Device.objects.filter(serial_no3 =atmid).filter(~Q(site_id = site_ids))
        if doublicate_panel_id is not None or doublicate_atm_id is not None:
          logger.info("Doublicate device found")
        
        
        else:
            with transaction.atomic():
                try:  # TODO
                    pass
                    print("001")
                # # Device.objects.get(site_id=site_id, serial_no1=device_id)
                    try:
                        print("002")

                        # device_data = Device.objects.get(site_id=site_id) # ! verfies device against site_id
                        device_data = Device.objects.get(site_id=site_ids) # ! verfies device against site_id
                        # print("Device data:",device_data)
                        print("003")

                    except Device.DoesNotExist:
                        device_data = None

                    if device_data is not None:
                        logger.info("re-auth request came for device {}".format(device_id)) # ! re-auth request

                        # device_data = Device.objects.get(site_id=site_id, serial_no1=device_id)
                        if device_data.serial_no2 is None:
                            device_data.serial_no2 = panelid
                            device_data.save()
                            logger.info("Added device serial numbers")

                            site_data = Site.objects.get(id=site_ids)
                            site_data.is_treatment_unit = True
                            site_data.token_verified = True
                            site_data.save()
                            logger.info("Updated site details for treatment unit")

                            subscription_data = Subscription()
                            subscription_data.site_id = site_ids
                            subscription_data.is_treatment_unit = True
                            subscription_data.company_id = self.company_id
                            subscription_data.save()
                            #changes by sir

                            # subscription_data = Subscription.objects.get(site_id=site_ids)
                            # subscription_data.site_id = site_ids
                            # subscription_data.is_treatment_unit = True
                            # subscription_data.company_id = self.company_id
                            # subscription_data.save()
                            logger.info("Added subscription details for treatment unit")
                        if device_data.serial_no3 is None:
                            device_data.serial_no3 = atmid
                            device_data.save()
                            logger.info("Added device serial numbers")

                            site_data = Site.objects.get(id=site_ids)
                            site_data.is_dispensing_unit = True
                            site_data.token_verified = True
                            site_data.save()
                            logger.info("Updated site details for dispensing unit")

                            # subscription_data = Subscription.objects.get(site_id=site_id)
                            # subscription_data.is_treatment_unit = True
                            # subscription_data.save()

                            subscription_data = Subscription()
                            subscription_data.site_id = site_ids
                            subscription_data.is_dispensing_unit = True
                            subscription_data.company_id = self.company_id
                            subscription_data.save()
                            logger.info("Added subscription details for dispensing unit")

                    else:
                        logger.info("Got new device add request ")
                        if panelid and atmid:
                            logger.info("Got both panel and atm id from device")

                            device_data = Device()
                            device_data.serial_no1 = device_id
                            device_data.serial_no2 = panelid
                            device_data.serial_no3 = atmid
                            device_data.site_id = site_ids
                            device_data.save()
                            logger.info("Added device serial numbers")

                            site_data = Site.objects.get(id=site_ids)
                            site_data.is_treatment_unit = True
                            site_data.is_dispensing_unit = True
                            site_data.token_verified = True
                            site_data.save()
                            logger.info("Updated site details for treatment unit")

                            subscription_data = Subscription()
                            subscription_data.site_id = site_ids
                            subscription_data.is_treatment_unit = True
                            subscription_data.company_id = self.company_id
                            subscription_data.save()

                            subscription_data1 = Subscription()
                            subscription_data1.site_id = site_ids
                            subscription_data1.is_dispensing_unit = True
                            subscription_data1.company_id = self.company_id
                            subscription_data1.save()
                            logger.info("Added subscription details for dispensing unit")

                            # site_data = Site.objects.get(id=site_ids)
                            # site_data.is_dispensing_unit = True
                            # site_data.save()
                            # logger.info("Updated site details for dispensing unit")

                            # subscription_data = Subscription.objects.get(site_id=site_id)
                            # subscription_data.is_treatment_unit = True
                            # subscription_data.save()

                            # subscription_data = Subscription()
                            # subscription_data.site_id = site_ids
                            # subscription_data.is_dispensing_unit = True
                            # subscription_data.company_id = self.company_id
                            # subscription_data.save()
                            # logger.info("Added subscription details for dispensing unit")
                        
                        elif panelid:
                            logger.info("Got only panel id from device")

                            device_data = Device()
                            device_data.serial_no1 = device_id
                            device_data.serial_no2 = panelid
                            device_data.serial_no3 = atmid
                            device_data.site_id = site_ids
                            device_data.save()
                            logger.info("Added device serial numbers")

                            site_data = Site.objects.get(id=site_ids)
                            site_data.is_treatment_unit = True
                            site_data.token_verified = True
                            site_data.save()
                            logger.info("Updated site details for treatment unit")

                            subscription_data = Subscription()
                            subscription_data.site_id = site_ids
                            subscription_data.is_treatment_unit = True
                            subscription_data.company_id = self.company_id
                            subscription_data.save()
                            logger.info("Added subscription details for treatment unit")

                        elif atmid:
                            logger.info("Got only atm id from device")
                            try:
                                device_data = Device()
                                device_data.serial_no1 = device_id
                                device_data.serial_no2 = panelid
                                device_data.serial_no3 = atmid
                                device_data.site_id = site_ids
                                device_data.save()
                            except DatabaseError as e:
                                print("25-8-23",e)

                            logger.info("data created successfully in device")
                            site_data = Site.objects.get(id=site_ids)
                            site_data.is_dispensing_unit = True
                            site_data.token_verified = True
                            site_data.save()
                            logger.info("Updated site details for dispensing unit")

                            subscription_data = Subscription()
                            subscription_data.site_id = site_ids
                            subscription_data.is_dispensing_unit = True
                            subscription_data.company_id = self.company_id
                            subscription_data.save()
                            logger.info("Added subscription details for dispensing unit")
                    site_data = Site.objects.get(id=site_ids)
                    # company_names=Company.objects.get(company_id=self.company_id)
                    print("*1*1*")
                    # print("email is:",email)
                    # print("email is:",user_login.email)
                    # logger.info("email is:",user_login.email)
                    # logged_user = User.objects.get(email=user_login.email)

                    # company_names = Company.objects.get(id=logged_user.company_id)
                    company_names = Company.objects.get(id=company_ids)

                    print("company_names:",company_names.company_name)
                    # records = [
                    # {
                    # "Device_id": panelid,
                    # "Device_name": "wc",
                    # "unit_type": "water_treatment",
                    # "company_name": company_names.company_name,
                    # "componant_name": "rwp",
                    # "site_name": site_data.site_name
                    # },
                    # {
                    # "Device_id": panelid,
                    # "Device_name": "wc",
                    # "unit_type": "water_treatment",
                    # "company_name": company_names.company_name,
                    # "componant_name": "rwp",
                    # "site_name": site_data.site_name
                    # },
                    # {
                    # "Device_id": panelid,
                    # "Device_name": "wc",
                    # "unit_type": "water_treatment",
                    # "company_name": company_names.company_name,
                    # "componant_name": "cnd_sen",
                    # "site_name": site_data.site_name
                    # },
                    # {
                    # "Device_id": panelid,
                    # "Device_name": "wc",
                    # "unit_type": "water_treatment",
                    # "company_name": company_names.company_name,
                    # "componant_name": "ampv1",
                    # "site_name": site_data.site_name
                    # },
                    # {
                    # "Device_id": panelid,
                    # "Device_name": "wc",
                    # "unit_type": "water_treatment",
                    # "company_name": company_names.company_name,
                    # "componant_name": "ampv2",
                    # "site_name": site_data.site_name
                    # },
                    # {
                    # "Device_id": panelid,
                    # "Device_name": "wc",
                    # "unit_type": "water_treatment",
                    # "company_name": company_names.company_name,
                    # "componant_name": "ampv3",
                    # "site_name": site_data.site_name
                    # },
                    # {
                    # "Device_id": panelid,
                    # "Device_name": "wc",
                    # "unit_type": "water_treatment",
                    # "company_name": company_names.company_name,
                    # "componant_name": "ampv4",
                    # "site_name": site_data.site_name
                    # },
                    # {
                    # "Device_id": panelid,
                    # "Device_name": "wc",
                    # "unit_type": "water_dispense",
                    # "company_name": company_names.company_name,
                    # "componant_name": "tap2",
                    # "site_name": site_data.site_name
                    # },
                    # {
                    # "Device_id": panelid,
                    # "Device_name": "wc",
                    # "unit_type": "water_dispense",
                    # "company_name": company_names.company_name,
                    # "componant_name": "tap3",
                    # "site_name": site_data.site_name
                    # },
                    # {
                    # "Device_id": panelid,
                    # "Device_name": "wc",
                    # "unit_type": "water_dispense",
                    # "company_name": company_names.company_name,
                    # "componant_name": "tap4",
                    # "site_name": site_data.site_name
                    # },
                    # {
                    # "Device_id": panelid,
                    # "Device_name": "wc",
                    # "unit_type": "water_treatment",
                    # "company_name": company_names.company_name,
                    # "componant_name": "hpp",
                    # "site_name": site_data.site_name
                    # },
                    # {
                    # "Device_id": panelid,
                    # "Device_name": "wc",
                    # "unit_type": "water_treatment",
                    # "company_name": company_names.company_name,
                    # "componant_name": "atm",
                    # "site_name": site_data.site_name
                    # },
                    # {
                    # "Device_id": panelid,
                    # "Device_name": "wc",
                    # "unit_type": "water_treatment",
                    # "company_name": company_names.company_name,
                    # "componant_name": "panel",
                    # "site_name": site_data.site_name
                    # },
                    # {

                    # "Device_id": panelid,
                    # "Device_name": "wc",
                    # "unit_type": "water_treatment",
                    # "company_name": company_names.company_name,
                    # "componant_name": "F_flowsen",
                    # "site_name": site_data.site_name
                    # },
                    # {
                    # "Device_id": panelid,
                    # "Device_name": "wc",
                    # "unit_type": "water_treatment",
                    # "company_name": company_names.company_name,
                    # "componant_name": "P_flowsen",
                    # "site_name": site_data.site_name
                    # },
                    # {
                    # "Device_id": panelid,
                    # "Device_name": "wc",
                    # "unit_type": "water_treatment",
                    # "company_name": company_names.company_name,
                    # "componant_name": "tds_sen",
                    # "site_name": site_data.site_name
                    # }]
                
                    # record_atm=[
                    # {
                    # "Device_id": atmid,
                    # "Device_name": "wc",
                    # "unit_type": "water_dispense",
                    # "company_name": company_names.company_name,
                    # "componant_name": "cnd_consen",
                    # "site_name": site_data.site_name
                    # },
                    # {
                    # "Device_id": atmid,
                    # "Device_name": "wc",
                    # "unit_type": "water_dispense",
                    # "company_name": company_names.company_name,
                    # "componant_name": "tds_consen",
                    # "site_name": site_data.site_name
                    # },
                    # {
                    # "Device_id": atmid,
                    # "Device_name": "wc",
                    # "unit_type": "water_dispense",
                    # "company_name": company_names.company_name,
                    # "componant_name": "atm",
                    # "site_name": site_data.site_name
                    # },
                    # {
                    # "Device_id": atmid,
                    # "Device_name": "wc",
                    # "unit_type": "water_dispense",
                    # "company_name": company_names.company_name,
                    # "componant_name": "flowsen1",
                    # "site_name": site_data.site_name
                    # },
                    # {
                    # "Device_id": atmid,
                    # "Device_name": "wc",
                    # "unit_type": "water_dispense",
                    # "company_name": company_names.company_name,
                    # "componant_name": "flowsen2",
                    # "site_name": site_data.site_name
                    # },
                    # {
                    # "Device_id": atmid,
                    # "Device_name": "wc",
                    # "unit_type": "water_dispense",
                    # "company_name": company_names.company_name,
                    # "componant_name": "flowsen3",
                    # "site_name": site_data.site_name
                    # },
                    # {
                    # "Device_id": atmid,
                    # "Device_name": "wc",
                    # "unit_type": "water_dispense",
                    # "company_name": company_names.company_name,
                    # "componant_name": "flowsen4",
                    # "site_name": site_data.site_name
                    # },
                    # {
                    # "Device_id": atmid,
                    # "Device_name": "wc",
                    # "unit_type": "water_dispense",
                    # "company_name": company_names.company_name,
                    # "componant_name": "tap1",
                    # "site_name": site_data.site_name
                    # },
                    # {
                    # "Device_id": atmid,
                    # "Device_name": "wc",
                    # "unit_type": "water_dispense",
                    # "company_name": company_names.company_name,
                    # "componant_name": "tap1",
                    # "site_name": site_data.site_name
                    # }
                    #                     # Add other records here
                    # ]
                    # print("*2*2*")
                    # # Insert the records into the collection
                    # # device_info.insert_many(records)
                    # if "panelid" in data1:
                    #     for record in records:
                    #         info=device_info.objects.create(**record)
                    #         info.save()
                    #         logger.info("panel records Added")
                    
                    # if "atmid" in data1:        
                    #     for record in record_atm:
                    #         info=device_info.objects.create(**record)
                    #         info.save()
                    #         logger.info("atm records Added")




                    # if atmid and panelid:
                    #     for record in records:
                    #         print("*3*3*")
                    #         info=device_info.objects.create(**record)
                    #  
                    #         info.save()
                    #         print("*5*5*")
                    #     for record in record_atm:
                    #         print("*3*3*")
                    #         info=device_info.objects.create(**record)
                    #  
                    #         info.save()

                    logger.info("Successfully added data to db over mqtt")
                    print("*6*6*")
                except Exception as err:
                    print("*7*7*")
                    transaction.set_rollback(True)
                    logger.error("MQTT - {}".format(err))

    def on_connect_1(self, client, userdata, flags, rc):
        logger.info("MQTT - connected")
        self.subscribe(self.topic)

    def subscribe(self, topic):
        self.client.subscribe(topic,1)
        logger.info("MQTT - Subscribed to topic '" + topic)

    def publish(self, topic, payload):
        logger.info("MQTT - Published message '" + str(payload) + "' on topic '" + topic)
        self.client.publish(topic, payload=payload)
        # self.client.loop_stop()

    def stop(self):
        logger.info("MQTT - Disconnecting from mqtt broker and cleaning up")
        self.client.disconnect()


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
    return JsonResponse({"Response": {"Status": "success"}, "Data": "Bad request"},
                        safe=False, status=status.HTTP_400_BAD_REQUEST)


# @login_required
@api_view(['POST'])
def send_otp(request):
    logger.info("Got send otp request for site adding")
    logger.info("Getting unverified sites")

    not_verified_sites = Site.objects.filter(phone_verified=False, token_verified=False)
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
        logger.debug("site add input parameters {} {} {} {} {}".format(site_name, address, city, state, site_mob))
        try:
            existing_site = Site.objects.get(company_id=request.user.company_id, site_name=site_name)
            # ! checks for duplication of site name
            if existing_site.token_verified and existing_site.phone_verified and existing_site.is_treatment_unit and existing_site.is_dispensing_unit:
                response = {"Response": {
                    "Status": "error"},
                    "message": "The site name is already registered"
                }
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
            # else:
            #     Site.objects.get(phone=site_mob)
            #     response = {"Response": {
            #         "Status": "error"},
            #         "message": "The phone number is already used for site registration"
            #     }
            #     return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        except Site.DoesNotExist:
            pass

        # try:
        #     si = Site.objects.get(phone=site_mob, site_name=site_name, phone_verified=True, token_verified=True)
        #     # ! checks if phone number is already in used 
        #     # ? Should be disabled ?
        #     response = {"Response": {
        #         "Status": "error"},
        #         "message": "The phone number is already used for site registration"
        #     }
        #     return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        # except Site.DoesNotExist:
        #     pass

        with transaction.atomic():
            try:
                site_obj = Site.objects.filter(company_id=request.user.company_id, site_name=site_name)
                print("*****:",site_obj)
                if site_obj:
                    logger.error("site {} already exists".format(site_name))

                    site_dat = Site.objects.get(company_id=request.user.company_id, site_name=site_name)
                    site_dat.site_name = site_name
                    site_dat.address = address
                    site_dat.city = city
                    site_dat.state = state
                    site_dat.phone = site_mob
                    site_dat.company = request.user.company
                    site_dat.save()
                else:
                    logger.info("site {} does not exists".format(site_name))
                    logger.info("so checking whether phone number is already used")
                    # try:
                    #     Site.objects.get(phone=site_mob)
                    #     response = {"Response": {   
                    #         "Status": "error"},
                    #         "message": "The phone number is already used for site registration"
                    #     }
                    #     return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
                    
                    # except Site.DoesNotExist:
                    #     pass
                    # logger.info("phone number is not used, hence adding site details")
                    site_dat = Site()
                    # ! initiates instance of the site

                    site_dat.site_name = site_name
                    site_dat.address = address
                    site_dat.city = city
                    site_dat.state = state
                    site_dat.phone = site_mob
                    site_dat.company = request.user.company
                    site_dat.save()
                    # ! saves the site
            
            except Exception as err:
                transaction.set_rollback(True)
                logger.error("Error in adding site details; {}".format(err))
                return JsonResponse({"Response": {"Status": "error"},
                                     "message": "Site name is already taken"},
                                    safe=False, status=status.HTTP_200_OK)

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
            if site_obj.phone_verified and site_obj.token_verified:
                return JsonResponse({"Response": {"Status": "error"},
                                     "message": "Site is already verified"},  # Site is already verified
                                    # Site name is already taken
                                    safe=False, status=status.HTTP_200_OK)
            else:
                site_obj.phone_verified = False
            logger.info("Both OTP and token are not verified hence resending the otp")
            threading.Thread(target=connect_mqtt_in_background, args=(request.user.company_id, )).start()
            # ! connects MQTT 

            # sent = site_obj.send_verification_sms(site_obj.id)
            sent = site_obj.send_verification_sms(random.randint(1000, 9999))
            # ! sends verification sms to the mobile
            
            logger.info("sent")
            if sent["status"]:
                return JsonResponse({"Response": {"Status": "success"},
                                     "message": "OTP sent to the registered number",
                                     "valid_for": OTP_VALID_FOR,
                                     "otp": {"token": "{0:04}".format(site_obj.id), "otp": sent["otp"]}  # TODO remove
                                     },
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
    # mqttc.on_message = mqttc.on_message_1



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
        print("site_name: ", site_name)
        try:
            print("Request data:",request.data)
            authenticate_device = request.data['authenticate_device']
        except Exception as err:
            authenticate_device = None

        if authenticate_device is None:
            print("token auth for new device")
            logger.info("Verify token for newly added device")
            try:
                site_obj = Site.objects.get(company_id=request.user.company_id, site_name=site_name, phone_verified=True)
                print("site_obj:", site_obj)
            except Exception as err:
                logger.error("Verify token error , {}".format(err))
                return JsonResponse({"Response": {"Status": "error"},
                                     "message": "OTP is not verified"},
                                    safe=False, status=status.HTTP_200_OK)
            try:
                print("111")
                sub_count = Subscription.objects.filter(site_id=site_obj.id).count()
                print("112")
                logger.debug(sub_count)
                print("113")
                if sub_count > 0:
                    print("114")
                    dev_obj = Device.objects.get(site_id=site_obj.id)
                    print("115")
                    response = {
                        'device_name1': dev_obj.serial_no1,
                        "device_name2": dev_obj.serial_no2,
                        "device_name3": dev_obj.serial_no3
                    }
                    print("116")
                    # site_obj.token_verified = True 
                    print("117")
                    site_obj.save()
                    print("118")
                    if dev_obj.serial_no2 and dev_obj.serial_no3:
                        print("119")
                        return JsonResponse({"Response": {"Status": "success"},
                                             "message": "Both treatment and dispensing units verified successfully!"},
                                            safe=False, status=status.HTTP_200_OK)
                    elif dev_obj.serial_no2:
                        print("120")
                        return JsonResponse({"Response": {"Status": "success"},
                                             "message": "Treatment unit verified successfully!"},
                                            safe=False, status=status.HTTP_200_OK)
                    elif dev_obj.serial_no3:
                        return JsonResponse({"Response": {"Status": "success"},
                                             "message": "Dispensing unit verified successfully!"},
                                            safe=False, status=status.HTTP_200_OK)
                return JsonResponse({"Response": {"Status": "error"},
                                    #  "message": "Token verification failed. Didn't get the token from device1"},
                                     "message": "device communications failed please turn on your device "},
                                    safe=False, status=status.HTTP_200_OK)
            except Exception as err:
                return JsonResponse({"Response": {"Status": "error"},
                                     "message": "Token verification failed, didn't get the device serial numbers over mqtt."
                                                " {}".format(err)}, safe=False, status=status.HTTP_200_OK)
        else:
            print("token auth for already existing device")
            logger.info("Verify token for already added device")
            print(authenticate_device)
            try:
                site_obj = Site.objects.get(company_id=request.user.company_id, site_name=site_name,
                                            phone_verified=True)
            except Exception as err:
                logger.error("Verify token error , {}".format(err))
                return JsonResponse({"Response": {"Status": "error"},
                                     "message": "OTP is not verified"},
                                    safe=False, status=status.HTTP_200_OK)
            try:
                sub_count = Subscription.objects.filter(site_id=site_obj.id).count()
                logger.debug(sub_count)
                if sub_count > 0:
                    dev_obj = Device.objects.get(site_id=site_obj.id)
                    response = {
                        'device_name1': dev_obj.serial_no1,
                        "device_name2": dev_obj.serial_no2,
                        "device_name3": dev_obj.serial_no3
                    }
                    site_obj.token_verified = True
                    # site_obj.token = None
                    site_obj.save()
                    len_authenticate_device = len(authenticate_device)
                    print(len_authenticate_device)
                    if (len_authenticate_device == 2) and (dev_obj.serial_no2 and dev_obj.serial_no3):
                    # if dev_obj.serial_no2 and dev_obj.serial_no3:
                        return JsonResponse({"Response": {"Status": "success"},
                                             "message": "Both treatment and dispensing units verified successfully!"},
                                            safe=False, status=status.HTTP_200_OK)

                    elif len_authenticate_device == 1 and authenticate_device[0] == "treatment_unit" and dev_obj.serial_no2:
                        return JsonResponse({"Response": {"Status": "success"},
                                             "message": "Treatment unit verified successfully!"},
                                            safe=False, status=status.HTTP_200_OK)
                    elif len_authenticate_device == 1 and authenticate_device[0] == "dispensing_unit" and dev_obj.serial_no3:
                        return JsonResponse({"Response": {"Status": "success"},
                                             "message": "Dispensing unit verified successfully!"},
                                            safe=False, status=status.HTTP_200_OK)
                return JsonResponse({"Response": {"Status": "error"},
                                     "message": "2Token verification failed. Didn't get the token from device2"},
                                    safe=False, status=status.HTTP_200_OK)
            except Exception as err:
                return JsonResponse({"Response": {"Status": "error"},
                                     "message": "Token verification failed, didn't get the device serial numbers over mqtt."
                                                " {}".format(err)}, safe=False, status=status.HTTP_200_OK)


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
            # print(device.serial_no1)
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

    # Request to send verification sms
    if request.method == 'POST':
        # phone = request.data['phone']
        # site_name = request.data['site_name']

        site_name = request.data['site_name']
        # address = request.data['address']
        # city = request.data['city']
        # state = request.data['state']
        # phone_country = "+91"
        # mob = re.sub(r"\D", "", request.data['phone'])
        # site_mob = phone_country + str(mob)

        try:
            site_obj = Site.objects.get(company_id=request.user.company_id, site_name=site_name)

            logger.info("Re-auth request for device added")
            threading.Thread(target=connect_mqtt_in_background, args=(request.user.company_id, )).start()
            # sent = site_obj.send_verification_sms(site_obj.id)
            sent = site_obj.send_verification_sms(random.randint(1000, 9999))
            logger.info(sent)
            if sent["status"]:
                return JsonResponse({"Response": {"Status": "success"},
                                     "message": "OTP sent to the registered number",
                                     "valid_for": OTP_VALID_FOR,
                                     "otp": {"token": "{0:04}".format(site_obj.id), "otp": sent["otp"]}  # TODO remove
                                     },
                                    safe=False, status=status.HTTP_200_OK)
                # return HttpResponse('', status=200)
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





@api_view(['POST'])
def obtain_token(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username and password:
        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })

    return Response({'error': 'Invalid credentials'}, status=400)
 
def dateandtime():
    year=datetime.today().strftime('%Y')
    month=datetime.today().strftime('%m')
    day=datetime.today().strftime('%d')
    hour=datetime.now().strftime('%H')
    minit=datetime.now().strftime('%M')
    second=datetime.now().strftime('%S')
    return year,month,day,hour,minit,second



qs={}
# class LastRecordsView(APIView):
    # def get(self, request):
    #     records = Errors.objects.order_by('-id')[:10]
    #     serializer = last_ten_errors(records, many=True)
    #     return Response(serializer.data)
    # def post(self, request):
    #     serializer = last_ten_errors(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=201)
    #     return Response(serializer.errors, status=400)
class LastRecordsView(viewsets.ModelViewSet):
    def dispatch(self, request, *args, **kwargs):
        my_list = [] 
        fields_to_exclude = ['model', 'pk']
        print(request.body,"BODY")
        data = json.loads(request.body)
        print(data,type(data),"last data:")
        dinfo = device_info.objects.filter(**data)
        did=dinfo[0].Device_id
        print(did,"DID***")
        last_error = Errors.objects.filter(device_id=did).order_by('-id')[:10]
        print("qsss:",last_error)
        
        # if not qs_sta:
        #     data_sta = {}
        # else:
        #     data_sta = serialize("json", qs_sta)
        #     data_sta = json.loads(data_sta)
        #     print("data_sta is:",data_sta)
        #     for item in data_sta:
        #         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
        #     data_sta = json.dumps(data_sta)
        #     data_sta = json.loads(data_sta)
        
        # response_data=[data_sta]
        # # return JsonResponse(response_data, content_type="application/json")  
        # return JsonResponse(response_data,safe=False)  


        if not last_error:
            last_error={}
        else:
            last_error = serialize("json", last_error)
            last_error = json.loads(last_error)
            for item in last_error:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
                my_list.append(item['fields'])
        last_error = json.dumps(my_list)
        last_error = json.loads(last_error)

        # data_final = {'error':last_error}
        # response_data = {
        #     #new code
        # 'data': data_final,  # Include the 'data' field
        # 'status': 200,  # Add the status field
        # 'message': "Data get successful", # Add the message field
        # # 'error':err,
        # }
        # response_data=[last_error]
        return JsonResponse(last_error, safe=False, content_type="application/json")
      
# class LastRecordsView(viewsets.ModelViewSet):
#     queryset = Errors.objects.all()
#     serializer_class = YourModelSerializer

#all data from minit table
class all_panelListAPIView(generics.ListAPIView):
    # define queryset
	queryset = treat_panel.objects.all()

	serializer_class = all_panelSerializer
class all_cndListAPIView(generics.ListAPIView):
    # define queryset
	queryset = treat_cnd_sen.objects.all()

	# specify serializer to be used
	serializer_class = all_cndSerializer
class all_tdsListAPIView(generics.ListAPIView):
    # define queryset
	queryset = treat_tds_sen.objects.all()

	# specify serializer to be used
	serializer_class = all_tdsSerializer
class all_rwpListAPIView(generics.ListAPIView):
    # define queryset
	queryset = treat_rwp.objects.all()

	# specify serializer to be used
	serializer_class = all_rwpSerializer
class all_ampv1ListAPIView(generics.ListAPIView):
    # define queryset
	queryset = treat_ampv1.objects.all()

	# specify serializer to be used
	serializer_class = all_ampv1Serializer
        
class all_ampv2ListAPIView(generics.ListAPIView):
    # define queryset
	queryset = treat_ampv2.objects.all()

	# specify serializer to be used
	serializer_class = all_ampv2Serializer
        
class all_ampv3ListAPIView(generics.ListAPIView):
    # define queryset
	queryset = treat_ampv3.objects.all()
	# specify serializer to be used
	serializer_class = all_ampv3Serializer
class all_ampv4ListAPIView(generics.ListAPIView):
    # define queryset
	queryset = treat_ampv4.objects.all()

	# specify serializer to be used
	serializer_class = all_ampv4Serializer

class all_ampv5ListAPIView(generics.ListAPIView):
    # define queryset
	queryset = treat_ampv5.objects.all()

	# specify serializer to be used
	serializer_class = all_ampv5Serializer
class all_hppListAPIView(generics.ListAPIView):
    # define queryset
	queryset = treat_hpp.objects.all()

	# specify serializer to be used
	serializer_class = all_hppSerializer
class all_F_flowsenListAPIView(generics.ListAPIView):
    # define queryset
	queryset = treat_F_flowsen.objects.all()

	# specify serializer to be used
	serializer_class = all_F_flowsenSerializer
class all_P_flowsenListAPIView(generics.ListAPIView):
    # define queryset
	queryset = treat_P_flowsen.objects.all()

	# specify serializer to be used
	serializer_class = all_P_flowsenSerializer
class all_cnd_consenListAPIView(generics.ListAPIView):
    # define queryset
	queryset = disp_cnd_consen.objects.all()

	# specify serializer to be used
	serializer_class = all_cnd_consenSerializer
class all_tds_consenListAPIView(generics.ListAPIView):
    # define queryset
	queryset = disp_tds_consen.objects.all()

	# specify serializer to be used
	serializer_class = all_tds_consenSerializer

class all_atmListAPIView(generics.ListAPIView):
    # define queryset
	queryset = disp_atm.objects.all()

	# specify serializer to be used
	serializer_class = all_atmSerializer
class all_tap1ListAPIView(generics.ListAPIView):
    # define queryset
	queryset = disp_tap1.objects.all()

	# specify serializer to be used
	serializer_class = all_tap1Serializer
class all_tap2ListAPIView(generics.ListAPIView):
    # define queryset
	queryset = disp_tap2.objects.all()

	# specify serializer to be used
	serializer_class = all_tap2Serializer
class all_tap3ListAPIView(generics.ListAPIView):
    # define queryset
	queryset = disp_tap3.objects.all()

	# specify serializer to be used
	serializer_class = all_tap3Serializer
class all_tap4ListAPIView(generics.ListAPIView):
    # define queryset
	queryset = disp_tap4.objects.all()

	# specify serializer to be used
	serializer_class = all_tap4Serializer
class all_flowsen1ListAPIView(generics.ListAPIView):
    # define queryset
	queryset = disp_flowsen1.objects.all()

	# specify serializer to be used
	serializer_class = all_flowsen1Serializer
class all_flowsen2ListAPIView(generics.ListAPIView):
    # define queryset
	queryset = disp_flowsen2.objects.all()

	# specify serializer to be used
	serializer_class = all_flowsen2Serializer
class all_flowsen3ListAPIView(generics.ListAPIView):
    # define queryset
	queryset = disp_flowsen3.objects.all()

	# specify serializer to be used
	serializer_class = all_flowsen3Serializer
class all_flowsen4ListAPIView(generics.ListAPIView):
    # define queryset
	queryset = disp_flowsen4.objects.all()

	# specify serializer to be used
	serializer_class = all_flowsen4Serializer
import json
cid=None
class site_check(viewsets.ModelViewSet):
    def dispatch(self, request, *args, **kwargs):
        fields_to_exclude = ['model', 'pk']
        print(request.body,"BODY")
        data = json.loads(request.body)
        print(data,type(data),"DATA")
        companydata=mo.Company.objects.filter(company_name=data['company_name'])
        print(companydata,type(companydata),"***")
        for i in companydata:
            global cid
            cid=i.id
        # number_of_sites=mo.Site.objects.filter(company_id=cid)
        number_of_sites=mo.Site.objects.filter(company=self.company_id)
        site_name=[]
        for sit in number_of_sites:
            site_name.append(sit.site_name)

        # dinfo = device_info.objects.filter(**data)
        # did=dinfo[0].Device_id
        # print(dinfo,type(dinfo))
        # qs_sta = treat_rwp.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
        # # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        # if not qs_sta:
        #     data_sta = {}
        # else:
        #     data_sta = serialize("json", qs_sta)
        #     data_sta = json.loads(data_sta)
        #     print("data_sta is:",data_sta)
        #     for item in data_sta:
        #         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
        #     data_sta = json.dumps(data_sta[0]["fields"])
        #     data_sta = json.loads(data_sta)
        
        # qs_set = treat_rwp.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
        # if not qs_set:
        #     data_set = {}
        # else:
        #     data_set = serialize("json", qs_set)
        #     data_set = json.loads(data_set)
        #     print("data_set is:",data_set)
        #     for item in data_set:
        #         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

        #     data_set = json.dumps(data_set[0]["fields"])
        #     data_set = json.loads(data_set)

        # # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        # last_error=Errors.objects.filter(service='rwp')
        # if not last_error:
        #     last_error={}
        # else:
        #     last_error = serialize("json", last_error)
        #     last_error = json.loads(last_error)
        #     for item in last_error:
        #         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            
        #     last_error = json.dumps(last_error[0]["fields"])
        #     last_error = json.loads(last_error)

        # data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
        response_data = {
            #new code
        'data': site_name,  # Include the 'data' field
        'status': 200,  # Add the status field
        'message': "Data get successful", # Add the message field
        # 'error':err,
        }
        response_data=[response_data]
        return JsonResponse(response_data, safe=False, content_type="application/json")

class updated_treat_rwpViewset(viewsets.ModelViewSet):

    def dispatch(self, request, *args, **kwargs):
        fields_to_exclude = ['model', 'pk']
        print(request.body,"BODY")
        data = json.loads(request.body)
        print(data,type(data),"DATA")
        dinfo = device_info.objects.filter(**data)
        did=dinfo[0].Device_id
        print(dinfo,type(dinfo))
        qs_sta = treat_rwp.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        if not qs_sta:
            data_sta = {}
        else:
            data_sta = serialize("json", qs_sta)
            data_sta = json.loads(data_sta)
            print("data_sta is:",data_sta)
            for item in data_sta:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            data_sta = json.dumps(data_sta[0]["fields"])
            data_sta = json.loads(data_sta)
        
        qs_set = treat_rwp.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
        if not qs_set:
            data_set = {}
        else:
            data_set = serialize("json", qs_set)
            data_set = json.loads(data_set)
            print("data_set is:",data_set)
            for item in data_set:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

            data_set = json.dumps(data_set[0]["fields"])
            data_set = json.loads(data_set)

        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        last_error=Errors.objects.filter(service='rwp')
        if not last_error:
            last_error={}
        else:
            last_error = serialize("json", last_error)
            last_error = json.loads(last_error)
            for item in last_error:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            
            last_error = json.dumps(last_error[0]["fields"])
            last_error = json.loads(last_error)

        data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
        response_data = {
            #new code
        'data': data_final,  # Include the 'data' field
        'status': 200,  # Add the status field
        'message': "Data get successful", # Add the message field
        # 'error':err,
        }
        response_data=[response_data]
        return JsonResponse(response_data, safe=False, content_type="application/json")
    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         did = 0
    #         data_dict = json.loads(request.body)
    #         value_list = list(data_dict.values())
    #         dinfo = device_info.objects.filter(componant_name=value_list[2], unit_type=value_list[0], company_name=value_list[1])
            
    #         for x in dinfo:
    #             did = x.Device_id
    #             cmpname = x.componant_name
    #         qs_sta = treat_rwp.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
    #         qs_set = treat_rwp.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
    #         fields_to_exclude = ['model', 'pk']
            
    #         data_sta = serialize("json", qs_sta)
    #         data_sta = json.loads(data_sta)
    #         print("Data_sta is:",data_sta)
    #         for item in data_sta:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
    #         #new code
    #         data_set = serialize("json", qs_set)
    #         data_set = json.loads(data_set)
    #         print("data_set is:",data_set)
    #         for item in data_set:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

    #         ero=Errors.objects.filter(service='rwp')
           
    #         if not data_sta and data_set:
    #             response_data = {

    #                 'data': [],  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data not found"  # Add the message field
    #             }
    #         else:     
    #             data_sta = json.dumps(data_sta[0]["fields"])
    #             data_sta = json.loads(data_sta)

    #             #new code
    #             data_set = json.dumps(data_set[0]["fields"])
    #             data_set = json.loads(data_set)
    #             last_error=Errors.objects.filter(service='rwp').last()
    #             #new code
    #             # data_final = [data_sta,data_set]
    #             data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error.e_discriptions}
    #             response_data = {
    #                  #new code
    #                 'data': data_final,  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data get successful", # Add the message field
    #                 # 'error':err,
    #             }
    #         response_data=[response_data]
    #     except Exception as e:
    #                 response_data = {
    #                     'data':e,  # Include the 'data' field
    #                     'status': 200,  # Add the status field
    #                     'message': "Exception found"  # Add the message field
                        
    #                 }
    #     return JsonResponse(response_data, safe=False, content_type="application/json")


class updated_treat_cnd_senViewset(viewsets.ModelViewSet):
	# define queryset
    def dispatch(self, request, *args, **kwargs):
        fields_to_exclude = ['model', 'pk']
        print(request.body,"BODY")
        data = json.loads(request.body)
        print(data,type(data),"DATA**********")
        dinfo = device_info.objects.filter(**data)
        print(dinfo,type(dinfo),"device_info*****")
        did=dinfo[0].Device_id
        # print(dinfo,type(dinfo))
        print("**!!!***1:",did)
        # did=dinfo[0].Device_id
        # print("**!!!***0:",did)
        qs_sta = treat_cnd_sen.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
        if not qs_sta:
            data_sta = {}
        else:
            data_sta = serialize("json", qs_sta)
            data_sta = json.loads(data_sta)
            print("data_sta is:",data_sta)
            for item in data_sta:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            data_sta = json.dumps(data_sta[0]["fields"])
            data_sta = json.loads(data_sta)
        
        qs_set = treat_cnd_sen.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
        if not qs_set:
            data_set = {}
        else:
            data_set = serialize("json", qs_set)
            data_set = json.loads(data_set)
            print("data_set is:",data_set)
            for item in data_set:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

            data_set = json.dumps(data_set[0]["fields"])
            data_set = json.loads(data_set)

        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        last_error=Errors.objects.filter(service='cnd_sen')
        if not last_error:
            last_error={}
        else:
            last_error = serialize("json", last_error)
            last_error = json.loads(last_error)
            for item in last_error:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            
            last_error = json.dumps(last_error[0]["fields"])
            last_error = json.loads(last_error)

        data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
        response_data = {
            #new code
        'data': data_final,  # Include the 'data' field
        'status': 200,  # Add the status field
        'message': "Data get successful", # Add the message field
        # 'error':err,
        }
        response_data=[response_data]
        return JsonResponse(response_data, safe=False, content_type="application/json")   
    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         did = 0
    #         data_dict = json.loads(request.body)
    #         value_list = list(data_dict.values())
    #         dinfo = device_info.objects.filter(componant_name=value_list[2], unit_type=value_list[0], company_name=value_list[1])
            
    #         for x in dinfo:
    #             did = x.Device_id
    #             cmpname = x.componant_name
            
    #         qs_sta = treat_cnd_sen.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
    #         #new code
    #         qs_set = treat_cnd_sen.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
    #         fields_to_exclude = ['model', 'pk']
            
    #         data_sta = serialize("json", qs_sta)
    #         data_sta = json.loads(data_sta)
    #         print("Data_sta is:",data_sta)
    #         for item in data_sta:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
    #         #new code
    #         data_set = serialize("json", qs_set)
    #         data_set = json.loads(data_set)
    #         print("data_set is:",data_set)
    #         for item in data_set:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

           
    #         if not data_sta and data_set:
    #             response_data = {

    #                 'data': [],  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data not found"  # Add the message field
    #             }
    #         else:     
    #             data_sta = json.dumps(data_sta[0]["fields"])
    #             data_sta = json.loads(data_sta)

    #             #new code
    #             data_set = json.dumps(data_set[0]["fields"])
    #             data_set = json.loads(data_set)
    #             last_error=Errors.objects.filter(service='cnd_sen').last()
    #             #new code
    #             # data_final = [data_sta,data_set]
    #             data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error.e_discriptions}
    #             response_data = {
    #                  #new code
    #                 'data': data_final,  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data get successful", # Add the message field
    #                 # 'error':err,
    #             }
    #         response_data=[response_data]
    #     except Exception as e:
    #                 response_data = {
    #                     'data':e,  # Include the 'data' field
    #                     'status': 200,  # Add the status field
    #                     'message': "Exception found"  # Add the message field
                        
    #                 }
    #     return JsonResponse(response_data, safe=False, content_type="application/json")
class updated_treat_tds_senViewset(viewsets.ModelViewSet):
	# define queryset
    def dispatch(self, request, *args, **kwargs):
        fields_to_exclude = ['model', 'pk']
        print(request.body,"BODY")
        data = json.loads(request.body)
        print(data,type(data),"DATA")
        dinfo = device_info.objects.filter(**data)
        did=dinfo[0].Device_id
        
        qs_sta = treat_tds_sen.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
        if not qs_sta:
            data_sta = {}
        else:
            data_sta = serialize("json", qs_sta)
            data_sta = json.loads(data_sta)
            print("data_sta is:",data_sta)
            for item in data_sta:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            data_sta = json.dumps(data_sta[0]["fields"])
            data_sta = json.loads(data_sta)
        
        qs_set = treat_tds_sen.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
        if not qs_set:
            data_set = {}
        else:
            data_set = serialize("json", qs_set)
            data_set = json.loads(data_set)
            print("data_set is:",data_set)
            for item in data_set:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

            data_set = json.dumps(data_set[0]["fields"])
            data_set = json.loads(data_set)

        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        last_error=Errors.objects.filter(service='tds_sen')
        if not last_error:
            last_error={}
        else:
            last_error = serialize("json", last_error)
            last_error = json.loads(last_error)
            for item in last_error:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            
            last_error = json.dumps(last_error[0]["fields"])
            last_error = json.loads(last_error)

        data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
        response_data = {
            #new code
        'data': data_final,  # Include the 'data' field
        'status': 200,  # Add the status field
        'message': "Data get successful", # Add the message field
        # 'error':err,
        }
        response_data=[response_data]
        return JsonResponse(response_data, safe=False, content_type="application/json")    
    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         did = 0
    #         data_dict = json.loads(request.body)
    #         value_list = list(data_dict.values())
    #         dinfo = device_info.objects.filter(componant_name=value_list[2], unit_type=value_list[0], company_name=value_list[1])
            
    #         for x in dinfo:
    #             did = x.Device_id
    #             cmpname = x.componant_name
    #         qs_sta = treat_tds_sen.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
    #         qs_set = treat_tds_sen.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
    #         fields_to_exclude = ['model', 'pk']
            
    #         data_sta = serialize("json", qs_sta)
    #         data_sta = json.loads(data_sta)
    #         print("Data_sta is:",data_sta)
    #         for item in data_sta:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
    #         #new code
    #         data_set = serialize("json", qs_set)
    #         data_set = json.loads(data_set)
    #         print("data_set is:",data_set)
    #         for item in data_set:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

           
    #         if not data_sta and data_set:
    #             response_data = {

    #                 'data': [],  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data not found"  # Add the message field
    #             }
    #         else:     
    #             data_sta = json.dumps(data_sta[0]["fields"])
    #             data_sta = json.loads(data_sta)

    #             #new code
    #             data_set = json.dumps(data_set[0]["fields"])
    #             data_set = json.loads(data_set)
    #             last_error=Errors.objects.filter(service='tds_sen').last()
    #             #new code
    #             # data_final = [data_sta,data_set]
    #             data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error.e_discriptions}
    #             response_data = {
    #                  #new code
    #                 'data': data_final,  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data get successful", # Add the message field
    #                 # 'error':err,
    #             }
    #         response_data=[response_data]
    #     except Exception as e:
    #                 response_data = {
    #                     'data':e,  # Include the 'data' field
    #                     'status': 200,  # Add the status field
    #                     'message': "Exception found"  # Add the message field
                        
    #                 }
    #     return JsonResponse(response_data, safe=False, content_type="application/json")

class updated_treat_hppViewset(viewsets.ModelViewSet):
	# define queryset
    def dispatch(self, request, *args, **kwargs):
        fields_to_exclude = ['model', 'pk']
        print(request.body,"BODY")
        data = json.loads(request.body)
        print(data,type(data),"DATA")
        dinfo = device_info.objects.filter(**data)
        did=dinfo[0].Device_id
        print(dinfo,type(dinfo))
        qs_sta = treat_hpp.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
        if not qs_sta:
            data_sta = {}
        else:
            data_sta = serialize("json", qs_sta)
            data_sta = json.loads(data_sta)
            print("data_sta is:",data_sta)
            for item in data_sta:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            data_sta = json.dumps(data_sta[0]["fields"])
            data_sta = json.loads(data_sta)
        
        qs_set = treat_hpp.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
        if not qs_set:
            data_set = {}
        else:
            data_set = serialize("json", qs_set)
            data_set = json.loads(data_set)
            print("data_set is:",data_set)
            for item in data_set:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

            data_set = json.dumps(data_set[0]["fields"])
            data_set = json.loads(data_set)

        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        last_error=Errors.objects.filter(service='hpp')
        if not last_error:
            last_error={}
        else:
            last_error = serialize("json", last_error)
            last_error = json.loads(last_error)
            for item in last_error:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            
            last_error = json.dumps(last_error[0]["fields"])
            last_error = json.loads(last_error)

        data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
        response_data = {
            #new code
        'data': data_final,  # Include the 'data' field
        'status': 200,  # Add the status field
        'message': "Data get successful", # Add the message field
        # 'error':err,
        }
        response_data=[response_data]
        return JsonResponse(response_data, safe=False, content_type="application/json")    
        
    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         did = 0
    #         data_dict = json.loads(request.body)
    #         value_list = list(data_dict.values())
    #         dinfo = device_info.objects.filter(componant_name=value_list[2], unit_type=value_list[0], company_name=value_list[1])
            
    #         for x in dinfo:
    #             did = x.Device_id
    #             cmpname = x.componant_name
            
    #         qs_sta = treat_hpp.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
    #         qs_set = treat_hpp.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
    #         fields_to_exclude = ['model', 'pk']
            
    #         data_sta = serialize("json", qs_sta)
    #         data_sta = json.loads(data_sta)
    #         print("Data_sta is:",data_sta)
    #         for item in data_sta:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
    #         #new code
    #         data_set = serialize("json", qs_set)
    #         data_set = json.loads(data_set)
    #         print("data_set is:",data_set)
    #         for item in data_set:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

           
    #         if not data_sta and data_set:
    #             response_data = {

    #                 'data': [],  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data not found"  # Add the message field
    #             }
    #         else:     
    #             data_sta = json.dumps(data_sta[0]["fields"])
    #             data_sta = json.loads(data_sta)

    #             #new code
    #             data_set = json.dumps(data_set[0]["fields"])
    #             data_set = json.loads(data_set)
    #             last_error=Errors.objects.filter(service='hpp').last()
    #             print("Errors:",last_error.e_discriptions)
    #             #new code
    #             # data_final = [data_sta,data_set]
    #             data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error.e_discriptions}
    #             response_data = {
    #                  #new code
    #                 'data': data_final,  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data get successful", # Add the message field
    #                 # 'error':err,
    #             }
    #         response_data=[response_data]
    #     except Exception as e:
    #                 response_data = {
    #                     'data':e,  # Include the 'data' field
    #                     'status': 200,  # Add the status field
    #                     'message': "Exception found"  # Add the message field
                        
    #                 }
    #     return JsonResponse(response_data, safe=False, content_type="application/json")

class updated_treat_ampv1Viewset(viewsets.ModelViewSet):
	# define queryset

    def dispatch(self, request, *args, **kwargs):
        try:
            fields_to_exclude = ['model', 'pk']
            print(request.body,"BODY")
            data = json.loads(request.body)
            print(data,type(data),"DATA")
            dinfo = device_info.objects.filter(**data)
            did=dinfo[0].Device_id
        
            print(dinfo,type(dinfo))
            qs_sta = treat_ampv1.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
            # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
            if not qs_sta:
                data_sta = {}
            else:
                data_sta = serialize("json", qs_sta)
                data_sta = json.loads(data_sta)
                print("data_sta is:",data_sta)
                for item in data_sta:
                    item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
                data_sta = json.dumps(data_sta[0]["fields"])
                data_sta = json.loads(data_sta)
            
            qs_set = treat_ampv1.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
            if not qs_set:
                data_set = {}
            else:
                data_set = serialize("json", qs_set)
                data_set = json.loads(data_set)
                print("data_set is:",data_set)
                for item in data_set:
                    item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

                data_set = json.dumps(data_set[0]["fields"])
                data_set = json.loads(data_set)

            # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
            last_error=Errors.objects.filter(service='ampv1')
            if not last_error:
                last_error={}
            else:
                last_error = serialize("json", last_error)
                last_error = json.loads(last_error)
                for item in last_error:
                    item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
                
                last_error = json.dumps(last_error[0]["fields"])
                last_error = json.loads(last_error)

            data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
            response_data = {
                #new code
            'data': data_final,  # Include the 'data' field
            'status': 200,  # Add the status field
            'message': "Data get successful", # Add the message field
            # 'error':err,
            }
            response_data=[response_data]
            return JsonResponse(response_data, safe=False, content_type="application/json")    
        except Exception as e :
            print(e)  
    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         did = 0
    #         data_dict = json.loads(request.body)
    #         value_list = list(data_dict.values())
    #         dinfo = device_info.objects.filter(componant_name=value_list[2], unit_type=value_list[0], company_name=value_list[1])
            
    #         for x in dinfo:
    #             did = x.Device_id
    #             cmpname = x.componant_name
            
    #         qs_sta = treat_ampv1.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
    #         qs_set = treat_ampv1.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
    #         fields_to_exclude = ['model', 'pk']
            
    #         data_sta = serialize("json", qs_sta)
    #         data_sta = json.loads(data_sta)
    #         print("Data_sta is:",data_sta)
    #         for item in data_sta:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
    #         #new code
    #         data_set = serialize("json", qs_set)
    #         data_set = json.loads(data_set)
    #         print("data_set is:",data_set)
    #         for item in data_set:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

           
    #         if not data_sta and data_set:
    #             response_data = {

    #                 'data': [],  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data not found"  # Add the message field
    #             }
    #         else:     
    #             data_sta = json.dumps(data_sta[0]["fields"])
    #             data_sta = json.loads(data_sta)

    #             #new code
    #             data_set = json.dumps(data_set[0]["fields"])
    #             data_set = json.loads(data_set)
    #             last_error=Errors.objects.filter(service='ampv1').last()
    #             #new code
    #             # data_final = [data_sta,data_set]
    #             data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error.e_discriptions}
    #             response_data = {
    #                  #new code
    #                 'data': data_final,  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data get successful", # Add the message field
    #                 # 'error':err,
    #             }
    #         response_data=[response_data]
    #     except Exception as e:
    #                 response_data = {
    #                     'data':e,  # Include the 'data' field
    #                     'status': 200,  # Add the status field
    #                     'message': "Exception found"  # Add the message field
                        
    #                 }
    #     return JsonResponse(response_data, safe=False, content_type="application/json")
class updated_treat_ampv2Viewset(viewsets.ModelViewSet):
	# define queryset
    def dispatch(self, request, *args, **kwargs):
        fields_to_exclude = ['model', 'pk']
        print(request.body,"BODY")
        data = json.loads(request.body)
        print(data,type(data),"DATA")
        dinfo = device_info.objects.filter(**data)
        did=dinfo[0].Device_id
        print(dinfo,type(dinfo))
        qs_sta = treat_ampv2.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        if not qs_sta:
            data_sta = {}
        else:
            data_sta = serialize("json", qs_sta)
            data_sta = json.loads(data_sta)
            print("data_sta is:",data_sta)
            for item in data_sta:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            data_sta = json.dumps(data_sta[0]["fields"])
            data_sta = json.loads(data_sta)
        
        qs_set = treat_ampv2.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
        if not qs_set:
            data_set = {}
        else:
            data_set = serialize("json", qs_set)
            data_set = json.loads(data_set)
            print("data_set is:",data_set)
            for item in data_set:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

            data_set = json.dumps(data_set[0]["fields"])
            data_set = json.loads(data_set)

        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        last_error=Errors.objects.filter(service='ampv2')
        if not last_error:
            last_error={}
        else:
            last_error = serialize("json", last_error)
            last_error = json.loads(last_error)
            for item in last_error:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            
            last_error = json.dumps(last_error[0]["fields"])
            last_error = json.loads(last_error)

        data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
        response_data = {
            #new code
        'data': data_final,  # Include the 'data' field
        'status': 200,  # Add the status field
        'message': "Data get successful", # Add the message field
        # 'error':err,
        }
        response_data=[response_data]
        return JsonResponse(response_data, safe=False, content_type="application/json")    
    
    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         did = 0
    #         data_dict = json.loads(request.body)
    #         value_list = list(data_dict.values())
    #         dinfo = device_info.objects.filter(componant_name=value_list[2], unit_type=value_list[0], company_name=value_list[1])
            
    #         for x in dinfo:
    #             did = x.Device_id
    #             cmpname = x.componant_name
            
    #         qs_sta = treat_ampv2.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
    #         qs_set = treat_ampv2.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
    #         fields_to_exclude = ['model', 'pk']
            
    #         data_sta = serialize("json", qs_sta)
    #         data_sta = json.loads(data_sta)
    #         print("Data_sta is:",data_sta)
    #         for item in data_sta:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
    #         #new code
    #         data_set = serialize("json", qs_set)
    #         data_set = json.loads(data_set)
    #         print("data_set is:",data_set)
    #         for item in data_set:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

           
    #         if not data_sta and data_set:
    #             response_data = {

    #                 'data': [],  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data not found"  # Add the message field
    #             }
    #         else:     
    #             data_sta = json.dumps(data_sta[0]["fields"])
    #             data_sta = json.loads(data_sta)

    #             #new code
    #             data_set = json.dumps(data_set[0]["fields"])
    #             data_set = json.loads(data_set)
    #             last_error=Errors.objects.filter(service='ampv2').last()
    #             #new code
    #             # data_final = [data_sta,data_set]
    #             data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error.e_discriptions}
    #             response_data = {
    #                  #new code
    #                 'data': data_final,  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data get successful", # Add the message field
    #                 # 'error':err,
    #             }
    #         response_data=[response_data]
    #     except Exception as e:
    #                 response_data = {
    #                     'data':e,  # Include the 'data' field
    #                     'status': 200,  # Add the status field
    #                     'message': "Exception found"  # Add the message field
                        
    #                 }
    #     return JsonResponse(response_data, safe=False, content_type="application/json")
    

class updated_treat_panelViewset(viewsets.ModelViewSet):
	# define queryset
    def dispatch(self, request, *args, **kwargs):
        fields_to_exclude = ['model', 'pk']
        print(request.body,"BODY")
        data = json.loads(request.body)
        print(data,type(data),"DATA")
        dinfo = device_info.objects.filter(**data)
        did=dinfo[0].Device_id
        print(dinfo,type(dinfo))
        qs_sta = treat_panel.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        if not qs_sta:
            data_sta = {}
        else:
            data_sta = serialize("json", qs_sta)
            data_sta = json.loads(data_sta)
            print("data_sta is:",data_sta)
            for item in data_sta:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            data_sta = json.dumps(data_sta[0]["fields"])
            data_sta = json.loads(data_sta)
        
        qs_set = treat_panel.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
        if not qs_set:
            data_set = {}
        else:
            data_set = serialize("json", qs_set)
            data_set = json.loads(data_set)
            print("data_set is:",data_set)
            for item in data_set:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

            data_set = json.dumps(data_set[0]["fields"])
            data_set = json.loads(data_set)

        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        last_error=Errors.objects.filter(service='panel')
        if not last_error:
            last_error={}
        else:
            last_error = serialize("json", last_error)
            last_error = json.loads(last_error)
            for item in last_error:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            
            last_error = json.dumps(last_error[0]["fields"])
            last_error = json.loads(last_error)

        data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
        response_data = {
            #new code
        'data': data_final,  # Include the 'data' field
        'status': 200,  # Add the status field
        'message': "Data get successful", # Add the message field
        # 'error':err,
        }
        response_data=[response_data]
        return JsonResponse(response_data, safe=False, content_type="application/json")    
        
    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         did = 0
    #         data_dict = json.loads(request.body)
    #         value_list = list(data_dict.values())
    #         dinfo = device_info.objects.filter(componant_name=value_list[2], unit_type=value_list[0], company_name=value_list[1])
            
    #         for x in dinfo:
    #             did = x.Device_id
    #             cmpname = x.componant_name
            
    #         qs_sta = treat_panel.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
    #         qs_set = treat_panel.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
    #         fields_to_exclude = ['model', 'pk']
            
    #         data_sta = serialize("json", qs_sta)
    #         data_sta = json.loads(data_sta)
    #         print("Data_sta is:",data_sta)
    #         for item in data_sta:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
    #         #new code
    #         data_set = serialize("json", qs_set)
    #         data_set = json.loads(data_set)
    #         print("data_set is:",data_set)
    #         for item in data_set:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

           
    #         if not data_sta and data_set:
    #             response_data = {

    #                 'data': [],  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data not found"  # Add the message field
    #             }
    #         else:     
    #             data_sta = json.dumps(data_sta[0]["fields"])
    #             data_sta = json.loads(data_sta)

    #             #new code
    #             data_set = json.dumps(data_set[0]["fields"])
    #             data_set = json.loads(data_set)
    #             last_error=Errors.objects.filter(service='panel').last()
    #             #new code
    #             # data_final = [data_sta,data_set]
    #             data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error.e_discriptions}
    #             response_data = {
    #                  #new code
    #                 'data': data_final,  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data get successful", # Add the message field
    #                 # 'error':err,
    #             }
    #         response_data=[response_data]
    #     except Exception as e:
    #                 response_data = {
    #                     'data':e,  # Include the 'data' field
    #                     'status': 200,  # Add the status field
    #                     'message': "Exception found"  # Add the message field
                        
    #                 }
    #     return JsonResponse(response_data, safe=False, content_type="application/json")

class updated_disp_atmViewset(viewsets.ModelViewSet):
	# define queryset
    def dispatch(self, request, *args, **kwargs):
        fields_to_exclude = ['model', 'pk']
        print(request.body,"BODY")
        data = json.loads(request.body)
        print(data,type(data),"DATA")
        dinfo = device_info.objects.filter(**data)
        did=dinfo[0].Device_id
        print(dinfo,type(dinfo))
        qs_sta = disp_atm.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        last_error=Errors.objects.filter(service='atm')
        if not qs_sta:
            data_sta = {}
        else:
            data_sta = serialize("json", qs_sta)
            data_sta = json.loads(data_sta)
            print("data_sta is:",data_sta)
            for item in data_sta:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            data_sta = json.dumps(data_sta[0]["fields"])
            data_sta = json.loads(data_sta)
        
        qs_set = disp_atm.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
        if not qs_set:
            data_set = {}
        else:
            data_set = serialize("json", qs_set)
            data_set = json.loads(data_set)
            print("data_set is:",data_set)
            for item in data_set:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

            data_set = json.dumps(data_set[0]["fields"])
            data_set = json.loads(data_set)

        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        last_error=Errors.objects.filter(service='atm')
        if not last_error:
            last_error={}
        else:
            last_error = serialize("json", last_error)
            last_error = json.loads(last_error)
            for item in last_error:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            
            last_error = json.dumps(last_error[0]["fields"])
            last_error = json.loads(last_error)

        data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
        response_data = {
            #new code
        'data': data_final,  # Include the 'data' field
        'status': 200,  # Add the status field
        'message': "Data get successful", # Add the message field
        # 'error':err,
        }
        response_data=[response_data]
        return JsonResponse(response_data, safe=False, content_type="application/json")    
        
    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         did = 0
    #         data_dict = json.loads(request.body)
    #         value_list = list(data_dict.values())
    #         dinfo = device_info.objects.filter(componant_name=value_list[2], unit_type=value_list[0], company_name=value_list[1])
            
    #         for x in dinfo:
    #             did = x.Device_id
    #             cmpname = x.componant_name
            
            
    #         qs_sta = disp_atm.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
    #         qs_set = disp_atm.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
    #         fields_to_exclude = ['model', 'pk']
            
    #         data_sta = serialize("json", qs_sta)
    #         data_sta = json.loads(data_sta)
    #         print("Data_sta is:",data_sta)
    #         for item in data_sta:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
    #         #new code
    #         data_set = serialize("json", qs_set)
    #         data_set = json.loads(data_set)
    #         print("data_set is:",data_set)
    #         for item in data_set:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

           
    #         if not data_sta and data_set:
    #             response_data = {

    #                 'data': [],  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data not found"  # Add the message field
    #             }
    #         else:     
    #             data_sta = json.dumps(data_sta[0]["fields"])
    #             data_sta = json.loads(data_sta)

    #             #new code
    #             data_set = json.dumps(data_set[0]["fields"])
    #             data_set = json.loads(data_set)
    #             last_error=Errors.objects.filter(service='atm').last()
    #             #new code
    #             # data_final = [data_sta,data_set]
    #             data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error.e_discriptions}
    #             response_data = {
    #                  #new code
    #                 'data': data_final,  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data get successful", # Add the message field
    #                 # 'error':err,
    #             }
    #         response_data=[response_data]
    #     except Exception as e:
    #                 response_data = {
    #                     'data':e,  # Include the 'data' field
    #                     'status': 200,  # Add the status field
    #                     'message': "Exception found"  # Add the message field
                        
    #                 }
    #     return JsonResponse(response_data, safe=False, content_type="application/json")

class getDeviceID(viewsets.ModelViewSet):
	# define queryset
    def dispatch(self, request, *args, **kwargs):
        try:
            did = 0
            data_dict = json.loads(request.body)
            value_list = list(data_dict.values())
            dinfo = device_info.objects.filter(componant_name=value_list[2], unit_type=value_list[1], company_name=value_list[0])
            # print("value_list",dinfo)
            # data = serialize("json", dinfo, fields=('Device_id'))
            # return HttpResponse(data, content_type="application/json")

            fields_to_exclude = ['model', 'pk']
                
            data = serialize("json", dinfo)
            data = json.loads(data)
            
            for item in data:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            
            
            if not data:
                response_data = {
                    'data': [],  # Include the 'data' field
                    'status': 200,  # Add the status field
                    'message': "Data not found"  # Add the message field
                }
            else:     
                data = json.dumps(data[0]["fields"])
                data = json.loads(data)
                data = [data]
                response_data = {
                    'data': data[0],  # Include the 'data' field
                    'status': 200,  # Add the status field
                    'message': "Data get successfully"  # Add the message field
                }
            response_data=[response_data]
        except Exception as e:
                    response_data = {
                        'data':e,  # Include the 'data' field
                        'status': 200,  # Add the status field
                        'message': "Exception found"  # Add the message field
                    }
        
        return JsonResponse(response_data, safe=False, content_type="application/json")


class updated_disp_tap1Viewset(viewsets.ModelViewSet):
	# define queryset
    def dispatch(self, request, *args, **kwargs):
        fields_to_exclude = ['model', 'pk']
        print(request.body,"BODY")
        data = json.loads(request.body)
        print(data,type(data),"DATA")
        dinfo = device_info.objects.filter(**data)
        did=dinfo[0].Device_id
        print(dinfo,type(dinfo))
        qs_sta = disp_tap1.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        if not qs_sta:
            data_sta = {}
        else:
            data_sta = serialize("json", qs_sta)
            data_sta = json.loads(data_sta)
            print("data_sta is:",data_sta)
            for item in data_sta:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            data_sta = json.dumps(data_sta[0]["fields"])
            data_sta = json.loads(data_sta)
        
        qs_set = disp_tap1.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
        if not qs_set:
            data_set = {}
        else:
            data_set = serialize("json", qs_set)
            data_set = json.loads(data_set)
            print("data_set is:",data_set)
            for item in data_set:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

            data_set = json.dumps(data_set[0]["fields"])
            data_set = json.loads(data_set)

        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        last_error=Errors.objects.filter(service='tap1')
        if not last_error:
            last_error={}
        else:
            last_error = serialize("json", last_error)
            last_error = json.loads(last_error)
            for item in last_error:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            
            last_error = json.dumps(last_error[0]["fields"])
            last_error = json.loads(last_error)

        data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
        response_data = {
            #new code
        'data': data_final,  # Include the 'data' field
        'status': 200,  # Add the status field
        'message': "Data get successful", # Add the message field
        # 'error':err,
        }
        response_data=[response_data]
        return JsonResponse(response_data, safe=False, content_type="application/json")    
    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         did = 0
    #         data_dict = json.loads(request.body)
    #         value_list = list(data_dict.values())
    #         dinfo = device_info.objects.filter(componant_name=value_list[2], unit_type=value_list[0], company_name=value_list[1])
            
    #         for x in dinfo:
    #             did = x.Device_id
    #             cmpname = x.componant_name
            
    #         qs_sta = disp_tap1.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
    #         qs_set = disp_tap1.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
    #         fields_to_exclude = ['model', 'pk']
            
    #         data_sta = serialize("json", qs_sta)
    #         data_sta = json.loads(data_sta)
    #         print("Data_sta is:",data_sta)
    #         for item in data_sta:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
    #         #new code
    #         data_set = serialize("json", qs_set)
    #         data_set = json.loads(data_set)
    #         print("data_set is:",data_set)
    #         for item in data_set:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

           
    #         if not data_sta and data_set:
    #             response_data = {

    #                 'data': [],  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data not found"  # Add the message field
    #             }
    #         else:     
    #             data_sta = json.dumps(data_sta[0]["fields"])
    #             data_sta = json.loads(data_sta)

    #             #new code
    #             data_set = json.dumps(data_set[0]["fields"])
    #             data_set = json.loads(data_set)
    #             last_error=Errors.objects.filter(service='tap1').last()
    #             #new code
    #             # data_final = [data_sta,data_set]
    #             data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error.e_discriptions}
    #             response_data = {
    #                  #new code
    #                 'data': data_final,  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data get successful", # Add the message field
    #                 # 'error':err,
    #             }
    #         response_data=[response_data]
    #     except Exception as e:
    #                 response_data = {
    #                     'data':e,  # Include the 'data' field
    #                     'status': 200,  # Add the status field
    #                     'message': "Exception found"  # Add the message field
                        
    #                 }
    #     return JsonResponse(response_data, safe=False, content_type="application/json")

class updated_disp_tap2Viewset(viewsets.ModelViewSet):
	# define queryset
    def dispatch(self, request, *args, **kwargs):
        fields_to_exclude = ['model', 'pk']
        print(request.body,"BODY")
        data = json.loads(request.body)
        print(data,type(data),"DATA")
        dinfo = device_info.objects.filter(**data)
        did=dinfo[0].Device_id
        print(dinfo,type(dinfo))
        qs_sta = disp_tap2.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        if not qs_sta:
            data_sta = {}
        else:
            data_sta = serialize("json", qs_sta)
            data_sta = json.loads(data_sta)
            print("data_sta is:",data_sta)
            for item in data_sta:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            data_sta = json.dumps(data_sta[0]["fields"])
            data_sta = json.loads(data_sta)
        
        qs_set = disp_tap2.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
        if not qs_set:
            data_set = {}
        else:
            data_set = serialize("json", qs_set)
            data_set = json.loads(data_set)
            print("data_set is:",data_set)
            for item in data_set:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

            data_set = json.dumps(data_set[0]["fields"])
            data_set = json.loads(data_set)

        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        last_error=Errors.objects.filter(service='tap2')
        if not last_error:
            last_error={}
        else:
            last_error = serialize("json", last_error)
            last_error = json.loads(last_error)
            for item in last_error:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            
            last_error = json.dumps(last_error[0]["fields"])
            last_error = json.loads(last_error)

        data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
        response_data = {
            #new code
        'data': data_final,  # Include the 'data' field
        'status': 200,  # Add the status field
        'message': "Data get successful", # Add the message field
        # 'error':err,
        }
        response_data=[response_data]
        return JsonResponse(response_data, safe=False, content_type="application/json")    
    
    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         did = 0
    #         data_dict = json.loads(request.body)
    #         value_list = list(data_dict.values())
    #         dinfo = device_info.objects.filter(componant_name=value_list[2], unit_type=value_list[0], company_name=value_list[1])
            
    #         for x in dinfo:
    #             did = x.Device_id
    #             cmpname = x.componant_name

    #         qs_sta = disp_tap2.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
    #         qs_set = disp_tap2.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
    #         fields_to_exclude = ['model', 'pk']
            
    #         data_sta = serialize("json", qs_sta)
    #         data_sta = json.loads(data_sta)
    #         print("Data_sta is:",data_sta)
    #         for item in data_sta:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
    #         #new code
    #         data_set = serialize("json", qs_set)
    #         data_set = json.loads(data_set)
    #         print("data_set is:",data_set)
    #         for item in data_set:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

           
    #         if not data_sta and data_set:
    #             response_data = {

    #                 'data': [],  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data not found"  # Add the message field
    #             }
    #         else:     
    #             data_sta = json.dumps(data_sta[0]["fields"])
    #             data_sta = json.loads(data_sta)

    #             #new code
    #             data_set = json.dumps(data_set[0]["fields"])
    #             data_set = json.loads(data_set)
    #             last_error=Errors.objects.filter(service='tap2').last()
    #             #new code
    #             # data_final = [data_sta,data_set]
    #             data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error.e_discriptions}
    #             response_data = {
    #                  #new code
    #                 'data': data_final,  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data get successful", # Add the message field
    #                 # 'error':err,
    #             }
    #         response_data=[response_data]
    #     except Exception as e:
    #                 response_data = {
    #                     'data':e,  # Include the 'data' field
    #                     'status': 200,  # Add the status field
    #                     'message': "Exception found"  # Add the message field
                        
    #                 }
    #     return JsonResponse(response_data, safe=False, content_type="application/json")

           
class updated_disp_tap3Viewset(viewsets.ModelViewSet):
	# define queryset
    def dispatch(self, request, *args, **kwargs):
        fields_to_exclude = ['model', 'pk']
        print(request.body,"BODY")
        data = json.loads(request.body)
        print(data,type(data),"DATA")
        dinfo = device_info.objects.filter(**data)
        did=dinfo[0].Device_id
        print(dinfo,type(dinfo))
        qs_sta = disp_tap3.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        if not qs_sta:
            data_sta = {}
        else:
            data_sta = serialize("json", qs_sta)
            data_sta = json.loads(data_sta)
            print("data_sta is:",data_sta)
            for item in data_sta:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            data_sta = json.dumps(data_sta[0]["fields"])
            data_sta = json.loads(data_sta)
        
        qs_set = disp_tap3.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
        if not qs_set:
            data_set = {}
        else:
            data_set = serialize("json", qs_set)
            data_set = json.loads(data_set)
            print("data_set is:",data_set)
            for item in data_set:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

            data_set = json.dumps(data_set[0]["fields"])
            data_set = json.loads(data_set)

        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        last_error=Errors.objects.filter(service='tap3')
        if not last_error:
            last_error={}
        else:
            last_error = serialize("json", last_error)
            last_error = json.loads(last_error)
            for item in last_error:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            
            last_error = json.dumps(last_error[0]["fields"])
            last_error = json.loads(last_error)

        data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
        response_data = {
            #new code
        'data': data_final,  # Include the 'data' field
        'status': 200,  # Add the status field
        'message': "Data get successful", # Add the message field
        # 'error':err,
        }
        response_data=[response_data]
        return JsonResponse(response_data, safe=False, content_type="application/json")    
        
    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         did = 0
    #         data_dict = json.loads(request.body)
    #         value_list = list(data_dict.values())
    #         dinfo = device_info.objects.filter(componant_name=value_list[2], unit_type=value_list[0], company_name=value_list[1])
            
    #         for x in dinfo:
    #             did = x.Device_id
    #             cmpname = x.componant_name
            
    #         qs_sta = disp_tap3.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
    #         qs_set = disp_tap3.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
    #         fields_to_exclude = ['model', 'pk']
            
    #         data_sta = serialize("json", qs_sta)
    #         data_sta = json.loads(data_sta)
    #         print("Data_sta is:",data_sta)
    #         for item in data_sta:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
    #         #new code
    #         data_set = serialize("json", qs_set)
    #         data_set = json.loads(data_set)
    #         print("data_set is:",data_set)
    #         for item in data_set:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

           
    #         if not data_sta and data_set:
    #             response_data = {

    #                 'data': [],  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data not found"  # Add the message field
    #             }
    #         else:     
    #             data_sta = json.dumps(data_sta[0]["fields"])
    #             data_sta = json.loads(data_sta)

    #             #new code
    #             data_set = json.dumps(data_set[0]["fields"])
    #             data_set = json.loads(data_set)
    #             last_error=Errors.objects.filter(service='tap3').last()
    #             #new code
    #             # data_final = [data_sta,data_set]
    #             data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error.e_discriptions}
    #             response_data = {
    #                  #new code
    #                 'data': data_final,  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data get successful", # Add the message field
    #                 # 'error':err,
    #             }
    #         response_data=[response_data]
    #     except Exception as e:
    #                 response_data = {
    #                     'data':e,  # Include the 'data' field
    #                     'status': 200,  # Add the status field
    #                     'message': "Exception found"  # Add the message field
                        
    #                 }
    #     return JsonResponse(response_data, safe=False, content_type="application/json")

class updated_disp_tap4Viewset(viewsets.ModelViewSet):
	# define queryset
    def dispatch(self, request, *args, **kwargs):
        fields_to_exclude = ['model', 'pk']
        print(request.body,"BODY")
        data = json.loads(request.body)
        print(data,type(data),"DATA")
        dinfo = device_info.objects.filter(**data)
        did=dinfo[0].Device_id
        print(dinfo,type(dinfo))
        qs_sta = disp_tap4.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        if not qs_sta:
            data_sta = {}
        else:
            data_sta = serialize("json", qs_sta)
            data_sta = json.loads(data_sta)
            print("data_sta is:",data_sta)
            for item in data_sta:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            data_sta = json.dumps(data_sta[0]["fields"])
            data_sta = json.loads(data_sta)
        
        qs_set = disp_tap4.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
        if not qs_set:
            data_set = {}
        else:
            data_set = serialize("json", qs_set)
            data_set = json.loads(data_set)
            print("data_set is:",data_set)
            for item in data_set:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

            data_set = json.dumps(data_set[0]["fields"])
            data_set = json.loads(data_set)

        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        last_error=Errors.objects.filter(service='tap4')
        if not last_error:
            last_error={}
        else:
            last_error = serialize("json", last_error)
            last_error = json.loads(last_error)
            for item in last_error:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            
            last_error = json.dumps(last_error[0]["fields"])
            last_error = json.loads(last_error)

        data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
        response_data = {
            #new code
        'data': data_final,  # Include the 'data' field
        'status': 200,  # Add the status field
        'message': "Data get successful", # Add the message field
        # 'error':err,
        }
        response_data=[response_data]
        return JsonResponse(response_data, safe=False, content_type="application/json")    
                        

    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         did = 0
    #         data_dict = json.loads(request.body)
    #         value_list = list(data_dict.values())
    #         dinfo = device_info.objects.filter(componant_name=value_list[2], unit_type=value_list[0], company_name=value_list[1])
            
    #         for x in dinfo:
    #             did = x.Device_id
    #             cmpname = x.componant_name
            
    #         qs_sta = disp_tap4.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
    #         qs_set = disp_tap4.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
    #         fields_to_exclude = ['model', 'pk']
            
    #         data_sta = serialize("json", qs_sta)
    #         data_sta = json.loads(data_sta)
    #         print("Data_sta is:",data_sta)
    #         for item in data_sta:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
    #         #new code
    #         data_set = serialize("json", qs_set)
    #         data_set = json.loads(data_set)
    #         print("data_set is:",data_set)
    #         for item in data_set:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

           
    #         if not data_sta and data_set:
    #             response_data = {

    #                 'data': [],  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data not found"  # Add the message field
    #             }
    #         else:     
    #             data_sta = json.dumps(data_sta[0]["fields"])
    #             data_sta = json.loads(data_sta)

    #             #new code
    #             data_set = json.dumps(data_set[0]["fields"])
    #             data_set = json.loads(data_set)
    #             last_error=Errors.objects.filter(service='tap4').last()
    #             #new code
    #             # data_final = [data_sta,data_set]
    #             data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error.e_discriptions}
    #             response_data = {
    #                  #new code
    #                 'data': data_final,  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data get successful", # Add the message field
    #                 # 'error':err,
    #             }
    #         response_data=[response_data]
    #     except Exception as e:
    #                 response_data = {
    #                     'data':e,  # Include the 'data' field
    #                     'status': 200,  # Add the status field
    #                     'message': "Exception found"  # Add the message field
                        
    #                 }
    #     return JsonResponse(response_data, safe=False, content_type="application/json")


class updated_disp_cnd_consenViewset(viewsets.ModelViewSet):
	# define queryset
    def dispatch(self, request, *args, **kwargs):
        fields_to_exclude = ['model', 'pk']
        print(request.body,"BODY")
        data = json.loads(request.body)
        print(data,type(data),"DATA")
        dinfo = device_info.objects.filter(**data)
        did=dinfo[0].Device_id
        print(dinfo,type(dinfo))
        qs_sta = disp_cnd_consen.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        if not qs_sta:
            data_sta = {}
        else:
            data_sta = serialize("json", qs_sta)
            data_sta = json.loads(data_sta)
            print("data_sta is:",data_sta)
            for item in data_sta:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            data_sta = json.dumps(data_sta[0]["fields"])
            data_sta = json.loads(data_sta)
        
        qs_set = disp_cnd_consen.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
        if not qs_set:
            data_set = {}
        else:
            data_set = serialize("json", qs_set)
            data_set = json.loads(data_set)
            print("data_set is:",data_set)
            for item in data_set:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

            data_set = json.dumps(data_set[0]["fields"])
            data_set = json.loads(data_set)

        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        last_error=Errors.objects.filter(service='cnd_consen')
        if not last_error:
            last_error={}
        else:
            last_error = serialize("json", last_error)
            last_error = json.loads(last_error)
            for item in last_error:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            
            last_error = json.dumps(last_error[0]["fields"])
            last_error = json.loads(last_error)

        data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
        response_data = {
            #new code
        'data': data_final,  # Include the 'data' field
        'status': 200,  # Add the status field
        'message': "Data get successful", # Add the message field
        # 'error':err,
        }
        response_data=[response_data]
        return JsonResponse(response_data, safe=False, content_type="application/json")    
    
    # queryset = disp_cnd_consen
    # serializer_class = 
    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         did = 0
    #         data_dict = json.loads(request.body)
    #         value_list = list(data_dict.values())
    #         dinfo = device_info.objects.filter(componant_name=value_list[2], unit_type=value_list[0], company_name=value_list[1])
            
    #         for x in dinfo:
    #             did = x.Device_id
    #             cmpname = x.componant_name
            
    #         qs_sta = disp_cnd_consen.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
    #         qs_set = disp_cnd_consen.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
    #         fields_to_exclude = ['model', 'pk']
            
    #         data_sta = serialize("json", qs_sta)
    #         data_sta = json.loads(data_sta)
    #         print("Data_sta is:",data_sta)
    #         for item in data_sta:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
    #         #new code
    #         data_set = serialize("json", qs_set)
    #         data_set = json.loads(data_set)
    #         print("data_set is:",data_set)
    #         for item in data_set:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

           
    #         if not data_sta and data_set:
    #             response_data = {

    #                 'data': [],  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data not found"  # Add the message field
    #             }
    #         else:     
    #             data_sta = json.dumps(data_sta[0]["fields"])
    #             data_sta = json.loads(data_sta)

    #             #new code
    #             data_set = json.dumps(data_set[0]["fields"])
    #             data_set = json.loads(data_set)
    #             last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
    #             #new code
    #             # data_final = [data_sta,data_set]
    #             data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error.e_discriptions}
    #             response_data = {
    #                  #new code
    #                 'data': data_final,  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data get successful", # Add the message field
    #                 # 'error':err,
    #             }
    #         response_data=[response_data]
    #     except Exception as e:
    #                 response_data = {
    #                     'data':e,  # Include the 'data' field
    #                     'status': 200,  # Add the status field
    #                     'message': "Exception found"  # Add the message field
                        
    #                 }
    #     return JsonResponse(response_data, safe=False, content_type="application/json")

class updated_disp_tds_consenViewset(viewsets.ModelViewSet):
    # define queryset
    def dispatch(self, request, *args, **kwargs):
        fields_to_exclude = ['model', 'pk']
        print(request.body,"BODY")
        data = json.loads(request.body)
        print(data,type(data),"DATA")
        dinfo = device_info.objects.filter(**data)
        did=dinfo[0].Device_id
        print(dinfo,type(dinfo))
        qs_sta = disp_tds_consen.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        if not qs_sta:
            data_sta = {}
        else:
            data_sta = serialize("json", qs_sta)
            data_sta = json.loads(data_sta)
            print("data_sta is:",data_sta)
            for item in data_sta:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            data_sta = json.dumps(data_sta[0]["fields"])
            data_sta = json.loads(data_sta)
        
        qs_set = disp_tds_consen.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
        if not qs_set:
            data_set = {}
        else:
            data_set = serialize("json", qs_set)
            data_set = json.loads(data_set)
            print("data_set is:",data_set)
            for item in data_set:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

            data_set = json.dumps(data_set[0]["fields"])
            data_set = json.loads(data_set)

        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        last_error=Errors.objects.filter(service='tds_consen')
        if not last_error:
            last_error={}
        else:
            last_error = serialize("json", last_error)
            last_error = json.loads(last_error)
            for item in last_error:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            
            last_error = json.dumps(last_error[0]["fields"])
            last_error = json.loads(last_error)

        data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
        response_data = {
            #new code
        'data': data_final,  # Include the 'data' field
        'status': 200,  # Add the status field
        'message': "Data get successful", # Add the message field
        # 'error':err,
        }
        response_data=[response_data]
        return JsonResponse(response_data, safe=False, content_type="application/json")    
        
    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         did = 0
    #         data_dict = json.loads(request.body)
    #         value_list = list(data_dict.values())
    #         dinfo = device_info.objects.filter(componant_name=value_list[2], unit_type=value_list[0], company_name=value_list[1])
            
    #         for x in dinfo:
    #             did = x.Device_id
    #             cmpname = x.componant_name
            
    #         qs_sta = disp_tds_consen.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
    #         qs_set = disp_tds_consen.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
    #         fields_to_exclude = ['model', 'pk']
            
    #         data_sta = serialize("json", qs_sta)
    #         data_sta = json.loads(data_sta)
    #         print("Data_sta is:",data_sta)
    #         for item in data_sta:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
    #         #new code
    #         data_set = serialize("json", qs_set)
    #         data_set = json.loads(data_set)
    #         print("data_set is:",data_set)
    #         for item in data_set:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

        
    #         if not data_sta and data_set:
    #             response_data = {

    #                 'data': [],  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data not found"  # Add the message field
    #             }
    #         else:     
    #             data_sta = json.dumps(data_sta[0]["fields"])
    #             data_sta = json.loads(data_sta)

    #             #new code
    #             data_set = json.dumps(data_set[0]["fields"])
    #             data_set = json.loads(data_set)
    #             last_error=Errors.objects.filter(service='tds_consen').last()
    #             #new code
    #             # data_final = [data_sta,data_set]
    #             data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error.e_discriptions}
    #             response_data = {
    #                 #new code
    #                 'data': data_final,  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data get successful", # Add the message field
    #                 # 'error':err,
    #             }
    #         response_data=[response_data]
    #     except Exception as e:
    #                 response_data = {
    #                     'data':e,  # Include the 'data' field
    #                     'status': 200,  # Add the status field
    #                     'message': "Exception found"  # Add the message field
                        
    #                 }
    #     return JsonResponse(response_data, safe=False, content_type="application/json")

    
class updated_treat_F_flowsenViewset(viewsets.ModelViewSet):
	# define queryset
    def dispatch(self, request, *args, **kwargs):
        fields_to_exclude = ['model', 'pk']
        print(request.body,"BODY")
        data = json.loads(request.body)
        print(data,type(data),"DATA")
        dinfo = device_info.objects.filter(**data)
        did=dinfo[0].Device_id
        print(dinfo,type(dinfo))
        qs_sta = treat_F_flowsen.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        if not qs_sta:
            data_sta = {}
        else:
            data_sta = serialize("json", qs_sta)
            data_sta = json.loads(data_sta)
            print("data_sta is:",data_sta)
            for item in data_sta:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            data_sta = json.dumps(data_sta[0]["fields"])
            data_sta = json.loads(data_sta)
        
        qs_set = treat_F_flowsen.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
        if not qs_set:
            data_set = {}
        else:
            data_set = serialize("json", qs_set)
            data_set = json.loads(data_set)
            print("data_set is:",data_set)
            for item in data_set:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

            data_set = json.dumps(data_set[0]["fields"])
            data_set = json.loads(data_set)

        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        last_error=Errors.objects.filter(service='F_flowsen')
        if not last_error:
            last_error={}
        else:
            last_error = serialize("json", last_error)
            last_error = json.loads(last_error)
            for item in last_error:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            
            last_error = json.dumps(last_error[0]["fields"])
            last_error = json.loads(last_error)

        data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
        response_data = {
            #new code
        'data': data_final,  # Include the 'data' field
        'status': 200,  # Add the status field
        'message': "Data get successful", # Add the message field
        # 'error':err,
        }
        response_data=[response_data]
        return JsonResponse(response_data, safe=False, content_type="application/json")    
        
    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         did = 0
    #         data_dict = json.loads(request.body)
    #         value_list = list(data_dict.values())
    #         dinfo = device_info.objects.filter(componant_name=value_list[2], unit_type=value_list[0], company_name=value_list[1])
            
    #         for x in dinfo:
    #             did = x.Device_id
    #             cmpname = x.componant_name
            
    #         qs_sta = treat_F_flowsen.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
    #         qs_set = treat_F_flowsen.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
    #         fields_to_exclude = ['model', 'pk']
            
    #         data_sta = serialize("json", qs_sta)
    #         data_sta = json.loads(data_sta)
    #         print("Data_sta is:",data_sta)
    #         for item in data_sta:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
    #         #new code
    #         data_set = serialize("json", qs_set)
    #         data_set = json.loads(data_set)
    #         print("data_set is:",data_set)
    #         for item in data_set:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

           
    #         if not data_sta and data_set:
    #             response_data = {

    #                 'data': [],  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data not found"  # Add the message field
    #             }
    #         else:     
    #             data_sta = json.dumps(data_sta[0]["fields"])
    #             data_sta = json.loads(data_sta)

    #             #new code
    #             data_set = json.dumps(data_set[0]["fields"])
    #             data_set = json.loads(data_set)
    #             last_error=Errors.objects.filter(service='F_flowsen').last()
    #             #new code
    #             # data_final = [data_sta,data_set]
    #             data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error.e_discriptions}
    #             response_data = {
    #                  #new code
    #                 'data': data_final,  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data get successful", # Add the message field
    #                 # 'error':err,
    #             }
    #         response_data=[response_data]
    #     except Exception as e:
    #                 response_data = {
    #                     'data':e,  # Include the 'data' field
    #                     'status': 200,  # Add the status field
    #                     'message': "Exception found"  # Add the message field
                        
    #                 }
    #     return JsonResponse(response_data, safe=False, content_type="application/json")

class getDeviceID(viewsets.ModelViewSet):
	# define queryset
    def dispatch(self, request, *args, **kwargs):
        try:
            did = 0
            data_dict = json.loads(request.body)
            value_list = list(data_dict.values())
            dinfo = device_info.objects.filter(componant_name=value_list[2], unit_type=value_list[1], company_name=value_list[0])
            # print("value_list",dinfo)
            # data = serialize("json", dinfo, fields=('Device_id'))
            # return HttpResponse(data, content_type="application/json")

            fields_to_exclude = ['model', 'pk']
                
            data = serialize("json", dinfo)
            data = json.loads(data)
            
            for item in data:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            
            
            if not data:
                response_data = {
                    'data': [],  # Include the 'data' field
                    'status': 200,  # Add the status field
                    'message': "Data not found"  # Add the message field
                }
            else:     
                data = json.dumps(data[0]["fields"])
                data = json.loads(data)
                data = [data]
                response_data = {
                    'data': data[0],  # Include the 'data' field
                    'status': 200,  # Add the status field
                    'message': "Data get successfully"  # Add the message field
                }
            response_data=[response_data]
        except Exception as e:
                    response_data = {
                        'data':e,  # Include the 'data' field
                        'status': 200,  # Add the status field
                        'message': "Exception found"  # Add the message field
                    }
        
        return JsonResponse(response_data, safe=False, content_type="application/json")

class updated_treat_P_flowsenViewset(viewsets.ModelViewSet):
	# define queryset
    def dispatch(self, request, *args, **kwargs):
        fields_to_exclude = ['model', 'pk']
        print(request.body,"BODY")
        data = json.loads(request.body)
        print(data,type(data),"DATA")
        dinfo = device_info.objects.filter(**data)
        did=dinfo[0].Device_id
        print(dinfo,type(dinfo))
        qs_sta = treat_P_flowsen.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        if not qs_sta:
            data_sta = {}
        else:
            data_sta = serialize("json", qs_sta)
            data_sta = json.loads(data_sta)
            print("data_sta is:",data_sta)
            for item in data_sta:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            data_sta = json.dumps(data_sta[0]["fields"])
            data_sta = json.loads(data_sta)
        
        qs_set = treat_P_flowsen.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
        if not qs_set:
            data_set = {}
        else:
            data_set = serialize("json", qs_set)
            data_set = json.loads(data_set)
            print("data_set is:",data_set)
            for item in data_set:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

            data_set = json.dumps(data_set[0]["fields"])
            data_set = json.loads(data_set)

        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        last_error=Errors.objects.filter(service='P_flowsen')
        if not last_error:
            last_error={}
        else:
            last_error = serialize("json", last_error)
            last_error = json.loads(last_error)
            for item in last_error:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            
            last_error = json.dumps(last_error[0]["fields"])
            last_error = json.loads(last_error)

        data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
        response_data = {
            #new code
        'data': data_final,  # Include the 'data' field
        'status': 200,  # Add the status field
        'message': "Data get successful", # Add the message field
        # 'error':err,
        }
        response_data=[response_data]
        return JsonResponse(response_data, safe=False, content_type="application/json")    
                        
#     def dispatch(self, request, *args, **kwargs):
#         try:
#             did = 0
#             data_dict = json.loads(request.body)
#             value_list = list(data_dict.values())
#             dinfo = device_info.objects.filter(componant_name=value_list[2], unit_type=value_list[0], company_name=value_list[1])
            
#             for x in dinfo:
#                 did = x.Device_id
#                 cmpname = x.componant_name
            
#             qs_sta = treat_P_flowsen.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
#             qs_set = treat_P_flowsen.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
#             fields_to_exclude = ['model', 'pk']
            
#             data_sta = serialize("json", qs_sta)
#             data_sta = json.loads(data_sta)
#             print("Data_sta is:",data_sta)
#             for item in data_sta:
#                 item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
#             #new code
#             data_set = serialize("json", qs_set)
#             data_set = json.loads(data_set)
#             print("data_set is:",data_set)
#             for item in data_set:
#                 item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

           
#             if not data_sta and data_set:
#                 response_data = {

#                     'data': [],  # Include the 'data' field
#                     'status': 200,  # Add the status field
#                     'message': "Data not found"  # Add the message field
#                 }
#             else:     
#                 data_sta = json.dumps(data_sta[0]["fields"])
#                 data_sta = json.loads(data_sta)

#                 #new code
#                 data_set = json.dumps(data_set[0]["fields"])
#                 data_set = json.loads(data_set)
#                 last_error=Errors.objects.filter(service='P_flowsen').last()
#                 #new code
#                 # data_final = [data_sta,data_set]
#                 data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error.e_discriptions}
#                 response_data = {
#                      #new code
#                     'data': data_final,  # Include the 'data' field
#                     'status': 200,  # Add the status field
#                     'message': "Data get successful", # Add the message field
#                     # 'error':err,
#                 }
#             response_data=[response_data]
#         except Exception as e:
#                     response_data = {
#                         'data':e,  # Include the 'data' field
#                         'status': 200,  # Add the status field
#                         'message': "Exception found"  # Add the message field
                        
#                     }
#         return JsonResponse(response_data, safe=False, content_type="application/json")

class updated_disp_flowsen1Viewset(viewsets.ModelViewSet):
	# define queryset

    def dispatch(self, request, *args, **kwargs):
        fields_to_exclude = ['model', 'pk']
        print(request.body,"BODY")
        data = json.loads(request.body)
        print(data,type(data),"DATA")
        dinfo = device_info.objects.filter(**data)
        did=dinfo[0].Device_id
        print(dinfo,type(dinfo))
        qs_sta = disp_flowsen1.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        if not qs_sta:
            data_sta = {}
        else:
            data_sta = serialize("json", qs_sta)
            data_sta = json.loads(data_sta)
            print("data_sta is:",data_sta)
            for item in data_sta:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            data_sta = json.dumps(data_sta[0]["fields"])
            data_sta = json.loads(data_sta)
        
        qs_set = disp_flowsen1.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
        if not qs_set:
            data_set = {}
        else:
            data_set = serialize("json", qs_set)
            data_set = json.loads(data_set)
            print("data_set is:",data_set)
            for item in data_set:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

            data_set = json.dumps(data_set[0]["fields"])
            data_set = json.loads(data_set)

        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        last_error=Errors.objects.filter(service='flowsen1')
        if not last_error:
            last_error={}
        else:
            last_error = serialize("json", last_error)
            last_error = json.loads(last_error)
            for item in last_error:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            
            last_error = json.dumps(last_error[0]["fields"])
            last_error = json.loads(last_error)

        data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
        response_data = {
            #new code
        'data': data_final,  # Include the 'data' field
        'status': 200,  # Add the status field
        'message': "Data get successful", # Add the message field
        # 'error':err,
        }
        response_data=[response_data]
        return JsonResponse(response_data, safe=False, content_type="application/json")    
    
    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         did = 0
    #         data_dict = json.loads(request.body)
    #         value_list = list(data_dict.values())
    #         dinfo = device_info.objects.filter(componant_name=value_list[2], unit_type=value_list[0], company_name=value_list[1])
            
    #         for x in dinfo:
    #             did = x.Device_id
    #             cmpname = x.componant_name
            
    #         qs_sta = disp_flowsen1.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
    #         qs_set = disp_flowsen1.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
    #         fields_to_exclude = ['model', 'pk']
            
    #         data_sta = serialize("json", qs_sta)
    #         data_sta = json.loads(data_sta)
    #         print("Data_sta is:",data_sta)
    #         for item in data_sta:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
    #         #new code
    #         data_set = serialize("json", qs_set)
    #         data_set = json.loads(data_set)
    #         print("data_set is:",data_set)
    #         for item in data_set:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

           
    #         if not data_sta and data_set:
    #             response_data = {

    #                 'data': [],  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data not found"  # Add the message field
    #             }
    #         else:     
    #             data_sta = json.dumps(data_sta[0]["fields"])
    #             data_sta = json.loads(data_sta)

    #             #new code
    #             data_set = json.dumps(data_set[0]["fields"])
    #             data_set = json.loads(data_set)
    #             last_error=Errors.objects.filter(service='flowsen1').last()
    #             #new code
    #             # data_final = [data_sta,data_set]
    #             data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error.e_discriptions}
    #             response_data = {
    #                  #new code
    #                 'data': data_final,  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data get successful", # Add the message field
    #                 # 'error':err,
    #             }
    #         response_data=[response_data]
    #     except Exception as e:
    #                 response_data = {
    #                     'data':e,  # Include the 'data' field
    #                     'status': 200,  # Add the status field
    #                     'message': "Exception found"  # Add the message field
                        
    #                 }
    #     return JsonResponse(response_data, safe=False, content_type="application/json")

class updated_disp_flowsen2Viewset(viewsets.ModelViewSet):
	# define queryset
    def dispatch(self, request, *args, **kwargs):
        fields_to_exclude = ['model', 'pk']
        print(request.body,"BODY")
        data = json.loads(request.body)
        print(data,type(data),"DATA")
        dinfo = device_info.objects.filter(**data)
        did=dinfo[0].Device_id
        print(dinfo,type(dinfo))
        qs_sta = disp_flowsen2.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        if not qs_sta:
            data_sta = {}
        else:
            data_sta = serialize("json", qs_sta)
            data_sta = json.loads(data_sta)
            print("data_sta is:",data_sta)
            for item in data_sta:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            data_sta = json.dumps(data_sta[0]["fields"])
            data_sta = json.loads(data_sta)
        
        qs_set = disp_flowsen2.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
        if not qs_set:
            data_set = {}
        else:
            data_set = serialize("json", qs_set)
            data_set = json.loads(data_set)
            print("data_set is:",data_set)
            for item in data_set:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

            data_set = json.dumps(data_set[0]["fields"])
            data_set = json.loads(data_set)

        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        last_error=Errors.objects.filter(service='flowsen2')
        if not last_error:
            last_error={}
        else:
            last_error = serialize("json", last_error)
            last_error = json.loads(last_error)
            for item in last_error:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            
            last_error = json.dumps(last_error[0]["fields"])
            last_error = json.loads(last_error)

        data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
        response_data = {
            #new code
        'data': data_final,  # Include the 'data' field
        'status': 200,  # Add the status field
        'message': "Data get successful", # Add the message field
        # 'error':err,
        }
        response_data=[response_data]
        return JsonResponse(response_data, safe=False, content_type="application/json")    
                            
                       
    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         did = 0
    #         data_dict = json.loads(request.body)
    #         value_list = list(data_dict.values())
    #         dinfo = device_info.objects.filter(componant_name=value_list[2], unit_type=value_list[0], company_name=value_list[1])
            
    #         for x in dinfo:
    #             did = x.Device_id
    #             cmpname = x.componant_name
            
    #         qs_sta = disp_flowsen2.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
    #         qs_set = disp_flowsen2.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
    #         fields_to_exclude = ['model', 'pk']
            
    #         data_sta = serialize("json", qs_sta)
    #         data_sta = json.loads(data_sta)
    #         print("Data_sta is:",data_sta)
    #         for item in data_sta:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
    #         #new code
    #         data_set = serialize("json", qs_set)
    #         data_set = json.loads(data_set)
    #         print("data_set is:",data_set)
    #         for item in data_set:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

           
    #         if not data_sta and data_set:
    #             response_data = {

    #                 'data': [],  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data not found"  # Add the message field
    #             }
    #         else:     
    #             data_sta = json.dumps(data_sta[0]["fields"])
    #             data_sta = json.loads(data_sta)

    #             #new code
    #             data_set = json.dumps(data_set[0]["fields"])
    #             data_set = json.loads(data_set)
    #             last_error=Errors.objects.filter(service='flowsen2').last()
    #             #new code
    #             # data_final = [data_sta,data_set]
    #             data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error.e_discriptions}
    #             response_data = {
    #                  #new code
    #                 'data': data_final,  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data get successful", # Add the message field
    #                 # 'error':err,
    #             }
    #         response_data=[response_data]
    #     except Exception as e:
    #                 response_data = {
    #                     'data':e,  # Include the 'data' field
    #                     'status': 200,  # Add the status field
    #                     'message': "Exception found"  # Add the message field
                        
    #                 }
    #     return JsonResponse(response_data, safe=False, content_type="application/json")

class updated_disp_flowsen3Viewset(viewsets.ModelViewSet):
	# define queryset
    def dispatch(self, request, *args, **kwargs):
        fields_to_exclude = ['model', 'pk']
        print(request.body,"BODY")
        data = json.loads(request.body)
        print(data,type(data),"DATA")
        dinfo = device_info.objects.filter(**data)
        did=dinfo[0].Device_id
        print(dinfo,type(dinfo))
        qs_sta = disp_flowsen3.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        if not qs_sta:
            data_sta = {}
        else:
            data_sta = serialize("json", qs_sta)
            data_sta = json.loads(data_sta)
            print("data_sta is:",data_sta)
            for item in data_sta:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            data_sta = json.dumps(data_sta[0]["fields"])
            data_sta = json.loads(data_sta)
        
        qs_set = disp_flowsen3.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
        if not qs_set:
            data_set = {}
        else:
            data_set = serialize("json", qs_set)
            data_set = json.loads(data_set)
            print("data_set is:",data_set)
            for item in data_set:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

            data_set = json.dumps(data_set[0]["fields"])
            data_set = json.loads(data_set)

        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        last_error=Errors.objects.filter(service='flowsen3')
        if not last_error:
            last_error={}
        else:
            last_error = serialize("json", last_error)
            last_error = json.loads(last_error)
            for item in last_error:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            
            last_error = json.dumps(last_error[0]["fields"])
            last_error = json.loads(last_error)

        data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
        response_data = {
            #new code
        'data': data_final,  # Include the 'data' field
        'status': 200,  # Add the status field
        'message': "Data get successful", # Add the message field
        # 'error':err,
        }
        response_data=[response_data]
        return JsonResponse(response_data, safe=False, content_type="application/json")    
                        
                          
    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         did = 0
    #         data_dict = json.loads(request.body)
    #         value_list = list(data_dict.values())
    #         dinfo = device_info.objects.filter(componant_name=value_list[2], unit_type=value_list[0], company_name=value_list[1])
            
    #         for x in dinfo:
    #             did = x.Device_id
    #             cmpname = x.componant_name
            
    #         qs_sta = disp_flowsen3.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
    #         qs_set = disp_flowsen3.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
    #         fields_to_exclude = ['model', 'pk']
            
    #         data_sta = serialize("json", qs_sta)
    #         data_sta = json.loads(data_sta)
    #         print("Data_sta is:",data_sta)
    #         for item in data_sta:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
    #         #new code
    #         data_set = serialize("json", qs_set)
    #         data_set = json.loads(data_set)
    #         print("data_set is:",data_set)
    #         for item in data_set:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

           
    #         if not data_sta and data_set:
    #             response_data = {

    #                 'data': [],  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data not found"  # Add the message field
    #             }
    #         else:     
    #             data_sta = json.dumps(data_sta[0]["fields"])
    #             data_sta = json.loads(data_sta)

    #             #new code
    #             data_set = json.dumps(data_set[0]["fields"])
    #             data_set = json.loads(data_set)
    #             last_error=Errors.objects.filter(service='flowsen3').last()
    #             #new code
    #             # data_final = [data_sta,data_set]
    #             data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error.e_discriptions}
    #             response_data = {
    #                  #new code
    #                 'data': data_final,  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data get successful", # Add the message field
    #                 # 'error':err,
    #             }
    #         response_data=[response_data]
    #     except Exception as e:
    #                 response_data = {
    #                     'data':e,  # Include the 'data' field
    #                     'status': 200,  # Add the status field
    #                     'message': "Exception found"  # Add the message field
                        
    #                 }
    #     return JsonResponse(response_data, safe=False, content_type="application/json")

class updated_disp_flowsen4Viewset(viewsets.ModelViewSet):
	# define queryset
    def dispatch(self, request, *args, **kwargs):
        fields_to_exclude = ['model', 'pk']
        print(request.body,"BODY")
        data = json.loads(request.body)
        print(data,type(data),"DATA")
        dinfo = device_info.objects.filter(**data)
        did=dinfo[0].Device_id
        print(dinfo,type(dinfo))
        qs_sta = disp_flowsen4.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        if not qs_sta:
            data_sta = {}
        else:
            data_sta = serialize("json", qs_sta)
            data_sta = json.loads(data_sta)
            print("data_sta is:",data_sta)
            for item in data_sta:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            data_sta = json.dumps(data_sta[0]["fields"])
            data_sta = json.loads(data_sta)
        
        qs_set = disp_flowsen4.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
        if not qs_set:
            data_set = {}
        else:
            data_set = serialize("json", qs_set)
            data_set = json.loads(data_set)
            print("data_set is:",data_set)
            for item in data_set:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

            data_set = json.dumps(data_set[0]["fields"])
            data_set = json.loads(data_set)

        # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
        last_error=Errors.objects.filter(service='flowsen4')
        if not last_error:
            last_error={}
        else:
            last_error = serialize("json", last_error)
            last_error = json.loads(last_error)
            for item in last_error:
                item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            
            last_error = json.dumps(last_error[0]["fields"])
            last_error = json.loads(last_error)

        data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
        response_data = {
            #new code
        'data': data_final,  # Include the 'data' field
        'status': 200,  # Add the status field
        'message': "Data get successful", # Add the message field
        # 'error':err,
        }
        response_data=[response_data]
        return JsonResponse(response_data, safe=False, content_type="application/json")    
                    
    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         did = 0
    #         data_dict = json.loads(request.body)
    #         value_list = list(data_dict.values())
    #         dinfo = device_info.objects.filter(componant_name=value_list[2], unit_type=value_list[0], company_name=value_list[1])
            
    #         for x in dinfo:
    #             did = x.Device_id
    #             cmpname = x.componant_name
            
    #         qs_sta = disp_flowsen4.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
    #         qs_set = disp_flowsen4.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
    #         fields_to_exclude = ['model', 'pk']
            
    #         data_sta = serialize("json", qs_sta)
    #         data_sta = json.loads(data_sta)
    #         print("Data_sta is:",data_sta)
    #         for item in data_sta:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
    #         #new code
    #         data_set = serialize("json", qs_set)
    #         data_set = json.loads(data_set)
    #         print("data_set is:",data_set)
    #         for item in data_set:
    #             item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

           
    #         if not data_sta and data_set:
    #             response_data = {

    #                 'data': [],  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data not found"  # Add the message field
    #             }
    #         else:     
    #             data_sta = json.dumps(data_sta[0]["fields"])
    #             data_sta = json.loads(data_sta)

    #             #new code
    #             data_set = json.dumps(data_set[0]["fields"])
    #             data_set = json.loads(data_set)
    #             last_error=Errors.objects.filter(service='flowsen4').last()
    #             #new code
    #             # data_final = [data_sta,data_set]
    #             data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error.e_discriptions}
    #             response_data = {
    #                  #new code
    #                 'data': data_final,  # Include the 'data' field
    #                 'status': 200,  # Add the status field
    #                 'message': "Data get successful", # Add the message field
    #                 # 'error':err,
    #             }
    #         response_data=[response_data]
    #     except Exception as e:
    #                 response_data = {
    #                     'data':e,  # Include the 'data' field
    #                     'status': 200,  # Add the status field
    #                     'message': "Exception found"  # Add the message field
                        
    #                 }
    #     return JsonResponse(response_data, safe=False, content_type="application/json")
class cnd_YearlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = cnd_repo_yearly.objects.all()

	# specify serializer to be used
	serializer_class = cnd_YearlySerializer
                
        
class cnd_HourlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = cnd_repo_hourly.objects.all()

	# specify serializer to be used
	serializer_class = cnd_HourlySerializer
        
class cnd_MonthlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = cnd_repo_monthly.objects.all()

	# specify serializer to be used
	serializer_class = cnd_MonthlySerializer
        
class cnd_DailyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = cnd_repo_daily.objects.all()

	# specify serializer to be used
	serializer_class = cnd_DailySerializer
class tds_YearlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = tds_repo_yearly.objects.all()

	# specify serializer to be used
	serializer_class = tds_YearlySerializer
                
        
class tds_HourlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = tds_repo_hourly.objects.all()

	# specify serializer to be used
	serializer_class = tds_HourlySerializer
        
class tds_MonthlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = tds_repo_monthly.objects.all()

	# specify serializer to be used
	serializer_class = tds_MonthlySerializer
        
class tds_DailyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = tds_repo_daily.objects.all()

	# specify serializer to be used
	serializer_class = tds_DailySerializer
class rwp_YearlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = rwp_repo_yearly.objects.all()

	# specify serializer to be used
	serializer_class = rwp_YearlySerializer
                
        
class rwp_HourlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = rwp_repo_hourly.objects.all()

	# specify serializer to be used
	serializer_class = rwp_HourlySerializer
        
class rwp_MonthlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = rwp_repo_monthly.objects.all()

	# specify serializer to be used
	serializer_class = rwp_MonthlySerializer
        
class rwp_DailyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = rwp_repo_daily.objects.all()

	# specify serializer to be used
	serializer_class = rwp_DailySerializer

class hpp_YearlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = hpp_repo_yearly.objects.all()

	# specify serializer to be used
	serializer_class = hpp_YearlySerializer
                
        
class hpp_HourlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = hpp_repo_hourly.objects.all()

	# specify serializer to be used
	serializer_class = hpp_HourlySerializer
        
class hpp_MonthlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = hpp_repo_monthly.objects.all()

	# specify serializer to be used
	serializer_class = hpp_MonthlySerializer
        
class hpp_DailyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = hpp_repo_daily.objects.all()

	# specify serializer to be used
	serializer_class = hpp_DailySerializer
        

class panel_YearlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = hpp_repo_yearly.objects.all()

	# specify serializer to be used
	serializer_class = hpp_YearlySerializer
                
        
class panel_HourlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = panel_repo_hourly.objects.all()

	# specify serializer to be used
	serializer_class = panel_HourlySerializer
        
class panel_MonthlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = panel_repo_monthly.objects.all()

	# specify serializer to be used
	serializer_class = panel_MonthlySerializer
        
class panel_DailyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = panel_repo_daily.objects.all()

	# specify serializer to be used
	serializer_class = panel_DailySerializer
        

class F_flowsen_YearlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = F_flowsen_repo_yearly.objects.all()

	# specify serializer to be used
	serializer_class = F_flowsen_YearlySerializer
class P_flowsen_YearlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = P_flowsen_repo_yearly.objects.all()

	# specify serializer to be used
	serializer_class = P_flowsen_YearlySerializer
                
        
class F_flowsen_HourlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = F_flowsen_repo_hourly.objects.all()

	# specify serializer to be used
	serializer_class = F_flowsen_HourlySerializer
        
class P_flowsen_HourlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = P_flowsen_repo_hourly.objects.all()

	# specify serializer to be used
	serializer_class = P_flowsen_HourlySerializer
        
class F_flowsen_MonthlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = F_flowsen_repo_monthly.objects.all()

	# specify serializer to be used
	serializer_class = F_flowsen_MonthlySerializer
        
class P_flowsen_MonthlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = P_flowsen_repo_monthly.objects.all()

	# specify serializer to be used
	serializer_class = P_flowsen_MonthlySerializer
        
class F_flowsen_DailyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = F_flowsen_repo_daily.objects.all()

	# specify serializer to be used
	serializer_class = F_flowsen_DailySerializer       
        
class P_flowsen_DailyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = P_flowsen_repo_daily.objects.all()

	# specify serializer to be used
	serializer_class = P_flowsen_DailySerializer       
        

class ampv1_YearlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = ampv1_repo_yearly.objects.all()

	# specify serializer to be used
	serializer_class = ampv1_YearlySerializer
                
        
class ampv1_HourlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = ampv1_repo_hourly.objects.all()

	# specify serializer to be used
	serializer_class = ampv1_HourlySerializer
        
class ampv1_MonthlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = ampv1_repo_monthly.objects.all()

	# specify serializer to be used
	serializer_class = ampv1_MonthlySerializer
        
class ampv1_DailyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = ampv1_repo_daily.objects.all()

	# specify serializer to be used
	serializer_class = ampv1_DailySerializer       
        
class ampv2_YearlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = ampv2_repo_yearly.objects.all()

	# specify serializer to be used
	serializer_class = ampv2_YearlySerializer
                
        
class ampv2_HourlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = ampv2_repo_hourly.objects.all()

	# specify serializer to be used
	serializer_class = ampv2_HourlySerializer
        
class ampv2_MonthlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = ampv2_repo_monthly.objects.all()

	# specify serializer to be used
	serializer_class = ampv2_MonthlySerializer
        
class ampv2_DailyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = ampv2_repo_daily.objects.all()

	# specify serializer to be used
	serializer_class = ampv2_DailySerializer       
        
class ampv3_YearlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = ampv3_repo_yearly.objects.all()

	# specify serializer to be used
	serializer_class = ampv3_YearlySerializer
                
        
class ampv3_HourlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = ampv3_repo_hourly.objects.all()

	# specify serializer to be used
	serializer_class = ampv3_HourlySerializer
        
class ampv3_MonthlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = ampv3_repo_monthly.objects.all()

	# specify serializer to be used
	serializer_class = ampv3_MonthlySerializer
        
class ampv3_DailyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = ampv3_repo_daily.objects.all()

	# specify serializer to be used
	serializer_class = ampv3_DailySerializer       
        
class ampv4_YearlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = ampv4_repo_yearly.objects.all()

	# specify serializer to be used
	serializer_class = ampv4_YearlySerializer
                
        
class ampv4_HourlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = ampv4_repo_hourly.objects.all()

	# specify serializer to be used
	serializer_class = ampv4_HourlySerializer
        
class ampv4_MonthlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = ampv4_repo_monthly.objects.all()

	# specify serializer to be used
	serializer_class = ampv4_MonthlySerializer
        
class ampv4_DailyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = ampv4_repo_daily.objects.all()

	# specify serializer to be used
	serializer_class = ampv4_DailySerializer       
        
class ampv5_YearlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = ampv5_repo_yearly.objects.all()

	# specify serializer to be used
	serializer_class = ampv5_YearlySerializer
                
        
class ampv5_HourlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = ampv5_repo_hourly.objects.all()

	# specify serializer to be used
	serializer_class = ampv5_HourlySerializer
        
class ampv5_MonthlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = ampv5_repo_monthly.objects.all()

	# specify serializer to be used
	serializer_class = ampv5_MonthlySerializer
        
class ampv5_DailyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = ampv5_repo_daily.objects.all()

	# specify serializer to be used
	serializer_class = ampv5_DailySerializer       
class tap1_YearlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = tap1_repo_yearly.objects.all()

	# specify serializer to be used
	serializer_class = tap1_YearlySerializer
                
        
class tap1_HourlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = tap1_repo_hourly.objects.all()

	# specify serializer to be used
	serializer_class = tap1_HourlySerializer
        
class tap1_MonthlyViewset(viewsets.ModelViewSet):
    # define queryset
    queryset = tap1_repo_monthly.objects.all()

    # specify serializer to be used
    serializer_class = tap1_MonthlySerializer
    authentication_classes = [JWTAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
class MyTokenObtainPairView(TokenObtainPairView):
    pass

class MyTokenRefreshView(TokenRefreshView):
    pass
        
class tap1_DailyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = tap1_repo_daily.objects.all()

	# specify serializer to be used
	serializer_class = tap1_DailySerializer       
class tap2_YearlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = tap2_repo_yearly.objects.all()

	# specify serializer to be used
	serializer_class = tap2_YearlySerializer
                
        
class tap2_HourlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = tap2_repo_hourly.objects.all()

	# specify serializer to be used
	serializer_class = tap2_HourlySerializer
        
class tap2_MonthlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = tap2_repo_monthly.objects.all()

	# specify serializer to be used
	serializer_class = tap2_MonthlySerializer
        
class tap2_DailyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = tap2_repo_daily.objects.all()

	# specify serializer to be used
	serializer_class = tap2_DailySerializer       
class tap3_YearlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = tap3_repo_yearly.objects.all()

	# specify serializer to be used
	serializer_class = tap3_YearlySerializer
                
        
class tap3_HourlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = tap3_repo_hourly.objects.all()

	# specify serializer to be used
	serializer_class = tap3_HourlySerializer
        
class tap3_MonthlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = tap3_repo_monthly.objects.all()

	# specify serializer to be used
	serializer_class = tap3_MonthlySerializer
        
class tap3_DailyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = tap3_repo_daily.objects.all()

	# specify serializer to be used
	serializer_class = tap3_DailySerializer       
class tap4_YearlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = tap4_repo_yearly.objects.all()

	# specify serializer to be used
	serializer_class = tap4_YearlySerializer
                
        
class tap4_HourlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = tap4_repo_hourly.objects.all()

	# specify serializer to be used
	serializer_class = tap4_HourlySerializer
        
class tap4_MonthlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = tap4_repo_monthly.objects.all()

	# specify serializer to be used
	serializer_class = tap4_MonthlySerializer
        
class tap4_DailyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = tap4_repo_daily.objects.all()

	# specify serializer to be used
	serializer_class = tap4_DailySerializer       
        
class cnd_consen_YearlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = cnd_consen_repo_yearly.objects.all()

	# specify serializer to be used
	serializer_class = cnd_consen_YearlySerializer
                
        
class tds_consen_YearlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = tds_consen_repo_yearly.objects.all()

	# specify serializer to be used
	serializer_class = tds_consen_YearlySerializer
                
        
class cnd_consen_HourlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = cnd_consen_repo_hourly.objects.all()

	# specify serializer to be used
	serializer_class = cnd_consen_HourlySerializer
class tds_consen_HourlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = tds_consen_repo_hourly.objects.all()

	# specify serializer to be used
	serializer_class = tds_consen_HourlySerializer
        
class cnd_consen_MonthlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = cnd_consen_repo_monthly.objects.all()

	# specify serializer to be used
	serializer_class = cnd_consen_MonthlySerializer
class tds_consen_MonthlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = tds_consen_repo_monthly.objects.all()

	# specify serializer to be used
	serializer_class = tds_consen_MonthlySerializer
        
class cnd_consen_DailyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = cnd_consen_repo_daily.objects.all()

	# specify serializer to be used
	serializer_class = cnd_consen_DailySerializer
class tds_consen_DailyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = tds_consen_repo_daily.objects.all()

	# specify serializer to be used
	serializer_class = tds_consen_DailySerializer


class atm_YearlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = atm_repo_yearly.objects.all()

	# specify serializer to be used
	serializer_class = atm_YearlySerializer
                
        
class atm_HourlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = atm_repo_hourly.objects.all()

	# specify serializer to be used
	serializer_class = atm_HourlySerializer
        
class atm_MonthlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = atm_repo_monthly.objects.all()

	# specify serializer to be used
	serializer_class = atm_MonthlySerializer
        
class atm_DailyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = atm_repo_daily.objects.all()

	# specify serializer to be used
	serializer_class = atm_DailySerializer
class flowsen1_YearlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = flowsen1_repo_yearly.objects.all()

	# specify serializer to be used
	serializer_class = flowsen1_YearlySerializer
                
        
class flowsen1_HourlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = flowsen1_repo_hourly.objects.all()

	# specify serializer to be used
	serializer_class = flowsen1_HourlySerializer
        
class flowsen1_MonthlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = flowsen1_repo_monthly.objects.all()

	# specify serializer to be used
	serializer_class = flowsen1_MonthlySerializer
        
class flowsen1_DailyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = flowsen1_repo_daily.objects.all()

	# specify serializer to be used
	serializer_class = flowsen1_DailySerializer   


class flowsen2_YearlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = flowsen2_repo_yearly.objects.all()

	# specify serializer to be used
	serializer_class = flowsen2_YearlySerializer
                
        
class flowsen2_HourlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = flowsen2_repo_hourly.objects.all()

	# specify serializer to be used
	serializer_class = flowsen2_HourlySerializer
        
class flowsen2_MonthlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = flowsen2_repo_monthly.objects.all()

	# specify serializer to be used
	serializer_class = flowsen2_MonthlySerializer
        
class flowsen2_DailyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = flowsen2_repo_daily.objects.all()

	# specify serializer to be used
	serializer_class = flowsen2_DailySerializer   


class flowsen3_YearlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = flowsen3_repo_yearly.objects.all()

	# specify serializer to be used
	serializer_class = flowsen3_YearlySerializer
                
        
class flowsen3_HourlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = flowsen3_repo_hourly.objects.all()

	# specify serializer to be used
	serializer_class = flowsen3_HourlySerializer
        
class flowsen3_MonthlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = flowsen3_repo_monthly.objects.all()

	# specify serializer to be used
	serializer_class = flowsen3_MonthlySerializer
        
class flowsen3_DailyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = flowsen1_repo_daily.objects.all()

	# specify serializer to be used
	serializer_class = flowsen1_DailySerializer   


class flowsen4_YearlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = flowsen4_repo_yearly.objects.all()

	# specify serializer to be used
	serializer_class = flowsen4_YearlySerializer
                
        
class flowsen4_HourlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = flowsen4_repo_hourly.objects.all()

	# specify serializer to be used
	serializer_class = flowsen4_HourlySerializer
        
class flowsen4_MonthlyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = flowsen4_repo_monthly.objects.all()

	# specify serializer to be used
	serializer_class = flowsen4_MonthlySerializer
        
class flowsen4_DailyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = flowsen4_repo_daily.objects.all()

	# specify serializer to be used
	serializer_class = flowsen4_DailySerializer

# # import mongoengine
# # mongoengine.connect(db=waterinn, host=localhost:27017, username=username, password=pwc)
class TopicViewSet(viewsets.ModelViewSet):
	# define queryset
	queryset = topics.objects.all()

	# specify serializer to be used
	serializer_class = TopicSerializer
        
        
class DeviceViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = device_info.objects.all()

	# specify serializer to be used
	serializer_class = DeviceSerializer
        
class keyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = key_info.objects.all()

	# specify serializer to be used
	serializer_class = KeySerializer
        
        
class GraphViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = graph_info.objects.all()

	# specify serializer to be used
	serializer_class = GraphSerializer
class TopicViewSet(viewsets.ModelViewSet):
	# define queryset
	queryset = topics.objects.all()

	# specify serializer to be used
	serializer_class = TopicSerializer
# class YearlyViewset(viewsets.ModelViewSet):
# 	# define queryset
# 	queryset = repo_yearly.objects.all()

# 	# specify serializer to be used
# 	serializer_class = YearlySerializer

class DeviceViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = device_info.objects.all()

	# specify serializer to be used
	serializer_class = DeviceSerializer
        
class keyViewset(viewsets.ModelViewSet):
	# define queryset
	queryset = key_info.objects.all()

	# specify serializer to be used
	serializer_class = KeySerializer
        
class RwpstateViewset(viewsets.ModelViewSet):
        # define queryset
        queryset = Rwp_state.objects.all()
        # specify serializer to be used
        serializer_class = RwpstateSerializer
        # permission_classes = [permissions.IsAuthenticated]
        deviceid=0
        def dispatch(self, request, *args, **kwargs):
            try:
                data_dict = json.loads(request.body)
                unwanted_keys = ["unit_type", "water_treatment","company_name","componant_name","site_name","device_id"]  # Example of unwanted keys
                
                value_list=list(data_dict.values())
                print("datadict:",data_dict)
                dinfo=device_info.objects.filter(componant_name=value_list[2],unit_type=value_list[1],company_name=value_list[0])
                for x in dinfo:
                    global deviceid
                    did=x.Device_id
                    deviceid=did
                    cmpname=x.componant_name
                    
                for key in unwanted_keys:
                    if key in data_dict:
                        del data_dict[key]
                print("datadict1:",data_dict)
                for key in data_dict:
                    data_dict[key] = str(data_dict[key])
                mqttc.publish(f'wc1/{did}/chgsta/{cmpname}',str(data_dict).replace(' ',''))
                print("***$$$@",str(data_dict).replace(' ',''))
                dd=dateandtime()
                e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} rwp status change has been requested - status:{value_list[3]}"
                erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='rwp',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                erro.save()

            except Exception as e:
                pass  
            return super().dispatch(request)    
        def perform_create(self, serializer):
            try:
                serializer.save()  # Save the data to the database
                ddid=Rwp_state.objects.filter(device_id='').update(device_id=deviceid)
                ddid.save()
            except Exception as e:
                pass    
        def desptroy(self, request):
            try:
                instance = self.get_object()
                self.perform_destroy(instance)
            except Http404:
                pass

did=0
class rwpsettingViewset(viewsets.ModelViewSet):
	# define queryset
    print("hi ok ")
    # queryset = rwp_setting.objects.all().order_by('-id')[:1]
    queryset = rwp_setting.objects.all()
    # print("queryset is:::",queryset)

    # data=queryset.last()
    # print("OLc",data.olc)
    # data = {'olc':data.olc,'drc':data.drc,'spn':data.spn,'units_type':data.unit_type,'company_name':data.company_name,'component_name':data.componant_name}
    # print('data is:',data)
    # # dosome()
    # print("Hi Satish")
    
    
	# specify serializer to be used
    serializer_class = rwpsettingSerializer
    def dispatch(self, request, *args, **kwargs):
        
        try:
            data_dict = json.loads(request.body)
            unwanted_keys = ["unit_type", "water_treatment","company_name","componant_name","site_name"]  # Example of unwanted keys
            print("dict data is:",data_dict)
            value_list=list(data_dict.values())
            print("value_list:",value_list)
            dinfo=device_info.objects.filter(componant_name=value_list[2],unit_type=value_list[1],company_name=value_list[0])
            for x in dinfo:
                print("did id:",x.Device_id)
                did=x.Device_id
                cmpname=x.componant_name
                print("ddddid is",did)
            for key in unwanted_keys:
                if key in data_dict:
                    del data_dict[key]
            for key in data_dict:
                    data_dict[key] = str(data_dict[key])
            mqttc.publish(f'wc1/{did}/chgset/{cmpname}',str(data_dict).replace(' ',''))
            
            print("data send to hivemq")
                
            
            # rwp_setting.objects.filter(device_id='').update(device_id=did)
            # rwp_setting.objects.all().update(device_id=did)
            dd=dateandtime()
            e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} rwp settings change has been requested - over load current:{value_list[3]}, span:{value_list[4]}, dry run current:{value_list[5]}"
            erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='rwp',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
            erro.save()
            
        except Exception as e:
            print("Error",e)
            dd=dateandtime()
            e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} Hpp has a fault-{e}"
            erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='hpp',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
            erro.save()
        return super().dispatch(request)    
    def perform_create(self, serializer):
        try:
            data_dict = serializer.validated_data
            # unwanted_keys = ["unit_type", "water_treatment", "company_name", "componant_nam,"site_name"e"]
            
            # Get the device information based on the provided values
            dinfo = device_info.objects.filter(componant_name=data_dict['componant_name'],
                                               unit_type=data_dict['unit_type'],
                                              company_name=data_dict['company_name']).last()
            deviceid=0
            if dinfo:
                did = dinfo.Device_id
                deviceid=did
                cmpname = dinfo.componant_name
                # data_dict['device_id'] = did
                # Remove unwanted keys from the data_dict
                # for key in unwanted_keys:
                #     if key in data_dict:
                #         del data_dict[key]
                        
                # Publish data_dict to HiveMQ
                # mqttc.publish(f'wc1/{did}/updset/{cmpname}', str(data_dict).replace(' ',''))
                # print("Data sent to HiveMQ")
                
            serializer.save()  # Save the data to the database
            ddid=rwp_setting.objects.filter(device_id='').update(device_id=deviceid)
            ddid.save()
            
        except Exception as e:
            print("Error:", e)
    def desptroy(self, request):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            pass
class hppstateViewset(viewsets.ModelViewSet):
	# define queryset
        queryset = hpp_state.objects.all()

        # specify serializer to be used
        serializer_class = hppstateSerializer
        # permission_classes = [permissions.IsAuthenticated]
        deviceid=0
        def dispatch(self, request, *args, **kwargs):
        
            try:
                data_dict = json.loads(request.body)
                unwanted_keys = ["unit_type", "water_treatment","company_name","componant_name","site_name","device_id"]  # Example of unwanted keys
                
                value_list=list(data_dict.values())
                
                dinfo=device_info.objects.filter(componant_name=value_list[2],unit_type=value_list[1],company_name=value_list[0])
                global deviceid
                for x in dinfo:
                    
                    did=x.Device_id
                    cmpname=x.componant_name
                    deviceid=did
                for key in unwanted_keys:
                    if key in data_dict:
                        del data_dict[key]
                for key in data_dict:
                    data_dict[key] = str(data_dict[key])
                mqttc.publish(f'wc1/{did}/chgsta/{cmpname}',str(data_dict).replace(' ',''))
                dd=dateandtime()
                e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} Hpp status change has been requested - status:{value_list[3]}"
                erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='hpp',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                erro.save()

            except Exception as e:
                dd=dateandtime()
                e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} Hpp has a fault-{e}"
                erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='hpp',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                erro.save()   
            return super().dispatch(request)    
        def perform_create(self, serializer):
            try:

                serializer.save()  # Save the data to the database
                ddid=hpp_state.objects.filter(device_id='').update(device_id=deviceid)
                ddid.save()
            except Exception as e:
                pass     
        def desptroy(self, request):
            try:
                instance = self.get_object()
                self.perform_destroy(instance)
            except Http404:
                pass   
class hppsettingViewset(viewsets.ModelViewSet):
        # define queryset
        queryset = hpp_setting.objects.all()
        # specify serializer to be used
        serializer_class = hppsettingSerializer
        # permission_classes = [permissions.IsAuthenticated]
        deviceid=0
        def dispatch(self, request, *args, **kwargs):
            
            try:
                data_dict = json.loads(request.body)
                unwanted_keys = ["unit_type", "water_treatment","company_name","componant_name","site_name","device_id"]  # Example of unwanted keys
                
                value_list=list(data_dict.values())
                
                dinfo=device_info.objects.filter(componant_name=value_list[2],unit_type=value_list[1],company_name=value_list[0])
                global deviceid
                for x in dinfo:
                    did=x.Device_id
                    cmpname=x.componant_name
                    deviceid=did
                for key in unwanted_keys:
                    if key in data_dict:
                        del data_dict[key]
                for key in data_dict:
                    data_dict[key] = str(data_dict[key])
                mqttc.publish(f'wc1/{did}/chgset/{cmpname}',str(data_dict).replace(' ',''))
                dd=dateandtime()
                e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} Hpp settings change has been requested - over load current:{value_list[3]}, span:{value_list[4]}, dry run current:{value_list[5]}"
                erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='hpp',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                erro.save()

            except Exception as e:
                pass    
            return super().dispatch(request)    
        def perform_create(self, serializer):
            try:
                serializer.save()  # Save the data to the database
                ddid=hpp_setting.objects.filter(device_id='').update(device_id=deviceid)
                ddid.save()
                
            except Exception as e:
                pass        
        def desptroy(self, request):
            try:
                instance = self.get_object()
                self.perform_destroy(instance)
            except Http404:
                pass
class device_infoViewset(viewsets.ModelViewSet):
        # define queryset
        def dispatch(self, request, *args, **kwargs):
            fields_to_exclude = ['model', 'pk']
            print(request.body,"BODY")
            data = json.loads(request.body)
            print(data,type(data),"DATA11:")
            u_id=data['user_id']
            print("uid",u_id)
            dinfo = device_info.objects.filter(company_name=data['company_name'])
            # did=dinfo[0].Device_id
            # site_name=dinfo[5].site_name
            # print(dinfo,type(dinfo))
            allsites=[]
            for si in dinfo:
                allsites.append(si.site_name)
            allsiteset=set(allsites)
            allsitelist=list(allsiteset)
            
            sites=[]
            # pubs = mo.siteandpermision.objects.filter(user_id='4').select_related('SitePermission', 'Site')
            # print('pubs:',pubs,type(pubs))
            # role = data.user_role


            # raw_sql = "SELECT iwater_site.site_name FROM iwater_site INNER JOIN iwater_site_permissions ON iwater_site.id=iwater_site_permissions.site_id where user_id='4'";
            # # raw_query = RawSQL(raw_sql, ())
            # results = mo.SitePermission.objects.raw(raw_sql)
            # print("results:", results)
            raw_sql = "SELECT iwater_site.site_name FROM iwater_site INNER JOIN iwater_site_permissions ON iwater_site.id=iwater_site_permissions.site_id WHERE iwater_site_permissions.user_id=%s"


            try:
                # Execute the raw SQL query and fetch the results
                with connection.cursor() as cursor:
                    cursor.execute(raw_sql,[u_id])
                    results = cursor.fetchall()
                    print("Results",results)

                # Print the results
                for result in results:
                    print("Site Name1:", result[0])
                    sites.append(result[0])
            except Exception as e:
                print("***")
                # for z in dinfo:
                #     sites.append(z.site_name)
            if data['user_role']== "super_admin" or data['user_role']== "administrator":

                siteset=set(allsites)
                siteset=list(siteset)
            else:
                siteset=set(sites)
                siteset=list(siteset)

            # qs_sta = treat_rwp.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
            # # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
            # if not qs_sta:
            #     data_sta = {}
            # else:
            #     data_sta = serialize("json", qs_sta)
            #     data_sta = json.loads(data_sta)
            #     print("data_sta is:",data_sta)
            #     for item in data_sta:
            #         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            #     data_sta = json.dumps(data_sta[0]["fields"])
            #     data_sta = json.loads(data_sta)
            
            # qs_set = treat_rwp.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
            # if not qs_set:
            #     data_set = {}
            # else:
            #     data_set = serialize("json", qs_set)
            #     data_set = json.loads(data_set)
            #     print("data_set is:",data_set)
            #     for item in data_set:
            #         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

            #     data_set = json.dumps(data_set[0]["fields"])
            #     data_set = json.loads(data_set)

            # # last_error=Errors.objects.filter(service='cnd_consen').order_by('-id')[:1:10]
            # last_error=Errors.objects.filter(service='rwp')
            # if not last_error:
            #     last_error={}
            # else:
            #     last_error = serialize("json", last_error)
            #     last_error = json.loads(last_error)
            #     for item in last_error:
            #         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
                
            #     last_error = json.dumps(last_error[0]["fields"])
            #     last_error = json.loads(last_error)

            # data_final = {'site_name':siteset,}
            response_data = {
                #new code
            'data': siteset,  # Include the 'data' field
            'status': 200,  # Add the status field
            'message': "Data get successful", # Add the message field
            # 'error':err,
            }
            response_data=[response_data]
            return JsonResponse(response_data, safe=False, content_type="application/json")   
        # def perform_create(self, serializer):
        #     try:
        #         serializer.save()  # Save the data to the database
        #         ddid=hpp_setting.objects.filter(device_id='').update(device_id=deviceid)
        #         ddid.save()
                
        #     except Exception as e:
        #         pass        
        # def desptroy(self, request):
        #     try:
        #         instance = self.get_object()
        #         self.perform_destroy(instance)
        #     except Http404:
        #         pass
                
class cndsettingViewset(viewsets.ModelViewSet):
	# define queryset
        queryset = cnd_setting.objects.all()
        serializer_class = cndsettingSerializer
        # permission_classes = [permissions.IsAuthenticated]
        deviceid =0
        def dispatch(self, request, *args, **kwargs):
            try:
                data_dict = json.loads(request.body)
                unwanted_keys = ["unit_type", "water_treatment","company_name","componant_name","site_name","device_id"]  # Example of unwanted keys
                value_list=list(data_dict.values())
                dinfo=device_info.objects.filter(componant_name=value_list[2],unit_type=value_list[1],company_name=value_list[0])
                did = 0
                cmpname = ''
                global deviceid
                for x in dinfo:
                    did=x.Device_id
                    deviceid=did
                    cmpname=x.componant_name
                for key in unwanted_keys:
                    if key in data_dict:
                        del data_dict[key]
                for key in data_dict:
                    data_dict[key] = str(data_dict[key])
                mqttc.publish(f'wc1/{did}/chgset/{cmpname}',str(data_dict).replace(' ',''))
                dd=dateandtime()
                e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} cnd settings change has been requested - span:{value_list[3]}, trip_setpoint:{value_list[4]}, atert_setpoint:{value_list[5]}"
                erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='cnd',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                erro.save()
            except Exception as e:
                pass
            return super().dispatch(request)    
        def perform_create(self, serializer):
            try:
                serializer.save()  # Save the data to the database
                ddid=cnd_setting.objects.filter(device_id='').update(device_id=deviceid)
                ddid.save()
            except Exception as e:
                pass        
        def desptroy(self, request):
            try:
                instance = self.get_object()
                self.perform_destroy(instance)
            except Http404:
                pass
        
class tdssettingViewset(viewsets.ModelViewSet):
        # define queryset
        queryset = tds_setting.objects.all()

        # specify serializer to be used
        serializer_class = tdssettingSerializer
        # permission_classes = [permissions.IsAuthenticated]
        deviceid=0
        def dispatch(self, request, *args, **kwargs):
        
            try:
                data_dict = json.loads(request.body)
                unwanted_keys = ["unit_type", "water_treatment","company_name","componant_name","site_name","device_id"]  # Example of unwanted keys
                
                value_list=list(data_dict.values())
                print("valuelist is:",value_list)
                dinfo=device_info.objects.filter(componant_name=value_list[2],unit_type=value_list[1],company_name=value_list[0])
                global deviceid
                for x in dinfo:
                    
                    did=x.Device_id
                    cmpname=x.componant_name
                    deviceid=did
                for key in unwanted_keys:
                    if key in data_dict:
                        del data_dict[key]
                for key in data_dict:
                    data_dict[key] = str(data_dict[key])
                mqttc.publish(f'wc1/{did}/chgset/{cmpname}',str(data_dict).replace(' ',''))
                print("data successfully send to hivemqtt")
                print("did is:",did)
                print("cname:",cmpname)
                dd=dateandtime()
                e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tds settings change has been requested - span:{value_list[3]}, trip_setpoint:{value_list[4]}, atert_setpoint:{value_list[5]}"
                erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='tds',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                erro.save()
            except Exception as e:
                pass    
            return super().dispatch(request)    
        def perform_create(self, serializer):
            try:
                serializer.save()  # Save the data to the database
                ddid=tds_setting.objects.filter(device_id='').update(device_id=deviceid)
                ddid.save()
            except Exception as e:
                pass        
        def desptroy(self, request):
            try:
                instance = self.get_object()
                self.perform_destroy(instance)
            except Http404:
                pass
    
class FflowsensettingViewset(viewsets.ModelViewSet):
        # define queryset
        queryset = F_flowsen_setting.objects.all()

        # specify serializer to be used
        serializer_class = FflowsensettingSerializer
        # permission_classes = [permissions.IsAuthenticated]
        deviceid=0
        def dispatch(self, request, *args, **kwargs):
        
            try:
                data_dict = json.loads(request.body)
                unwanted_keys = ["unit_type", "water_treatment","company_name","componant_name","site_name","device_id"]  # Example of unwanted keys
                
                value_list=list(data_dict.values())
                
                dinfo=device_info.objects.filter(componant_name=value_list[2],unit_type=value_list[1],company_name=value_list[0])
                global deviceid
                for x in dinfo:
                    
                    did=x.Device_id
                    cmpname=x.componant_name
                    deviceid=did
                for key in unwanted_keys:
                    if key in data_dict:
                        del data_dict[key]
                for key in data_dict:
                    data_dict[key] = str(data_dict[key])
                mqttc.publish(f'wc1/{did}/chgset/{cmpname}',str(data_dict).replace(' ',''))
                dd=dateandtime()
                e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} Fflowsen settings change has been requested - flow factor:{value_list[3]}"
                erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='Fflowsen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                erro.save()

            except Exception as e:
                pass    
            return super().dispatch(request)    
        def perform_create(self, serializer):
            try:
                serializer.save()  # Save the data to the database
                ddid=F_flowsen_setting.objects.filter(device_id='').update(device_id=deviceid)
                ddid.save()
            except Exception as e:
                pass        
        def desptroy(self, request):
            try:
                instance = self.get_object()
                self.perform_destroy(instance)
            except Http404:
                pass
        
class PflowsensettingViewset(viewsets.ModelViewSet):
	# define queryset
        queryset = P_flowsen_setting.objects.all()

        # specify serializer to be used
        serializer_class =PflowsensettingSerializer
        # permission_classes = [permissions.IsAuthenticated]
        deviceid=0
        def dispatch(self, request, *args, **kwargs):
        
            try:
                data_dict = json.loads(request.body)
                unwanted_keys = ["unit_type", "water_treatment","company_name","componant_name","site_name","device_id"]  # Example of unwanted keys
                
                value_list=list(data_dict.values())
                
                dinfo=device_info.objects.filter(componant_name=value_list[2],unit_type=value_list[1],company_name=value_list[0])
                global deviceid
                for x in dinfo:
                    
                    did=x.Device_id
                    cmpname=x.componant_name
                    deviceid=did
                for key in unwanted_keys:
                    if key in data_dict:
                        del data_dict[key]
                for key in data_dict:
                    data_dict[key] = str(data_dict[key])
                mqttc.publish(f'wc1/{did}/chgset/{cmpname}',str(data_dict).replace(' ',''))
                dd=dateandtime()
                e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} Pflowsen settings change has been requested - flow factor:{value_list[3]}"
                erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='Pflowsen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                erro.save()

            except Exception as e:
                pass    
            return super().dispatch(request)    
        def perform_create(self, serializer):
            try:
                serializer.save()  # Save the data to the database
                ddid=P_flowsen_setting.objects.filter(device_id='').update(device_id=deviceid)
                ddid.save()
            except Exception as e:
                pass        
        def desptroy(self, request):
            try:
                instance = self.get_object()
                self.perform_destroy(instance)
            except Http404:
                pass
class panelsettingViewset(viewsets.ModelViewSet):
	# define queryset
        queryset = panel_setting.objects.all()

        # specify serializer to be used
        serializer_class = panelsettingSerializer
        # permission_classes = [permissions.IsAuthenticated]
        deviceid=0
        def dispatch(self, request, *args, **kwargs):
        
            try:
                data_dict = json.loads(request.body)
                unwanted_keys = ["unit_type", "water_treatment","company_name","componant_name","site_name","device_id"]  # Example of unwanted keys
                
                value_list=list(data_dict.values())
                
                dinfo=device_info.objects.filter(componant_name=value_list[2],unit_type=value_list[1],company_name=value_list[0])
                global deviceid
                for x in dinfo:
                    
                    did=x.Device_id
                    cmpname=x.componant_name
                    deviceid=did
                for key in unwanted_keys:
                    if key in data_dict:
                        del data_dict[key]
                changesrt=data_dict['srt']
                changesrt=changesrt.split(":")
                hrtominit=int(changesrt[0])*60
                data_dict['srt']=hrtominit+int(changesrt[1])
                for key in data_dict:
                    data_dict[key] = str(data_dict[key])
                mqttc.publish(f'wc1/{did}/chgset/{cmpname}',str(data_dict).replace(' ',''))
                print("MMM:",data_dict)
                dd=dateandtime()
                e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} panel settings change has been requested - mode:{value_list[3]}, under voltage:{value_list[6]}, over voltage:{value_list[7]}, span:{value_list[8]}, no.of multiport valve:{value_list[4]}, sensor type:{value_list[5]}, service time:{value_list[9]}, backwash time:{value_list[10]}, rinse time:{value_list[11]}"
                erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='panel',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                erro.save()    

            except Exception as e:
                pass    
            return super().dispatch(request)    
        def perform_create(self, serializer):
            try:
                serializer.save()  # Save the data to the database
                ddid=panel_setting.objects.filter(device_id='').update(device_id=deviceid)
                ddid.save()
            except Exception as e:
                pass        
        def desptroy(self, request):
            try:
                instance = self.get_object()
                self.perform_destroy(instance)
            except Http404:
                pass
class atmsettingViewset(viewsets.ModelViewSet):
	# define queryset
        queryset = atm_setting.objects.all()

        # specify serializer to be used
        serializer_class = atmsettingSerializer
        # permission_classes = [permissions.IsAuthenticated]
        deviceid=0
        def dispatch(self, request, *args, **kwargs):
        
            try:
                data_dict = json.loads(request.body)
                unwanted_keys = ["unit_type", "water_treatment","company_name","componant_name","site_name","device_id","ntt"]  # Example of unwanted keys
                
                value_list=list(data_dict.values())
                
                dinfo=device_info.objects.filter(componant_name=value_list[2],unit_type=value_list[1],company_name=value_list[0])
                global deviceid
                for x in dinfo:
                    
                    did=x.Device_id
                    cmpname=x.componant_name
                    deviceid=did
                for key in unwanted_keys:
                    if key in data_dict:
                        del data_dict[key]
                for key in data_dict:
                    data_dict[key] = str(data_dict[key])
                mqttc.publish(f'wc1/{did}/chgset/{cmpname}',str(data_dict).replace(' ',''))
                dd=dateandtime()
                e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} atm settings change has been requested - over no. Of  tap:{value_list[3]}, no. Of volume:{value_list[4]}, volume1:{value_list[5]}, volume2:{value_list[6]}, volume3:{value_list[7]}, volume4:{value_list[8]}, rate1:{value_list[9]}, rate2:{value_list[10]}, rate3:{value_list[11]}, rate4:{value_list[12]}"
                erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='atm',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                erro.save() 

            except Exception as e:
                pass    
            return super().dispatch(request)    
        def perform_create(self, serializer):
            try:
                serializer.save()  # Save the data to the database
                ddid=atm_setting.objects.filter(device_id='').update(device_id=deviceid)
                ddid.save()
            except Exception as e:
                pass        
        def desptroy(self, request):
            try:
                instance = self.get_object()
                self.perform_destroy(instance)
            except Http404:
                pass
        
class cnd_consensettingViewset(viewsets.ModelViewSet):
    # define queryset
        queryset = cnd_consen_setting.objects.all()

        # specify serializer to be used
        serializer_class = cnd_consensettingSerializer
        # permission_classes = [permissions.IsAuthenticated]
        deviceid=0
        def dispatch(self, request, *args, **kwargs):
        
            try:
                data_dict = json.loads(request.body)
                unwanted_keys = ["unit_type", "water_treatment","company_name","componant_name","site_name","device_id"]  # Example of unwanted keys
                
                value_list=list(data_dict.values())
                
                dinfo=device_info.objects.filter(componant_name=value_list[2],unit_type=value_list[1],company_name=value_list[0])
                global deviceid
                for x in dinfo:
                    did=x.Device_id
                    cmpname=x.componant_name
                    deviceid=did
                for key in unwanted_keys:
                    if key in data_dict:
                        del data_dict[key]
                print("device is:", deviceid)
                for key in data_dict:
                    data_dict[key] = str(data_dict[key])
                mqttc.publish(f'wc1/{did}/chgset/{cmpname}',str(data_dict).replace(' ',''))
                dd=dateandtime()
                e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} cnd_consen settings change has been requested - span:{value_list[3]}, atert_setpoint:{value_list[4]}"
                erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='cnd_consen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                erro.save()

            except Exception as e:
                pass    
            return super().dispatch(request)    
        def perform_create(self, serializer):
            try:
                serializer.save()  # Save the data to the database
                ddid=cnd_consen_setting.objects.filter(device_id='').update(device_id=deviceid)
                ddid.save()
            except Exception as e:
                pass        
        def desptroy(self, request):
            try:
                instance = self.get_object()
                self.perform_destroy(instance)
            except Http404:
                pass
class tds_consensettingViewset(viewsets.ModelViewSet):
    # define queryset
        queryset = tds_consen_setting.objects.all()

        # specify serializer to be used
        serializer_class = tds_consensettingSerializer
        # permission_classes = [permissions.IsAuthenticated]
        deviceid=0
        def dispatch(self, request, *args, **kwargs):
        
            try:
                data_dict = json.loads(request.body)
                unwanted_keys = ["unit_type", "water_treatment","company_name","componant_name","site_name","device_id"]  # Example of unwanted keys
                
                value_list=list(data_dict.values())
                
                dinfo=device_info.objects.filter(componant_name=value_list[2],unit_type=value_list[1],company_name=value_list[0])
                global deviceid
                for x in dinfo:
                    
                    did=x.Device_id
                    cmpname=x.componant_name
                    deviceid=did
                for key in unwanted_keys:
                    if key in data_dict:
                        del data_dict[key]
                for key in data_dict:
                    data_dict[key] = str(data_dict[key])
                mqttc.publish(f'wc1/{did}/chgset/{cmpname}',str(data_dict).replace(' ',''))
                dd=dateandtime()
                e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tds_consen settings change has been requested - span:{value_list[3]}, atert_setpoint:{value_list[4]}"
                erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='tds_consen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                erro.save()

            except Exception as e:
                pass    
            return super().dispatch(request)    
        def perform_create(self, serializer):
            try:
                serializer.save()  # Save the data to the database
                ddid=tds_setting.objects.filter(device_id='').update(device_id=deviceid)
                ddid.save()
            except Exception as e:
                pass        
        def desptroy(self, request):
            try:
                instance = self.get_object()
                self.perform_destroy(instance)
            except Http404:
                pass
class ampv1stateViewset(viewsets.ModelViewSet):
        # define queryset
        queryset = ampv1_state.objects.all()

        # specify serializer to be used
        serializer_class = ampv1stateSerializer
        # permission_classes = [permissions.IsAuthenticated]
        deviceid=0
        def dispatch(self, request, *args, **kwargs):
        
            try:
                data_dict = json.loads(request.body)
                unwanted_keys = ["unit_type", "water_treatment","company_name","componant_name","site_name","device_id"]  # Example of unwanted keys
                
                value_list=list(data_dict.values())
                
                dinfo=device_info.objects.filter(componant_name=value_list[2],unit_type=value_list[1],company_name=value_list[0])
                global deviceid
                for x in dinfo:
                    
                    did=x.Device_id
                    cmpname=x.componant_name
                    deviceid=did
                for key in unwanted_keys:
                    if key in data_dict:
                        del data_dict[key]
                for key in data_dict:
                    data_dict[key] = str(data_dict[key])
                mqttc.publish(f'wc1/{did}/chgsta/{cmpname}',str(data_dict).replace(' ',''))
                dd=dateandtime()
                e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} ampv1 status change has been requested - position:{value_list[3]}"
                erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='ampv1',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                erro.save()

            except Exception as e:
                pass    
            return super().dispatch(request)    
        def perform_create(self, serializer):
            try:
                serializer.save()  # Save the data to the database
                ddid=ampv1_state.objects.filter(device_id='').update(device_id=deviceid)
                ddid.save()
            except Exception as e:
                pass        
        def desptroy(self, request):
            try:
                instance = self.get_object()
                self.perform_destroy(instance)
            except Http404:
                pass
        
class ampv1settingViewset(viewsets.ModelViewSet):
# 	# define queryset
        queryset = ampv1_setting.objects.all()

        # specify serializer to be used
        serializer_class = ampv1settingSerializer
        # permission_classes = [permissions.IsAuthenticated]
        deviceid=0
        def dispatch(self, request, *args, **kwargs):
        
            try:
                data_dict = json.loads(request.body)
                unwanted_keys = ["unit_type", "water_treatment","company_name","componant_name","site_name","device_id"]  # Example of unwanted keys
                
                value_list=list(data_dict.values())
                
                dinfo=device_info.objects.filter(componant_name=value_list[2],unit_type=value_list[1],company_name=value_list[0])
                global deviceid
                for x in dinfo:
                    
                    did=x.Device_id
                    cmpname=x.componant_name
                    deviceid=did
                for key in unwanted_keys:
                    if key in data_dict:
                        del data_dict[key]
                changesrt=data_dict['srt']
                changesrt=changesrt.split(":")
                hrtominit=int(changesrt[0])*60
                data_dict['srt']=hrtominit+int(changesrt[1])
                for key in data_dict:
                    data_dict[key] = str(data_dict[key])
                mqttc.publish(f'wc1/{did}/chgset/{cmpname}',str(data_dict).replace(' ',''))
                print("Dattta:",data_dict)
                dd=dateandtime()
                e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} ampv1 settings change has been requested - service time:{value_list[8]}, backwash time:{value_list[9]}, rins time:{value_list[10]}, motor on delay time:{value_list[11]}, output1:{value_list[12]}, output2:{value_list[13]}, output3:{value_list[14]}, input1:{value_list[4]}, input2:{value_list[5]}, input3:{value_list[6]}, pressure switch input:{value_list[7]}, sensor type:{value_list[3]}"
                erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='ampv1',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                erro.save()

            except Exception as e:
                pass    
            return super().dispatch(request)    
        def perform_create(self, serializer):
            try:
                serializer.save()  # Save the data to the database
                ddid=ampv1_setting.objects.filter(device_id='').update(device_id=deviceid)
                ddid.save()
            except Exception as e:
                pass        
        def desptroy(self, request):
            try:
                instance = self.get_object()
                self.perform_destroy(instance)
            except Http404:
                pass
class ampv2stateViewset(viewsets.ModelViewSet):
        # define queryset
        queryset = ampv2_state.objects.all()

        # specify serializer to be used
        serializer_class = ampv2stateSerializer
        # permission_classes = [permissions.IsAuthenticated]
        deviceid=0
        def dispatch(self, request, *args, **kwargs):
        
            try:
                data_dict = json.loads(request.body)
                unwanted_keys = ["unit_type", "water_treatment","company_name","componant_name","site_name","device_id"]  # Example of unwanted keys
                
                value_list=list(data_dict.values())
                
                dinfo=device_info.objects.filter(componant_name=value_list[2],unit_type=value_list[1],company_name=value_list[0])
                global deviceid
                for x in dinfo:
                    
                    did=x.Device_id
                    cmpname=x.componant_name
                    deviceid=did
                for key in unwanted_keys:
                    if key in data_dict:
                        del data_dict[key]
                for key in data_dict:
                    data_dict[key] = str(data_dict[key])
                mqttc.publish(f'wc1/{did}/chgsta/{cmpname}',str(data_dict).replace(' ',''))
                dd=dateandtime()
                e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} ampv2 status change has been requested - position:{value_list[3]}"
                erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='ampv2',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                erro.save()
            except Exception as e:
                pass    
            return super().dispatch(request)    
        def perform_create(self, serializer):
            try:
                serializer.save()  # Save the data to the database
                ddid=ampv2_state.objects.filter(device_id='').update(device_id=deviceid)
                ddid.save()
            except Exception as e:
                pass        
        def desptroy(self, request):
            try:
                instance = self.get_object()
                self.perform_destroy(instance)
            except Http404:
                pass
class ampv2settingViewset(viewsets.ModelViewSet):
	# define queryset
        queryset = ampv2_setting.objects.all()

        # specify serializer to be used
        serializer_class = ampv2settingSerializer
        # permission_classes = [permissions.IsAuthenticated]
        deviceid=0
        def dispatch(self, request, *args, **kwargs):
        
            try:
                data_dict = json.loads(request.body)
                unwanted_keys = ["unit_type", "water_treatment","company_name","componant_name","site_name","device_id"]  # Example of unwanted keys
                
                value_list=list(data_dict.values())
                
                dinfo=device_info.objects.filter(componant_name=value_list[2],unit_type=value_list[1],company_name=value_list[0])
                global deviceid
                for x in dinfo:
                    
                    did=x.Device_id
                    cmpname=x.componant_name
                    deviceid=did
                for key in unwanted_keys:
                    if key in data_dict:
                        del data_dict[key]
                changesrt=data_dict['srt']
                changesrt=changesrt.split(":")
                hrtominit=int(changesrt[0])*60
                data_dict['srt']=hrtominit+int(changesrt[1])
                for key in data_dict:
                    data_dict[key] = str(data_dict[key])
                mqttc.publish(f'wc1/{did}/chgset/{cmpname}',str(data_dict).replace(' ',''))
                dd=dateandtime()
                e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} ampv2 settings change has been requested - service time:{value_list[8]}, backwash time:{value_list[9]}, rins time:{value_list[10]}, motor on delay time:{value_list[11]}, output1:{value_list[12]}, output2:{value_list[13]}, output3:{value_list[14]}, input1:{value_list[4]}, input2:{value_list[5]}, input3:{value_list[6]}, pressure switch input:{value_list[7]}, sensor type:{value_list[3]}"
                erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='ampv2',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                erro.save()
            except Exception as e:
                pass    
            return super().dispatch(request)    
        def perform_create(self, serializer):
            try:
                serializer.save()  # Save the data to the database
                ddid=ampv2_setting.objects.filter(device_id='').update(device_id=deviceid)
                ddid.save()
            except Exception as e:
                pass        
        def desptroy(self, request):
            try:
                instance = self.get_object()
                self.perform_destroy(instance)
            except Http404:
                pass

class tap1settingViewset(viewsets.ModelViewSet):
	# define queryset
        queryset = tap1_setting.objects.all()

        # specify serializer to be used
        serializer_class = tap1settingSerializer
        # permission_classes = [permissions.IsAuthenticated]
        deviceid=0
        def dispatch(self, request, *args, **kwargs):
        
            try:
                data_dict = json.loads(request.body)
                unwanted_keys = ["unit_type", "water_treatment","company_name","componant_name","site_name","device_id"]  # Example of unwanted keys
                
                value_list=list(data_dict.values())
                
                dinfo=device_info.objects.filter(componant_name=value_list[2],unit_type=value_list[1],company_name=value_list[0])
                global deviceid
                for x in dinfo:
                    
                    did=x.Device_id
                    cmpname=x.componant_name
                    deviceid=did
                for key in unwanted_keys:
                    if key in data_dict:
                        del data_dict[key]
                for key in data_dict:
                    data_dict[key] = str(data_dict[key])
                mqttc.publish(f'wc1/{did}/chgset/{cmpname}',str(data_dict).replace(' ',''))
                print("*!*!*!:",data_dict)
                dd=dateandtime()
                e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tap1 settings change has been requested - pulse1:{value_list[3]}, pulse2:{value_list[4]}, pulse3:{value_list[5]}, pulse4:{value_list[6]}"
                erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='tap1',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                erro.save()

            except Exception as e:
                pass    
            return super().dispatch(request)    
        def perform_create(self, serializer):
            try:
                serializer.save()  # Save the data to the database
                ddid=tap1_setting.objects.filter(device_id='').update(device_id=deviceid)
                ddid.save()
            except Exception as e:
                pass        
        def desptroy(self, request):
            try:
                instance = self.get_object()
                self.perform_destroy(instance)
            except Http404:
                pass
class tap2settingViewset(viewsets.ModelViewSet):
	# define queryset
        queryset = tap2_setting.objects.all()

        # specify serializer to be used
        serializer_class = tap2settingSerializer
        # permission_classes = [permissions.IsAuthenticated]
        deviceid=0
        def dispatch(self, request, *args, **kwargs):
        
            try:
                data_dict = json.loads(request.body)
                unwanted_keys = ["unit_type", "water_treatment","company_name","componant_name","site_name","device_id"]  # Example of unwanted keys
                
                value_list=list(data_dict.values())
                
                dinfo=device_info.objects.filter(componant_name=value_list[2],unit_type=value_list[1],company_name=value_list[0])
                global deviceid
                for x in dinfo:
                    
                    did=x.Device_id
                    cmpname=x.componant_name
                    deviceid=did
                for key in unwanted_keys:
                    if key in data_dict:
                        del data_dict[key]
                for key in data_dict:
                    data_dict[key] = str(data_dict[key])
                mqttc.publish(f'wc1/{did}/chgset/{cmpname}',str(data_dict).replace(' ',''))
                dd=dateandtime()
                e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tap2 settings change has been requested - pulse1:{value_list[1]}, pulse2:{value_list[2]}, pulse3:{value_list[3]}, pulse4:{value_list[4]}"
                erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='tap2',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                erro.save()

            except Exception as e:
                pass    
            return super().dispatch(request)    
        def perform_create(self, serializer):
            try:
                serializer.save()  # Save the data to the database
                ddid=tap2_setting.objects.filter(device_id='').update(device_id=deviceid)
                ddid.save()
            except Exception as e:
                pass        
        def desptroy(self, request):
            try:
                instance = self.get_object()
                self.perform_destroy(instance)
            except Http404:
                pass
class tap3settingViewset(viewsets.ModelViewSet):
	# define queryset
        queryset = tap3_setting.objects.all()

        # specify serializer to be used
        serializer_class = tap3settingSerializer
        # permission_classes = [permissions.IsAuthenticated]
        deviceid=0
        def dispatch(self, request, *args, **kwargs):
        
            try:
                data_dict = json.loads(request.body)
                unwanted_keys = ["unit_type", "water_treatment","company_name","componant_name","site_name","device_id"]  # Example of unwanted keys
                
                value_list=list(data_dict.values())
                
                dinfo=device_info.objects.filter(componant_name=value_list[2],unit_type=value_list[1],company_name=value_list[0])
                global deviceid
                for x in dinfo:
                    
                    did=x.Device_id
                    cmpname=x.componant_name
                    deviceid=did
                for key in unwanted_keys:
                    if key in data_dict:
                        del data_dict[key]
                for key in data_dict:
                    data_dict[key] = str(data_dict[key])
                mqttc.publish(f'wc1/{did}/chgset/{cmpname}',str(data_dict).replace(' ',''))
                dd=dateandtime()
                e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tap3 settings change has been requested - pulse1:{value_list[3]}, pulse2:{value_list[4]}, pulse3:{value_list[5]}, pulse4:{value_list[6]}"
                erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='tap3',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                erro.save()

            except Exception as e:
                pass    
            return super().dispatch(request)    
        def perform_create(self, serializer):
            try:
                serializer.save()  # Save the data to the database
                ddid=tap3_setting.objects.filter(device_id='').update(device_id=deviceid)
                ddid.save()
            except Exception as e:
                pass        
        def desptroy(self, request):
            try:
                instance = self.get_object()
                self.perform_destroy(instance)
            except Http404:
                pass
class tap4settingViewset(viewsets.ModelViewSet):
	# define queryset
        queryset = tap4_setting.objects.all()

        # specify serializer to be used
        serializer_class = tap4settingSerializer
        # permission_classes = [permissions.IsAuthenticated]
    
        deviceid=0
        def dispatch(self, request, *args, **kwargs):
        
            try:
                data_dict = json.loads(request.body)
                unwanted_keys = ["unit_type", "water_treatment","company_name","componant_name","site_name","device_id"]  # Example of unwanted keys
                
                value_list=list(data_dict.values())
                
                dinfo=device_info.objects.filter(componant_name=value_list[2],unit_type=value_list[1],company_name=value_list[0])
                global deviceid
                for x in dinfo:
                    
                    did=x.Device_id
                    cmpname=x.componant_name
                    deviceid=did
                for key in unwanted_keys:
                    if key in data_dict:
                        del data_dict[key]
                for key in data_dict:
                    data_dict[key] = str(data_dict[key])
                mqttc.publish(f'wc1/{did}/chgset/{cmpname}',str(data_dict).replace(' ',''))
                dd=dateandtime()
                e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tap4 settings change has been requested - pulse1:{value_list[3]}, pulse2:{value_list[4]}, pulse3:{value_list[5]}, pulse4:{value_list[6]}"
                erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='tap4',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                erro.save()


            except Exception as e:
                pass    
            return super().dispatch(request)    
        def perform_create(self, serializer):
            try:
                serializer.save()  # Save the data to the database
                ddid=tap4_setting.objects.filter(device_id='').update(device_id=deviceid)
                ddid.save()
            except Exception as e:
                pass        
        def desptroy(self, request):
            try:
                instance = self.get_object()
                self.perform_destroy(instance)
            except Http404:
                pass
def on_message(client, userdata, msg):
    # Process the received MQTT message
    # data = message.payload.decode('utf-8')
    # logger.info("Received MQTT message: {}".format(data),type(data))

    # # Send an HTTP request to the Django server
    # # url = "http://localhost:8000"  # Replace with your Django server URL
    # params = {'data': data}
    # response = requests.get(url, params=params)
    # logger.info("HTTP response status code: {}".format(response.status_code))
        global msgo
        print("Data from mqtt:",msg.payload)
        jstring=msg.payload
        print("type is:",type(jstring))
        # #new changes 16-8
        # print("Data received1!!!",msg.payload)
        # jstr=msg.payload
        # if isinstance(jstr, bytes):
        #     data = jstr.decode("utf-8")
        #     print("data:",data,type(data))
        # if data.startswith("{'") and data.endswith("'}"):
        
        #     # if data.startswith("{'") and data.endswith("'}"):
        #         # dict_str = jstring.decode("UTF-8")
        #     # data = json.loads(str(message.payload.decode('utf-8')))
        #     print("Data received!!!",data,type(data))
        #     # token=
        #     logger.info("MQTT data {}".format(data))
        #     tok=data.split(":")
        #     # site_id = data["token"]
        #     site_id = int(tok[1])
        #     print("siteidis:",site_id)

        #     # token_ = data["token"]
        #     # site_id= Site.objects.filter(token=token_).latest()
        #     # site_id = str(data["token"]).lstrip("0")
        #     # site_id = site_id['id']
        #     device_id = data["deviceid"]
        #     panelid = data["panelid"] if data["panelid"] else None
        #     atmid = data["atmid"] if data["atmid"] else None

        #     logger.info("site_id {}".format(site_id))
        #     logger.info("company_id {}".format(self.company_id))
        #     logger.info("device_id {}".format(device_id))
        #     logger.info("panelid {}".format(panelid))
        #     logger.info("atmid {}".format(atmid))

        #     with transaction.atomic():
        #         try:  # TODO
        #             # # Device.objects.get(site_id=site_id, serial_no1=device_id)
        #             try:
        #                 device_data = Device.objects.get(site_id=site_id) # ! verfies device against site_id
        #                 # print(device_data)
        #             except Device.DoesNotExist:
        #                 device_data = None

        #             if device_data is not None:
        #                 logger.info("re-auth request came for device {}".format(device_id)) # ! re-auth request

        #                 # device_data = Device.objects.get(site_id=site_id, serial_no1=device_id)
        #                 if device_data.serial_no2 is None:
        #                     device_data.serial_no2 = panelid
        #                     device_data.save()
        #                     logger.info("Added device serial numbers")

        #                     site_data = Site.objects.get(id=site_id)
        #                     site_data.is_treatment_unit = True
        #                     site_data.save()
        #                     logger.info("Updated site details for treatment unit")

        #                     subscription_data = Subscription.objects.get(site_id=site_id)
        #                     subscription_data.site_id = site_id
        #                     subscription_data.is_treatment_unit = True
        #                     subscription_data.company_id = self.company_id
        #                     subscription_data.save()
        #                     logger.info("Added subscription details for treatment unit")
        #                 if device_data.serial_no3 is None:
        #                     device_data.serial_no3 = atmid
        #                     device_data.save()
        #                     logger.info("Added device serial numbers")

        #                     site_data = Site.objects.get(id=site_id)
        #                     site_data.is_dispensing_unit = True
        #                     site_data.save()
        #                     logger.info("Updated site details for dispensing unit")

        #                     # subscription_data = Subscription.objects.get(site_id=site_id)
        #                     # subscription_data.is_treatment_unit = True
        #                     # subscription_data.save()

        #                     subscription_data = Subscription()
        #                     subscription_data.site_id = site_id
        #                     subscription_data.is_dispensing_unit = True
        #                     subscription_data.company_id = self.company_id
        #                     subscription_data.save()
        #                     logger.info("Added subscription details for dispensing unit")

        #             else:
        #                 logger.info("Got new device add request ")
        #                 if panelid and atmid:
        #                     logger.info("Got both panel and atm id from device")

        #                     device_data = Device()
        #                     device_data.serial_no1 = device_id
        #                     device_data.serial_no2 = panelid
        #                     device_data.serial_no3 = atmid
        #                     device_data.site_id = site_id
        #                     device_data.save()
        #                     logger.info("Added device serial numbers")

        #                     site_data = Site.objects.get(id=site_id)
        #                     site_data.is_treatment_unit = True
        #                     site_data.save()
        #                     logger.info("Updated site details for treatment unit")

        #                     subscription_data = Subscription()
        #                     subscription_data.site_id = site_id
        #                     subscription_data.is_treatment_unit = True
        #                     subscription_data.company_id = self.company_id
        #                     subscription_data.save()
        #                     logger.info("Added subscription details for treatment unit")

        #                     site_data = Site.objects.get(id=site_id)
        #                     site_data.is_dispensing_unit = True
        #                     site_data.save()
        #                     logger.info("Updated site details for dispensing unit")

        #                     # subscription_data = Subscription.objects.get(site_id=site_id)
        #                     # subscription_data.is_treatment_unit = True
        #                     # subscription_data.save()

        #                     subscription_data = Subscription()
        #                     subscription_data.site_id = site_id
        #                     subscription_data.is_dispensing_unit = True
        #                     subscription_data.company_id = self.company_id
        #                     subscription_data.save()
        #                     logger.info("Added subscription details for dispensing unit")

        #                 elif panelid:
        #                     logger.info("Got only panel id from device")

        #                     device_data = Device()
        #                     device_data.serial_no1 = device_id
        #                     device_data.serial_no2 = panelid
        #                     device_data.serial_no3 = atmid
        #                     device_data.site_id = site_id
        #                     device_data.save()
        #                     logger.info("Added device serial numbers")

        #                     site_data = Site.objects.get(id=site_id)
        #                     site_data.is_treatment_unit = True
        #                     site_data.save()
        #                     logger.info("Updated site details for treatment unit")

        #                     subscription_data = Subscription()
        #                     subscription_data.site_id = site_id
        #                     subscription_data.is_treatment_unit = True
        #                     subscription_data.company_id = self.company_id
        #                     subscription_data.save()
        #                     logger.info("Added subscription details for treatment unit")

        #                 elif atmid:
        #                     logger.info("Got only atm id from device")

        #                     device_data = Device()
        #                     device_data.serial_no1 = device_id
        #                     device_data.serial_no2 = panelid
        #                     device_data.serial_no3 = atmid
        #                     device_data.site_id = site_id
        #                     device_data.save()

        #                     site_data = Site.objects.get(id=site_id)
        #                     site_data.is_dispensing_unit = True
        #                     site_data.save()
        #                     logger.info("Updated site details for dispensing unit")

        #                     subscription_data = Subscription()
        #                     subscription_data.site_id = site_id
        #                     subscription_data.is_dispensing_unit = True
        #                     subscription_data.company_id = self.company_id
        #                     subscription_data.save()
        #                     logger.info("Added subscription details for dispensing unit")
        #             site_data = Site.objects.get(id=site_id)
        #             # company_names=Company.objects.get(company_id=self.company_id)
        #             print("*1*1*")
        #             print("email is:",user_login.email)
        #             logged_user = User.objects.get(email=user_login.email)

        #             company_names = Company.objects.get(id=logged_user.company_id)

        #             print("company_names:",company_names.company_name)
        #             records = [
        #             {
        #             "Device_id": device_id,
        #             "Device_name": "wc",
        #             "unit_type": "water_treatment",
        #             "company_name": company_names.company_name,
        #             "componant_name": "rwp",
        #             "site_name": site_data.site_name
        #             },
        #             {
        #             "Device_id": device_id,
        #             "Device_name": "wc",
        #             "unit_type": "water_treatment",
        #             "company_name": company_names.company_name,
        #             "componant_name": "rwp",
        #             "site_name": site_data.site_name
        #             },
        #             {
        #             "Device_id": device_id,
        #             "Device_name": "wc",
        #             "unit_type": "water_treatment",
        #             "company_name": company_names.company_name,
        #             "componant_name": "cnd_sen",
        #             "site_name": site_data.site_name
        #             },
        #             {
        #             "Device_id": device_id,
        #             "Device_name": "wc",
        #             "unit_type": "water_treatment",
        #             "company_name": company_names.company_name,
        #             "componant_name": "ampv1",
        #             "site_name": site_data.site_name
        #             },
        #             {
        #             "Device_id": device_id,
        #             "Device_name": "wc",
        #             "unit_type": "water_treatment",
        #             "company_name": company_names.company_name,
        #             "componant_name": "ampv2",
        #             "site_name": site_data.site_name
        #             },
        #             {
        #             "Device_id": device_id,
        #             "Device_name": "wc",
        #             "unit_type": "water_treatment",
        #             "company_name": company_names.company_name,
        #             "componant_name": "ampv3",
        #             "site_name": site_data.site_name
        #             },
        #             {
        #             "Device_id": device_id,
        #             "Device_name": "wc",
        #             "unit_type": "water_treatment",
        #             "company_name": company_names.company_name,
        #             "componant_name": "ampv4",
        #             "site_name": site_data.site_name
        #             },
        #             {
        #             "Device_id": device_id,
        #             "Device_name": "wc",
        #             "unit_type": "water_dispense",
        #             "company_name": company_names.company_name,
        #             "componant_name": "tap2",
        #             "site_name": site_data.site_name
        #             },
        #             {
        #             "Device_id": device_id,
        #             "Device_name": "wc",
        #             "unit_type": "water_dispense",
        #             "company_name": company_names.company_name,
        #             "componant_name": "tap3",
        #             "site_name": site_data.site_name
        #             },
        #             {
        #             "Device_id": device_id,
        #             "Device_name": "wc",
        #             "unit_type": "water_dispense",
        #             "company_name": company_names.company_name,
        #             "componant_name": "tap4",
        #             "site_name": site_data.site_name
        #             },
        #             {
        #             "Device_id": device_id,
        #             "Device_name": "wc",
        #             "unit_type": "water_treatment",
        #             "company_name": company_names.company_name,
        #             "componant_name": "hpp",
        #             "site_name": site_data.site_name
        #             },
        #             {
        #             "Device_id": device_id,
        #             "Device_name": "wc",
        #             "unit_type": "water_treatment",
        #             "company_name": company_names.company_name,
        #             "componant_name": "atm",
        #             "site_name": site_data.site_name
        #             },
        #             {
        #             "Device_id": device_id,
        #             "Device_name": "wc",
        #             "unit_type": "water_treatment",
        #             "company_name": company_names.company_name,
        #             "componant_name": "panel",
        #             "site_name": site_data.site_name
        #             },
        #             {

        #             "Device_id": device_id,
        #             "Device_name": "wc",
        #             "unit_type": "water_treatment",
        #             "company_name": company_names.company_name,
        #             "componant_name": "F_flowsen",
        #             "site_name": site_data.site_name
        #             },
        #             {
        #             "Device_id": device_id,
        #             "Device_name": "wc",
        #             "unit_type": "water_treatment",
        #             "company_name": company_names.company_name,
        #             "componant_name": "P_flowsen",
        #             "site_name": site_data.site_name
        #             },
        #             {
        #             "Device_id": device_id,
        #             "Device_name": "wc",
        #             "unit_type": "water_treatment",
        #             "company_name": company_names.company_name,
        #             "componant_name": "tds_sen",
        #             "site_name": site_data.site_name
        #             },
        #             {
        #             "Device_id": device_id,
        #             "Device_name": "wc",
        #             "unit_type": "water_dispense",
        #             "company_name": company_names.company_name,
        #             "componant_name": "cnd_consen",
        #             "site_name": site_data.site_name
        #             },
        #             {
        #             "Device_id": device_id,
        #             "Device_name": "wc",
        #             "unit_type": "water_dispense",
        #             "company_name": company_names.company_name,
        #             "componant_name": "tds_consen",
        #             "site_name": site_data.site_name
        #             },
        #             {
        #             "Device_id": device_id,
        #             "Device_name": "wc",
        #             "unit_type": "water_dispense",
        #             "company_name": company_names.company_name,
        #             "componant_name": "atm",
        #             "site_name": site_data.site_name
        #             },
        #             {
        #             "Device_id": device_id,
        #             "Device_name": "wc",
        #             "unit_type": "water_dispense",
        #             "company_name": company_names.company_name,
        #             "componant_name": "flowsen1",
        #             "site_name": site_data.site_name
        #             },
        #             {
        #             "Device_id": device_id,
        #             "Device_name": "wc",
        #             "unit_type": "water_dispense",
        #             "company_name": company_names.company_name,
        #             "componant_name": "flowsen2",
        #             "site_name": site_data.site_name
        #             },
        #             {
        #             "Device_id": device_id,
        #             "Device_name": "wc",
        #             "unit_type": "water_dispense",
        #             "company_name": company_names.company_name,
        #             "componant_name": "flowsen3",
        #             "site_name": site_data.site_name
        #             },
        #             {
        #             "Device_id": device_id,
        #             "Device_name": "wc",
        #             "unit_type": "water_dispense",
        #             "company_name": company_names.company_name,
        #             "componant_name": "flowsen4",
        #             "site_name": site_data.site_name
        #             },
        #             {
        #             "Device_id": device_id,
        #             "Device_name": "wc",
        #             "unit_type": "water_dispense",
        #             "company_name": company_names.company_name,
        #             "componant_name": "tap1",
        #             "site_name": site_data.site_name
        #             },
        #             {
        #             "Device_id": device_id,
        #             "Device_name": "wc",
        #             "unit_type": "water_dispense",
        #             "company_name": company_names.company_name,
        #             "componant_name": "tap1",
        #             "site_name": site_data.site_name
        #             }
        #                                 # Add other records here
        #             ]
        #             print("*2*2*")
        #             # Insert the records into the collection
        #             # device_info.insert_many(records)
        #             for record in records:
        #                 print("*3*3*")
        #                 info=device_info.objects.create(**record)
        #          
        #                 info.save()
        #                 print("*5*5*")

        #             logger.info("Successfully added data to db over mqtt")
        #             print("*6*6*")
        #         except Exception as err:
        #             print("*7*7*")
        #             transaction.set_rollback(True)
        #             logger.error("MQTT - {}".format(err))


        # mydata1=0
        if isinstance(jstring, bytes):
            dict_str = jstring.decode("utf-8")
            print("dict_str:",dict_str,type(dict_str))
        if dict_str.startswith("{'") and dict_str.endswith("'}") or 'version' not in dict_str:
            # dict_str = jstring.decode("UTF-8")
            dict_split=dict_str.split(":")
            print("dict_split:",dict_split,type(dict_split))

            dict_data = ast.literal_eval(dict_str)
            converted_list = [f"{key}:{value}" for key, value in dict_data.items()]
            # print("converted_list:",converted_list)
            # rep1=dict_str.replace("}",'')
            # rep2=rep1.replace("{",'')
            # # print("rep2:",rep2)
            # rep2=rep2.replace('"','')
            # # print("after replace rep2:",rep2)
            # array_dat = rep2.split(',')
            array_dat =converted_list
            # formatted_strings = [s.replace('"','') for s in array_dat]
            # formatted_strings = [s.strip("'").replace('"', '') for s in array_dat]
            # formatted_strings = [s.strip("'").replace("'", '') for s in formatted_strings]
            print("array_dat1:",array_dat,type(array_dat))
            mydata ={}

            cnd=0
            tds=0
            spn=0
            tsp=0
            asp=0
            sts=''
            crt=0
            olc=0
            drc=0
            rtl=''
            ttl=''
            lps=''
            hps=''
            dgp=''
            mod=''
            ipv=0
            unv=0
            ovv=0
            nmv=0
            stp=0
            srt=0
            bkt=0
            rst=0
            err=''
            fr1=0
            fr2=0
            ff1=0
            ff2=0
            pos=''
            rmt=0
            cct=0
            srt=0
            bkt=0
            mot=0
            stp=''
            op1=''
            op2=''
            op3=''
            ip1=''
            ip2=''
            ip3=''
            psi=''
            ndv=0
            ntt=''
            nta=0
            tmp=0
            whr=''
            custid=''
            ntp=0
            nov=0
            vl1=0
            vl2=0
            vl3=0
            vl4=0
            re1=0
            re2=0
            re3=0
            re4=0
            p1=0
            p2=0
            p3=0
            p4=0
            fr=0

            for loop_data in array_dat:
                
                removed_col = loop_data.split(':')
                
                mydata[removed_col[0]] =removed_col[1]
                
                if removed_col[0]=='cnd':
                    if removed_col[1].isdigit():
                        cnd=int(removed_col[1])
                elif removed_col[0]=='spn':
                    spn=int(removed_col[1])
                elif removed_col[0]=='tds':
                    if removed_col[1].isdigit():
                        tds=int(removed_col[1])
                elif removed_col[0]=='tsp':
                    tsp=int(removed_col[1])
                elif removed_col[0]=='asp':
                    asp=int(removed_col[1])
                elif removed_col[0]=='sts':
                    sts=removed_col[1]
                elif removed_col[0]=='crt':
                    crt=removed_col[1]
                elif removed_col[0]=='olc':
                    olc=removed_col[1]
                elif removed_col[0]=='drc':
                    drc=removed_col[1]
                elif removed_col[0]=='rtl':
                    rtl=removed_col[1]
                elif removed_col[0]=='ttl':
                    ttl=removed_col[1]
                elif removed_col[0]=='lps':
                    lps=removed_col[1]
                elif removed_col[0]=='hps':
                    hps=removed_col[1]
                elif removed_col[0]=='dgp':
                    dgp=removed_col[1]
                elif removed_col[0]=='mod':
                    mod=removed_col[1]
                elif removed_col[0]=='ipv':
                    ipv=removed_col[1]
                elif removed_col[0]=='unv':
                    unv=removed_col[1]
                elif removed_col[0]=='ovv':
                    ovv=removed_col[1]
                elif removed_col[0]=='nmv':
                    nmv=removed_col[1]
                elif removed_col[0]=='stp':
                    stp=removed_col[1]
                elif removed_col[0]=='bkt':
                    bkt=removed_col[1]
                elif removed_col[0]=='rst':
                    rst=removed_col[1]
                elif removed_col[0]=='err':
                    err=removed_col[1]
                elif removed_col[0]=='fr1':
                    fr1=removed_col[1]
                elif removed_col[0]=='fr2':
                    fr2=removed_col[1]
                elif removed_col[0]=='ff1':
                    ff1=removed_col[1]
                elif removed_col[0]=='ff2':
                    ff2=removed_col[1]
                elif removed_col[0]=='pos':
                    pos=removed_col[1]
                elif removed_col[0]=='rmt':
                    rmt=removed_col[1]
                elif removed_col[0]=='cct':
                    cct=removed_col[1]
                elif removed_col[0]=='srt':
                    srt=removed_col[1]
                    # srt2=int(srt1)
                    # srt=srt2/60
                    # srt=str(srt)
                    # mints=srt.split(".")
                    # mintconvert=str(mints[1])
                    # mintconvert1="0."+mintconvert
                    # mintconvert2=round(float(mintconvert1)*60)
                    # srt=f"{str(mints[0])}:{str(mintconvert2)}"
                    # srt2=removed_col[2]
                    # srt=srt1+':'+srt2
                elif removed_col[0]=='bkt':
                    bkt=removed_col[1]
                elif removed_col[0]=='mot':
                    mot=removed_col[1]
                elif removed_col[0]=='stp':
                    stp=removed_col[1]
                elif removed_col[0]=='op1':
                    op1=removed_col[1]
                elif removed_col[0]=='op2':
                    op2=removed_col[1]
                elif removed_col[0]=='op3':
                    op3=removed_col[1]
                elif removed_col[0]=='ip1':
                    ip1=removed_col[1]
                elif removed_col[0]=='ip2':
                    ip2=removed_col[1]
                elif removed_col[0]=='ip3':
                    ip3=removed_col[1]
                elif removed_col[0]=='psi':
                    psi=removed_col[1]
                elif removed_col[0]=='ndv':
                    ndv=removed_col[1]
                elif removed_col[0]=='ntt':
                    ntt=removed_col[1]
                elif removed_col[0]=='nta':
                    nta=removed_col[1]
                elif removed_col[0]=='tmp':
                    tmp=removed_col[1]
                elif removed_col[0]=='ntp':
                    ntp=removed_col[1]
                elif removed_col[0]=='nov':
                    nov=removed_col[1]
                elif removed_col[0]=='vl1':
                    vl1=removed_col[1]
                elif removed_col[0]=='vl2':
                    vl2=removed_col[1]
                elif removed_col[0]=='vl3':
                    vl3=removed_col[1]
                elif removed_col[0]=='vl4':
                    vl4=removed_col[1]
                elif removed_col[0]=='re1':
                    re1=removed_col[1]
                elif removed_col[0]=='re2':
                    re2=removed_col[1]
                elif removed_col[0]=='re3':
                    re3=removed_col[1]
                elif removed_col[0]=='re4':
                    re4=removed_col[1]
                elif removed_col[0]=='p1':
                    p1=removed_col[1]
                elif removed_col[0]=='p2':
                    p2=removed_col[1]
                elif removed_col[0]=='p3':
                    p3=removed_col[1]
                elif removed_col[0]=='p4':
                    p4=removed_col[1]
                elif removed_col[0]=='fr':
                    fr=removed_col[1]
                elif removed_col[0]=='whr':
                    whr=removed_col[1]
                elif removed_col[0]=='custid':
                    custid=removed_col[1]
            
            
            
            
            

            
            mydata1=mydata      
            mydata = json.dumps(mydata, indent = 4) 
            # mydata = ast.literal_eval(mydata)
            # mydata = ast.literal_eval(dict_str)
            
            mydatadict=json.loads(mydata)
            
            hmq=msg.topic
            hmqm_split=hmq.split('/')
            
            device_id=hmqm_split[1]
            msg_type=hmqm_split[2]

            if(msg_type == 'updset' or msg_type == 'updsta'):
                print("msg_type",msg_type)
                components=hmqm_split[3]
                
                od=mydata.strip()
                
                repo_histobj=repo_history.objects.create(device_id=device_id,message_type=msg_type,component_name=components,msg_json=mydata1)
                repo_histobj.save()
                
                get_device_id=repo_latestdata.objects.all()
                
                device_idlist=[]
                cnd_sen={}
                tds_sen={}
                rwp={}
                hpp={}
                panel={}
                flowsen={}
                ampv1={}
                ampv2={}
                ampv3={}
                ampv4={}
                ampv5={}
                atm={}
                tap1={}
                tap2={}
                tap3={}
                tap4={}
                consen={}
                flowsen1={}
                flowsen2={}
                flowsen3={}
                flowsen4={}

                monthset=set()
                # print("dgid is:",get_device_id)
                for did in get_device_id:
                    s=str(did.device_id)
                    if device_id == s:
                        
                        
                        tds1=did.cnd_sen
                        cnd_sen=tds1
                        # tdsstr=(str(tds))
                        
                        tds_sen=did.tds_sen
                        rwp=did.rwp
                        
                        hpp=did.hpp
                        
                        panel=did.panel
                        
                        flowsen=did.flowsen
                        
                        ampv1=did.ampv1
                        
                        ampv2=did.ampv2
                        
                        ampv3=did.ampv3
                        
                        ampv4=did.ampv4
                        
                        ampv5=did.ampv5
                        
                        atm=did.atm
                        
                        tap1=did.tap1
                        
                        tap2=did.tap2
                        
                        tap3=did.tap3
                        
                        tap4=did.tap4
                        
                        # consen=did.consen
                        flowsen1=did.flowsen1
                        flowsen2=did.flowsen2
                        flowsen3=did.flowsen3
                        flowsen4=did.flowsen4
                        
                    device_idlist.append(s)
                    
                
                service_list=[]
                
                repoyearly=cnd_repo_yearly.objects.all()
                for ry in repoyearly:
                        ser=ry.service
                        service_list.append(ser)
                        
                
                olddata={}
                hourset=set()
                dd=dateandtime() 
                try:
                    if 'cnd_sen'== components:
                        if device_id not in device_idlist:
                            repo_latestdata.objects.create(device_id=device_id,message_type=msg_type,cnd_sen=mydata1)
                        else:
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, cnd_sen=mydata1)

                            get_device_id=repo_latestdata.objects.all()
                            for did in get_device_id:
                                s=str(did.device_id)
                                if device_id == s:
                                    
                                    
                                    tds1=did.cnd_sen
                                    cnd_sen=tds1
                                    # tdsstr=(str(tds))
                                    
                                    

                            klist = list(cnd_sen.keys())
                            
                            mydatakey = list(mydata1.keys())
                            
                            for k,v in cnd_sen.items():
                                if k not in mydatakey:
                                    olddata.update({k:v})
                                    
                            mydata5=olddata.update(mydata1)    
                            
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, cnd_sen=olddata)
                        
                        dd=dateandtime()  
                        
                        
                        ds=treat_cnd_sen.objects.create(device_id=device_id,message_type=msg_type,cnd=cnd,spn=spn,tsp=tsp,asp=asp,year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                        ds.save()
                        if msg_type == 'updset':
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} cnd_sen settings has been updated span:{spn} trip_setpoint:{tsp} alert_setpoint:{asp}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='cnd_sen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        else:
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} cnd_sen status has been updated conductivity:{cnd}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='cnd_sen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        # Hour
                        yrdata=treat_cnd_sen.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_cnd=0
                        sums_spn=0
                        sums_tsp=0
                        sums_asp=0
                        avgs_cnd = 0
                        avgs_spn = 0
                        avgs_tsp = 0
                        avgs_asp = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    cnds=yr.cnd
                                    spns=yr.spn
                                    tsps=yr.tsp
                                    asps=yr.asp
                                    
                                    sums_cnd=sums_cnd+cnds
                                    sums_spn=sums_spn+spns
                                    sums_tsp=sums_tsp+tsps
                                    sums_asp=sums_asp+asps
                                    count=count+1
                                    
                                    
                                    if cnds or spns or tsp or asp == 0:
                                        zerocount=zerocount+1
                                        
                            count1=count-zerocount
                            avgs_cnd=sums_cnd/count
                            avgs_spn=sums_spn/count
                            avgs_tsp=sums_tsp/count
                            avgs_asp=sums_asp/count
                        hr=cnd_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        if hr:
                            yr_data=cnd_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id).update(device_id=device_id,service='cnd',cnd={'sum':sums_cnd,'avg':avgs_cnd,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},tsp={'sum':sums_tsp,'avg':avgs_tsp,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=cnd_repo_hourly.objects.create(device_id=device_id,service='cnd',cnd={'sum':sums_cnd,'avg':avgs_cnd,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},tsp={'sum':sums_tsp,'avg':avgs_tsp,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                            
                        #day   
                        yrdata=treat_cnd_sen.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        # yrdata=cnd_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        count=0
                        count_sum=0
                        count_cnd=0
                        count_spn=0
                        count_tsp=0
                        count_asp=0
                        sums_cnd=0
                        sums_spn=0
                        sums_tsp=0
                        sums_asp=0
                        avgs_cnd = 0
                        avgs_spn = 0
                        avgs_tsp = 0
                        avgs_asp = 0
                        if yrdata:
                            for yr in yrdata:
                                
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    
                                    cnds_d=yr.cnd
                                    spns_d=yr.spn
                                    tsps_d=yr.tsp
                                    asps_d=yr.asp
                                    
                                    sums_cnd=sums_cnd+cnds_d
                                    sums_spn=sums_spn+spns_d
                                    sums_tsp=sums_tsp+tsps_d
                                    sums_asp=sums_asp+asps_d
                                    count_sum=count_sum+count_cnd

                                    count=count+1
                                    
                            
                            
                            avgs_cnd=sums_cnd/count
                            

                            avgs_spn=sums_spn/count
                            
                            avgs_tsp=sums_tsp/count
                            avgs_asp=sums_asp/count
                        hr=cnd_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        if hr:
                            
                            yr_data=cnd_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id).update(device_id=device_id,service='cnd_sen',cnd={'sum':sums_cnd,'avg':avgs_cnd,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},tsp={'sum':sums_tsp,'avg':avgs_tsp,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                            
                        else:
                            yr_data=cnd_repo_daily.objects.create(device_id=device_id,service='cnd_sen',cnd={'sum':sums_cnd,'avg':avgs_cnd,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},tsp={'sum':sums_tsp,'avg':avgs_tsp,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                            yr_data.save()
                            
                        #month
                        
                        yrdata=treat_cnd_sen.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        count=0
                        sums_cnd=0
                        sums_spn=0
                        sums_tsp=0
                        sums_asp=0
                        avgs_cnd = 0
                        avgs_spn = 0
                        avgs_tsp = 0
                        avgs_asp = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    cnds=yr.cnd
                                    spns=yr.spn
                                    tsps=yr.tsp
                                    asps=yr.asp
                                    
                                    sums_cnd=sums_cnd+cnds
                                    sums_spn=sums_spn+spns
                                    sums_tsp=sums_tsp+tsps
                                    sums_asp=sums_asp+asps
                                    count=count+1
                                    
                                    
                                    if cnds or spns or tsp or asp == 0:
                                        zerocount=zerocount+1
                            
                            avgs_cnd=sums_cnd/count
                            avgs_spn=sums_spn/count
                            avgs_tsp=sums_tsp/count
                            avgs_asp=sums_asp/count
                        hr=cnd_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        if hr:
                            yr_data=cnd_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id).update(device_id=device_id,service='cnd_sen',cnd={'sum':sums_cnd,'avg':avgs_cnd,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},tsp={'sum':sums_tsp,'avg':avgs_tsp,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                        else:
                            yr_data=cnd_repo_monthly.objects.create(device_id=device_id,service='cnd_sen',cnd={'sum':sums_cnd,'avg':avgs_cnd,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},tsp={'sum':sums_tsp,'avg':avgs_tsp,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                            yr_data.save()
                    
                        # year
                        yrdata=treat_cnd_sen.objects.filter(year=dd[0],device_id=device_id)
                        count=0
                        sums_cnd=0
                        sums_spn=0
                        sums_tsp=0
                        sums_asp=0
                        avgs_cnd = 0
                        avgs_spn = 0
                        avgs_tsp = 0
                        avgs_asp = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    cnds=yr.cnd
                                    spns=yr.spn
                                    tsps=yr.tsp
                                    asps=yr.asp
                                    
                                    sums_cnd=sums_cnd+cnds
                                    sums_spn=sums_spn+spns
                                    sums_tsp=sums_tsp+tsps
                                    sums_asp=sums_asp+asps
                                    count=count+1
                                    
                                    
                                    if cnds or spns or tsp or asp == 0:
                                        zerocount=zerocount+1
                            avgs_cnd=sums_cnd/count
                            avgs_spn=sums_spn/count
                            avgs_tsp=sums_tsp/count
                            avgs_asp=sums_asp/count
                        hr=cnd_repo_yearly.objects.filter(year=dd[0],device_id=device_id)
                        if hr:
                            yr_data=cnd_repo_yearly.objects.filter(device_id=device_id).update(device_id=device_id,service='cnd_sen',cnd={'sum':sums_cnd,'avg':avgs_cnd,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},tsp={'sum':sums_tsp,'avg':avgs_tsp,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                        else:
                            yr_data=cnd_repo_yearly.objects.create(device_id=device_id,service='cnd_sen',cnd={'sum':sums_cnd,'avg':avgs_cnd,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},tsp={'sum':sums_tsp,'avg':avgs_tsp,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                            yr_data.save()
                        
                except Exception as e:
                    # le=Errors.objects.all().last()
                    # print("le is:",le,type(le))
                    # if le.service == 'cnd_sen':
                    #     print("Error is alrady prasent")
                    # else:
                        erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='cnd_sen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                        erro.save()
                    # error_message = traceback.format_exc()
                    # print("error is:",e)
                # Send the error message to the WebSocket client
                    # send_error_message_to_websocket(error_message)
                    # error_message = e
                    # global eg
                    # eg = e
                    
                    
                    # EchoConsumer.websocket_receive('event','event')
                    

                try:
                    if 'tds_sen'== components:
                        if device_id not in device_idlist:
                            repo_latestdata.objects.create(device_id=device_id,message_type=msg_type,tds_sen=mydata1)
                        else:
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, tds_sen=mydata1)

                            get_device_id=repo_latestdata.objects.all()
                            for did in get_device_id:
                                s=str(did.device_id)
                                if device_id == s:
                                    
                                    
                                    tds1=did.tds_sen
                                    tds_sen=tds1
                                    # tdsstr=(str(tds))
                                    
                                    
                            
                            klist = list(tds_sen.keys())
                            
                            mydatakey = list(mydata1.keys())

                            for k,v in tds_sen.items():
                                if k not in mydatakey:
                                    olddata.update({k:v})
                                    
                            mydata5=olddata.update(mydata1)    
                            
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, tds_sen=olddata)
                        
                        dd=dateandtime()  
                    
                        ds=treat_tds_sen.objects.create(device_id=device_id,message_type=msg_type,tds=tds,spn=spn,tsp=tsp,asp=asp,year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                        ds.save()
                        if msg_type == 'updset':
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tds_sen settings has been updated span:{spn} trip_setpoint:{tsp} alert_setpoint:{asp}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='tds_sen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        else:
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tds_sen status has been updated conductivity:{tds}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='tds_sen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        # Hour
                        yrdata=treat_tds_sen.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_tds=0
                        sums_spn=0
                        sums_tsp=0
                        sums_asp=0
                        avgs_tds = 0
                        avgs_spn = 0
                        avgs_tsp = 0
                        avgs_asp = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    tdss=yr.tds
                                    spns=yr.spn
                                    tsps=yr.tsp
                                    asps=yr.asp
                                    
                                    sums_tds=sums_tds+tdss
                                    sums_spn=sums_spn+spns
                                    sums_tsp=sums_tsp+tsps
                                    sums_asp=sums_asp+asps
                                    count=count+1
                                    
                                    
                                    if tdss or spns or tsp or asp == 0:
                                        zerocount=zerocount+1
                                        
                            count1=count-zerocount
                            avgs_tds=sums_tds/count
                            avgs_spn=sums_spn/count
                            avgs_tsp=sums_tsp/count
                            avgs_asp=sums_asp/count
                        hr=tds_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        if hr:
                            yr_data=tds_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id).update(device_id=device_id,service='tds_tds_sen',tds={'sum':sums_tds,'avg':avgs_tds,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},tsp={'sum':sums_tsp,'avg':avgs_tsp,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=tds_repo_hourly.objects.create(device_id=device_id,service='tds_tds_sen',tds={'sum':sums_tds,'avg':avgs_tds,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},tsp={'sum':sums_tsp,'avg':avgs_tsp,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        
                        #day   
                        yrdata=treat_tds_sen.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        count=0
                        count_sum=0
                        count_tds=0
                        count_spn=0
                        count_tsp=0
                        count_asp=0
                        sums_tds=0
                        sums_spn=0
                        sums_tsp=0
                        sums_asp=0
                        avgs_tds = 0
                        avgs_spn = 0
                        avgs_tsp = 0
                        avgs_asp = 0
                        if yrdata:
                            for yr in yrdata:
                                
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    
                                    tdss_d=yr.tds
                                    spns_d=yr.spn
                                    tsps_d=yr.tsp
                                    asps_d=yr.asp
                                    sums_tds=sums_tds+tdss_d
                                    sums_spn=sums_spn+spns_d
                                    sums_tsp=sums_tsp+tsps_d
                                    sums_asp=sums_asp+asps_d
                                    count_sum=count_sum+count_tds

                                    count=count+1
                                    
                            
                            
                            avgs_tds=sums_tds/count
                            

                            avgs_spn=sums_spn/count
                            
                            avgs_tsp=sums_tsp/count
                            avgs_asp=sums_asp/count
                        hr=tds_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        if hr:
                            
                            yr_data=tds_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id).update(device_id=device_id,service='tds_tds_sen',tds={'sum':sums_tds,'avg':avgs_tds,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},tsp={'sum':sums_tsp,'avg':avgs_tsp,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                            
                        else:
                            yr_data=tds_repo_daily.objects.create(device_id=device_id,service='tds_tds_sen',tds={'sum':sums_tds,'avg':avgs_tds,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},tsp={'sum':sums_tsp,'avg':avgs_tsp,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                            yr_data.save()
                            
                        #month
                        
                        yrdata=treat_tds_sen.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        count=0
                        sums_tds=0
                        sums_spn=0
                        sums_tsp=0
                        sums_asp=0
                        avgs_tds = 0
                        avgs_spn = 0
                        avgs_tsp = 0
                        avgs_asp = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    tdss=yr.tds
                                    spns=yr.spn
                                    tsps=yr.tsp
                                    asps=yr.asp
                                    
                                    sums_tds=sums_tds+tdss
                                    sums_spn=sums_spn+spns
                                    sums_tsp=sums_tsp+tsps
                                    sums_asp=sums_asp+asps
                                    count=count+1
                                    
                                    
                                    if tdss or spns or tsp or asp == 0:
                                        zerocount=zerocount+1
                            
                            avgs_tds=sums_tds/count
                            avgs_spn=sums_spn/count
                            avgs_tsp=sums_tsp/count
                            avgs_asp=sums_asp/count
                        hr=tds_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        if hr:
                            yr_data=tds_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id).update(device_id=device_id,service='tds_tds_sen',tds={'sum':sums_tds,'avg':avgs_tds,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},tsp={'sum':sums_tsp,'avg':avgs_tsp,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                        else:
                            yr_data=tds_repo_monthly.objects.create(device_id=device_id,service='tds_tds_sen',tds={'sum':sums_tds,'avg':avgs_tds,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},tsp={'sum':sums_tsp,'avg':avgs_tsp,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                            yr_data.save()
                    
                        # year
                        yrdata=treat_tds_sen.objects.filter(year=dd[0],device_id=device_id)
                        count=0
                        sums_tds=0
                        sums_spn=0
                        sums_tsp=0
                        sums_asp=0
                        avgs_tds = 0
                        avgs_spn = 0
                        avgs_tsp = 0
                        avgs_asp = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    tdss=yr.tds
                                    spns=yr.spn
                                    tsps=yr.tsp
                                    asps=yr.asp
                                    
                                    sums_tds=sums_tds+tdss
                                    sums_spn=sums_spn+spns
                                    sums_tsp=sums_tsp+tsps
                                    sums_asp=sums_asp+asps
                                    count=count+1
                                    
                                    
                                    if tdss or spns or tsp or asp == 0:
                                        zerocount=zerocount+1
                            avgs_tds=sums_tds/count
                            avgs_spn=sums_spn/count
                            avgs_tsp=sums_tsp/count
                            avgs_asp=sums_asp/count
                        hr=tds_repo_yearly.objects.filter(year=dd[0],device_id=device_id)
                        if hr:
                            yr_data=tds_repo_yearly.objects.filter(device_id=device_id).update(device_id=device_id,service='tds_tds_sen',tds={'sum':sums_tds,'avg':avgs_tds,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},tsp={'sum':sums_tsp,'avg':avgs_tsp,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                        else:
                            yr_data=tds_repo_yearly.objects.create(device_id=device_id,service='tds_tds_sen',tds={'sum':sums_tds,'avg':avgs_tds,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},tsp={'sum':sums_tsp,'avg':avgs_tsp,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                            yr_data.save()
                                    
                except Exception as e:
                    # le=Errors.objects.all().last()
                    # print("le is:",le,type(le))
                    # if le.service == 'tds_sen':
                    #     print("Error is alrady prasent")
                    # else:
                        erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='tds_sen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                        erro.save()
                    # error_message = e

                    # # global eg
                    # eg = e
                try:
                    if 'rwp'==components:
                        
                        if device_id not in device_idlist:
                            repo_latestdata.objects.create(device_id=device_id,message_type=msg_type,rwp=mydata1)
                        else:
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, rwp=mydata1)

                            get_device_id=repo_latestdata.objects.all()
                            for did in get_device_id:
                                s=str(did.device_id)
                                if device_id == s:
                                    rwp=did.rwp
                                    # rwp=rwp
                            klist = list(rwp.keys())
                            
                            mydatakey = list(mydata1.keys())
                            
                            for k,v in rwp.items():
                                if k not in mydatakey:
                                    olddata.update({k:v})
                                    
                            mydata5=olddata.update(mydata1)    
                            
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, rwp=olddata)
                        dd=dateandtime()  
                        
                        
                        # repo_latestobj=repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id,message_type=msg_type,rwp=mydata1)
                        ds=treat_rwp.objects.create(device_id=device_id,message_type=msg_type,sts=sts,crt=crt,olc=olc,drc=drc,spn=spn,year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                        ds.save()
                        if msg_type == 'updset':
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} rwp settings has been updated over load current:{olc} dry run current:{drc} span:{spn}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='rwp',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        else:
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} rwp status has been updated status:{sts},current:{crt}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='rwp',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        # hour
                        yrdata=treat_rwp.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        count=0
                        sumd={}
                        sums_cnd=0
                        sums_spn=0
                        sums_tsp=0
                        sums_asp=0
                        avgs_cnd = 0
                        avgs_spn = 0
                        avgs_tsp = 0
                        avgs_asp = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    cnds=yr.crt
                                    spns=yr.olc
                                    tsps=yr.drc
                                    asps=yr.spn
                                    
                                    sums_cnd=sums_cnd+cnds
                                    sums_spn=sums_spn+spns
                                    sums_tsp=sums_tsp+tsps
                                    sums_asp=sums_asp+asps
                                    count=count+1
                                    
                                    
                            avgs_cnd=sums_cnd/count
                            avgs_spn=sums_spn/count
                            avgs_tsp=sums_tsp/count
                            avgs_asp=sums_asp/count
                            
                    
                        hr=rwp_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        if hr:
                            yr_data=rwp_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id).update(device_id=device_id,service='rwp',crt={'sum':sums_cnd,'avg':avgs_cnd,'count':count},olc={'sum':sums_spn,'avg':avgs_spn,'count':count},drc={'sum':sums_tsp,'avg':avgs_tsp,'count':count},spn={'sum':sums_asp,'avg':avgs_asp,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=rwp_repo_hourly.objects.create(device_id=device_id,service='rwp',crt={'sum':sums_cnd,'avg':avgs_cnd,'count':count},olc={'sum':sums_spn,'avg':avgs_spn,'count':count},drc={'sum':sums_tsp,'avg':avgs_tsp,'count':count},spn={'sum':sums_asp,'avg':avgs_asp,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                    
                        # day
                        yrdata=treat_rwp.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        count=0
                        count_sum=0
                        count_cnd=0
                        count_spn=0
                        count_tsp=0
                        count_asp=0
                        sums_cnd=0
                        sums_spn=0
                        sums_tsp=0
                        sums_asp=0
                        avgs_cnd = 0
                        avgs_spn = 0
                        avgs_tsp = 0
                        avgs_asp = 0
                        if yrdata:
                            for yr in yrdata:
                                
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    cnds=yr.crt
                                    spns=yr.olc
                                    tsps=yr.drc
                                    asps=yr.spn
                                    
                                    sums_cnd=sums_cnd+cnds
                                    sums_spn=sums_spn+spns
                                    sums_tsp=sums_tsp+tsps
                                    sums_asp=sums_asp+asps
                                    count=count+1
                            
                            avgs_cnd=sums_cnd/count
                            

                            avgs_spn=sums_spn/count
                            
                            avgs_tsp=sums_tsp/count
                            avgs_asp=sums_asp/count
                        hr=rwp_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        if hr:
                            
                            yr_data=rwp_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id).update(device_id=device_id,service='rwp',crt={'sum':sums_cnd,'avg':avgs_cnd,'count':count},olc={'sum':sums_spn,'avg':avgs_spn,'count':count},drc={'sum':sums_tsp,'avg':avgs_tsp,'count':count},spn={'sum':sums_asp,'avg':avgs_asp,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                            
                        else:
                            yr_data=rwp_repo_daily.objects.create(device_id=device_id,service='rwp',crt={'sum':sums_cnd,'avg':avgs_cnd,'count':count},olc={'sum':sums_spn,'avg':avgs_spn,'count':count},drc={'sum':sums_tsp,'avg':avgs_tsp,'count':count},spn={'sum':sums_asp,'avg':avgs_asp,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                            yr_data.save()
                        #monthly
                        yrdata=treat_rwp.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        count=0
                        sums_cnd=0
                        sums_spn=0
                        sums_tsp=0
                        sums_asp=0
                        avgs_cnd = 0
                        avgs_spn = 0
                        avgs_tsp = 0
                        avgs_asp = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    cnds=yr.crt
                                    spns=yr.olc
                                    tsps=yr.drc
                                    asps=yr.spn
                                    
                                    sums_cnd=sums_cnd+cnds
                                    sums_spn=sums_spn+spns
                                    sums_tsp=sums_tsp+tsps
                                    sums_asp=sums_asp+asps
                                    count=count+1
                                    count_sum=count_sum+count_cnd
                            
                            avgs_cnd=sums_cnd/count
                            avgs_spn=sums_spn/count
                            
                            avgs_tsp=sums_tsp/count
                            avgs_asp=sums_asp/count
                        hr=rwp_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        if hr:
                            yr_data=rwp_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id).update(device_id=device_id,service='rwp',crt={'sum':sums_cnd,'avg':avgs_cnd,'count':count},olc={'sum':sums_spn,'avg':avgs_spn,'count':count},drc={'sum':sums_tsp,'avg':avgs_tsp,'count':count},spn={'sum':sums_asp,'avg':avgs_asp,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                        else:
                            yr_data=rwp_repo_monthly.objects.create(device_id=device_id,service='rwp',crt={'sum':sums_cnd,'avg':avgs_cnd,'count':count},olc={'sum':sums_spn,'avg':avgs_spn,'count':count},drc={'sum':sums_tsp,'avg':avgs_tsp,'count':count},spn={'sum':sums_asp,'avg':avgs_asp,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                            yr_data.save()
                    
                        # year
                        yrdata=treat_rwp.objects.filter(year=dd[0],device_id=device_id)
                        count=0
                        sums_cnd=0
                        sums_spn=0
                        sums_tsp=0
                        sums_asp=0
                        avgs_cnd = 0
                        avgs_spn = 0
                        avgs_tsp = 0
                        avgs_asp = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    cnds=yr.crt
                                    spns=yr.olc
                                    tsps=yr.drc
                                    asps=yr.spn
                                    
                                    sums_cnd=sums_cnd+cnds
                                    sums_spn=sums_spn+spns
                                    sums_tsp=sums_tsp+tsps
                                    sums_asp=sums_asp+asps
                                    count=count+1
                                    count_sum=count_sum+count_cnd
                            avgs_cnd=sums_cnd/count
                            avgs_spn=sums_spn/count
                            
                            avgs_tsp=sums_tsp/count
                            avgs_asp=sums_asp/count
                        hr=rwp_repo_yearly.objects.filter(year=dd[0],device_id=device_id)
                        if hr:
                            yr_data=rwp_repo_yearly.objects.filter(device_id=device_id).update(device_id=device_id,service='rwp',crt={'sum':sums_cnd,'avg':avgs_cnd,'count':count},olc={'sum':sums_spn,'avg':avgs_spn,'count':count},drc={'sum':sums_tsp,'avg':avgs_tsp,'count':count},spn={'sum':sums_asp,'avg':avgs_asp,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                        else:
                            yr_data=rwp_repo_yearly.objects.create(device_id=device_id,service='rwp',crt={'sum':sums_cnd,'avg':avgs_cnd,'count':count},olc={'sum':sums_spn,'avg':avgs_spn,'count':count},drc={'sum':sums_tsp,'avg':avgs_tsp,'count':count},spn={'sum':sums_asp,'avg':avgs_asp,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                            yr_data.save()
                except Exception as e:
                    # le=Errors.objects.all().last()
                    # print("le is:",le,type(le))
                    # if le.service == 'rwp':
                    #     print("Error is alrady prasent")
                    # else:
                        erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='rwp',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                        erro.save()
                    # error_message = e
                    # # global eg
                    # eg = e
                    
                    
                    # EchoConsumer.websocket_receive('event','event')           
                try:
                    if 'hpp'==components:
                        # com=cl
                        if device_id not in device_idlist:
                            repo_latestdata.objects.create(device_id=device_id,message_type=msg_type,hpp=mydata1)
                        else:
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, hpp=mydata1)

                            get_device_id=repo_latestdata.objects.all()
                            for did in get_device_id:
                                s=str(did.device_id)
                                if device_id == s:
                                    hpp=did.hpp
                            klist = list(hpp.keys())
                            
                            mydatakey = list(mydata1.keys())
                            
                            for k,v in hpp.items():
                                if k not in mydatakey:
                                    olddata.update({k:v})
                                    
                            mydata5=olddata.update(mydata1)    
                            
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, hpp=olddata)

                        ds=treat_hpp.objects.create(device_id=device_id,message_type=msg_type,sts=sts,crt=crt,olc=olc,drc=drc,spn=spn,year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                        ds.save()
                        if msg_type == 'updset':
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} hpp settings has been updated over load current:{olc} dry run current:{drc} span:{spn}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='hpp',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        else:
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} hpp status has been updated status:{sts},current:{crt}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='hpp',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        # hour
                        yrdata=treat_hpp.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        count=0
                        sumd={}
                        sums_cnd=0
                        sums_spn=0
                        sums_tsp=0
                        sums_asp=0
                        avgs_cnd = 0
                        avgs_spn = 0
                        avgs_tsp = 0
                        avgs_asp = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    cnds=yr.crt
                                    spns=yr.olc
                                    tsps=yr.drc
                                    asps=yr.spn
                                    
                                    sums_cnd=sums_cnd+cnds
                                    sums_spn=sums_spn+spns
                                    sums_tsp=sums_tsp+tsps
                                    sums_asp=sums_asp+asps
                                    count=count+1
                                    
                                    
                            avgs_cnd=sums_cnd/count
                            avgs_spn=sums_spn/count
                            avgs_tsp=sums_tsp/count
                            avgs_asp=sums_asp/count
                            
                    
                        hr=hpp_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        if hr:
                            yr_data=hpp_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id).update(device_id=device_id,service='hpp',crt={'sum':sums_cnd,'avg':avgs_cnd,'count':count},olc={'sum':sums_spn,'avg':avgs_spn,'count':count},drc={'sum':sums_tsp,'avg':avgs_tsp,'count':count},spn={'sum':sums_asp,'avg':avgs_asp,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=hpp_repo_hourly.objects.create(device_id=device_id,service='hpp',crt={'sum':sums_cnd,'avg':avgs_cnd,'count':count},olc={'sum':sums_spn,'avg':avgs_spn,'count':count},drc={'sum':sums_tsp,'avg':avgs_tsp,'count':count},spn={'sum':sums_asp,'avg':avgs_asp,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                    
                        # day
                        yrdata=treat_hpp.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        count=0
                        count_sum=0
                        count_cnd=0
                        count_spn=0
                        count_tsp=0
                        count_asp=0
                        sums_cnd=0
                        sums_spn=0
                        sums_tsp=0
                        sums_asp=0
                        avgs_cnd = 0
                        avgs_spn = 0
                        avgs_tsp = 0
                        avgs_asp = 0
                        if yrdata:
                            for yr in yrdata:
                                
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    
                                    cnds=yr.crt
                                    spns=yr.olc
                                    tsps=yr.drc
                                    asps=yr.spn
                                    sums_cnd=sums_cnd+cnds
                                    sums_spn=sums_spn+spns
                                    sums_tsp=sums_tsp+tsps
                                    sums_asp=sums_asp+asps
                                    count=count+1
                                    count_sum=count_sum+count_cnd

                            avgs_cnd=sums_cnd/count
                            

                            avgs_spn=sums_spn/count
                            
                            avgs_tsp=sums_tsp/count
                            avgs_asp=sums_asp/count
                        hr=hpp_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        if hr:
                            
                            yr_data=hpp_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id).update(device_id=device_id,service='hpp',crt={'sum':sums_cnd,'avg':avgs_cnd,'count':count},olc={'sum':sums_spn,'avg':avgs_spn,'count':count},drc={'sum':sums_tsp,'avg':avgs_tsp,'count':count},spn={'sum':sums_asp,'avg':avgs_asp,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                            
                        else:
                            yr_data=hpp_repo_daily.objects.create(device_id=device_id,service='hpp',crt={'sum':sums_cnd,'avg':avgs_cnd,'count':count},olc={'sum':sums_spn,'avg':avgs_spn,'count':count},drc={'sum':sums_tsp,'avg':avgs_tsp,'count':count},spn={'sum':sums_asp,'avg':avgs_asp,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                            yr_data.save()
                        #monthly
                        yrdata=treat_hpp.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        count=0
                        sums_cnd=0
                        sums_spn=0
                        sums_tsp=0
                        sums_asp=0
                        avgs_cnd = 0
                        avgs_spn = 0
                        avgs_tsp = 0
                        avgs_asp = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    cnds=yr.crt
                                    spns=yr.olc
                                    tsps=yr.drc
                                    asps=yr.spn
                                    sums_cnd=sums_cnd+cnds
                                    sums_spn=sums_spn+spns
                                    sums_tsp=sums_tsp+tsps
                                    sums_asp=sums_asp+asps
                                    # count=count+1
                                    count_sum=count_sum+count_cnd

                                    count=count+1
                                    
                            
                            
                            avgs_cnd=sums_cnd/count
                            

                            avgs_spn=sums_spn/count
                            
                            avgs_tsp=sums_tsp/count
                            avgs_asp=sums_asp/count
                        hr=hpp_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        if hr:
                            yr_data=hpp_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id).update(device_id=device_id,service='hpp',crt={'sum':sums_cnd,'avg':avgs_cnd,'count':count},olc={'sum':sums_spn,'avg':avgs_spn,'count':count},drc={'sum':sums_tsp,'avg':avgs_tsp,'count':count},spn={'sum':sums_asp,'avg':avgs_asp,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                        else:
                            yr_data=hpp_repo_monthly.objects.create(device_id=device_id,service='hpp',crt={'sum':sums_cnd,'avg':avgs_cnd,'count':count},olc={'sum':sums_spn,'avg':avgs_spn,'count':count},drc={'sum':sums_tsp,'avg':avgs_tsp,'count':count},spn={'sum':sums_asp,'avg':avgs_asp,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                            yr_data.save()
                    
                        # year
                        yrdata=treat_hpp.objects.filter(year=dd[0],device_id=device_id)
                        count=0
                        sums_cnd=0
                        sums_spn=0
                        sums_tsp=0
                        sums_asp=0
                        avgs_cnd = 0
                        avgs_spn = 0
                        avgs_tsp = 0
                        avgs_asp = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    cnds=yr.crt
                                    spns=yr.olc
                                    tsps=yr.drc
                                    asps=yr.spn
                                    sums_cnd=sums_cnd+cnds
                                    sums_spn=sums_spn+spns
                                    sums_tsp=sums_tsp+tsps
                                    sums_asp=sums_asp+asps
                                    # count=count+1
                                    count_sum=count_sum+count_cnd
                                    count=count+1
                                    
                            
                            
                            avgs_cnd=sums_cnd/count
                            

                            avgs_spn=sums_spn/count
                            
                            avgs_tsp=sums_tsp/count
                            avgs_asp=sums_asp/count
                        hr=hpp_repo_yearly.objects.filter(year=dd[0],device_id=device_id)
                        if hr:
                            yr_data=hpp_repo_yearly.objects.filter(device_id=device_id).update(device_id=device_id,service='hpp',crt={'sum':sums_cnd,'avg':avgs_cnd,'count':count},olc={'sum':sums_spn,'avg':avgs_spn,'count':count},drc={'sum':sums_tsp,'avg':avgs_tsp,'count':count},spn={'sum':sums_asp,'avg':avgs_asp,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                        else:
                            yr_data=hpp_repo_yearly.objects.create(device_id=device_id,service='hpp',crt={'sum':sums_cnd,'avg':avgs_cnd,'count':count},olc={'sum':sums_spn,'avg':avgs_spn,'count':count},drc={'sum':sums_tsp,'avg':avgs_tsp,'count':count},spn={'sum':sums_asp,'avg':avgs_asp,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                            yr_data.save()
                except Exception as e:
                    # le=Errors.objects.all().last()
                    # print("le is:",le,type(le))
                    # if le.service == 'hpp':
                    #     print("Error is alrady prasent")
                    # else:
                        erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='hpp',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                        erro.save()
                    # error_message = e
                    # # global eg
                    # eg = e
                    
                    
                    # EchoConsumer.websocket_receive('event','event')  
                try:
                    # print("00000000000000000000000000")
                    if 'panel'==components:
                        # com=cl
                        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                        if device_id not in device_idlist:
                            repo_latestdata.objects.create(device_id=device_id,message_type=msg_type,panel=mydata1)
                        else:
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, panel=mydata1)

                            get_device_id=repo_latestdata.objects.all()
                            for did in get_device_id:
                                s=str(did.device_id)
                                if device_id == s:
                                    panel=did.panel
                            klist = list(panel.keys())
                            
                            mydatakey = list(mydata1.keys())
                            
                            for k,v in panel.items():
                                if k not in mydatakey:
                                    olddata.update({k:v})
                                    
                            mydata5=olddata.update(mydata1)    
                            
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, panel=olddata)

                        ds=treat_panel.objects.create(device_id=device_id,message_type=msg_type,sts=sts,rtl=rtl,ttl=ttl,lps=lps,hps=hps,dgp=dgp,mod=mod,ipv=ipv,unv=unv,ovv=ovv,spn=spn,nmv=nmv,stp=stp,srt=srt,bkt=bkt,rst=rst,err=err,year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                        ds.save()
                        if msg_type == 'updset':
                            dd=dateandtime()
                            e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]}panel settings has been updated mode:{mod} under voltage:{unv} over voltage:{ovv} span:{spn} no.of multiport valve:{nmv} sensor type:{stp} service time:{srt} backwash time:{bkt} rinse time:{rst}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e,service='panel',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        else:
                            dd=dateandtime()
                            e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} panel status has been updated status:{sts},row water tank level:{rtl} trated water tank level:{ttl} low pressure switch:{lps} high pressure switch:{hps} dosing pump:{dgp} input voltage:{ipv} error:{err}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e,service='panel',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        
                        #hour
                        yrdata=treat_panel.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        count=0
                        sums_ipv=0
                        sums_unv=0
                        sums_ovv=0
                        sums_spn=0
                        sums_nmv=0
                        sums_srt=0
                        sums_bkt=0
                        sums_rst=0
                        avgs_ipv = 0
                        avgs_unv = 0
                        avgs_ovv = 0
                        avgs_spn = 0
                        avgs_nmv = 0
                        avgs_srt = 0
                        avgs_bkt = 0
                        avgs_rst = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    ipvo=yr.ipv
                                    unvo=yr.unv
                                    ovvo=yr.ovv
                                    spno=yr.spn
                                    nmvo=yr.nmv
                                    srto=yr.srt
                                    bkto=yr.bkt
                                    rsto=yr.rst
                                    
                                    sums_ipv=sums_ipv+ipvo
                                    sums_unv=sums_unv+unvo
                                    sums_ovv=sums_ovv+ovvo
                                    sums_spn=sums_spn+spno
                                    sums_nmv=sums_nmv+nmvo
                                    srto=srto.replace(':','')
                                    sums_srt=sums_srt+int(srto)
                                    sums_bkt=sums_bkt+bkto
                                    
                                    sums_rst=sums_rst+rsto
                                    count=count+1
                                    
                            avgs_ipv=sums_ipv/count
                            
                            avgs_unv=sums_unv/count
                            
                            avgs_ovv=sums_ovv/count
                            avgs_spn=sums_spn/count
                            avgs_nmv=sums_nmv/count
                            avgs_srt=sums_srt/count
                            avgs_bkt=sums_bkt/count
                            avgs_rst=sums_rst/count
                            
                        hr=panel_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        if hr:
                            yr_data=panel_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id).update(device_id=device_id,service='panel',ipv={'sum':sums_ipv,'avg':avgs_ipv,'count':count},unv={'sum':sums_unv,'avg':avgs_unv,'count':count},ovv={'sum':sums_ovv,'avg':avgs_ovv,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},nmv={'sum':sums_nmv,'avg':avgs_nmv,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                        else:
                            yr_data=panel_repo_hourly.objects.create(device_id=device_id,service='panel',ipv={'sum':sums_ipv,'avg':avgs_ipv,'count':count},unv={'sum':sums_unv,'avg':avgs_unv,'count':count},ovv={'sum':sums_ovv,'avg':avgs_ovv,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},nmv={'sum':sums_nmv,'avg':avgs_nmv,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                            yr_data.save()
                        # month
                        yrdata=treat_panel.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        count=0
                        sums_ipv=0
                        sums_unv=0
                        sums_ovv=0
                        sums_spn=0
                        sums_nmv=0
                        sums_srt=0
                        sums_bkt=0
                        sums_rst=0
                        avgs_ipv = 0
                        avgs_unv = 0
                        avgs_ovv = 0
                        avgs_spn = 0
                        avgs_nmv = 0
                        avgs_srt = 0
                        avgs_bkt = 0
                        avgs_rst = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    ipv=yr.ipv
                                    unv=yr.unv
                                    ovv=yr.ovv
                                    spn=yr.spn
                                    nmv=yr.nmv
                                    srt=yr.srt
                                    bkt=yr.bkt
                                    rst=yr.rst
                                    sums_ipv=sums_ipv+ipv
                                    sums_unv=sums_unv+unv
                                    sums_ovv=sums_ovv+ovv
                                    sums_spn=sums_spn+spn
                                    sums_nmv=sums_nmv+nmv
                                    # srt=srt.replace(':','')
                                    sums_srt=sums_srt+int(srt)
                                    sums_bkt=sums_bkt+bkt
                                    sums_rst=sums_rst+rst
                                    count=count+1
                                    
                            avgs_ipv=sums_ipv/count
                            
                            avgs_unv=sums_unv/count
                            
                            avgs_ovv=sums_ovv/count
                            avgs_spn=sums_spn/count
                            avgs_nmv=sums_nmv/count
                            avgs_srt=sums_srt/count
                            avgs_bkt=sums_bkt/count
                            avgs_rst=sums_rst/count
                        hr=panel_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        if hr:
                            yr_data=panel_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id).update(device_id=device_id,service='panel',ipv={'sum':sums_ipv,'avg':avgs_ipv,'count':count},unv={'sum':sums_unv,'avg':avgs_unv,'count':count},ovv={'sum':sums_ovv,'avg':avgs_ovv,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},nmv={'sum':sums_nmv,'avg':avgs_nmv,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                        else:
                            yr_data=panel_repo_monthly.objects.create(device_id=device_id,service='panel',ipv={'sum':sums_ipv,'avg':avgs_ipv,'count':count},unv={'sum':sums_unv,'avg':avgs_unv,'count':count},ovv={'sum':sums_ovv,'avg':avgs_ovv,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},nmv={'sum':sums_nmv,'avg':avgs_nmv,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                            yr_data.save()
                    # day
                        yrdata=treat_panel.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        count=0
                        sums_ipv=0
                        sums_unv=0
                        sums_ovv=0
                        sums_spn=0
                        sums_nmv=0
                        sums_srt=0
                        sums_bkt=0
                        sums_rst=0
                        avgs_ipv = 0
                        avgs_unv = 0
                        avgs_ovv = 0
                        avgs_spn = 0
                        avgs_nmv = 0
                        avgs_srt = 0
                        avgs_bkt = 0
                        avgs_rst = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    ipv=yr.ipv
                                    unv=yr.unv
                                    ovv=yr.ovv
                                    spn=yr.spn
                                    nmv=yr.nmv
                                    srt=yr.srt
                                    bkt=yr.bkt
                                    rst=yr.rst
                                    sums_ipv=sums_ipv+ipv
                                    sums_unv=sums_unv+unv
                                    sums_ovv=sums_ovv+ovv
                                    sums_spn=sums_spn+spn
                                    sums_nmv=sums_nmv+nmv
                                    # srt=srt.replace(':','')
                                    sums_srt=sums_srt+int(srt)
                                    sums_bkt=sums_bkt+bkt
                                    sums_rst=sums_rst+rst
                                    count=count+1
                                    
                            avgs_ipv=sums_ipv/count
                            
                            avgs_unv=sums_unv/count
                            
                            avgs_ovv=sums_ovv/count
                            avgs_spn=sums_spn/count
                            avgs_nmv=sums_nmv/count
                            avgs_srt=sums_srt/count
                            avgs_bkt=sums_bkt/count
                            avgs_rst=sums_rst/count
                        hr=panel_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        if hr:
                            yr_data=panel_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id).update(device_id=device_id,service='panel',ipv={'sum':sums_ipv,'avg':avgs_ipv,'count':count},unv={'sum':sums_unv,'avg':avgs_unv,'count':count},ovv={'sum':sums_ovv,'avg':avgs_ovv,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},nmv={'sum':sums_nmv,'avg':avgs_nmv,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                        else:
                            yr_data=panel_repo_daily.objects.create(device_id=device_id,service='panel',ipv={'sum':sums_ipv,'avg':avgs_ipv,'count':count},unv={'sum':sums_unv,'avg':avgs_unv,'count':count},ovv={'sum':sums_ovv,'avg':avgs_ovv,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},nmv={'sum':sums_nmv,'avg':avgs_nmv,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                            yr_data.save()
                    #year
                        yrdata=treat_panel.objects.filter(year=dd[0],device_id=device_id)
                        count=0
                        sums_ipv=0
                        sums_unv=0
                        sums_ovv=0
                        sums_spn=0
                        sums_nmv=0
                        sums_srt=0
                        sums_bkt=0
                        sums_rst=0
                        avgs_ipv = 0
                        avgs_unv = 0
                        avgs_ovv = 0
                        avgs_spn = 0
                        avgs_nmv = 0
                        avgs_srt = 0
                        avgs_bkt = 0
                        avgs_rst = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    ipv=yr.ipv
                                    unv=yr.unv
                                    ovv=yr.ovv
                                    spn=yr.spn
                                    nmv=yr.nmv
                                    srt=yr.srt
                                    bkt=yr.bkt
                                    rst=yr.rst
                                    sums_ipv=sums_ipv+ipv
                                    sums_unv=sums_unv+unv
                                    sums_ovv=sums_ovv+ovv
                                    sums_spn=sums_spn+spn
                                    sums_nmv=sums_nmv+nmv
                                    # srt=srt.replace(':','')
                                    sums_srt=sums_srt+int(srt)
                                    sums_bkt=sums_bkt+bkt
                                    sums_rst=sums_rst+rst
                                    count=count+1
                                    
                            avgs_ipv=sums_ipv/count
                            
                            avgs_unv=sums_unv/count
                            
                            avgs_ovv=sums_ovv/count
                            avgs_spn=sums_spn/count
                            avgs_nmv=sums_nmv/count
                            avgs_srt=sums_srt/count
                            avgs_bkt=sums_bkt/count
                            avgs_rst=sums_rst/count
                        hr=panel_repo_yearly.objects.filter(year=dd[0],device_id=device_id)
                        if hr:
                            yr_data=panel_repo_yearly.objects.filter(year=dd[0],device_id=device_id).update(device_id=device_id,service='panel',ipv={'sum':sums_ipv,'avg':avgs_ipv,'count':count},unv={'sum':sums_unv,'avg':avgs_unv,'count':count},ovv={'sum':sums_ovv,'avg':avgs_ovv,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},nmv={'sum':sums_nmv,'avg':avgs_nmv,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                        else:
                            yr_data=panel_repo_yearly.objects.create(device_id=device_id,service='panel',ipv={'sum':sums_ipv,'avg':avgs_ipv,'count':count},unv={'sum':sums_unv,'avg':avgs_unv,'count':count},ovv={'sum':sums_ovv,'avg':avgs_ovv,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},nmv={'sum':sums_nmv,'avg':avgs_nmv,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},month=dd[1],year=dd[0],day=dd[2],hour=dd[3])
                            yr_data.save()
                except Exception as e:
                    # le=Errors.objects.all().last()
                    # print("le is:",le,type(le))
                    # if le.service == 'panel':
                    #     print("Error is alrady prasent")
                    # else:
                        erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='panel',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                        erro.save()
                    # error_message = e
                    # # global eg
                    # eg = e
                        
                try:
                    if 'ampv1'==components:
                        # com=cl
                        if device_id not in device_idlist:
                            repo_latestdata.objects.create(device_id=device_id,message_type=msg_type,ampv1=mydata1)
                        else:
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, ampv1=mydata1)

                            get_device_id=repo_latestdata.objects.all()
                            for did in get_device_id:
                                s=str(did.device_id)
                                if device_id == s:
                                    ampv1=did.ampv1
                            klist = list(ampv1.keys())
                            
                            mydatakey = list(mydata1.keys())
                            
                            for k,v in ampv1.items():
                                if k not in mydatakey:
                                    olddata.update({k:v})
                                    
                            mydata5=olddata.update(mydata1)    
                            
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, ampv1=olddata)

                        ds=treat_ampv1.objects.create(device_id=device_id,message_type=msg_type,pos=pos,rmt=rmt,cct=cct,srt=srt,bkt=bkt,rst=rst,mot=mot,stp=stp,op1=op1,op2=op2,op3=op3,ip1=ip1,ip2=ip2,ip3=ip3,psi=psi,year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                        ds.save()
                        if msg_type == 'updset':
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} ampv1 settings has been updated service time:{srt} backwash time:{bkt} rinse time:{rst} motor on delay time:{mot}sensor type:{stp} output1:{op1}output2:{op2}output3:{op3}input1:{ip1}input2:{ip2}input3:{ip3}pressure switch input:{psi}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='ampv1',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        else:
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} ampv1 status has been updated position:{pos}remaining time:{rmt}cycle count:{cct}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='ampv1',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        
                        #hour
                        yrdata=treat_ampv1.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_rmt=0
                        sums_cct=0
                        sums_srt=0
                        sums_bkt=0
                        sums_rst=0
                        sums_mot=0
                        avgs_rmt = 0
                        avgs_cct = 0
                        avgs_srt = 0
                        avgs_bkt = 0
                        avgs_rst = 0
                        avgs_mot = 0
                        # avgs_bktsums_bkt = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    rmt=yr.rmt
                                    cct=yr.cct
                                    srt=yr.srt
                                    bkt=yr.bkt
                                    rst=yr.rst
                                    mot=yr.mot
                                    sums_rmt=sums_rmt+rmt
                                    sums_cct=sums_cct+cct
                                    # srt=srt.replace(':','')
                                    sums_srt=sums_srt+int(srt)
                                    sums_bkt=sums_bkt+bkt
                                    sums_rst=sums_rst+rst
                                    sums_mot=sums_mot+mot
                                    count=count+1
                            avgs_rmt=sums_rmt/count
                            avgs_cct=sums_cct/count
                            avgs_srt=sums_srt/count
                            avgs_bkt=sums_bkt/count
                            avgs_rst=sums_rst/count
                            avgs_mot=sums_mot/count
                        hr=ampv1_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        if hr:
                            yr_data=ampv1_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id).update(device_id=device_id,service='ampv1',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=ampv1_repo_hourly.objects.create(device_id=device_id,service='ampv1',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #daily
                        yrdata=treat_ampv1.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_rmt=0
                        sums_cct=0
                        sums_srt=0
                        sums_bkt=0
                        sums_rst=0
                        sums_mot=0
                        avgs_rmt = 0
                        avgs_cct = 0
                        avgs_srt = 0
                        avgs_bkt = 0
                        avgs_rst = 0
                        avgs_mot = 0
                        # avgs_bktsums_bkt = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    rmt=yr.rmt
                                    cct=yr.cct
                                    srt=yr.srt
                                    bkt=yr.bkt
                                    rst=yr.rst
                                    mot=yr.mot
                                    sums_rmt=sums_rmt+rmt
                                    sums_cct=sums_cct+cct
                                    # srt=srt.replace(':','')
                                    sums_srt=sums_srt+int(srt)
                                    sums_bkt=sums_bkt+bkt
                                    sums_rst=sums_rst+rst
                                    sums_mot=sums_mot+mot
                                    count=count+1
                            avgs_rmt=sums_rmt/count
                            avgs_cct=sums_cct/count
                            avgs_srt=sums_srt/count
                            avgs_bkt=sums_bkt/count
                            avgs_rst=sums_rst/count
                            avgs_mot=sums_mot/count
                        hr=ampv1_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        if hr:
                            yr_data=ampv1_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id).update(device_id=device_id,service='ampv1',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=ampv1_repo_daily.objects.create(device_id=device_id,service='ampv1',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #month
                        yrdata=treat_ampv1.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_rmt=0
                        sums_cct=0
                        sums_srt=0
                        sums_bkt=0
                        sums_rst=0
                        sums_mot=0
                        avgs_rmt = 0
                        avgs_cct = 0
                        avgs_srt = 0
                        avgs_bkt = 0
                        avgs_rst = 0
                        avgs_mot = 0
                        # avgs_bktsums_bkt = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    rmt=yr.rmt
                                    cct=yr.cct
                                    srt=yr.srt
                                    bkt=yr.bkt
                                    rst=yr.rst
                                    mot=yr.mot
                                    sums_rmt=sums_rmt+rmt
                                    sums_cct=sums_cct+cct
                                    # srt=srt.replace(':','')
                                    sums_srt=sums_srt+int(srt)
                                    sums_bkt=sums_bkt+bkt
                                    sums_rst=sums_rst+rst
                                    sums_mot=sums_mot+mot
                                    count=count+1
                            avgs_rmt=sums_rmt/count
                            avgs_cct=sums_cct/count
                            avgs_srt=sums_srt/count
                            avgs_bkt=sums_bkt/count
                            avgs_rst=sums_rst/count
                            avgs_mot=sums_mot/count
                        hr=ampv1_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        if hr:
                            yr_data=ampv1_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id).update(device_id=device_id,service='ampv1',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=ampv1_repo_monthly.objects.create(device_id=device_id,service='ampv1',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #year
                        yrdata=treat_ampv1.objects.filter(year=dd[0],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_rmt=0
                        sums_cct=0
                        sums_srt=0
                        sums_bkt=0
                        sums_rst=0
                        sums_mot=0
                        avgs_rmt = 0
                        avgs_cct = 0
                        avgs_srt = 0
                        avgs_bkt = 0
                        avgs_rst = 0
                        avgs_mot = 0
                        # avgs_bktsums_bkt = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    rmt=yr.rmt
                                    cct=yr.cct
                                    srt=yr.srt
                                    bkt=yr.bkt
                                    rst=yr.rst
                                    mot=yr.mot
                                    sums_rmt=sums_rmt+rmt
                                    sums_cct=sums_cct+cct
                                    # srt=srt.replace(':','')
                                    sums_srt=sums_srt+int(srt)
                                    sums_bkt=sums_bkt+bkt
                                    sums_rst=sums_rst+rst
                                    sums_mot=sums_mot+mot
                                    count=count+1
                            avgs_rmt=sums_rmt/count
                            avgs_cct=sums_cct/count
                            avgs_srt=sums_srt/count
                            avgs_bkt=sums_bkt/count
                            avgs_rst=sums_rst/count
                            avgs_mot=sums_mot/count
                        hr=ampv1_repo_yearly.objects.filter(year=dd[0],device_id=device_id)
                        if hr:
                            yr_data=ampv1_repo_yearly.objects.filter(year=dd[0],device_id=device_id).update(device_id=device_id,service='ampv1',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=ampv1_repo_yearly.objects.create(device_id=device_id,service='ampv1',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                except Exception as e:
                    # le=Errors.objects.all().last()
                    # print("le is:",le,type(le))
                    # if le.service == 'ampv1':
                    #     print("Error is alrady prasent")
                    # else:
                        erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='ampv1',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                        erro.save()
                    # error_message = e
                    # # global eg
                    # eg = e
                    
                    
                    # EchoConsumer.websocket_receive('event','event') 
                try:
                    if 'ampv2'==components:
                        # com=cl

                        if device_id not in device_idlist:
                            repo_latestdata.objects.create(device_id=device_id,message_type=msg_type,ampv2=mydata1)
                        else:
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, ampv2=mydata1)

                            get_device_id=repo_latestdata.objects.all()
                            for did in get_device_id:
                                s=str(did.device_id)
                                if device_id == s:
                                    ampv2=did.ampv2
                            klist = list(ampv2.keys())
                            
                            mydatakey = list(mydata1.keys())
                            
                            for k,v in ampv2.items():
                                if k not in mydatakey:
                                    olddata.update({k:v})
                                    
                            mydata5=olddata.update(mydata1)    
                            
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, ampv2=olddata)

                        # repo_latestobj=repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id,message_type=msg_type,ampv2=mydata1)
                        # repo_latestobj.save()
                        ds=treat_ampv2.objects.create(device_id=device_id,message_type=msg_type,pos=pos,rmt=rmt,cct=cct,srt=srt,bkt=bkt,rst=rst,mot=mot,stp=stp,op1=op1,op2=op2,op3=op3,ip1=ip1,ip2=ip2,ip3=ip3,psi=psi,year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                        ds.save()
                        if msg_type == 'updset':
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} ampv2 settings has been updated service time:{srt} backwash time:{bkt} rinse time:{rst} motor on delay time:{mot}sensor type:{stp} output1:{op1}output2:{op2}output3:{op3}input1:{ip1}input2:{ip2}input3:{ip3}pressure switch input:{psi}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='ampv2',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        else:
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} ampv2 status has been updated position:{pos}remaining time:{rmt}cycle count:{cct}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='ampv2',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        #hour
                        yrdata=treat_ampv2.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_rmt=0
                        sums_cct=0
                        sums_srt=0
                        sums_bkt=0
                        sums_rst=0
                        sums_mot=0
                        avgs_rmt = 0
                        avgs_cct = 0
                        avgs_srt = 0
                        avgs_bkt = 0
                        avgs_rst = 0
                        avgs_mot = 0
                        # avgs_bktsums_bkt = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    rmt=yr.rmt
                                    cct=yr.cct
                                    srt=yr.srt
                                    bkt=yr.bkt
                                    rst=yr.rst
                                    mot=yr.mot
                                    sums_rmt=sums_rmt+rmt
                                    sums_cct=sums_cct+cct
                                    # srt=srt.replace(':','')
                                    sums_srt=sums_srt+int(srt)
                                    sums_bkt=sums_bkt+bkt
                                    sums_rst=sums_rst+rst
                                    sums_mot=sums_mot+mot
                                    count=count+1
                            avgs_rmt=sums_rmt/count
                            avgs_cct=sums_cct/count
                            avgs_srt=sums_srt/count
                            avgs_bkt=sums_bkt/count
                            avgs_rst=sums_rst/count
                            avgs_mot=sums_mot/count
                        hr=ampv2_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        if hr:
                            yr_data=ampv2_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id).update(device_id=device_id,service='ampv2',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=ampv2_repo_hourly.objects.create(device_id=device_id,service='ampv2',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #daily
                        yrdata=treat_ampv2.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_rmt=0
                        sums_cct=0
                        sums_srt=0
                        sums_bkt=0
                        sums_rst=0
                        sums_mot=0
                        avgs_rmt = 0
                        avgs_cct = 0
                        avgs_srt = 0
                        avgs_bkt = 0
                        avgs_rst = 0
                        avgs_mot = 0
                        # avgs_bktsums_bkt = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    rmt=yr.rmt
                                    cct=yr.cct
                                    srt=yr.srt
                                    bkt=yr.bkt
                                    rst=yr.rst
                                    mot=yr.mot
                                    sums_rmt=sums_rmt+rmt
                                    sums_cct=sums_cct+cct
                                    # srt=srt.replace(':','')
                                    sums_srt=sums_srt+int(srt)
                                    sums_bkt=sums_bkt+bkt
                                    sums_rst=sums_rst+rst
                                    sums_mot=sums_mot+mot
                                    count=count+1
                            avgs_rmt=sums_rmt/count
                            avgs_cct=sums_cct/count
                            avgs_srt=sums_srt/count
                            avgs_bkt=sums_bkt/count
                            avgs_rst=sums_rst/count
                            avgs_mot=sums_mot/count
                        hr=ampv2_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        if hr:
                            yr_data=ampv2_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id).update(device_id=device_id,service='ampv2',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=ampv2_repo_daily.objects.create(device_id=device_id,service='ampv2',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #month
                        yrdata=treat_ampv2.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_rmt=0
                        sums_cct=0
                        sums_srt=0
                        sums_bkt=0
                        sums_rst=0
                        sums_mot=0
                        avgs_rmt = 0
                        avgs_cct = 0
                        avgs_srt = 0
                        avgs_bkt = 0
                        avgs_rst = 0
                        avgs_mot = 0
                        # avgs_bktsums_bkt = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    rmt=yr.rmt
                                    cct=yr.cct
                                    srt=yr.srt
                                    bkt=yr.bkt
                                    rst=yr.rst
                                    mot=yr.mot
                                    sums_rmt=sums_rmt+rmt
                                    sums_cct=sums_cct+cct
                                    # srt=srt.replace(':','')
                                    sums_srt=sums_srt+int(srt)
                                    sums_bkt=sums_bkt+bkt
                                    sums_rst=sums_rst+rst
                                    sums_mot=sums_mot+mot
                                    count=count+1
                            avgs_rmt=sums_rmt/count
                            avgs_cct=sums_cct/count
                            avgs_srt=sums_srt/count
                            avgs_bkt=sums_bkt/count
                            avgs_rst=sums_rst/count
                            avgs_mot=sums_mot/count
                        hr=ampv2_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        if hr:
                            yr_data=ampv2_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id).update(device_id=device_id,service='ampv2',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=ampv2_repo_monthly.objects.create(device_id=device_id,service='ampv2',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #year
                        yrdata=treat_ampv2.objects.filter(year=dd[0],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_rmt=0
                        sums_cct=0
                        sums_srt=0
                        sums_bkt=0
                        sums_rst=0
                        sums_mot=0
                        avgs_rmt = 0
                        avgs_cct = 0
                        avgs_srt = 0
                        avgs_bkt = 0
                        avgs_rst = 0
                        avgs_mot = 0
                        # avgs_bktsums_bkt = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    rmt=yr.rmt
                                    cct=yr.cct
                                    srt=yr.srt
                                    bkt=yr.bkt
                                    rst=yr.rst
                                    mot=yr.mot
                                    sums_rmt=sums_rmt+rmt
                                    sums_cct=sums_cct+cct
                                    # srt=srt.replace(':','')
                                    sums_srt=sums_srt+int(srt)
                                    sums_bkt=sums_bkt+bkt
                                    sums_rst=sums_rst+rst
                                    sums_mot=sums_mot+mot
                                    count=count+1
                            avgs_rmt=sums_rmt/count
                            avgs_cct=sums_cct/count
                            avgs_srt=sums_srt/count
                            avgs_bkt=sums_bkt/count
                            avgs_rst=sums_rst/count
                            avgs_mot=sums_mot/count
                        hr=ampv2_repo_yearly.objects.filter(year=dd[0],device_id=device_id)
                        if hr:
                            yr_data=ampv2_repo_yearly.objects.filter(year=dd[0],device_id=device_id).update(device_id=device_id,service='ampv2',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=ampv2_repo_yearly.objects.create(device_id=device_id,service='ampv2',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                except Exception as e:
                    # le=Errors.objects.all().last()
                    # print("le is:",le,type(le))
                    # if le.service == 'ampv2':
                    #     print("Error is alrady prasent")
                    # else:
                        erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='ampv2',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                        erro.save()
                    # error_message = e
                    # # global eg
                    # eg = e
                    
                    
                    # EchoConsumer.websocket_receive('event','event') 
                try:
                    if 'ampv3'==components:
                        # com=cl
                        if device_id not in device_idlist:
                            repo_latestdata.objects.create(device_id=device_id,message_type=msg_type,ampv3=mydata1)
                        else:
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, ampv3=mydata1)

                            get_device_id=repo_latestdata.objects.all()
                            for did in get_device_id:
                                s=str(did.device_id)
                                if device_id == s:
                                    ampv3=did.ampv3
                            klist = list(ampv3.keys())
                            
                            mydatakey = list(mydata1.keys())
                            
                            for k,v in ampv3.items():
                                if k not in mydatakey:
                                    olddata.update({k:v})
                                    
                            mydata5=olddata.update(mydata1)    
                            
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, ampv3=olddata)

                        ds=treat_ampv3.objects.create(device_id=device_id,message_type=msg_type,pos=pos,rmt=rmt,cct=cct,srt=srt,bkt=bkt,rst=rst,mot=mot,stp=stp,op1=op1,op2=op2,op3=op3,ip1=ip1,ip2=ip2,ip3=ip3,psi=psi,year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                        ds.save()
                        if msg_type == 'updset':
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} ampv3 settings has been updated service time:{srt} backwash time:{bkt} rinse time:{rst} motor on delay time:{mot}sensor type:{stp} output1:{op1}output2:{op2}output3:{op3}input1:{ip1}input2:{ip2}input3:{ip3}pressure switch input:{psi}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='ampv3',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        else:
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} ampv3 status has been updated position:{pos}remaining time:{rmt}cycle count:{cct}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='ampv3',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        #hour
                        yrdata=treat_ampv3.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_rmt=0
                        sums_cct=0
                        sums_srt=0
                        sums_bkt=0
                        sums_rst=0
                        sums_mot=0
                        avgs_rmt = 0
                        avgs_cct = 0
                        avgs_srt = 0
                        avgs_bkt = 0
                        avgs_rst = 0
                        avgs_mot = 0
                        # avgs_bktsums_bkt = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    rmt=yr.rmt
                                    cct=yr.cct
                                    srt=yr.srt
                                    bkt=yr.bkt
                                    rst=yr.rst
                                    mot=yr.mot
                                    sums_rmt=sums_rmt+rmt
                                    sums_cct=sums_cct+cct
                                    # srt=srt.replace(':','')
                                    sums_srt=sums_srt+int(srt)
                                    sums_bkt=sums_bkt+bkt
                                    sums_rst=sums_rst+rst
                                    sums_mot=sums_mot+mot
                                    count=count+1
                            avgs_rmt=sums_rmt/count
                            avgs_cct=sums_cct/count
                            avgs_srt=sums_srt/count
                            avgs_bkt=sums_bkt/count
                            avgs_rst=sums_rst/count
                            avgs_mot=sums_mot/count
                        hr=ampv3_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        if hr:
                            yr_data=ampv3_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id).update(device_id=device_id,service='ampv3',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=ampv3_repo_hourly.objects.create(device_id=device_id,service='ampv3',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #daily
                        yrdata=treat_ampv3.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_rmt=0
                        sums_cct=0
                        sums_srt=0
                        sums_bkt=0
                        sums_rst=0
                        sums_mot=0
                        avgs_rmt = 0
                        avgs_cct = 0
                        avgs_srt = 0
                        avgs_bkt = 0
                        avgs_rst = 0
                        avgs_mot = 0
                        # avgs_bktsums_bkt = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    rmt=yr.rmt
                                    cct=yr.cct
                                    srt=yr.srt
                                    bkt=yr.bkt
                                    rst=yr.rst
                                    mot=yr.mot
                                    sums_rmt=sums_rmt+rmt
                                    sums_cct=sums_cct+cct
                                    sums_srt=sums_srt+int(srt)
                                    sums_bkt=sums_bkt+bkt
                                    sums_rst=sums_rst+rst
                                    sums_mot=sums_mot+mot
                                    count=count+1
                            avgs_rmt=sums_rmt/count
                            avgs_cct=sums_cct/count
                            avgs_srt=sums_srt/count
                            avgs_bkt=sums_bkt/count
                            avgs_rst=sums_rst/count
                            avgs_mot=sums_mot/count
                        hr=ampv3_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        if hr:
                            yr_data=ampv3_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id).update(device_id=device_id,service='ampv3',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=ampv3_repo_daily.objects.create(device_id=device_id,service='ampv3',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #month
                        yrdata=treat_ampv3.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_rmt=0
                        sums_cct=0
                        sums_srt=0
                        sums_bkt=0
                        sums_rst=0
                        sums_mot=0
                        avgs_rmt = 0
                        avgs_cct = 0
                        avgs_srt = 0
                        avgs_bkt = 0
                        avgs_rst = 0
                        avgs_mot = 0
                        # avgs_bktsums_bkt = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    rmt=yr.rmt
                                    cct=yr.cct
                                    srt=yr.srt
                                    bkt=yr.bkt
                                    rst=yr.rst
                                    mot=yr.mot
                                    sums_rmt=sums_rmt+rmt
                                    sums_cct=sums_cct+cct
                                    sums_srt=sums_srt+int(srt)
                                    sums_bkt=sums_bkt+bkt
                                    sums_rst=sums_rst+rst
                                    sums_mot=sums_mot+mot
                                    count=count+1
                            avgs_rmt=sums_rmt/count
                            avgs_cct=sums_cct/count
                            avgs_srt=sums_srt/count
                            avgs_bkt=sums_bkt/count
                            avgs_rst=sums_rst/count
                            avgs_mot=sums_mot/count
                        hr=ampv3_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        if hr:
                            yr_data=ampv3_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id).update(device_id=device_id,service='ampv3',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=ampv3_repo_monthly.objects.create(device_id=device_id,service='ampv3',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #year
                        yrdata=treat_ampv3.objects.filter(year=dd[0],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_rmt=0
                        sums_cct=0
                        sums_srt=0
                        sums_bkt=0
                        sums_rst=0
                        sums_mot=0
                        avgs_rmt = 0
                        avgs_cct = 0
                        avgs_srt = 0
                        avgs_bkt = 0
                        avgs_rst = 0
                        avgs_mot = 0
                        # avgs_bktsums_bkt = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    rmt=yr.rmt
                                    cct=yr.cct
                                    srt=yr.srt
                                    bkt=yr.bkt
                                    rst=yr.rst
                                    mot=yr.mot
                                    sums_rmt=sums_rmt+rmt
                                    sums_cct=sums_cct+cct
                                    sums_srt=sums_srt+int(srt)
                                    sums_bkt=sums_bkt+bkt
                                    sums_rst=sums_rst+rst
                                    sums_mot=sums_mot+mot
                                    count=count+1
                            avgs_rmt=sums_rmt/count
                            avgs_cct=sums_cct/count
                            avgs_srt=sums_srt/count
                            avgs_bkt=sums_bkt/count
                            avgs_rst=sums_rst/count
                            avgs_mot=sums_mot/count
                        hr=ampv3_repo_yearly.objects.filter(year=dd[0],device_id=device_id)
                        if hr:
                            yr_data=ampv3_repo_yearly.objects.filter(year=dd[0],device_id=device_id).update(device_id=device_id,service='ampv3',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=ampv3_repo_yearly.objects.create(device_id=device_id,service='ampv3',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                except Exception as e:
                    # le=Errors.objects.all().last()
                    # print("le is:",le,type(le))
                    # if le.service == 'ampv3':
                    #     print("Error is alrady prasent")
                    # else:
                        erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='ampv3',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                        erro.save()
                    # error_message = e
                    # # global eg
                    # eg = e
                    
                    
                    # EchoConsumer.websocket_receive('event','event') 
                try:        
                    if 'ampv4'==components:
                        # com=cl
                        if device_id not in device_idlist:
                            repo_latestdata.objects.create(device_id=device_id,message_type=msg_type,ampv4=mydata1)
                        else:
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, ampv4=mydata1)

                            get_device_id=repo_latestdata.objects.all()
                            for did in get_device_id:
                                s=str(did.device_id)
                                if device_id == s:
                                    ampv4=did.ampv4
                            klist = list(ampv4.keys())
                            
                            mydatakey = list(mydata1.keys())
                            
                            for k,v in ampv4.items():
                                if k not in mydatakey:
                                    olddata.update({k:v})
                                    
                            mydata5=olddata.update(mydata1)    
                            
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, ampv4=olddata)

                        ds=treat_ampv4.objects.create(device_id=device_id,message_type=msg_type,pos=pos,rmt=rmt,cct=cct,srt=srt,bkt=bkt,rst=rst,mot=mot,stp=stp,op1=op1,op2=op2,op3=op3,ip1=ip1,ip2=ip2,ip3=ip3,psi=psi,year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                        ds.save()
                        if msg_type == 'updset':
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} ampv4 settings has been updated service time:{srt} backwash time:{bkt} rinse time:{rst} motor on delay time:{mot}sensor type:{stp} output1:{op1}output2:{op2}output3:{op3}input1:{ip1}input2:{ip2}input3:{ip3}pressure switch input:{psi}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='ampv4',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        else:
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} ampv4 status has been updated position:{pos}remaining time:{rmt}cycle count:{cct}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='ampv4',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        #hour
                        yrdata=treat_ampv4.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_rmt=0
                        sums_cct=0
                        sums_srt=0
                        sums_bkt=0
                        sums_rst=0
                        sums_mot=0
                        avgs_rmt = 0
                        avgs_cct = 0
                        avgs_srt = 0
                        avgs_bkt = 0
                        avgs_rst = 0
                        avgs_mot = 0
                        # avgs_bktsums_bkt = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    rmt=yr.rmt
                                    cct=yr.cct
                                    srt=yr.srt
                                    bkt=yr.bkt
                                    rst=yr.rst
                                    mot=yr.mot
                                    sums_rmt=sums_rmt+rmt
                                    sums_cct=sums_cct+cct
                                    sums_srt=sums_srt+int(srt)
                                    sums_bkt=sums_bkt+bkt
                                    sums_rst=sums_rst+rst
                                    sums_mot=sums_mot+mot
                                    count=count+1
                            avgs_rmt=sums_rmt/count
                            avgs_cct=sums_cct/count
                            avgs_srt=sums_srt/count
                            avgs_bkt=sums_bkt/count
                            avgs_rst=sums_rst/count
                            avgs_mot=sums_mot/count
                        hr=ampv4_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        if hr:
                            yr_data=ampv4_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id).update(device_id=device_id,service='ampv4',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=ampv4_repo_hourly.objects.create(device_id=device_id,service='ampv4',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #daily
                        yrdata=treat_ampv4.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_rmt=0
                        sums_cct=0
                        sums_srt=0
                        sums_bkt=0
                        sums_rst=0
                        sums_mot=0
                        avgs_rmt = 0
                        avgs_cct = 0
                        avgs_srt = 0
                        avgs_bkt = 0
                        avgs_rst = 0
                        avgs_mot = 0
                        # avgs_bktsums_bkt = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    rmt=yr.rmt
                                    cct=yr.cct
                                    srt=yr.srt
                                    bkt=yr.bkt
                                    rst=yr.rst
                                    mot=yr.mot
                                    sums_rmt=sums_rmt+rmt
                                    sums_cct=sums_cct+cct
                                    sums_srt=sums_srt+int(srt)
                                    sums_bkt=sums_bkt+bkt
                                    sums_rst=sums_rst+rst
                                    sums_mot=sums_mot+mot
                                    count=count+1
                            avgs_rmt=sums_rmt/count
                            avgs_cct=sums_cct/count
                            avgs_srt=sums_srt/count
                            avgs_bkt=sums_bkt/count
                            avgs_rst=sums_rst/count
                            avgs_mot=sums_mot/count
                        hr=ampv4_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        if hr:
                            yr_data=ampv4_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id).update(device_id=device_id,service='ampv4',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=ampv4_repo_daily.objects.create(device_id=device_id,service='ampv4',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #month
                        yrdata=treat_ampv4.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_rmt=0
                        sums_cct=0
                        sums_srt=0
                        sums_bkt=0
                        sums_rst=0
                        sums_mot=0
                        avgs_rmt = 0
                        avgs_cct = 0
                        avgs_srt = 0
                        avgs_bkt = 0
                        avgs_rst = 0
                        avgs_mot = 0
                        # avgs_bktsums_bkt = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    rmt=yr.rmt
                                    cct=yr.cct
                                    srt=yr.srt
                                    bkt=yr.bkt
                                    rst=yr.rst
                                    mot=yr.mot
                                    sums_rmt=sums_rmt+rmt
                                    sums_cct=sums_cct+cct
                                    sums_srt=sums_srt+int(srt)
                                    sums_bkt=sums_bkt+bkt
                                    sums_rst=sums_rst+rst
                                    sums_mot=sums_mot+mot
                                    count=count+1
                            avgs_rmt=sums_rmt/count
                            avgs_cct=sums_cct/count
                            avgs_srt=sums_srt/count
                            avgs_bkt=sums_bkt/count
                            avgs_rst=sums_rst/count
                            avgs_mot=sums_mot/count
                        hr=ampv4_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        if hr:
                            yr_data=ampv4_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id).update(device_id=device_id,service='ampv4',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=ampv4_repo_monthly.objects.create(device_id=device_id,service='ampv4',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #year
                        yrdata=treat_ampv4.objects.filter(year=dd[0],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_rmt=0
                        sums_cct=0
                        sums_srt=0
                        sums_bkt=0
                        sums_rst=0
                        sums_mot=0
                        avgs_rmt = 0
                        avgs_cct = 0
                        avgs_srt = 0
                        avgs_bkt = 0
                        avgs_rst = 0
                        avgs_mot = 0
                        # avgs_bktsums_bkt = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    rmt=yr.rmt
                                    cct=yr.cct
                                    srt=yr.srt
                                    bkt=yr.bkt
                                    rst=yr.rst
                                    mot=yr.mot
                                    sums_rmt=sums_rmt+rmt
                                    sums_cct=sums_cct+cct
                                    sums_srt=sums_srt+int(srt)
                                    sums_bkt=sums_bkt+bkt
                                    sums_rst=sums_rst+rst
                                    sums_mot=sums_mot+mot
                                    count=count+1
                            avgs_rmt=sums_rmt/count
                            avgs_cct=sums_cct/count
                            avgs_srt=sums_srt/count
                            avgs_bkt=sums_bkt/count
                            avgs_rst=sums_rst/count
                            avgs_mot=sums_mot/count
                        hr=ampv4_repo_yearly.objects.filter(year=dd[0],device_id=device_id)
                        if hr:
                            yr_data=ampv4_repo_yearly.objects.filter(year=dd[0],device_id=device_id).update(device_id=device_id,service='ampv4',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=ampv4_repo_yearly.objects.create(device_id=device_id,service='ampv4',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                except Exception as e:
                    erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='ampv4',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()
                    # error_message = e
                    # # global eg
                    # eg = e
                    
                    
                    # EchoConsumer.websocket_receive('event','event') 
                try:       
                    if 'ampv5'==components:
                        # com=cl
                        if device_id not in device_idlist:
                            repo_latestdata.objects.create(device_id=device_id,message_type=msg_type,ampv5=mydata1)
                        else:
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, ampv5=mydata1)

                            get_device_id=repo_latestdata.objects.all()
                            for did in get_device_id:
                                s=str(did.device_id)
                                if device_id == s:
                                    ampv5=did.ampv5
                            klist = list(ampv5.keys())
                            
                            mydatakey = list(mydata1.keys())
                            
                            for k,v in ampv5.items():
                                if k not in mydatakey:
                                    olddata.update({k:v})
                                    
                            mydata5=olddata.update(mydata1)    
                            
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, ampv5=olddata)

                        ds=treat_ampv5.objects.create(device_id=device_id,message_type=msg_type,pos=pos,rmt=rmt,cct=cct,srt=srt,bkt=bkt,rst=rst,mot=mot,stp=stp,op1=op1,op2=op2,op3=op3,ip1=ip1,ip2=ip2,ip3=ip3,psi=psi,year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                        ds.save()
                        if msg_type == 'updset':
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} ampv5 settings has been updated service time:{srt} backwash time:{bkt} rinse time:{rst} motor on delay time:{mot}sensor type:{stp} output1:{op1}output2:{op2}output3:{op3}input1:{ip1}input2:{ip2}input3:{ip3}pressure switch input:{psi}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='ampv5',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        else:
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} ampv5 status has been updated position:{pos}remaining time:{rmt}cycle count:{cct}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='ampv5',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()

                        #hour
                        yrdata=treat_ampv5.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_rmt=0
                        sums_cct=0
                        sums_srt=0
                        sums_bkt=0
                        sums_rst=0
                        sums_mot=0
                        avgs_rmt = 0
                        avgs_cct = 0
                        avgs_srt = 0
                        avgs_bkt = 0
                        avgs_rst = 0
                        avgs_mot = 0
                        # avgs_bktsums_bkt = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    rmt=yr.rmt
                                    cct=yr.cct
                                    srt=yr.srt
                                    bkt=yr.bkt
                                    rst=yr.rst
                                    mot=yr.mot
                                    sums_rmt=sums_rmt+rmt
                                    sums_cct=sums_cct+cct
                                    sums_srt=sums_srt+int(srt)
                                    sums_bkt=sums_bkt+bkt
                                    sums_rst=sums_rst+rst
                                    sums_mot=sums_mot+mot
                                    count=count+1
                            avgs_rmt=sums_rmt/count
                            avgs_cct=sums_cct/count
                            avgs_srt=sums_srt/count
                            avgs_bkt=sums_bkt/count
                            avgs_rst=sums_rst/count
                            avgs_mot=sums_mot/count
                        hr=ampv5_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        if hr:
                            yr_data=ampv5_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id).update(device_id=device_id,service='ampv5',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=ampv5_repo_hourly.objects.create(device_id=device_id,service='ampv5',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #daily
                        yrdata=treat_ampv5.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_rmt=0
                        sums_cct=0
                        sums_srt=0
                        sums_bkt=0
                        sums_rst=0
                        sums_mot=0
                        avgs_rmt = 0
                        avgs_cct = 0
                        avgs_srt = 0
                        avgs_bkt = 0
                        avgs_rst = 0
                        avgs_mot = 0
                        # avgs_bktsums_bkt = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    rmt=yr.rmt
                                    cct=yr.cct
                                    srt=yr.srt
                                    bkt=yr.bkt
                                    rst=yr.rst
                                    mot=yr.mot
                                    sums_rmt=sums_rmt+rmt
                                    sums_cct=sums_cct+cct
                                    sums_srt=sums_srt+int(srt)
                                    sums_bkt=sums_bkt+bkt
                                    sums_rst=sums_rst+rst
                                    sums_mot=sums_mot+mot
                                    count=count+1
                            avgs_rmt=sums_rmt/count
                            avgs_cct=sums_cct/count
                            avgs_srt=sums_srt/count
                            avgs_bkt=sums_bkt/count
                            avgs_rst=sums_rst/count
                            avgs_mot=sums_mot/count
                        hr=ampv5_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        if hr:
                            yr_data=ampv5_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id).update(device_id=device_id,service='ampv5',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=ampv5_repo_daily.objects.create(device_id=device_id,service='ampv5',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #month
                        yrdata=treat_ampv5.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_rmt=0
                        sums_cct=0
                        sums_srt=0
                        sums_bkt=0
                        sums_rst=0
                        sums_mot=0
                        avgs_rmt = 0
                        avgs_cct = 0
                        avgs_srt = 0
                        avgs_bkt = 0
                        avgs_rst = 0
                        avgs_mot = 0
                        # avgs_bktsums_bkt = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    rmt=yr.rmt
                                    cct=yr.cct
                                    srt=yr.srt
                                    bkt=yr.bkt
                                    rst=yr.rst
                                    mot=yr.mot
                                    sums_rmt=sums_rmt+rmt
                                    sums_cct=sums_cct+cct
                                    sums_srt=sums_srt+int(srt)
                                    sums_bkt=sums_bkt+bkt
                                    sums_rst=sums_rst+rst
                                    sums_mot=sums_mot+mot
                                    count=count+1
                            avgs_rmt=sums_rmt/count
                            avgs_cct=sums_cct/count
                            avgs_srt=sums_srt/count
                            avgs_bkt=sums_bkt/count
                            avgs_rst=sums_rst/count
                            avgs_mot=sums_mot/count
                        hr=ampv5_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        if hr:
                            yr_data=ampv5_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id).update(device_id=device_id,service='ampv5',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=ampv5_repo_monthly.objects.create(device_id=device_id,service='ampv5',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #year
                        yrdata=treat_ampv5.objects.filter(year=dd[0],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_rmt=0
                        sums_cct=0
                        sums_srt=0
                        sums_bkt=0
                        sums_rst=0
                        sums_mot=0
                        avgs_rmt = 0
                        avgs_cct = 0
                        avgs_srt = 0
                        avgs_bkt = 0
                        avgs_rst = 0
                        avgs_mot = 0
                        # avgs_bktsums_bkt = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    rmt=yr.rmt
                                    cct=yr.cct
                                    srt=yr.srt
                                    bkt=yr.bkt
                                    rst=yr.rst
                                    mot=yr.mot
                                    sums_rmt=sums_rmt+rmt
                                    sums_cct=sums_cct+cct
                                    sums_srt=sums_srt+int(srt)
                                    sums_bkt=sums_bkt+bkt
                                    sums_rst=sums_rst+rst
                                    sums_mot=sums_mot+mot
                                    count=count+1
                            avgs_rmt=sums_rmt/count
                            avgs_cct=sums_cct/count
                            avgs_srt=sums_srt/count
                            avgs_bkt=sums_bkt/count
                            avgs_rst=sums_rst/count
                            avgs_mot=sums_mot/count
                        hr=ampv5_repo_yearly.objects.filter(year=dd[0],device_id=device_id)
                        if hr:
                            yr_data=ampv5_repo_yearly.objects.filter(year=dd[0],device_id=device_id).update(device_id=device_id,service='ampv5',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=ampv5_repo_yearly.objects.create(device_id=device_id,service='ampv5',rmt={'sum':sums_rmt,'avg':avgs_rmt,'count':count},cct={'sum':sums_cct,'avg':avgs_cct,'count':count},srt={'sum':sums_srt,'avg':avgs_srt,'count':count},bkt={'sum':sums_bkt,'avg':avgs_bkt,'count':count},rst={'sum':sums_rst,'avg':avgs_rst,'count':count},mot={'sum':sums_mot,'avg':avgs_mot,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                except Exception as e:
                    erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='ampv5',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()
                    # error_message = e
                    # # global eg
                    # eg = e
                    
                    
                    # EchoConsumer.websocket_receive('event','event') 
                try:
                    if 'atm'==components:
                        # com=cl
                        if device_id not in device_idlist:
                            repo_latestdata.objects.create(device_id=device_id,message_type=msg_type,atm=mydata1)
                        else:
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, atm=mydata1)

                            get_device_id=repo_latestdata.objects.all()
                            for did in get_device_id:
                                s=str(did.device_id)
                                if device_id == s:
                                    atm=did.atm
                            klist = list(atm.keys())
                            
                            mydatakey = list(mydata1.keys())
                            
                            for k,v in atm.items():
                                if k not in mydatakey:
                                    olddata.update({k:v})
                                    
                            mydata5=olddata.update(mydata1)    
                            
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, atm=olddata)

                        ds=disp_atm.objects.create(device_id=device_id,message_type=msg_type,sts=sts,ndv=ndv,ntt=ntt,nta=nta,tmp=tmp,whr=whr,custid=custid,ntp=ntp,nov=nov,vl1=vl1,vl2=vl2,vl3=vl3,vl4=vl4,re1=re1,re2=re2,re3=re3,re4=re4,year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                        ds.save()
                        if msg_type == 'updset':
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} atm settings has been updated no. Of  tap:{ntp} no. Of volume:{nov} volume1:{vl1} volume2:{vl2} volume3:{vl3} volume4:{vl4} rate1:{re1} rate2:{re2} rate3:{re3} rate4:{re4}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='atm',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        else:
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} atm status has been updated status:{sts} new dispense volume:{ndv} new transaction type:{ntt} new transaction amount:{nta} water tempreture:{tmp} working hrs:{whr} card number:{custid}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='atm',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        #hourly
                        yrdata=disp_atm.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_ndv=0
                        sums_nta=0
                        sums_tmp=0
                        sums_whr=0
                        sums_whr=0
                        sums_ntp=0
                        sums_nov=0
                        sums_vl1=0
                        sums_vl2=0
                        sums_vl3=0
                        sums_vl4=0
                        sums_re1=0
                        sums_re2=0
                        sums_re3=0
                        sums_re4=0
                        avgs_ndv = 0
                        avgs_nta = 0
                        avgs_tmp = 0
                        avgs_whr=0
                        avgs_ntp = 0
                        avgs_nov = 0
                        avgs_vl1 = 0
                        avgs_vl2 = 0
                        avgs_vl3 = 0
                        avgs_vl4 = 0
                        avgs_re1 = 0
                        avgs_re2 = 0
                        avgs_re3 = 0
                        avgs_re4 = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    ndv=yr.ndv
                                    nta=yr.nta
                                    tmp=yr.tmp
                                    whr=float(yr.whr)
                                    custid=yr.custid
                                    ntp=yr.ntp
                                    nov=yr.nov
                                    vl1=yr.vl1
                                    vl2=yr.vl2
                                    vl3=yr.vl3
                                    vl4=yr.vl4
                                    re1=yr.re1
                                    re2=yr.re2
                                    re3=yr.re3
                                    re4=yr.re4
                                    sums_ndv=sums_ndv+ndv
                                    sums_nta=sums_nta+nta
                                    sums_tmp=sums_tmp+tmp
                                    sums_whr=sums_whr+whr
                                    sums_ntp=sums_ntp+ntp
                                    sums_nov=sums_nov+nov
                                    sums_vl1=sums_vl1+vl1
                                    sums_vl2=sums_vl2+vl2
                                    sums_vl3=sums_vl3+vl3
                                    sums_vl4=sums_vl4+vl4
                                    sums_re1=sums_re1+re1
                                    sums_re2=sums_re2+re2
                                    sums_re3=sums_re3+re3
                                    sums_re4=sums_re4+re4
                                    count=count+1
                            avgs_ndv=sums_ndv/count
                            avgs_nta=sums_nta/count
                            avgs_tmp=sums_tmp/count
                            avgs_whr=sums_whr/count
                            avgs_ntp=sums_ntp/count
                            avgs_nov=sums_nov/count
                            avgs_vl1=sums_vl1/count
                            avgs_vl2=sums_vl2/count
                            avgs_vl3=sums_vl3/count
                            avgs_vl4=sums_vl4/count
                            avgs_re1=sums_re1/count
                            avgs_re2=sums_re2/count
                            avgs_re3=sums_re3/count
                            avgs_re4=sums_re4/count
                        hr=atm_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        if hr:
                            yr_data=atm_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id).update(device_id=device_id,service='atm',ndv={'sum':sums_ndv,'avg':avgs_ndv,'count':count},nta={'sum':sums_nta,'avg':avgs_nta,'count':count},tmp={'sum':sums_tmp,'avg':avgs_tmp,'count':count},whr={'sum':sums_whr,'avg':avgs_whr,'count':count},ntp={'sum':sums_ntp,'avg':avgs_ntp,'count':count},nov={'sum':sums_nov,'avg':avgs_nov,'count':count},vl1={'sum':sums_vl1,'avg':avgs_vl1,'count':count},vl2={'sum':sums_vl2,'avg':avgs_vl2,'count':count},vl3={'sum':sums_vl3,'avg':avgs_vl3,'count':count},vl4={'sum':sums_vl4,'avg':avgs_vl4,'count':count},re1={'sum':sums_re1,'avg':avgs_re1,'count':count},re2={'sum':sums_re2,'avg':avgs_re2,'count':count},re3={'sum':sums_re3,'avg':avgs_re3,'count':count},re4={'sum':sums_re4,'avg':avgs_re4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=atm_repo_hourly.objects.create(device_id=device_id,service='atm',ndv={'sum':sums_ndv,'avg':avgs_ndv,'count':count},nta={'sum':sums_nta,'avg':avgs_nta,'count':count},tmp={'sum':sums_tmp,'avg':avgs_tmp,'count':count},whr={'sum':sums_whr,'avg':avgs_whr,'count':count},ntp={'sum':sums_ntp,'avg':avgs_ntp,'count':count},nov={'sum':sums_nov,'avg':avgs_nov,'count':count},vl1={'sum':sums_vl1,'avg':avgs_vl1,'count':count},vl2={'sum':sums_vl2,'avg':avgs_vl2,'count':count},vl3={'sum':sums_vl3,'avg':avgs_vl3,'count':count},vl4={'sum':sums_vl4,'avg':avgs_vl4,'count':count},re1={'sum':sums_re1,'avg':avgs_re1,'count':count},re2={'sum':sums_re2,'avg':avgs_re2,'count':count},re3={'sum':sums_re3,'avg':avgs_re3,'count':count},re4={'sum':sums_re4,'avg':avgs_re4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()

                        #day
                        yrdata=disp_atm.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_ndv=0
                        sums_nta=0
                        sums_tmp=0
                        sums_whr=0
                        sums_ntp=0
                        sums_nov=0
                        sums_vl1=0
                        sums_vl2=0
                        sums_vl3=0
                        sums_vl4=0
                        sums_re1=0
                        sums_re2=0
                        sums_re3=0
                        sums_re4=0
                        avgs_ndv = 0
                        avgs_nta = 0
                        avgs_tmp = 0
                        avgs_whr=0
                        avgs_ntp = 0
                        avgs_nov = 0
                        avgs_vl1 = 0
                        avgs_vl2 = 0
                        avgs_vl3 = 0
                        avgs_vl4 = 0
                        avgs_re1 = 0
                        avgs_re2 = 0
                        avgs_re3 = 0
                        avgs_re4 = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    ndv=yr.ndv
                                    nta=yr.nta
                                    tmp=yr.tmp
                                    whr=float(yr.whr)
                                    ntp=yr.ntp
                                    nov=yr.nov
                                    vl1=yr.vl1
                                    vl2=yr.vl2
                                    vl3=yr.vl3
                                    vl4=yr.vl4
                                    re1=yr.re1
                                    re2=yr.re2
                                    re3=yr.re3
                                    re4=yr.re4
                                    sums_ndv=sums_ndv+ndv
                                    sums_nta=sums_nta+nta
                                    sums_tmp=sums_tmp+tmp
                                    sums_whr=sums_whr+whr
                                    sums_ntp=sums_ntp+ntp
                                    sums_nov=sums_nov+nov
                                    sums_vl1=sums_vl1+vl1
                                    sums_vl2=sums_vl2+vl2
                                    sums_vl3=sums_vl3+vl3
                                    sums_vl4=sums_vl4+vl4
                                    sums_re1=sums_re1+re1
                                    sums_re2=sums_re2+re2
                                    sums_re3=sums_re3+re3
                                    sums_re4=sums_re4+re4
                                    count=count+1
                            avgs_ndv=sums_ndv/count
                            avgs_nta=sums_nta/count
                            avgs_tmp=sums_tmp/count
                            avgs_whr=sums_whr/count
                            avgs_ntp=sums_ntp/count
                            avgs_nov=sums_nov/count
                            avgs_vl1=sums_vl1/count
                            avgs_vl2=sums_vl2/count
                            avgs_vl3=sums_vl3/count
                            avgs_vl4=sums_vl4/count
                            avgs_re1=sums_re1/count
                            avgs_re2=sums_re2/count
                            avgs_re3=sums_re3/count
                            avgs_re4=sums_re4/count
                        hr=atm_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        if hr:
                            yr_data=atm_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id).update(device_id=device_id,service='atm',ndv={'sum':sums_ndv,'avg':avgs_ndv,'count':count},nta={'sum':sums_nta,'avg':avgs_nta,'count':count},tmp={'sum':sums_tmp,'avg':avgs_tmp,'count':count},whr={'sum':sums_whr,'avg':avgs_whr,'count':count},ntp={'sum':sums_ntp,'avg':avgs_ntp,'count':count},nov={'sum':sums_nov,'avg':avgs_nov,'count':count},vl1={'sum':sums_vl1,'avg':avgs_vl1,'count':count},vl2={'sum':sums_vl2,'avg':avgs_vl2,'count':count},vl3={'sum':sums_vl3,'avg':avgs_vl3,'count':count},vl4={'sum':sums_vl4,'avg':avgs_vl4,'count':count},re1={'sum':sums_re1,'avg':avgs_re1,'count':count},re2={'sum':sums_re2,'avg':avgs_re2,'count':count},re3={'sum':sums_re3,'avg':avgs_re3,'count':count},re4={'sum':sums_re4,'avg':avgs_re4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=atm_repo_daily.objects.create(device_id=device_id,service='atm',ndv={'sum':sums_ndv,'avg':avgs_ndv,'count':count},nta={'sum':sums_nta,'avg':avgs_nta,'count':count},tmp={'sum':sums_tmp,'avg':avgs_tmp,'count':count},whr={'sum':sums_whr,'avg':avgs_whr,'count':count},ntp={'sum':sums_ntp,'avg':avgs_ntp,'count':count},nov={'sum':sums_nov,'avg':avgs_nov,'count':count},vl1={'sum':sums_vl1,'avg':avgs_vl1,'count':count},vl2={'sum':sums_vl2,'avg':avgs_vl2,'count':count},vl3={'sum':sums_vl3,'avg':avgs_vl3,'count':count},vl4={'sum':sums_vl4,'avg':avgs_vl4,'count':count},re1={'sum':sums_re1,'avg':avgs_re1,'count':count},re2={'sum':sums_re2,'avg':avgs_re2,'count':count},re3={'sum':sums_re3,'avg':avgs_re3,'count':count},re4={'sum':sums_re4,'avg':avgs_re4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()

                        #monthly
                        yrdata=disp_atm.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_ndv=0
                        sums_nta=0
                        sums_tmp=0
                        sums_whr=0
                        sums_ntp=0
                        sums_nov=0
                        sums_vl1=0
                        sums_vl2=0
                        sums_vl3=0
                        sums_vl4=0
                        sums_re1=0
                        sums_re2=0
                        sums_re3=0
                        sums_re4=0
                        avgs_ndv = 0
                        avgs_nta = 0
                        avgs_tmp = 0
                        avgs_whr=0
                        avgs_ntp = 0
                        avgs_nov = 0
                        avgs_vl1 = 0
                        avgs_vl2 = 0
                        avgs_vl3 = 0
                        avgs_vl4 = 0
                        avgs_re1 = 0
                        avgs_re2 = 0
                        avgs_re3 = 0
                        avgs_re4 = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    ndv=yr.ndv
                                    nta=yr.nta
                                    tmp=yr.tmp
                                    whr=float(yr.whr)
                                    ntp=yr.ntp
                                    nov=yr.nov
                                    vl1=yr.vl1
                                    vl2=yr.vl2
                                    vl3=yr.vl3
                                    vl4=yr.vl4
                                    re1=yr.re1
                                    re2=yr.re2
                                    re3=yr.re3
                                    re4=yr.re4
                                    sums_ndv=sums_ndv+ndv
                                    sums_nta=sums_nta+nta
                                    sums_tmp=sums_tmp+tmp
                                    sums_whr=sums_whr+whr
                                    sums_ntp=sums_ntp+ntp
                                    sums_nov=sums_nov+nov
                                    sums_vl1=sums_vl1+vl1
                                    sums_vl2=sums_vl2+vl2
                                    sums_vl3=sums_vl3+vl3
                                    sums_vl4=sums_vl4+vl4
                                    sums_re1=sums_re1+re1
                                    sums_re2=sums_re2+re2
                                    sums_re3=sums_re3+re3
                                    sums_re4=sums_re4+re4
                                    count=count+1
                            avgs_ndv=sums_ndv/count
                            avgs_nta=sums_nta/count
                            avgs_tmp=sums_tmp/count
                            avgs_whr=sums_whr/count
                            avgs_ntp=sums_ntp/count
                            avgs_nov=sums_nov/count
                            avgs_vl1=sums_vl1/count
                            avgs_vl2=sums_vl2/count
                            avgs_vl3=sums_vl3/count
                            avgs_vl4=sums_vl4/count
                            avgs_re1=sums_re1/count
                            avgs_re2=sums_re2/count
                            avgs_re3=sums_re3/count
                            avgs_re4=sums_re4/count
                        hr=atm_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        if hr:
                            yr_data=atm_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id).update(device_id=device_id,service='atm',ndv={'sum':sums_ndv,'avg':avgs_ndv,'count':count},nta={'sum':sums_nta,'avg':avgs_nta,'count':count},tmp={'sum':sums_tmp,'avg':avgs_tmp,'count':count},whr={'sum':sums_whr,'avg':avgs_whr,'count':count},ntp={'sum':sums_ntp,'avg':avgs_ntp,'count':count},nov={'sum':sums_nov,'avg':avgs_nov,'count':count},vl1={'sum':sums_vl1,'avg':avgs_vl1,'count':count},vl2={'sum':sums_vl2,'avg':avgs_vl2,'count':count},vl3={'sum':sums_vl3,'avg':avgs_vl3,'count':count},vl4={'sum':sums_vl4,'avg':avgs_vl4,'count':count},re1={'sum':sums_re1,'avg':avgs_re1,'count':count},re2={'sum':sums_re2,'avg':avgs_re2,'count':count},re3={'sum':sums_re3,'avg':avgs_re3,'count':count},re4={'sum':sums_re4,'avg':avgs_re4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=atm_repo_monthly.objects.create(device_id=device_id,service='atm',ndv={'sum':sums_ndv,'avg':avgs_ndv,'count':count},nta={'sum':sums_nta,'avg':avgs_nta,'count':count},tmp={'sum':sums_tmp,'avg':avgs_tmp,'count':count},whr={'sum':sums_whr,'avg':avgs_whr,'count':count},ntp={'sum':sums_ntp,'avg':avgs_ntp,'count':count},nov={'sum':sums_nov,'avg':avgs_nov,'count':count},vl1={'sum':sums_vl1,'avg':avgs_vl1,'count':count},vl2={'sum':sums_vl2,'avg':avgs_vl2,'count':count},vl3={'sum':sums_vl3,'avg':avgs_vl3,'count':count},vl4={'sum':sums_vl4,'avg':avgs_vl4,'count':count},re1={'sum':sums_re1,'avg':avgs_re1,'count':count},re2={'sum':sums_re2,'avg':avgs_re2,'count':count},re3={'sum':sums_re3,'avg':avgs_re3,'count':count},re4={'sum':sums_re4,'avg':avgs_re4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()

                        #yearly
                        yrdata=disp_atm.objects.filter(year=dd[0],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_ndv=0
                        sums_nta=0
                        sums_tmp=0
                        sums_whr=0
                        sums_ntp=0
                        sums_nov=0
                        sums_vl1=0
                        sums_vl2=0
                        sums_vl3=0
                        sums_vl4=0
                        sums_re1=0
                        sums_re2=0
                        sums_re3=0
                        sums_re4=0
                        avgs_ndv = 0
                        avgs_nta = 0
                        avgs_tmp = 0
                        avgs_whr=0
                        avgs_ntp = 0
                        avgs_nov = 0
                        avgs_vl1 = 0
                        avgs_vl2 = 0
                        avgs_vl3 = 0
                        avgs_vl4 = 0
                        avgs_re1 = 0
                        avgs_re2 = 0
                        avgs_re3 = 0
                        avgs_re4 = 0
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    ndv=yr.ndv
                                    nta=yr.nta
                                    tmp=yr.tmp
                                    whr=float(yr.whr)
                                    ntp=yr.ntp
                                    nov=yr.nov
                                    vl1=yr.vl1
                                    vl2=yr.vl2
                                    vl3=yr.vl3
                                    vl4=yr.vl4
                                    re1=yr.re1
                                    re2=yr.re2
                                    re3=yr.re3
                                    re4=yr.re4
                                    sums_ndv=sums_ndv+ndv
                                    sums_nta=sums_nta+nta
                                    sums_tmp=sums_tmp+tmp
                                    sums_whr=sums_whr+whr
                                    sums_ntp=sums_ntp+ntp
                                    sums_nov=sums_nov+nov
                                    sums_vl1=sums_vl1+vl1
                                    sums_vl2=sums_vl2+vl2
                                    sums_vl3=sums_vl3+vl3
                                    sums_vl4=sums_vl4+vl4
                                    sums_re1=sums_re1+re1
                                    sums_re2=sums_re2+re2
                                    sums_re3=sums_re3+re3
                                    sums_re4=sums_re4+re4
                                    count=count+1
                            avgs_ndv=sums_ndv/count
                            avgs_nta=sums_nta/count
                            avgs_tmp=sums_tmp/count
                            avgs_whr=sums_whr/count
                            avgs_ntp=sums_ntp/count
                            avgs_nov=sums_nov/count
                            avgs_vl1=sums_vl1/count
                            avgs_vl2=sums_vl2/count
                            avgs_vl3=sums_vl3/count
                            avgs_vl4=sums_vl4/count
                            avgs_re1=sums_re1/count
                            avgs_re2=sums_re2/count
                            avgs_re3=sums_re3/count
                            avgs_re4=sums_re4/count
                        hr=atm_repo_yearly.objects.filter(year=dd[0],device_id=device_id)
                        if hr:
                            yr_data=atm_repo_yearly.objects.filter(year=dd[0],device_id=device_id).update(device_id=device_id,service='atm',ndv={'sum':sums_ndv,'avg':avgs_ndv,'count':count},nta={'sum':sums_nta,'avg':avgs_nta,'count':count},tmp={'sum':sums_tmp,'avg':avgs_tmp,'count':count},whr={'sum':sums_whr,'avg':avgs_whr,'count':count},ntp={'sum':sums_ntp,'avg':avgs_ntp,'count':count},nov={'sum':sums_nov,'avg':avgs_nov,'count':count},vl1={'sum':sums_vl1,'avg':avgs_vl1,'count':count},vl2={'sum':sums_vl2,'avg':avgs_vl2,'count':count},vl3={'sum':sums_vl3,'avg':avgs_vl3,'count':count},vl4={'sum':sums_vl4,'avg':avgs_vl4,'count':count},re1={'sum':sums_re1,'avg':avgs_re1,'count':count},re2={'sum':sums_re2,'avg':avgs_re2,'count':count},re3={'sum':sums_re3,'avg':avgs_re3,'count':count},re4={'sum':sums_re4,'avg':avgs_re4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=atm_repo_yearly.objects.create(device_id=device_id,service='atm',ndv={'sum':sums_ndv,'avg':avgs_ndv,'count':count},nta={'sum':sums_nta,'avg':avgs_nta,'count':count},tmp={'sum':sums_tmp,'avg':avgs_tmp,'count':count},whr={'sum':sums_whr,'avg':avgs_whr,'count':count},ntp={'sum':sums_ntp,'avg':avgs_ntp,'count':count},nov={'sum':sums_nov,'avg':avgs_nov,'count':count},vl1={'sum':sums_vl1,'avg':avgs_vl1,'count':count},vl2={'sum':sums_vl2,'avg':avgs_vl2,'count':count},vl3={'sum':sums_vl3,'avg':avgs_vl3,'count':count},vl4={'sum':sums_vl4,'avg':avgs_vl4,'count':count},re1={'sum':sums_re1,'avg':avgs_re1,'count':count},re2={'sum':sums_re2,'avg':avgs_re2,'count':count},re3={'sum':sums_re3,'avg':avgs_re3,'count':count},re4={'sum':sums_re4,'avg':avgs_re4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()

                except Exception as e:
                    erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='atm',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()
                    # error_message = e
                    # # global eg
                    # eg = e
                try:
                    if 'cnd_consen'==components:
                        # com=cl
                        if device_id not in device_idlist:
                            repo_latestdata.objects.create(device_id=device_id,message_type=msg_type,cnd_consen=mydata1)
                        else:
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, cnd_consen=mydata1)

                            get_device_id=repo_latestdata.objects.all()
                            for did in get_device_id:
                                s=str(did.device_id)
                                if device_id == s:
                                    cnd_consen=did.cnd_consen
                            klist = list(cnd_consen.keys())
                            
                            mydatakey = list(mydata1.keys())
                            
                            for k,v in cnd_consen.items():
                                if k not in mydatakey:
                                    olddata.update({k:v})
                                    
                            mydata5=olddata.update(mydata1)    
                            
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, cnd_consen=olddata)

                        ds=disp_cnd_consen.objects.create(device_id=device_id,message_type=msg_type,cnd=cnd,spn=spn,asp=asp,year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                        ds.save() 
                        if msg_type == 'updset':
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} cnd_consen settings has been updated no. Of  span:{spn}atert_setpoint:{asp}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='cnd_consen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        else:
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} cnd_consen status has been updated conductivity:{cnd}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='cnd_consen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        #hourly
                        yrdata=disp_cnd_consen.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_cnd=0
                        sums_spn=0
                        sums_asp=0
                        avgs_cnd = 0
                        avgs_spn = 0
                        avgs_asp = 0
                        
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    cnd=yr.cnd
                                    spn=yr.spn
                                    asp=yr.asp
                                    
                                    sums_cnd=sums_cnd+cnd
                                    sums_spn=sums_spn+spn
                                    sums_asp=sums_asp+asp
                                    
                                    count=count+1
                            avgs_cnd=sums_cnd/count
                            avgs_spn=sums_spn/count
                            avgs_asp=sums_asp/count
                    
                        hr=cnd_consen_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        if hr:
                            yr_data=cnd_consen_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id).update(device_id=device_id,service='cnd_consen',cnd={'sum':sums_cnd,'avg':avgs_cnd,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=cnd_consen_repo_hourly.objects.create(device_id=device_id,service='cnd_consen',cnd={'sum':sums_cnd,'avg':avgs_cnd,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #daily
                        yrdata=disp_cnd_consen.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_cnd=0
                        sums_spn=0
                        sums_asp=0
                        avgs_cnd = 0
                        avgs_spn = 0
                        avgs_asp = 0
                        
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    cnd=yr.cnd
                                    spn=yr.spn
                                    asp=yr.asp
                                    
                                    sums_cnd=sums_cnd+cnd
                                    sums_spn=sums_spn+spn
                                    sums_asp=sums_asp+asp
                                    
                                    count=count+1
                            avgs_cnd=sums_cnd/count
                            avgs_spn=sums_spn/count
                            avgs_asp=sums_asp/count
                    
                        hr=cnd_consen_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        if hr:
                            yr_data=cnd_consen_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id).update(device_id=device_id,service='cnd_consen',cnd={'sum':sums_cnd,'avg':avgs_cnd,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=cnd_consen_repo_daily.objects.create(device_id=device_id,service='cnd_consen',cnd={'sum':sums_cnd,'avg':avgs_cnd,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #monthly
                        yrdata=disp_cnd_consen.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_cnd=0
                        sums_spn=0
                        sums_asp=0
                        avgs_cnd = 0
                        avgs_spn = 0
                        avgs_asp = 0
                        
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    cnd=yr.cnd
                                    spn=yr.spn
                                    asp=yr.asp
                                    
                                    sums_cnd=sums_cnd+cnd
                                    sums_spn=sums_spn+spn
                                    sums_asp=sums_asp+asp
                                    
                                    count=count+1
                            avgs_cnd=sums_cnd/count
                            avgs_spn=sums_spn/count
                            avgs_asp=sums_asp/count
                    
                        hr=cnd_consen_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        if hr:
                            yr_data=cnd_consen_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id).update(device_id=device_id,service='cnd_consen',cnd={'sum':sums_cnd,'avg':avgs_cnd,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=cnd_consen_repo_monthly.objects.create(device_id=device_id,service='cnd_consen',cnd={'sum':sums_cnd,'avg':avgs_cnd,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #yearly
                        yrdata=disp_cnd_consen.objects.filter(year=dd[0],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_cnd=0
                        sums_spn=0
                        sums_asp=0
                        avgs_cnd = 0
                        avgs_spn = 0
                        avgs_asp = 0
                        
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    cnd=yr.cnd
                                    spn=yr.spn
                                    asp=yr.asp
                                    
                                    sums_cnd=sums_cnd+cnd
                                    sums_spn=sums_spn+spn
                                    sums_asp=sums_asp+asp
                                    
                                    count=count+1
                            avgs_cnd=sums_cnd/count
                            avgs_spn=sums_spn/count
                            avgs_asp=sums_asp/count
                    
                        hr=cnd_consen_repo_yearly.objects.filter(year=dd[0],device_id=device_id)
                        if hr:
                            yr_data=cnd_consen_repo_yearly.objects.filter(year=dd[0],device_id=device_id).update(device_id=device_id,service='cnd_consen',cnd={'sum':sums_cnd,'avg':avgs_cnd,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=cnd_consen_repo_yearly.objects.create(device_id=device_id,service='cnd_consen',cnd={'sum':sums_cnd,'avg':avgs_cnd,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        
                except Exception as e:
                    erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='cnd_consen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()
                    # error_message = e
                    # # global eg
                    # eg = e
                    
                    
                    # EchoConsumer.websocket_receive('event','event')
                try:
                    if 'tds_consen'==components:
                        # com=cl
                        if device_id not in device_idlist:
                            repo_latestdata.objects.create(device_id=device_id,message_type=msg_type,tds_consen=mydata1)
                        else:
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, tds_consen=mydata1)

                            get_device_id=repo_latestdata.objects.all()
                            for did in get_device_id:
                                s=str(did.device_id)
                                if device_id == s:
                                    tds_consen=did.tds_consen
                            klist = list(tds_consen.keys())
                            
                            mydatakey = list(mydata1.keys())
                            
                            for k,v in tds_consen.items():
                                if k not in mydatakey:
                                    olddata.update({k:v})
                                    
                            mydata5=olddata.update(mydata1)    
                            
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, tds_consen=olddata)

                        ds=disp_tds_consen.objects.create(device_id=device_id,message_type=msg_type,tds=tds,spn=spn,asp=asp,year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                        ds.save() 
                        if msg_type == 'updset':
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tds_consen settings has been updated no. Of  span:{spn}atert_setpoint:{asp}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='tds_consen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        else:
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tds_consen status has been updated conductivity:{cnd}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='tds_consen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        #hourly
                        yrdata=disp_tds_consen.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_tds=0
                        sums_spn=0
                        sums_asp=0
                        avgs_tds = 0
                        avgs_spn = 0
                        avgs_asp = 0
                        
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    tds=yr.tds
                                    spn=yr.spn
                                    asp=yr.asp
                                    
                                    sums_tds=sums_tds+tds
                                    sums_spn=sums_spn+spn
                                    sums_asp=sums_asp+asp
                                    
                                    count=count+1
                            avgs_tds=sums_tds/count
                            avgs_spn=sums_spn/count
                            avgs_asp=sums_asp/count
                    
                        hr=tds_consen_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        if hr:
                            yr_data=tds_consen_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id).update(device_id=device_id,service='tds_consen',tds={'sum':sums_tds,'avg':avgs_tds,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=tds_consen_repo_hourly.objects.create(device_id=device_id,service='tds_consen',tds={'sum':sums_tds,'avg':avgs_tds,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #daily
                        yrdata=disp_tds_consen.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_tds=0
                        sums_spn=0
                        sums_asp=0
                        avgs_tds = 0
                        avgs_spn = 0
                        avgs_asp = 0
                        
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    tds=yr.tds
                                    spn=yr.spn
                                    asp=yr.asp
                                    
                                    sums_tds=sums_tds+tds
                                    sums_spn=sums_spn+spn
                                    sums_asp=sums_asp+asp
                                    
                                    count=count+1
                            avgs_tds=sums_tds/count
                            avgs_spn=sums_spn/count
                            avgs_asp=sums_asp/count
                    
                        hr=tds_consen_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        if hr:
                            yr_data=tds_consen_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id).update(device_id=device_id,service='tds_consen',tds={'sum':sums_tds,'avg':avgs_tds,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=tds_consen_repo_daily.objects.create(device_id=device_id,service='tds_consen',tds={'sum':sums_tds,'avg':avgs_tds,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #monthly
                        yrdata=disp_tds_consen.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_tds=0
                        sums_spn=0
                        sums_asp=0
                        avgs_tds = 0
                        avgs_spn = 0
                        avgs_asp = 0
                        
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    tds=yr.tds
                                    spn=yr.spn
                                    asp=yr.asp
                                    
                                    sums_tds=sums_tds+tds
                                    sums_spn=sums_spn+spn
                                    sums_asp=sums_asp+asp
                                    
                                    count=count+1
                            avgs_tds=sums_tds/count
                            avgs_spn=sums_spn/count
                            avgs_asp=sums_asp/count
                    
                        hr=tds_consen_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        if hr:
                            yr_data=tds_consen_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id).update(device_id=device_id,service='tds_consen',tds={'sum':sums_tds,'avg':avgs_tds,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=tds_consen_repo_monthly.objects.create(device_id=device_id,service='tds_consen',tds={'sum':sums_tds,'avg':avgs_tds,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #yearly
                        yrdata=disp_tds_consen.objects.filter(year=dd[0],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_tds=0
                        sums_spn=0
                        sums_asp=0
                        avgs_tds = 0
                        avgs_spn = 0
                        avgs_asp = 0
                        
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    tds=yr.tds
                                    spn=yr.spn
                                    asp=yr.asp
                                    
                                    sums_tds=sums_tds+tds
                                    sums_spn=sums_spn+spn
                                    sums_asp=sums_asp+asp
                                    
                                    count=count+1
                            avgs_tds=sums_tds/count
                            avgs_spn=sums_spn/count
                            avgs_asp=sums_asp/count
                    
                        hr=tds_consen_repo_yearly.objects.filter(year=dd[0],device_id=device_id)
                        if hr:
                            yr_data=tds_consen_repo_yearly.objects.filter(year=dd[0],device_id=device_id).update(device_id=device_id,service='tds_consen',tds={'sum':sums_tds,'avg':avgs_tds,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=tds_consen_repo_yearly.objects.create(device_id=device_id,service='tds_consen',tds={'sum':sums_tds,'avg':avgs_tds,'count':count},spn={'sum':sums_spn,'avg':avgs_spn,'count':count},asp={'sum':sums_asp,'avg':avgs_asp,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        
                except Exception as e:
                    erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='tds_consen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()
                    # error_message = e
                    # # global eg
                    # eg = e
                    
                    
                    # EchoConsumer.websocket_receive('event','event')
                try:
                    if 'F_flowsen'==components:
                        # com=cl
                        if device_id not in device_idlist:
                            repo_latestdata.objects.create(device_id=device_id,message_type=msg_type,F_flowsen=mydata1)
                        else:
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, F_flowsen=mydata1)

                            get_device_id=repo_latestdata.objects.all()
                            for did in get_device_id:
                                s=str(did.device_id)
                                if device_id == s:
                                    F_flowsen=did.F_flowsen
                            klist = list(F_flowsen.keys())
                            
                            mydatakey = list(mydata1.keys())
                            
                            for k,v in F_flowsen.items():
                                if k not in mydatakey:
                                    olddata.update({k:v})
                                    
                            mydata5=olddata.update(mydata1)    
                            
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, F_flowsen=olddata)

                        ds=treat_F_flowsen.objects.create(device_id=device_id,message_type=msg_type,fr1=fr1,ff1=ff1,year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                        ds.save() 
                        if msg_type == 'updset':
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} F_flowsen settings has been updated flow factor:{ff1}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='F_flowsen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        else:
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} F_flowsen status has been updated flow rate:{fr1}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='F_flowsen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        #hourly
                        yrdata=treat_F_flowsen.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_fr1=0
                        sums_ff1=0
                        avgs_fr1 = 0
                        avgs_ff1 = 0
                        
                        
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    fr1=yr.fr1
                                    ff1=yr.ff1
                                    
                                    sums_fr1=sums_fr1+fr1
                                    sums_ff1=sums_ff1+ff1
                                    
                                    
                                    count=count+1
                            avgs_fr1=sums_fr1/count
                            avgs_ff1=sums_ff1/count
                            
                    
                        hr=F_flowsen_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        if hr:
                            yr_data=F_flowsen_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id).update(device_id=device_id,service='F_flowsen',fr1={'sum':sums_fr1,'avg':avgs_fr1,'count':count},ff1={'sum':sums_ff1,'avg':avgs_ff1,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=F_flowsen_repo_hourly.objects.create(device_id=device_id,service='F_flowsen',fr1={'sum':sums_fr1,'avg':avgs_fr1,'count':count},ff1={'sum':sums_ff1,'avg':avgs_ff1,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #daily
                        yrdata=treat_F_flowsen.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_fr1=0
                        sums_ff1=0
                        
                        avgs_fr1 = 0
                        avgs_ff1 = 0
                        
                        
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    fr1=yr.fr1
                                    ff1=yr.ff1
                                    
                                    
                                    sums_fr1=sums_fr1+fr1
                                    sums_ff1=sums_ff1+ff1
                                    
                                    
                                    count=count+1
                            avgs_fr1=sums_fr1/count
                            avgs_ff1=sums_ff1/count
                            
                    
                        hr=F_flowsen_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        if hr:
                            yr_data=F_flowsen_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id).update(device_id=device_id,service='F_flowsen',fr1={'sum':sums_fr1,'avg':avgs_fr1,'count':count},ff1={'sum':sums_ff1,'avg':avgs_ff1,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=F_flowsen_repo_daily.objects.create(device_id=device_id,service='F_flowsen',fr1={'sum':sums_fr1,'avg':avgs_fr1,'count':count},ff1={'sum':sums_ff1,'avg':avgs_ff1,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #monthly
                        yrdata=treat_F_flowsen.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_fr1=0
                        sums_ff1=0
                        
                        avgs_fr1 = 0
                        avgs_ff1 = 0
                        
                        
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    fr1=yr.fr1
                                    ff1=yr.ff1
                                    
                                    
                                    sums_fr1=sums_fr1+fr1
                                    sums_ff1=sums_ff1+ff1
                                    
                                    
                                    count=count+1
                            avgs_fr1=sums_fr1/count
                            avgs_ff1=sums_ff1/count
                            
                    
                        hr=F_flowsen_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        if hr:
                            yr_data=F_flowsen_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id).update(device_id=device_id,service='F_flowsen',fr1={'sum':sums_fr1,'avg':avgs_fr1,'count':count},ff1={'sum':sums_ff1,'avg':avgs_ff1,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=F_flowsen_repo_monthly.objects.create(device_id=device_id,service='F_flowsen',fr1={'sum':sums_fr1,'avg':avgs_fr1,'count':count},ff1={'sum':sums_ff1,'avg':avgs_ff1,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #yearly
                        yrdata=treat_F_flowsen.objects.filter(year=dd[0],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_fr1=0
                        sums_ff1=0
                        
                        avgs_fr1 = 0
                        avgs_ff1 = 0
                        
                        
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    fr1=yr.fr1
                                    ff1=yr.ff1
                                    
                                    
                                    sums_fr1=sums_fr1+fr1
                                    sums_ff1=sums_ff1+ff1
                                    
                                    
                                    count=count+1
                            avgs_fr1=sums_fr1/count
                            avgs_ff1=sums_ff1/count
                            
                    
                        hr=F_flowsen_repo_yearly.objects.filter(year=dd[0],device_id=device_id)
                        if hr:
                            yr_data=F_flowsen_repo_yearly.objects.filter(year=dd[0],device_id=device_id).update(device_id=device_id,service='F_flowsen',fr1={'sum':sums_fr1,'avg':avgs_fr1,'count':count},ff1={'sum':sums_ff1,'avg':avgs_ff1,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=F_flowsen_repo_yearly.objects.create(device_id=device_id,service='F_flowsen',fr1={'sum':sums_fr1,'avg':avgs_fr1,'count':count},ff1={'sum':sums_ff1,'avg':avgs_ff1,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        
                except Exception as e:
                    erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='F_flowsen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()
                    # error_message = e
                    # # global eg
                    # eg = e
                    
                    
                    # EchoConsumer.websocket_receive('event','event') 

                try:
                    if 'P_flowsen'==components:
                        # com=cl
                        if device_id not in device_idlist:
                            repo_latestdata.objects.create(device_id=device_id,message_type=msg_type,P_flowsen=mydata1)
                        else:
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, P_flowsen=mydata1)

                            get_device_id=repo_latestdata.objects.all()
                            for did in get_device_id:
                                s=str(did.device_id)
                                if device_id == s:
                                    P_flowsen=did.P_flowsen
                            klist = list(P_flowsen.keys())
                            
                            mydatakey = list(mydata1.keys())
                            
                            for k,v in P_flowsen.items():
                                if k not in mydatakey:
                                    olddata.update({k:v})
                                    
                            mydata5=olddata.update(mydata1)    
                            
                            repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, P_flowsen=olddata)

                        ds=treat_P_flowsen.objects.create(device_id=device_id,message_type=msg_type,fr2=fr2,ff2=ff2,year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                        ds.save() 
                        if msg_type == 'updset':
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} P_flowsen settings has been updated flow factor:{ff2}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='P_flowsen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        else:
                            dd=dateandtime()
                            e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} P_flowsen status has been updated flow rate:{fr2}"
                            erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='P_flowsen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                        #hourly
                        yrdata=treat_P_flowsen.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_fr2=0
                        sums_ff2=0
                        avgs_fr2 = 0
                        avgs_ff2 = 0
                        
                        
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    fr2=yr.fr2
                                    ff2=yr.ff2
                                    
                                    sums_fr2=sums_fr2+fr2
                                    sums_ff2=sums_ff2+ff2
                                    
                                    
                                    count=count+1
                            avgs_fr2=sums_fr2/count
                            avgs_ff2=sums_ff2/count
                            
                    
                        hr=P_flowsen_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                        if hr:
                            yr_data=P_flowsen_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id).update(device_id=device_id,service='P_flowsen',fr2={'sum':sums_fr2,'avg':avgs_fr2,'count':count},ff2={'sum':sums_ff2,'avg':avgs_ff2,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=P_flowsen_repo_hourly.objects.create(device_id=device_id,service='P_flowsen',fr2={'sum':sums_fr2,'avg':avgs_fr2,'count':count},ff2={'sum':sums_ff2,'avg':avgs_ff2,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #daily
                        yrdata=treat_P_flowsen.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_fr2=0
                        sums_ff2=0
                        
                        avgs_fr2 = 0
                        avgs_ff2 = 0
                        
                        
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    fr2=yr.fr2
                                    ff2=yr.ff2
                                    
                                    
                                    sums_fr2=sums_fr2+fr2
                                    sums_ff2=sums_ff2+ff2
                                    
                                    
                                    count=count+1
                            avgs_fr2=sums_fr2/count
                            avgs_ff2=sums_ff2/count
                            
                    
                        hr=P_flowsen_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                        if hr:
                            yr_data=P_flowsen_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id).update(device_id=device_id,service='P_flowsen',fr2={'sum':sums_fr2,'avg':avgs_fr2,'count':count},ff2={'sum':sums_ff2,'avg':avgs_ff2,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=P_flowsen_repo_daily.objects.create(device_id=device_id,service='P_flowsen',fr2={'sum':sums_fr2,'avg':avgs_fr2,'count':count},ff2={'sum':sums_ff2,'avg':avgs_ff2,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #monthly
                        yrdata=treat_P_flowsen.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_fr2=0
                        sums_ff2=0
                        
                        avgs_fr2 = 0
                        avgs_ff2 = 0
                        
                        
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    fr2=yr.fr2
                                    ff2=yr.ff2
                                    
                                    
                                    sums_fr2=sums_fr2+fr2
                                    sums_ff2=sums_ff2+ff2
                                    
                                    
                                    count=count+1
                            avgs_fr2=sums_fr2/count
                            avgs_ff2=sums_ff2/count
                            
                    
                        hr=P_flowsen_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                        if hr:
                            yr_data=P_flowsen_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id).update(device_id=device_id,service='P_flowsen',fr2={'sum':sums_fr2,'avg':avgs_fr2,'count':count},ff2={'sum':sums_ff2,'avg':avgs_ff2,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=P_flowsen_repo_monthly.objects.create(device_id=device_id,service='P_flowsen',fr2={'sum':sums_fr2,'avg':avgs_fr2,'count':count},ff2={'sum':sums_ff2,'avg':avgs_ff2,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        #yearly
                        yrdata=treat_P_flowsen.objects.filter(year=dd[0],device_id=device_id)
                        count=0
                        zerocount=-1
                        sumd={}
                        sums_fr2=0
                        sums_ff2=0
                        
                        avgs_fr2 = 0
                        avgs_ff2 = 0
                        
                        
                        if yrdata:
                            for yr in yrdata:
                                yr_d_id=yr.device_id
                                if yr_d_id == device_id:
                                    fr2=yr.fr2
                                    ff2=yr.ff2
                                    
                                    
                                    sums_fr2=sums_fr2+fr2
                                    sums_ff2=sums_ff2+ff2
                                    
                                    
                                    count=count+1
                            avgs_fr2=sums_fr2/count
                            avgs_ff2=sums_ff2/count
                            
                    
                        hr=P_flowsen_repo_yearly.objects.filter(year=dd[0],device_id=device_id)
                        if hr:
                            yr_data=P_flowsen_repo_yearly.objects.filter(year=dd[0],device_id=device_id).update(device_id=device_id,service='P_flowsen',fr2={'sum':sums_fr2,'avg':avgs_fr2,'count':count},ff2={'sum':sums_ff2,'avg':avgs_ff2,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                        else:
                            yr_data=P_flowsen_repo_yearly.objects.create(device_id=device_id,service='P_flowsen',fr2={'sum':sums_fr2,'avg':avgs_fr2,'count':count},ff2={'sum':sums_ff2,'avg':avgs_ff2,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            yr_data.save()
                        
                except Exception as e:
                    erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='P_flowsen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()
                    # error_message = e
                    # # global eg
                    # eg = e
                    
                    
                    # EchoConsumer.websocket_receive('event','event')    
                    
                        # EchoConsumer.websocket_receive('event','event') 
                try:

                    if 'tap1'==components:
                            # com=cl
                            if device_id not in device_idlist:
                                repo_latestdata.objects.create(device_id=device_id,message_type=msg_type,tap1=mydata1)
                            else:

                                # repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, flowsen=mydata1)
                                repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, tap1=mydata1)

                                get_device_id=repo_latestdata.objects.all()
                                for did in get_device_id:
                                    s=str(did.device_id)
                                    if device_id == s:
                                        tap1=did.tap1
                                klist = list(tap1.keys())
                                
                                mydatakey = list(mydata1.keys())
                                
                                for k,v in tap1.items():
                                    if k not in mydatakey:
                                        olddata.update({k:v})
                                        
                                mydata5=olddata.update(mydata1)    
                                
                                repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, tap1=olddata)

                            # repo_latestobj=repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id,message_type=msg_type,tap1=mydata1)
                            # repo_latestobj.save()  
                            ds=disp_tap1.objects.create(device_id=device_id,message_type=msg_type,p1=p1,p2=p2,p3=p3,p4=p4,year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            ds.save()
                            if msg_type == 'updset':
                                dd=dateandtime()
                                e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tap1 settings has been updated pulse1:{p1} pulse2:{p2} pulse3:{p3} pulse4:{p4}"
                                erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='tap1',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                                erro.save()
                            else:
                                pass
                            #hourly
                            yrdata=disp_tap1.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_p1=0
                            sums_p2=0
                            sums_p3=0
                            sums_p4=0
                            avgs_p1 = 0
                            avgs_p2 = 0
                            avgs_p3 = 0
                            avgs_p4 = 0
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        p1=yr.p1
                                        p2=yr.p2
                                        p3=yr.p3
                                        p4=yr.p4
                                        sums_p1=sums_p1+p1
                                        sums_p2=sums_p2+p2
                                        sums_p3=sums_p3+p3
                                        sums_p4=sums_p4+p4
                                        count=count+1
                                avgs_p1=sums_p1/count
                                avgs_p2=sums_p2/count
                                avgs_p3=sums_p3/count
                                avgs_p4=sums_p4/count
                            hr=tap1_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                            if hr:
                                yr_data=tap1_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id).update(device_id=device_id,service='tap1',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=tap1_repo_hourly.objects.create(device_id=device_id,service='tap1',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()

                            #daily
                            yrdata=disp_tap1.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_p1=0
                            sums_p2=0
                            sums_p3=0
                            sums_p4=0
                            avgs_p1 = 0
                            avgs_p2 = 0
                            avgs_p3 = 0
                            avgs_p4 = 0
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        p1=yr.p1
                                        p2=yr.p2
                                        p3=yr.p3
                                        p4=yr.p4
                                        sums_p1=sums_p1+p1
                                        sums_p2=sums_p2+p2
                                        sums_p3=sums_p3+p3
                                        sums_p4=sums_p4+p4
                                        count=count+1
                                avgs_p1=sums_p1/count
                                avgs_p2=sums_p2/count
                                avgs_p3=sums_p3/count
                                avgs_p4=sums_p4/count
                            hr=tap1_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                            if hr:
                                yr_data=tap1_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id).update(device_id=device_id,service='tap1',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=tap1_repo_daily.objects.create(device_id=device_id,service='tap1',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()
                            #monthly
                            yrdata=disp_tap1.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_p1=0
                            sums_p2=0
                            sums_p3=0
                            sums_p4=0
                            avgs_p1 = 0
                            avgs_p2 = 0
                            avgs_p3 = 0
                            avgs_p4 = 0
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        p1=yr.p1
                                        p2=yr.p2
                                        p3=yr.p3
                                        p4=yr.p4
                                        sums_p1=sums_p1+p1
                                        sums_p2=sums_p2+p2
                                        sums_p3=sums_p3+p3
                                        sums_p4=sums_p4+p4
                                        count=count+1
                                avgs_p1=sums_p1/count
                                avgs_p2=sums_p2/count
                                avgs_p3=sums_p3/count
                                avgs_p4=sums_p4/count
                            hr=tap1_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                            if hr:
                                yr_data=tap1_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id).update(device_id=device_id,service='tap1',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=tap1_repo_monthly.objects.create(device_id=device_id,service='tap1',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()
                            #yearly
                            yrdata=disp_tap1.objects.filter(year=dd[0],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_p1=0
                            sums_p2=0
                            sums_p3=0
                            sums_p4=0
                            avgs_p1 = 0
                            avgs_p2 = 0
                            avgs_p3 = 0
                            avgs_p4 = 0
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        p1=yr.p1
                                        p2=yr.p2
                                        p3=yr.p3
                                        p4=yr.p4
                                        sums_p1=sums_p1+p1
                                        sums_p2=sums_p2+p2
                                        sums_p3=sums_p3+p3
                                        sums_p4=sums_p4+p4
                                        count=count+1
                                avgs_p1=sums_p1/count
                                avgs_p2=sums_p2/count
                                avgs_p3=sums_p3/count
                                avgs_p4=sums_p4/count
                            hr=tap1_repo_yearly.objects.filter(year=dd[0],device_id=device_id)
                            if hr:
                                yr_data=tap1_repo_yearly.objects.filter(year=dd[0],device_id=device_id).update(device_id=device_id,service='tap1',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=tap1_repo_yearly.objects.create(device_id=device_id,service='tap1',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()
                except Exception as e:
                    erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='tap1',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()
                    # error_message = e
                    # # global eg
                    # eg = e
                    
                    
                    # EchoConsumer.websocket_receive('event','event')  
                try:
                    if 'tap2'==components:
                            # com=cl
                            if device_id not in device_idlist:
                                repo_latestdata.objects.create(device_id=device_id,message_type=msg_type,tap2=mydata1)
                            else:
                                repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, tap2=mydata1)

                                get_device_id=repo_latestdata.objects.all()
                                for did in get_device_id:
                                    s=str(did.device_id)
                                    if device_id == s:
                                        tap2=did.tap2
                                klist = list(tap2.keys())
                                
                                mydatakey = list(mydata1.keys())
                                
                                for k,v in tap2.items():
                                    if k not in mydatakey:
                                        olddata.update({k:v})
                                        
                                mydata5=olddata.update(mydata1)    
                                
                                repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, tap2=olddata)

                            # repo_latestobj=repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id,message_type=msg_type,tap2=mydata1)
                            # repo_latestobj.save()
                            ds=disp_tap2.objects.create(device_id=device_id,message_type=msg_type,p1=p1,p2=p2,p3=p3,p4=p4,year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            ds.save()
                            if msg_type == 'updset':
                                dd=dateandtime()
                                e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tap2 settings has been updated pulse1:{p1} pulse2:{p2} pulse3:{p3} pulse4:{p4}"
                                erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='tap2',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                                erro.save()
                            else:
                                pass
                            #hourly
                            yrdata=disp_tap2.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_p1=0
                            sums_p2=0
                            sums_p3=0
                            sums_p4=0
                            avgs_p1 = 0
                            avgs_p2 = 0
                            avgs_p3 = 0
                            avgs_p4 = 0
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        p1=yr.p1
                                        p2=yr.p2
                                        p3=yr.p3
                                        p4=yr.p4
                                        sums_p1=sums_p1+p1
                                        sums_p2=sums_p2+p2
                                        sums_p3=sums_p3+p3
                                        sums_p4=sums_p4+p4
                                        count=count+1
                                avgs_p1=sums_p1/count
                                avgs_p2=sums_p2/count
                                avgs_p3=sums_p3/count
                                avgs_p4=sums_p4/count
                            hr=tap2_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                            if hr:
                                yr_data=tap2_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id).update(device_id=device_id,service='tap2',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=tap2_repo_hourly.objects.create(device_id=device_id,service='tap2',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()

                            #daily
                            yrdata=disp_tap2.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_p1=0
                            sums_p2=0
                            sums_p3=0
                            sums_p4=0
                            avgs_p1 = 0
                            avgs_p2 = 0
                            avgs_p3 = 0
                            avgs_p4 = 0
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        p1=yr.p1
                                        p2=yr.p2
                                        p3=yr.p3
                                        p4=yr.p4
                                        sums_p1=sums_p1+p1
                                        sums_p2=sums_p2+p2
                                        sums_p3=sums_p3+p3
                                        sums_p4=sums_p4+p4
                                        count=count+1
                                avgs_p1=sums_p1/count
                                avgs_p2=sums_p2/count
                                avgs_p3=sums_p3/count
                                avgs_p4=sums_p4/count
                            hr=tap2_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                            if hr:
                                yr_data=tap2_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id).update(device_id=device_id,service='tap2',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=tap2_repo_daily.objects.create(device_id=device_id,service='tap2',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()
                            #monthly
                            yrdata=disp_tap2.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_p1=0
                            sums_p2=0
                            sums_p3=0
                            sums_p4=0
                            avgs_p1 = 0
                            avgs_p2 = 0
                            avgs_p3 = 0
                            avgs_p4 = 0
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        p1=yr.p1
                                        p2=yr.p2
                                        p3=yr.p3
                                        p4=yr.p4
                                        sums_p1=sums_p1+p1
                                        sums_p2=sums_p2+p2
                                        sums_p3=sums_p3+p3
                                        sums_p4=sums_p4+p4
                                        count=count+1
                                avgs_p1=sums_p1/count
                                avgs_p2=sums_p2/count
                                avgs_p3=sums_p3/count
                                avgs_p4=sums_p4/count
                            hr=tap2_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                            if hr:
                                yr_data=tap2_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id).update(device_id=device_id,service='tap2',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=tap2_repo_monthly.objects.create(device_id=device_id,service='tap2',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()
                            #yearly
                            yrdata=disp_tap2.objects.filter(year=dd[0],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_p1=0
                            sums_p2=0
                            sums_p3=0
                            sums_p4=0
                            avgs_p1 = 0
                            avgs_p2 = 0
                            avgs_p3 = 0
                            avgs_p4 = 0
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        p1=yr.p1
                                        p2=yr.p2
                                        p3=yr.p3
                                        p4=yr.p4
                                        sums_p1=sums_p1+p1
                                        sums_p2=sums_p2+p2
                                        sums_p3=sums_p3+p3
                                        sums_p4=sums_p4+p4
                                        count=count+1
                                avgs_p1=sums_p1/count
                                avgs_p2=sums_p2/count
                                avgs_p3=sums_p3/count
                                avgs_p4=sums_p4/count
                            hr=tap2_repo_yearly.objects.filter(year=dd[0],device_id=device_id)
                            if hr:
                                yr_data=tap2_repo_yearly.objects.filter(year=dd[0],device_id=device_id).update(device_id=device_id,service='tap2',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=tap2_repo_yearly.objects.create(device_id=device_id,service='tap2',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()
                except Exception as e:
                    erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='tap2',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()
                    # error_message = e
                    # # global eg
                    # eg = e
                try:

                    if 'tap3'==components:
                            # com=cl
                            if device_id not in device_idlist:
                                repo_latestdata.objects.create(device_id=device_id,message_type=msg_type,tap3=mydata1)
                            else:
                                repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, tap3=mydata1)

                                get_device_id=repo_latestdata.objects.all()
                                for did in get_device_id:
                                    s=str(did.device_id)
                                    if device_id == s:
                                        tap3=did.tap3
                                
                                klist = list(tap3.keys())
                                
                                mydatakey = list(mydata1.keys())
                                
                                for k,v in tap3.items():
                                    if k not in mydatakey:
                                        olddata.update({k:v})
                                        
                                mydata5=olddata.update(mydata1)    
                                
                                repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, tap3=olddata)

                            # repo_latestobj=repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id,message_type=msg_type,tap3=mydata1)
                            # repo_latestobj.save()   
                            ds=disp_tap3.objects.create(device_id=device_id,message_type=msg_type,p1=p1,p2=p2,p3=p3,p4=p4,year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            ds.save()
                            if msg_type == 'updset':
                                dd=dateandtime()
                                e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tap3 settings has been updated pulse1:{p1} pulse2:{p2} pulse3:{p3} pulse4:{p4}"
                                erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='tap3',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                                erro.save()
                            else:
                                pass
                            #hourly
                            yrdata=disp_tap3.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_p1=0
                            sums_p2=0
                            sums_p3=0
                            sums_p4=0
                            avgs_p1 = 0
                            avgs_p2 = 0
                            avgs_p3 = 0
                            avgs_p4 = 0
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        p1=yr.p1
                                        p2=yr.p2
                                        p3=yr.p3
                                        p4=yr.p4
                                        sums_p1=sums_p1+p1
                                        sums_p2=sums_p2+p2
                                        sums_p3=sums_p3+p3
                                        sums_p4=sums_p4+p4
                                        count=count+1
                                avgs_p1=sums_p1/count
                                avgs_p2=sums_p2/count
                                avgs_p3=sums_p3/count
                                avgs_p4=sums_p4/count
                            hr=tap3_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                            if hr:
                                yr_data=tap3_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id).update(device_id=device_id,service='tap3',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=tap3_repo_hourly.objects.create(device_id=device_id,service='tap3',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()

                            #daily
                            yrdata=disp_tap3.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_p1=0
                            sums_p2=0
                            sums_p3=0
                            sums_p4=0
                            avgs_p1 = 0
                            avgs_p2 = 0
                            avgs_p3 = 0
                            avgs_p4 = 0
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        p1=yr.p1
                                        p2=yr.p2
                                        p3=yr.p3
                                        p4=yr.p4
                                        sums_p1=sums_p1+p1
                                        sums_p2=sums_p2+p2
                                        sums_p3=sums_p3+p3
                                        sums_p4=sums_p4+p4
                                        count=count+1
                                avgs_p1=sums_p1/count
                                avgs_p2=sums_p2/count
                                avgs_p3=sums_p3/count
                                avgs_p4=sums_p4/count
                            hr=tap3_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                            if hr:
                                yr_data=tap3_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id).update(device_id=device_id,service='tap3',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=tap3_repo_daily.objects.create(device_id=device_id,service='tap3',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()
                            #monthly
                            yrdata=disp_tap3.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_p1=0
                            sums_p2=0
                            sums_p3=0
                            sums_p4=0
                            avgs_p1 = 0
                            avgs_p2 = 0
                            avgs_p3 = 0
                            avgs_p4 = 0
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        p1=yr.p1
                                        p2=yr.p2
                                        p3=yr.p3
                                        p4=yr.p4
                                        sums_p1=sums_p1+p1
                                        sums_p2=sums_p2+p2
                                        sums_p3=sums_p3+p3
                                        sums_p4=sums_p4+p4
                                        count=count+1
                                avgs_p1=sums_p1/count
                                avgs_p2=sums_p2/count
                                avgs_p3=sums_p3/count
                                avgs_p4=sums_p4/count
                            hr=tap3_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                            if hr:
                                yr_data=tap3_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id).update(device_id=device_id,service='tap3',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=tap3_repo_monthly.objects.create(device_id=device_id,service='tap3',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()
                            #yearly
                            yrdata=disp_tap3.objects.filter(year=dd[0],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_p1=0
                            sums_p2=0
                            sums_p3=0
                            sums_p4=0
                            avgs_p1 = 0
                            avgs_p2 = 0
                            avgs_p3 = 0
                            avgs_p4 = 0
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        p1=yr.p1
                                        p2=yr.p2
                                        p3=yr.p3
                                        p4=yr.p4
                                        sums_p1=sums_p1+p1
                                        sums_p2=sums_p2+p2
                                        sums_p3=sums_p3+p3
                                        sums_p4=sums_p4+p4
                                        count=count+1
                                avgs_p1=sums_p1/count
                                avgs_p2=sums_p2/count
                                avgs_p3=sums_p3/count
                                avgs_p4=sums_p4/count
                            hr=tap3_repo_yearly.objects.filter(year=dd[0],device_id=device_id)
                            if hr:
                                yr_data=tap3_repo_yearly.objects.filter(year=dd[0],device_id=device_id).update(device_id=device_id,service='tap3',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=tap3_repo_yearly.objects.create(device_id=device_id,service='tap3',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()
                except Exception as e:
                    erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='tap3',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()
                    # error_message = e
                    # # global eg
                    # eg = e

                try:

                    if 'tap4'==components:
                            # com=cl
                            if device_id not in device_idlist:
                                repo_latestdata.objects.create(device_id=device_id,message_type=msg_type,tap4=mydata1)
                            else:
                                repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, tap4=mydata1)

                                get_device_id=repo_latestdata.objects.all()
                                for did in get_device_id:
                                    s=str(did.device_id)
                                    if device_id == s:
                                        tap4=did.tap4
                                klist = list(tap4.keys())
                                
                                mydatakey = list(mydata1.keys())
                                
                                for k,v in tap4.items():
                                    if k not in mydatakey:
                                        olddata.update({k:v})
                                        
                                mydata5=olddata.update(mydata1)    
                                
                                repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, tap4=olddata)

                            # repo_latestobj=repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id,message_type=msg_type,tap4=mydata1)
                            # repo_latestobj.save()
                            
                            ds1=disp_tap4.objects.create(device_id=device_id,message_type=msg_type,p1=p1,p2=p2,p3=p3,p4=p4,year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            # ds1.save()
                            if msg_type == 'updset':
                                dd=dateandtime()
                                e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tap4 settings has been updated pulse1:{p1} pulse2:{p2} pulse3:{p3} pulse4:{p4}"
                                erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='tap4',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                                erro.save()
                            else:
                                pass
                            
                            #hourly
                            
                            yrdata=disp_tap4.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_p1=0
                            sums_p2=0
                            sums_p3=0
                            sums_p4=0
                            avgs_p1 = 0
                            avgs_p2 = 0
                            avgs_p3 = 0
                            avgs_p4 = 0
                            
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        p1=yr.p1
                                        p2=yr.p2
                                        p3=yr.p3
                                        p4=yr.p4
                                        sums_p1=sums_p1+p1
                                        sums_p2=sums_p2+p2
                                        sums_p3=sums_p3+p3
                                        sums_p4=sums_p4+p4
                                        count=count+1
                                avgs_p1=sums_p1/count
                                avgs_p2=sums_p2/count
                                avgs_p3=sums_p3/count
                                avgs_p4=sums_p4/count
                            
                            hr=tap4_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                            if hr:
                                yr_data=tap4_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id).update(device_id=device_id,service='tap4',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=tap4_repo_hourly.objects.create(device_id=device_id,service='tap4',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()

                            #daily
                            yrdata=disp_tap4.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_p1=0
                            sums_p2=0
                            sums_p3=0
                            sums_p4=0
                            avgs_p1 = 0
                            avgs_p2 = 0
                            avgs_p3 = 0
                            avgs_p4 = 0
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        p1=yr.p1
                                        p2=yr.p2
                                        p3=yr.p3
                                        p4=yr.p4
                                        sums_p1=sums_p1+p1
                                        sums_p2=sums_p2+p2
                                        sums_p3=sums_p3+p3
                                        sums_p4=sums_p4+p4
                                        count=count+1
                                avgs_p1=sums_p1/count
                                avgs_p2=sums_p2/count
                                avgs_p3=sums_p3/count
                                avgs_p4=sums_p4/count
                            hr=tap4_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                            if hr:
                                yr_data=tap4_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id).update(device_id=device_id,service='tap4',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=tap4_repo_daily.objects.create(device_id=device_id,service='tap4',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()
                            #monthly
                            yrdata=disp_tap4.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_p1=0
                            sums_p2=0
                            sums_p3=0
                            sums_p4=0
                            avgs_p1 = 0
                            avgs_p2 = 0
                            avgs_p3 = 0
                            avgs_p4 = 0
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        p1=yr.p1
                                        p2=yr.p2
                                        p3=yr.p3
                                        p4=yr.p4
                                        sums_p1=sums_p1+p1
                                        sums_p2=sums_p2+p2
                                        sums_p3=sums_p3+p3
                                        sums_p4=sums_p4+p4
                                        count=count+1
                                avgs_p1=sums_p1/count
                                avgs_p2=sums_p2/count
                                avgs_p3=sums_p3/count
                                avgs_p4=sums_p4/count
                            hr=tap4_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                            if hr:
                                yr_data=tap4_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id).update(device_id=device_id,service='tap4',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=tap4_repo_monthly.objects.create(device_id=device_id,service='tap4',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()
                            #yearly
                            yrdata=disp_tap4.objects.filter(year=dd[0],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_p1=0
                            sums_p2=0
                            sums_p3=0
                            sums_p4=0
                            avgs_p1 = 0
                            avgs_p2 = 0
                            avgs_p3 = 0
                            avgs_p4 = 0
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        p1=yr.p1
                                        p2=yr.p2
                                        p3=yr.p3
                                        p4=yr.p4
                                        sums_p1=sums_p1+p1
                                        sums_p2=sums_p2+p2
                                        sums_p3=sums_p3+p3
                                        sums_p4=sums_p4+p4
                                        count=count+1
                                avgs_p1=sums_p1/count
                                avgs_p2=sums_p2/count
                                avgs_p3=sums_p3/count
                                avgs_p4=sums_p4/count
                            hr=tap4_repo_yearly.objects.filter(year=dd[0],device_id=device_id)
                            if hr:
                                yr_data=tap4_repo_yearly.objects.filter(year=dd[0],device_id=device_id).update(device_id=device_id,service='tap4',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=tap4_repo_yearly.objects.create(device_id=device_id,service='tap4',p1={'sum':sums_p1,'avg':avgs_p1,'count':count},p2={'sum':sums_p2,'avg':avgs_p2,'count':count},p3={'sum':sums_p3,'avg':avgs_p3,'count':count},p4={'sum':sums_p4,'avg':avgs_p4,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()
                except Exception as e:
                    erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='tap4',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()
                    # error_message = e
                    # # global eg
                    # eg = e

                try:

                    if 'flowsen1'==components:
                            # com=cl
                            if device_id not in device_idlist:
                                repo_latestdata.objects.create(device_id=device_id,message_type=msg_type,flowsen1=mydata1)
                            else:
                                repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, flowsen1=mydata1)

                                get_device_id=repo_latestdata.objects.all()
                                for did in get_device_id:
                                    s=str(did.device_id)
                                    if device_id == s:
                                        flowsen1=did.flowsen1
                                klist = list(flowsen1.keys())
                                
                                mydatakey = list(mydata1.keys())
                                
                                for k,v in flowsen1.items():
                                    if k not in mydatakey:
                                        olddata.update({k:v})
                                        
                                mydata5=olddata.update(mydata1)    
                                
                                repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, flowsen1=olddata)

                            # repo_latestobj=repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id,message_type=msg_type,flowsen1=mydata1)
                            # repo_latestobj.save()
                            ds=disp_flowsen1.objects.create(device_id=device_id,message_type=msg_type,fr=fr,year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            ds.save()
                            if msg_type == 'updset':
                                dd=dateandtime()
                                e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} flowsen1 settings has been updated flow rate:{fr}"
                                erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='flowsen1',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                                erro.save()
                            else:
                                dd=dateandtime()
                                e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} flowsen1 status has been updated flow rate:{fr}"
                                erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='flowsen1',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                                erro.save()
                            #hourly
                            yrdata=disp_flowsen1.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_fr=0
                            avgs_fr = 0
                        
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        fr=yr.fr
                                        sums_fr=sums_fr+fr
                                        
                                        count=count+1
                                avgs_fr=sums_fr/count
                                
                            hr=flowsen1_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                            if hr:
                                yr_data=flowsen1_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id).update(device_id=device_id,service='flowsen1',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=flowsen1_repo_hourly.objects.create(device_id=device_id,service='flowsen1',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()

                            #daily
                            yrdata=disp_flowsen1.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_fr=0
                            
                            avgs_fr = 0
                            
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        fr=yr.fr
                                        sums_fr=sums_fr+fr
                                        
                                        count=count+1
                                avgs_fr=sums_fr/count
                                
                            hr=flowsen1_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                            if hr:
                                yr_data=flowsen1_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id).update(device_id=device_id,service='flowsen1',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=flowsen1_repo_daily.objects.create(device_id=device_id,service='flowsen1',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()
                            #monthly
                            yrdata=disp_flowsen1.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_fr=0
                            
                            avgs_fr = 0
                            
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        fr=yr.fr
                                        sums_fr=sums_fr+fr
                                        
                                        count=count+1
                                avgs_fr=sums_fr/count
                                
                            hr=flowsen1_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                            if hr:
                                yr_data=flowsen1_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id).update(device_id=device_id,service='flowsen1',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=flowsen1_repo_monthly.objects.create(device_id=device_id,service='flowsen1',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()
                            #yearly
                            yrdata=disp_flowsen1.objects.filter(year=dd[0],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_fr=0
                            
                            avgs_fr = 0
                            
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        fr=yr.fr
                                        sums_fr=sums_fr+fr
                                        
                                        count=count+1
                                avgs_fr=sums_fr/count
                                
                            hr=flowsen1_repo_yearly.objects.filter(year=dd[0],device_id=device_id)
                            if hr:
                                yr_data=flowsen1_repo_yearly.objects.filter(year=dd[0],device_id=device_id).update(device_id=device_id,service='flowsen1',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=flowsen1_repo_yearly.objects.create(device_id=device_id,service='flowsen1',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()
                except Exception as e:
                    erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='flowsen1',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()
                    # error_message = e
                    # # global eg
                    # eg = e
                try:

                    if 'flowsen2'==components:
                            # com=cl
                            if device_id not in device_idlist:
                                repo_latestdata.objects.create(device_id=device_id,message_type=msg_type,flowsen2=mydata1)
                            else:
                                repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, flowsen2=mydata1)

                                get_device_id=repo_latestdata.objects.all()
                                for did in get_device_id:
                                    s=str(did.device_id)
                                    if device_id == s:
                                        flowsen2=did.flowsen2
                                klist = list(flowsen2.keys())
                                
                                mydatakey = list(mydata1.keys())
                                
                                for k,v in flowsen2.items():
                                    if k not in mydatakey:
                                        olddata.update({k:v})
                                        
                                mydata5=olddata.update(mydata1)    
                                
                                repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, flowsen2=olddata)

                            # repo_latestobj=repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id,message_type=msg_type,flowsen2=mydata1)
                            # repo_latestobj.save()
                            ds=disp_flowsen2.objects.create(device_id=device_id,message_type=msg_type,fr=fr,year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            ds.save()
                            if msg_type == 'updset':
                                dd=dateandtime()
                                e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} flowsen2 settings has been updated flow rate:{fr}"
                                erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='flowsen2',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                                erro.save()
                            else:
                                dd=dateandtime()
                                e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} flowsen2 status has been updated flow rate:{fr}"
                                erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='flowsen2',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                                erro.save()
                            #hourly
                            yrdata=disp_flowsen2.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_fr=0
                            avgs_fr = 0
                        
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        fr=yr.fr
                                        sums_fr=sums_fr+fr
                                        
                                        count=count+1
                                avgs_fr=sums_fr/count
                                
                            hr=flowsen2_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                            if hr:
                                yr_data=flowsen2_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id).update(device_id=device_id,service='flowsen2',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=flowsen2_repo_hourly.objects.create(device_id=device_id,service='flowsen2',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()

                            #daily
                            yrdata=disp_flowsen2.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_fr=0
                            
                            avgs_fr = 0
                            
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        fr=yr.fr
                                        sums_fr=sums_fr+fr
                                        
                                        count=count+1
                                avgs_fr=sums_fr/count
                                
                            hr=flowsen2_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                            if hr:
                                yr_data=flowsen2_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id).update(device_id=device_id,service='flowsen2',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=flowsen2_repo_daily.objects.create(device_id=device_id,service='flowsen2',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()
                            #monthly
                            yrdata=disp_flowsen2.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_fr=0
                            
                            avgs_fr = 0
                            
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        fr=yr.fr
                                        sums_fr=sums_fr+fr
                                        
                                        count=count+1
                                avgs_fr=sums_fr/count
                                
                            hr=flowsen2_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                            if hr:
                                yr_data=flowsen2_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id).update(device_id=device_id,service='flowsen2',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=flowsen2_repo_monthly.objects.create(device_id=device_id,service='flowsen2',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()
                            #yearly
                            yrdata=disp_flowsen2.objects.filter(year=dd[0],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_fr=0
                            
                            avgs_fr = 0
                            
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        fr=yr.fr
                                        sums_fr=sums_fr+fr
                                        
                                        count=count+1
                                avgs_fr=sums_fr/count
                                
                            hr=flowsen2_repo_yearly.objects.filter(year=dd[0],device_id=device_id)
                            if hr:
                                yr_data=flowsen2_repo_yearly.objects.filter(year=dd[0],device_id=device_id).update(device_id=device_id,service='flowsen2',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=flowsen2_repo_yearly.objects.create(device_id=device_id,service='flowsen2',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()
                except Exception as e:
                    erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='flowsen2',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()
                    # error_message = e
                    # # global eg
                    # eg = e
                try:

                    if 'flowsen3'==components:
                            # com=cl
                            if device_id not in device_idlist:
                                repo_latestdata.objects.create(device_id=device_id,message_type=msg_type,flowsen3=mydata1)
                            else:
                                repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, flowsen3=mydata1)

                                get_device_id=repo_latestdata.objects.all()
                                for did in get_device_id:
                                    s=str(did.device_id)
                                    if device_id == s:
                                        flowsen3=did.flowsen3
                                klist = list(flowsen3.keys())
                                
                                mydatakey = list(mydata1.keys())
                                
                                for k,v in flowsen3.items():
                                    if k not in mydatakey:
                                        olddata.update({k:v})
                                        
                                mydata5=olddata.update(mydata1)    
                                
                                repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, flowsen3=olddata)

                            # repo_latestobj=repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id,message_type=msg_type,flowsen3=mydata1)
                            # repo_latestobj.save()
                            ds=disp_flowsen3.objects.create(device_id=device_id,message_type=msg_type,fr=fr,year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            ds.save()
                            if msg_type == 'updset':
                                dd=dateandtime()
                                e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} flowsen3 settings has been updated flow rate:{fr}"
                                erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='flowsen3',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                                erro.save()
                            else:
                                dd=dateandtime()
                                e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} flowsen3 status has been updated flow rate:{fr}"
                                erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='flowsen3',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                                erro.save()
                            #hourly
                            yrdata=disp_flowsen3.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_fr=0
                            avgs_fr = 0
                        
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        fr=yr.fr
                                        sums_fr=sums_fr+fr
                                        
                                        count=count+1
                                avgs_fr=sums_fr/count
                                
                            hr=flowsen3_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                            if hr:
                                yr_data=flowsen3_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id).update(device_id=device_id,service='flowsen3',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=flowsen3_repo_hourly.objects.create(device_id=device_id,service='flowsen3',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()

                            #daily
                            yrdata=disp_flowsen3.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_fr=0
                            
                            avgs_fr = 0
                            
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        fr=yr.fr
                                        sums_fr=sums_fr+fr
                                        
                                        count=count+1
                                avgs_fr=sums_fr/count
                                
                            hr=flowsen3_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                            if hr:
                                yr_data=flowsen3_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id).update(device_id=device_id,service='flowsen3',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=flowsen3_repo_daily.objects.create(device_id=device_id,service='flowsen3',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()
                            #monthly
                            yrdata=disp_flowsen3.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_fr=0
                            
                            avgs_fr = 0
                            
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        fr=yr.fr
                                        sums_fr=sums_fr+fr
                                        
                                        count=count+1
                                avgs_fr=sums_fr/count
                                
                            hr=flowsen3_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                            if hr:
                                yr_data=flowsen3_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id).update(device_id=device_id,service='flowsen3',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=flowsen3_repo_monthly.objects.create(device_id=device_id,service='flowsen3',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()
                            #yearly
                            yrdata=disp_flowsen3.objects.filter(year=dd[0],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_fr=0
                            
                            avgs_fr = 0
                            
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        fr=yr.fr
                                        sums_fr=sums_fr+fr
                                        
                                        count=count+1
                                avgs_fr=sums_fr/count
                                
                            hr=flowsen3_repo_yearly.objects.filter(year=dd[0],device_id=device_id)
                            if hr:
                                yr_data=flowsen3_repo_yearly.objects.filter(year=dd[0],device_id=device_id).update(device_id=device_id,service='flowsen3',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=flowsen3_repo_yearly.objects.create(device_id=device_id,service='flowsen3',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()
                except Exception as e:
                    erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='flowsen3',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()
                    # error_message = e
                    # # global eg
                    # eg = e
                try:

                    if 'flowsen4'==components:
                            # com=cl
                            if device_id not in device_idlist:
                                repo_latestdata.objects.create(device_id=device_id,message_type=msg_type,flowsen4=mydata1)
                            else:
                                repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, flowsen4=mydata1)

                                get_device_id=repo_latestdata.objects.all()
                                for did in get_device_id:
                                    s=str(did.device_id)
                                    if device_id == s:
                                        flowsen4=did.flowsen4
                                klist = list(flowsen4.keys())
                                
                                mydatakey = list(mydata1.keys())
                                
                                for k,v in flowsen4.items():
                                    if k not in mydatakey:
                                        olddata.update({k:v})
                                        
                                mydata5=olddata.update(mydata1)    
                                
                                repo_latestobj = repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id, message_type=msg_type, flowsen4=olddata)

                            # repo_latestobj=repo_latestdata.objects.filter(device_id=device_id).update(device_id=device_id,message_type=msg_type,flowsen4=mydata1)
                            # repo_latestobj.save()
                            ds=disp_flowsen4.objects.create(device_id=device_id,message_type=msg_type,fr=fr,year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            ds.save()
                            if msg_type == 'updset':
                                dd=dateandtime()
                                e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} flowsen4 settings has been updated flow rate:{fr}"
                                erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='flowsen4',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                                erro.save()
                            else:
                                dd=dateandtime()
                                e1=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} flowsen4 status has been updated flow rate:{fr}"
                                erro=Errors.objects.create(device_id=device_id,e_discriptions=e1,service='flowsen4',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                                erro.save()
                            #hourly
                            yrdata=disp_flowsen4.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_fr=0
                            avgs_fr = 0
                        
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        fr=yr.fr
                                        sums_fr=sums_fr+fr
                                        
                                        count=count+1
                                avgs_fr=sums_fr/count
                                
                            hr=flowsen4_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id)
                            if hr:
                                yr_data=flowsen4_repo_hourly.objects.filter(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],device_id=device_id).update(device_id=device_id,service='flowsen4',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=flowsen4_repo_hourly.objects.create(device_id=device_id,service='flowsen4',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()

                            #daily
                            yrdata=disp_flowsen4.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_fr=0
                            
                            avgs_fr = 0
                            
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        fr=yr.fr
                                        sums_fr=sums_fr+fr
                                        
                                        count=count+1
                                avgs_fr=sums_fr/count
                                
                            hr=flowsen4_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id)
                            if hr:
                                yr_data=flowsen4_repo_daily.objects.filter(year=dd[0],month=dd[1],day=dd[2],device_id=device_id).update(device_id=device_id,service='flowsen4',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=flowsen4_repo_daily.objects.create(device_id=device_id,service='flowsen4',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()
                            #monthly
                            yrdata=disp_flowsen4.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_fr=0
                            
                            avgs_fr = 0
                            
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        fr=yr.fr
                                        sums_fr=sums_fr+fr
                                        
                                        count=count+1
                                avgs_fr=sums_fr/count
                                
                            hr=flowsen4_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id)
                            if hr:
                                yr_data=flowsen4_repo_monthly.objects.filter(year=dd[0],month=dd[1],device_id=device_id).update(device_id=device_id,service='flowsen4',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=flowsen4_repo_monthly.objects.create(device_id=device_id,service='flowsen4',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()
                            #yearly
                            yrdata=disp_flowsen4.objects.filter(year=dd[0],device_id=device_id)
                            count=0
                            zerocount=-1
                            sumd={}
                            sums_fr=0
                            
                            avgs_fr = 0
                            
                            if yrdata:
                                for yr in yrdata:
                                    yr_d_id=yr.device_id
                                    if yr_d_id == device_id:
                                        fr=yr.fr
                                        sums_fr=sums_fr+fr
                                        
                                        count=count+1
                                avgs_fr=sums_fr/count
                                
                            hr=flowsen4_repo_yearly.objects.filter(year=dd[0],device_id=device_id)
                            if hr:
                                yr_data=flowsen4_repo_yearly.objects.filter(year=dd[0],device_id=device_id).update(device_id=device_id,service='flowsen4',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                            else:
                                yr_data=flowsen4_repo_yearly.objects.create(device_id=device_id,service='flowsen4',fr={'sum':sums_fr,'avg':avgs_fr,'count':count},hour=dd[3],month=dd[1],year=dd[0],day=dd[2])
                                yr_data.save()
                except Exception as e:
                    erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='flowsen4',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()


# mqttc.on_message = on_message
topic = "test"
try:
    mqttc = mqtt.Client()
    ssl_context= ssl_alpn()
    mqttc.tls_set_context(context=ssl_context)
    logger.info("start connect")
    # mqttc.connect(aws_iot_endpoint, port=443)
    mqttc.connect(aws_iot_endpoint, port=8883)
    logger.info("connect success")
    
    mqttc.subscribe('wc1/#',1)
    # client.subscribe('wc1/v1/OTP',1)

    mqttc.loop_start()
    # client.loop_start()

    # while True:
    #     now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    #     logger.info("try to publish:{}".format(now))
    #     # mqttc.publish(topic,"{'cnd':'100','spn':'3300','tsp':'500','asp':'700'}")
    #     mqttc.on_message = on_message
    #     time.sleep(5)

except Exception as e:
    logger.error("exception main()")
    logger.error("e obj:{}".format(vars(e)))
    # logger.error("message:{}".format(e.message))
    traceback.print_exc(file=sys.stdout)
mqttc.on_message = on_message
# client.message_callback_add("wc/v1/OTP", on_message_1)
# mqttc.message_callback_add("wc/#", on_message)