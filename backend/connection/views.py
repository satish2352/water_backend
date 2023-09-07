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
# mqttc = MqttClient()



class MqttClient:
    def __init__(self):
        print("Hi mqtt __init__")
        _topic = "wc1/v1/OTP"
        _topic_wc1 = "wc1/#"
        _port = 8883

        self.client = mqtt.Client()
        self.client = self.client 
        self.topic = _topic
        self.topic_wc1 = _topic_wc1
        self.client.on_connect = self.on_connect_1
        self.client.on_message = self.on_message_1
        ssl_context= ssl_alpn()
        self.client.tls_set_context(context=ssl_context)
        self.client.connect(aws_iot_endpoint, _port, OTP_VALID_FOR)
        self.client.loop_start()

    def on_message_1(self, client, userdata, message):
        pass
    def reconnect(self):
        _port = 8883
        ssl_context= ssl_alpn()
        self.client.tls_set_context(context=ssl_context)
        self.client.connect(aws_iot_endpoint, _port, OTP_VALID_FOR)
        self.client.loop_start()
        
    def otp_handler(self, client, userdata, message):
        print("I am in otp_handler")
        token_ = "0"
        company_ids = None
        panelid = None
        atmid = None
        print("Data received1!!!",message.payload)
        jstr=message.payload
        if isinstance(jstr, bytes):
            data1 = jstr.decode("utf-8")
        data=eval(data1)
        token_ = data["token"]
        device_id = data["deviceid"]
        print("*********134")
        if "panelid" in data1:
            # global panelid
            panelid = data["panelid"] if data["panelid"] else None
            if panelid:
                pass
            print("panelid")
        if "atmid" in data1:
            # global atmid
            atmid = data["atmid"] if data["atmid"] else None
            if atmid:
                pass
        print("Otp handler data['token']", data["token"])
        try:
            site_obj = Site.objects.get(token=data["token"])
        except Exception as err:
            print("Error in otp handler no site data found")
        else:
            print("OTP handler data panelid",panelid)
            print("OTP handler data atmid",atmid)
            print("OTP handler data site_obj",site_obj)
            if site_obj is not None:
                company_ids=site_obj.company_id
                site_ids=site_obj.id
                doublicate_panel_id=0
                doublicate_atm_id=0
                try:
                    if panelid is not None:
                        print("in panelid")
                        doublicate_panel_id=Device.objects.filter(serial_no2 =panelid).filter(~Q(site_id = site_ids)).count()
                    if atmid is not None:
                        print("in atmid")
                        doublicate_atm_id=Device.objects.filter(serial_no3 =atmid).filter(~Q(site_id = site_ids)).count()
                    
                except Exception as err:
                    print("error in panelid and atm duplicate checking error ".format(err))
                    
                
                if doublicate_panel_id >0 or doublicate_atm_id >0:
                        # site_obj_new = Site.objects.get(company_id=company_ids, id=site_ids)
                        if doublicate_panel_id>0:
                             site_obj.duplicate_panel=True
                        if doublicate_atm_id>0:
                             site_obj.duplicate_atm=True
                        print("Device duplicate found")
                        site_obj.token = None#6-9 time 10.20am

                        site_obj.save()

                else:
                    
                    with transaction.atomic():
                        try:  # TODO
                            try:
                                device_data = Device.objects.get(site_id=site_ids) # ! verfies device against site_id
                            except Device.DoesNotExist:
                                device_data = None
                                print("I am here device_data = None ")
                            if device_data is not None:
                                if device_data.serial_no2 is None:
                                    if panelid is not None:
                                        device_data.serial_no2 = panelid
                                        device_data.save()

                                        site_data = Site.objects.get(id=site_ids)
                                        site_data.is_treatment_unit = True
                                        site_data.token_verified = True
                                        site_data.token = None
                                        site_data.save()

                                        subscription_data = Subscription()
                                        subscription_data.site_id = site_ids
                                        subscription_data.is_treatment_unit = True
                                        subscription_data.company_id = company_ids
                                        subscription_data.save()
                                    else :
                                        site_data = Site.objects.get(id=site_ids)
                                        site_data.token = None
                                        site_data.save()
                                
                                if device_data.serial_no3 is None:
                                    if atmid is not None:
                                        device_data.serial_no3 = atmid
                                        device_data.save()

                                        site_data = Site.objects.get(id=site_ids)
                                        site_data.is_dispensing_unit = True
                                        site_data.token_verified = True
                                        site_data.token = None
                                        site_data.save()

                                        subscription_data = Subscription()
                                        subscription_data.site_id = site_ids
                                        subscription_data.is_dispensing_unit = True
                                        subscription_data.company_id = company_ids
                                        subscription_data.save()
                                        
                                    else :
                                        site_data = Site.objects.get(id=site_ids)
                                        site_data.token = None
                                        site_data.save()

                            else:
                                if panelid and atmid:

                                    device_data = Device()
                                    device_data.serial_no1 = device_id
                                    device_data.serial_no2 = panelid
                                    device_data.serial_no3 = atmid
                                    device_data.site_id = site_ids
                                    device_data.save()

                                    site_data = Site.objects.get(id=site_ids)
                                    site_data.is_treatment_unit = True
                                    site_data.is_dispensing_unit = True
                                    site_data.token_verified = True
                                    site_data.token = None
                                    site_data.save()

                                    subscription_data = Subscription()
                                    subscription_data.site_id = site_ids
                                    subscription_data.is_treatment_unit = True
                                    subscription_data.company_id = company_ids
                                    subscription_data.save()

                                    subscription_data1 = Subscription()
                                    subscription_data1.site_id = site_ids
                                    subscription_data1.is_dispensing_unit = True
                                    subscription_data1.company_id = company_ids
                                    subscription_data1.save()
                                
                                elif panelid:

                                    device_data = Device()
                                    device_data.serial_no1 = device_id
                                    device_data.serial_no2 = panelid
                                    device_data.serial_no3 = atmid
                                    device_data.site_id = site_ids
                                    device_data.save()

                                    site_data = Site.objects.get(id=site_ids)
                                    site_data.is_treatment_unit = True
                                    site_data.token_verified = True
                                    site_data.token = None
                                    site_data.save()

                                    subscription_data = Subscription()
                                    subscription_data.site_id = site_ids
                                    subscription_data.is_treatment_unit = True
                                    subscription_data.company_id = company_ids
                                    subscription_data.save()

                                elif atmid:
                                    try:
                                        device_data = Device()
                                        device_data.serial_no1 = device_id
                                        device_data.serial_no2 = panelid
                                        device_data.serial_no3 = atmid
                                        device_data.site_id = site_ids
                                        device_data.save()
                                    except DatabaseError as e:
                                        print("DatabaseError at line 283")

                                    site_data = Site.objects.get(id=site_ids)
                                    site_data.is_dispensing_unit = True
                                    site_data.token_verified = True
                                    site_data.token = None
                                    site_data.save()

                                    subscription_data = Subscription()
                                    subscription_data.site_id = site_ids
                                    subscription_data.is_dispensing_unit = True
                                    subscription_data.company_id = company_ids
                                    subscription_data.save()
                        
                        except Exception as err:
                            transaction.set_rollback(True)
                            logger.error("Exception at line 302".format(err))


    def ctrl_motr_handler(self, client, userdata, msg):
        print("I am in ctrl_motr_handler")
        topic_from_broker =msg.topic

        if topic_from_broker != "wc1/v1/OTP":
            # global msgo
            jstring=msg.payload
            if isinstance(jstring, bytes):
                dict_str = jstring.decode("utf-8")
            if dict_str.startswith("{'") and dict_str.endswith("'}") or 'version' not in dict_str:
                dict_split=dict_str.split(":")

                dict_data = ast.literal_eval(dict_str)
                converted_list = [f"{key}:{value}" for key, value in dict_data.items()]
                array_dat =converted_list
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
                tmp=None
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
                        if removed_col[1].isdigit():
                            spn=int(removed_col[1])
                    elif removed_col[0]=='tds':
                        if removed_col[1].isdigit():
                            tds=int(removed_col[1])
                    elif removed_col[0]=='tsp':
                        if removed_col[1].isdigit():
                            tsp=int(removed_col[1])
                    elif removed_col[0]=='asp':
                        if removed_col[1].isdigit():
                            asp=int(removed_col[1])
                    elif removed_col[0]=='sts':
                        sts=removed_col[1]
                    elif removed_col[0]=='crt':
                        if removed_col[1].isdigit():
                            crt=removed_col[1]
                    elif removed_col[0]=='olc':
                        if removed_col[1].isdigit():
                            olc=removed_col[1]
                    elif removed_col[0]=='drc':
                        if removed_col[1].isdigit():
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
                        if removed_col[1].isdigit():
                            ipv=removed_col[1]
                    elif removed_col[0]=='unv':
                        if removed_col[1].isdigit():
                            unv=removed_col[1]
                    elif removed_col[0]=='ovv':
                        if removed_col[1].isdigit():
                            ovv=removed_col[1]
                    elif removed_col[0]=='nmv':
                        if removed_col[1].isdigit():
                            nmv=removed_col[1]
                    elif removed_col[0]=='stp':
                        stp=removed_col[1]
                    elif removed_col[0]=='bkt':
                        if removed_col[1].isdigit():
                            bkt=removed_col[1]
                    elif removed_col[0]=='rst':
                        if removed_col[1].isdigit():
                            rst=removed_col[1]
                    elif removed_col[0]=='err':
                        err=removed_col[1]
                    elif removed_col[0]=='fr1':
                        if removed_col[1].isdigit():
                            fr1=removed_col[1]
                    elif removed_col[0]=='fr2':
                        if removed_col[1].isdigit():
                            fr2=removed_col[1]
                    elif removed_col[0]=='ff1':
                        if removed_col[1].isdigit():
                            ff1=removed_col[1]
                    elif removed_col[0]=='ff2':
                        if removed_col[1].isdigit():
                            ff2=removed_col[1]
                    elif removed_col[0]=='pos':
                        pos=removed_col[1]
                    elif removed_col[0]=='rmt':
                        if removed_col[1].isdigit():
                            rmt=removed_col[1]
                    elif removed_col[0]=='cct':
                        if removed_col[1].isdigit():
                            cct=removed_col[1]
                    elif removed_col[0]=='srt':
                        if removed_col[1].isdigit():
                            srt=removed_col[1]
                    elif removed_col[0]=='bkt':
                        if removed_col[1].isdigit():
                            bkt=removed_col[1]
                    elif removed_col[0]=='mot':
                        if removed_col[1].isdigit():
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
                        if removed_col[1].isdigit():
                            ndv=removed_col[1]
                    elif removed_col[0]=='ntt':
                        ntt=removed_col[1]
                    elif removed_col[0]=='nta':
                        if removed_col[1].isdigit():
                            nta=removed_col[1]
                    elif removed_col[0]=='tmp':
                        if removed_col[1].isdigit():
                            tmp=removed_col[1]
                        else:
                            tmp=None
                    elif removed_col[0]=='ntp':
                        ntp=removed_col[1]
                    elif removed_col[0]=='nov':
                        nov=removed_col[1]
                    elif removed_col[0]=='vl1':
                        if removed_col[1].isdigit():
                            vl1=removed_col[1]
                    elif removed_col[0]=='vl2':
                        if removed_col[1].isdigit():
                            vl2=removed_col[1]
                    elif removed_col[0]=='vl3':
                        if removed_col[1].isdigit():
                            vl3=removed_col[1]
                    elif removed_col[0]=='vl4':
                        if removed_col[1].isdigit():
                            vl4=removed_col[1]
                    elif removed_col[0]=='re1':
                        if removed_col[1].isdigit():
                            re1=removed_col[1]
                    elif removed_col[0]=='re2':
                        if removed_col[1].isdigit():
                            re2=removed_col[1]
                    elif removed_col[0]=='re3':
                        if removed_col[1].isdigit():
                            re3=removed_col[1]
                    elif removed_col[0]=='re4':
                        if removed_col[1].isdigit():
                            re4=removed_col[1]
                    elif removed_col[0]=='p1':
                        if removed_col[1].isdigit():
                            p1=removed_col[1]
                    elif removed_col[0]=='p2':
                        if removed_col[1].isdigit():
                            p2=removed_col[1]
                    elif removed_col[0]=='p3':
                        if removed_col[1].isdigit():
                            p3=removed_col[1]
                    elif removed_col[0]=='p4':
                        if removed_col[1].isdigit():
                            p4=removed_col[1]
                    elif removed_col[0]=='fr':
                        if removed_col[1].isdigit():
                            fr=removed_col[1]
                    elif removed_col[0]=='whr':
                        if removed_col[1].isdigit():
                            whr=removed_col[1]
                    elif removed_col[0]=='custid':
                        custid=removed_col[1]   
                mydata1=mydata      
                mydata = json.dumps(mydata, indent = 4) 
                mydatadict=json.loads(mydata)       
                hmq=msg.topic
                hmqm_split=hmq.split('/')      
                device_id=hmqm_split[1]
                msg_type=hmqm_split[2]
                if(msg_type == 'updset' or msg_type == 'updsta'):
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
                            erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='cnd_sen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
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
                            erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='tds_sen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
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
                            erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='rwp',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                    try:
                        if 'hpp'==components:
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
                            erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='hpp',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                    try:
                        if 'panel'==components:
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
                            erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='panel',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()    
                    try:
                        if 'ampv1'==components:
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
                            erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='ampv1',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                    try:
                        if 'ampv2'==components:
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
                            erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='ampv2',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                    try:
                        if 'ampv3'==components:
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
                            erro=Errors.objects.create(device_id=device_id,message_type=msg_type,e_discriptions=e,o_message=dict_str,service='ampv3',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                            erro.save()
                    try:        
                        if 'ampv4'==components:
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
                    try:       
                        if 'ampv5'==components:
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
                    try:
                        if 'atm'==components:
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
                    try:
                        if 'cnd_consen'==components:
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
                    try:
                        if 'tds_consen'==components:
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
                    try:
                        if 'F_flowsen'==components:
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
                    try:
                        if 'P_flowsen'==components:
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
                    try:
                        if 'tap1'==components:
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
                    try:
                        if 'tap2'==components:
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
                    try:
                        if 'tap3'==components:
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
                    try:
                        if 'tap4'==components:
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
                    try:
                        if 'flowsen1'==components:
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
                    try:

                        if 'flowsen2'==components:
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
                    try:
                        if 'flowsen3'==components:
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

    def on_connect_1(self, client, userdata, flags, rc):
        #logger.info("MQTT - connected")
        # self.subscribe(self.topic)
        self.subscribe("wc1/#",self.ctrl_motr_handler)
        self.subscribe("wc1/v1/OTP",self.otp_handler)


        
        
        

    def subscribe(self, topic,subscribe_callback):
        self.client.subscribe(topic,1)
        self.client.message_callback_add(topic, subscribe_callback)

    def publish(self, topic, payload):
        self.client.publish(topic, payload=payload)

    def stop(self):
        self.client.disconnect()

try:
    mqttc = MqttClient()
    print("MqttClient object created from views in connection app")
except Exception as e:
    print(" error in connection views while creating mqtt object ",e)


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
class LastRecordsView(viewsets.ModelViewSet):
    def dispatch(self, request, *args, **kwargs):
        my_list = [] 
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list=list(data.values())
        dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()

        if dinfo is not None:
            did=dinfo.Device_id
            last_error = Errors.objects.filter(device_id=did).order_by('-id')[:10]
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
            return JsonResponse(last_error, safe=False, content_type="application/json")
        else:
            response_data = {
                #new code
            'data': "",  # Include the 'data' field
            'status': 500,  # Add the status field
            'message': "Unable to find data", # Add the message field
            
            }
            response_data=[response_data]
            return JsonResponse(response_data, safe=False, content_type="application/json")

#all data from minit table
class all_panelListAPIView(generics.ListAPIView):
	queryset = treat_panel.objects.all()
	serializer_class = all_panelSerializer
class all_cndListAPIView(generics.ListAPIView):
	queryset = treat_cnd_sen.objects.all()
	serializer_class = all_cndSerializer
class all_tdsListAPIView(generics.ListAPIView):
	queryset = treat_tds_sen.objects.all()
	serializer_class = all_tdsSerializer
class all_rwpListAPIView(generics.ListAPIView):
    
	queryset = treat_rwp.objects.all()
	
	serializer_class = all_rwpSerializer
class all_ampv1ListAPIView(generics.ListAPIView):
    
	queryset = treat_ampv1.objects.all()
	
	serializer_class = all_ampv1Serializer  
class all_ampv2ListAPIView(generics.ListAPIView):
    
	queryset = treat_ampv2.objects.all()
	
	serializer_class = all_ampv2Serializer       
class all_ampv3ListAPIView(generics.ListAPIView):
    
	queryset = treat_ampv3.objects.all()
	
	serializer_class = all_ampv3Serializer
class all_ampv4ListAPIView(generics.ListAPIView):
    
	queryset = treat_ampv4.objects.all()
	
	serializer_class = all_ampv4Serializer
class all_ampv5ListAPIView(generics.ListAPIView):
    
	queryset = treat_ampv5.objects.all()
	
	serializer_class = all_ampv5Serializer
class all_hppListAPIView(generics.ListAPIView):
    
	queryset = treat_hpp.objects.all()
	
	serializer_class = all_hppSerializer
class all_F_flowsenListAPIView(generics.ListAPIView):
    
	queryset = treat_F_flowsen.objects.all()
	
	serializer_class = all_F_flowsenSerializer
class all_P_flowsenListAPIView(generics.ListAPIView):
    
	queryset = treat_P_flowsen.objects.all()
	
	serializer_class = all_P_flowsenSerializer
class all_cnd_consenListAPIView(generics.ListAPIView):
    
	queryset = disp_cnd_consen.objects.all()
	
	serializer_class = all_cnd_consenSerializer
class all_tds_consenListAPIView(generics.ListAPIView):
    
	queryset = disp_tds_consen.objects.all()
	
	serializer_class = all_tds_consenSerializer
class all_atmListAPIView(generics.ListAPIView):
    
	queryset = disp_atm.objects.all()
	
	serializer_class = all_atmSerializer
class all_tap1ListAPIView(generics.ListAPIView):
    
	queryset = disp_tap1.objects.all()
	
	serializer_class = all_tap1Serializer
class all_tap2ListAPIView(generics.ListAPIView):
    
	queryset = disp_tap2.objects.all()
	
	serializer_class = all_tap2Serializer
class all_tap3ListAPIView(generics.ListAPIView):
    
	queryset = disp_tap3.objects.all()
	
	serializer_class = all_tap3Serializer
class all_tap4ListAPIView(generics.ListAPIView):
    
	queryset = disp_tap4.objects.all()
	
	serializer_class = all_tap4Serializer
class all_flowsen1ListAPIView(generics.ListAPIView):
    
	queryset = disp_flowsen1.objects.all()
	
	serializer_class = all_flowsen1Serializer
class all_flowsen2ListAPIView(generics.ListAPIView):
    
	queryset = disp_flowsen2.objects.all()
	
	serializer_class = all_flowsen2Serializer
class all_flowsen3ListAPIView(generics.ListAPIView):
    
	queryset = disp_flowsen3.objects.all()
	
	serializer_class = all_flowsen3Serializer
class all_flowsen4ListAPIView(generics.ListAPIView):
    
	queryset = disp_flowsen4.objects.all()
	
	serializer_class = all_flowsen4Serializer
import json
cid=None
class site_check(viewsets.ModelViewSet):
    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         fields_to_exclude = ['model', 'pk']
    #         #print(request.body,"BODY")
    #         data = json.loads(request.body)
    #         #print(data,type(data),"DATA")
    #         # companydata=mo.Company.objects.filter(company_id=data['company_id'])
    #         # for i in companydata:
    #         #     global cid
    #         #     cid=i.id

    #         logged_user = User.objects.get(request.user.id)
    #         role = ""
    #         if logged_user.is_super_admin or logged_user.is_admin:
    #                 number_of_sites=mo.Site.objects.filter(company=request.user.company_id).filter(phone_verified=1,token_verified=1).order_by('-id')
    #                 site_name=[]
    #                 for sit in number_of_sites:
    #                     site_name.append(sit.site_name)
    #         else:
    #             valid_sites_for_user = mo.SitePermission.objects.filter(user_id=request.user.id)
    #             number_of_sites=mo.Site.objects.filter(id__in=valid_sites_for_user.values_list('site_id', flat=True)).filter(phone_verified=1,token_verified=1).order_by('-id')
    #             site_name=[]
    #             for sit in number_of_sites:
    #                 site_name.append(sit.site_name)
        
    #         response_data = {
    #             #new code
    #         'data': site_name,  # Include the 'data' field
    #         'status': 200,  # Add the status field
    #         'message': "Data get successful", # Add the message field
            
    #         }
    #         response_data=[response_data]
    #         return JsonResponse(response_data, safe=False, content_type="application/json")

    #     except Exception as e :
    #         print("Exception at line site_check ",e)  



    def dispatch(self, request, *args, **kwargs):
        fields_to_exclude = ['model', 'pk']
        #print(request.body,"BODY")
        data = json.loads(request.body)
        #print(data,type(data),"DATA")
        companydata=mo.Company.objects.filter(company_id=request.user.company_id)
        for i in companydata:
            # global cid
            cid=i.id
        number_of_sites=mo.Site.objects.filter(company_id=request.user.company_id)
        site_name=[]
        for sit in number_of_sites:
            site_name.append(sit.site_name)
        response_data = {
            #new code
        'data': site_name,  # Include the 'data' field
        'status': 200,  # Add the status field
        'message': "Data get successful", # Add the message field
        
        }
        response_data=[response_data]
        return JsonResponse(response_data, safe=False, content_type="application/json")

# class updated_treat_rwpViewset(viewsets.ModelViewSet):
#     def dispatch(self, request, *args, **kwargs):
#         try:
#             fields_to_exclude = ['model', 'pk']
#             data = json.loads(request.body)
#             value_list=list(data.values())
#             dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
#             if dinfo is not None:
#                 did=dinfo.Device_id
#                 qs_sta = treat_rwp.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
#                 if not qs_sta:
#                     data_sta = {}
#                 else:
#                     data_sta = serialize("json", qs_sta)
#                     data_sta = json.loads(data_sta)
#                     for item in data_sta:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
#                     data_sta = json.dumps(data_sta[0]["fields"])
#                     data_sta = json.loads(data_sta)
                
#                 qs_set = treat_rwp.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
#                 if not qs_set:
#                     data_set = {}
#                 else:
#                     data_set = serialize("json", qs_set)
#                     data_set = json.loads(data_set)
#                     for item in data_set:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

#                     data_set = json.dumps(data_set[0]["fields"])
#                     data_set = json.loads(data_set)

#                 last_error=Errors.objects.filter(service='rwp')
#                 if not last_error:
#                     last_error={}
#                 else:
#                     last_error = serialize("json", last_error)
#                     last_error = json.loads(last_error)
#                     for item in last_error:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
                    
#                     last_error = json.dumps(last_error[0]["fields"])
#                     last_error = json.loads(last_error)

#                 data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
#                 response_data = {
#                     #new code
#                 'data': data_final,  # Include the 'data' field
#                 'status': 200,  # Add the status field
#                 'message': "Data get successful", # Add the message field
                
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json")
#             else:
#                 response_data = {
#                     #new code
#                 'data': "",  # Include the 'data' field
#                 'status': 500,  # Add the status field
#                 'message': "Unable to update", # Add the message field
                
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json")

#         except Exception as e :
#             print("Exception at line 5168",e)  
    
# class updated_treat_cnd_senViewset(viewsets.ModelViewSet):
	
#     def dispatch(self, request, *args, **kwargs):
#         try:
#             fields_to_exclude = ['model', 'pk']
#             data = json.loads(request.body)
#             value_list=list(data.values())

#             dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()

#             if dinfo is not None:
#                 did=dinfo.Device_id

#                 qs_sta = treat_cnd_sen.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
#                 if not qs_sta:
#                     data_sta = {}
#                 else:
#                     data_sta = serialize("json", qs_sta)
#                     data_sta = json.loads(data_sta)
#                     for item in data_sta:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
#                     data_sta = json.dumps(data_sta[0]["fields"])
#                     data_sta = json.loads(data_sta)
                
#                 qs_set = treat_cnd_sen.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
#                 if not qs_set:
#                     data_set = {}
#                 else:
#                     data_set = serialize("json", qs_set)
#                     data_set = json.loads(data_set)
#                     for item in data_set:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

#                     data_set = json.dumps(data_set[0]["fields"])
#                     data_set = json.loads(data_set)

#                 last_error=Errors.objects.filter(service='cnd_sen')
#                 if not last_error:
#                     last_error={}
#                 else:
#                     last_error = serialize("json", last_error)
#                     last_error = json.loads(last_error)
#                     for item in last_error:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
                    
#                     last_error = json.dumps(last_error[0]["fields"])
#                     last_error = json.loads(last_error)

#                 data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
#                 response_data = {
#                     #new code
#                 'data': data_final,  # Include the 'data' field
#                 'status': 200,  # Add the status field
#                 'message': "Data get successful", # Add the message field
                
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json")   
#             else:
#                 response_data = {
#                     #new code
#                 'data': "",  # Include the 'data' field
#                 'status': 500,  # Add the status field
#                 'message': "Unable to update data", # Add the message field
                
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json")

#         except Exception as e :
#             print("Exception at line 5236",e)  
        
# class updated_treat_tds_senViewset(viewsets.ModelViewSet):
	
#     def dispatch(self, request, *args, **kwargs):
#         try:
#             fields_to_exclude = ['model', 'pk']
#             data = json.loads(request.body)
#             value_list=list(data.values())
#             dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
#             if dinfo is not None:
#                 did=dinfo.Device_id
#                 qs_sta = treat_tds_sen.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
#                 if not qs_sta:
#                     data_sta = {}
#                 else:
#                     data_sta = serialize("json", qs_sta)
#                     data_sta = json.loads(data_sta)
#                     for item in data_sta:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
#                     data_sta = json.dumps(data_sta[0]["fields"])
#                     data_sta = json.loads(data_sta)
                
#                 qs_set = treat_tds_sen.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
#                 if not qs_set:
#                     data_set = {}
#                 else:
#                     data_set = serialize("json", qs_set)
#                     data_set = json.loads(data_set)
#                     for item in data_set:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

#                     data_set = json.dumps(data_set[0]["fields"])
#                     data_set = json.loads(data_set)

#                 last_error=Errors.objects.filter(service='tds_sen')
#                 if not last_error:
#                     last_error={}
#                 else:
#                     last_error = serialize("json", last_error)
#                     last_error = json.loads(last_error)
#                     for item in last_error:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
                    
#                     last_error = json.dumps(last_error[0]["fields"])
#                     last_error = json.loads(last_error)

#                 data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
#                 response_data = {
#                     #new code
#                 'data': data_final,  # Include the 'data' field
#                 'status': 200,  # Add the status field
#                 'message': "Data get successful", # Add the message field
                
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json")    
#             else:
#                 response_data = {
#                     #new code
#                 'data': "",  # Include the 'data' field
#                 'status': 500,  # Add the status field
#                 'message': "Unable to update", # Add the message field
                
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json")
#         except Exception as e :
#             print("Exception at line 5304",e)  

# class updated_treat_hppViewset(viewsets.ModelViewSet):
	
#     def dispatch(self, request, *args, **kwargs):
#         try:
#             fields_to_exclude = ['model', 'pk']
#             data = json.loads(request.body)
#             value_list=list(data.values())
#             dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
#             if dinfo is not None:
#                 did=dinfo.Device_id
#                 qs_sta = treat_hpp.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
#                 if not qs_sta:
#                     data_sta = {}
#                 else:
#                     data_sta = serialize("json", qs_sta)
#                     data_sta = json.loads(data_sta)
#                     for item in data_sta:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
#                     data_sta = json.dumps(data_sta[0]["fields"])
#                     data_sta = json.loads(data_sta)
                
#                 qs_set = treat_hpp.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
#                 if not qs_set:
#                     data_set = {}
#                 else:
#                     data_set = serialize("json", qs_set)
#                     data_set = json.loads(data_set)
#                     for item in data_set:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

#                     data_set = json.dumps(data_set[0]["fields"])
#                     data_set = json.loads(data_set)

#                 last_error=Errors.objects.filter(service='hpp')
#                 if not last_error:
#                     last_error={}
#                 else:
#                     last_error = serialize("json", last_error)
#                     last_error = json.loads(last_error)
#                     for item in last_error:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
                    
#                     last_error = json.dumps(last_error[0]["fields"])
#                     last_error = json.loads(last_error)

#                 data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
#                 response_data = {
#                     #new code
#                 'data': data_final,  # Include the 'data' field
#                 'status': 200,  # Add the status field
#                 'message': "Data get successful", # Add the message field
                
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json")    
#             else:
#                     response_data = {
#                         #new code
#                     'data': "",  # Include the 'data' field
#                     'status': 500,  # Add the status field
#                     'message': "Unable to update", # Add the message field
                    
#                     }
#                     response_data=[response_data]
#                     return JsonResponse(response_data, safe=False, content_type="application/json")
#         except Exception as e :
#             print("Exception at line 5365 updated_treat_hppViewset",e)  

# class updated_treat_ampv1Viewset(viewsets.ModelViewSet):

#     def dispatch(self, request, *args, **kwargs):
#         try:
#             fields_to_exclude = ['model', 'pk']
#             data = json.loads(request.body)
#             value_list=list(data.values())
#             dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
#             if dinfo is not None:
#                 did=dinfo.Device_id
#                 qs_sta = treat_ampv1.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
#                 if not qs_sta:
#                     data_sta = {}
#                 else:
#                     data_sta = serialize("json", qs_sta)
#                     data_sta = json.loads(data_sta)

#                     for item in data_sta:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
#                     data_sta = json.dumps(data_sta[0]["fields"])
#                     data_sta = json.loads(data_sta)
                
#                 qs_set = treat_ampv1.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
#                 if not qs_set:
#                     data_set = {}
#                 else:
#                     data_set = serialize("json", qs_set)
#                     data_set = json.loads(data_set)

#                     for item in data_set:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

#                     data_set = json.dumps(data_set[0]["fields"])
#                     data_set = json.loads(data_set)


#                 last_error=Errors.objects.filter(service='ampv1')
#                 if not last_error:
#                     last_error={}
#                 else:
#                     last_error = serialize("json", last_error)
#                     last_error = json.loads(last_error)
#                     for item in last_error:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
                    
#                     last_error = json.dumps(last_error[0]["fields"])
#                     last_error = json.loads(last_error)

#                 data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
#                 response_data = {
#                     #new code
#                 'data': data_final,  # Include the 'data' field
#                 'status': 200,  # Add the status field
#                 'message': "Data get successful", # Add the message field
                
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json")    
#             else:
#                 response_data = {
#                     #new code
#                 'data': "",  # Include the 'data' field
#                 'status': 500,  # Add the status field
#                 'message': "Unable to update", # Add the message field
                
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json")
#         except Exception as e :
#             print("Exception at line 5447 updated_treat_ampv1Viewset",e)  

# class updated_treat_ampv2Viewset(viewsets.ModelViewSet):
	
#     def dispatch(self, request, *args, **kwargs):
#         try:
#             fields_to_exclude = ['model', 'pk']
#             data = json.loads(request.body)
#             value_list=list(data.values())
#             dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
#             if dinfo is not None:
#                 did=dinfo.Device_id
#                 qs_sta = treat_ampv2.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
#                 if not qs_sta:
#                     data_sta = {}
#                 else:
#                     data_sta = serialize("json", qs_sta)
#                     data_sta = json.loads(data_sta)
#                     for item in data_sta:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
#                     data_sta = json.dumps(data_sta[0]["fields"])
#                     data_sta = json.loads(data_sta)
                
#                 qs_set = treat_ampv2.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
#                 if not qs_set:
#                     data_set = {}
#                 else:
#                     data_set = serialize("json", qs_set)
#                     data_set = json.loads(data_set)
#                     for item in data_set:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

#                     data_set = json.dumps(data_set[0]["fields"])
#                     data_set = json.loads(data_set)

#                 last_error=Errors.objects.filter(service='ampv2')
#                 if not last_error:
#                     last_error={}
#                 else:
#                     last_error = serialize("json", last_error)
#                     last_error = json.loads(last_error)
#                     for item in last_error:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
                    
#                     last_error = json.dumps(last_error[0]["fields"])
#                     last_error = json.loads(last_error)

#                 data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
#                 response_data = {
#                     #new code
#                 'data': data_final,  # Include the 'data' field
#                 'status': 200,  # Add the status field
#                 'message': "Data get successful", # Add the message field
                
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json")
#             else:
#                 response_data = {
#                     #new code
#                 'data': "",  # Include the 'data' field
#                 'status': 500,  # Add the status field
#                 'message': "Unable to update", # Add the message field
                
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json")
#         except Exception as e :
#             print("Exception at line 5515 updated_treat_ampv2Viewset",e)  
    
# class updated_treat_panelViewset(viewsets.ModelViewSet):
	
#     def dispatch(self, request, *args, **kwargs):
#         try:
#             fields_to_exclude = ['model', 'pk']
#             data = json.loads(request.body)
#             value_list=list(data.values())
#             dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
#             if dinfo is not None:
#                 did=dinfo.Device_id
#                 qs_sta = treat_panel.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
#                 if not qs_sta:
#                     data_sta = {}
#                 else:
#                     data_sta = serialize("json", qs_sta)
#                     data_sta = json.loads(data_sta)
#                     for item in data_sta:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
#                     data_sta = json.dumps(data_sta[0]["fields"])
#                     data_sta = json.loads(data_sta)
                
#                 qs_set = treat_panel.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
#                 if not qs_set:
#                     data_set = {}
#                 else:
#                     data_set = serialize("json", qs_set)
#                     data_set = json.loads(data_set)
#                     for item in data_set:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

#                     data_set = json.dumps(data_set[0]["fields"])
#                     data_set = json.loads(data_set)

#                 last_error=Errors.objects.filter(service='panel')
#                 if not last_error:
#                     last_error={}
#                 else:
#                     last_error = serialize("json", last_error)
#                     last_error = json.loads(last_error)
#                     for item in last_error:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
                    
#                     last_error = json.dumps(last_error[0]["fields"])
#                     last_error = json.loads(last_error)

#                 data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
#                 response_data = {
#                     #new code
#                 'data': data_final,  # Include the 'data' field
#                 'status': 200,  # Add the status field
#                 'message': "Data get successful", # Add the message field
                
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json") 
#             else:
#                     response_data = {
#                         #new code
#                     'data': "",  # Include the 'data' field
#                     'status': 500,  # Add the status field
#                     'message': "Unable to update", # Add the message field
                    
#                     }
#                     response_data=[response_data]
#                     return JsonResponse(response_data, safe=False, content_type="application/json")
#         except Exception as e :
#             print("Exception at line 5583 updated_treat_panelViewset",e)    

class updated_disp_atmViewset(viewsets.ModelViewSet):
    def dispatch(self, request, *args, **kwargs):
        try:
            fields_to_exclude = ['model', 'pk']
            data = json.loads(request.body)
            value_list=list(data.values())
            dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
            if dinfo is not None:
                did=dinfo.Device_id
                qs_sta = disp_atm.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
                last_error=Errors.objects.filter(service='atm')
                if not qs_sta:
                    data_sta = {}
                else:
                    data_sta = serialize("json", qs_sta)
                    data_sta = json.loads(data_sta)
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
                    for item in data_set:
                        item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

                    data_set = json.dumps(data_set[0]["fields"])
                    data_set = json.loads(data_set)

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
                
                }
                response_data=[response_data]
                return JsonResponse(response_data, safe=False, content_type="application/json")    
            else:
                    response_data = {
                        #new code
                    'data': "",  # Include the 'data' field
                    'status': 500,  # Add the status field
                    'message': "Unable to update", # Add the message field
                    
                    }
                    response_data=[response_data]
                    return JsonResponse(response_data, safe=False, content_type="application/json")
        except Exception as e :
            print("Exception at line 5652 updated_disp_atmViewset",e) 
        
# class getDeviceID(viewsets.ModelViewSet):
# 	
#     def dispatch(self, request, *args, **kwargs):
#         try:
#             did = 0
#             data_dict = json.loads(request.body)
#             value_list = list(data_dict.values())
#             dinfo = device_info.objects.filter(componant_name=value_list[2], unit_type=value_list[1], company_id=value_list[0])
#             # #print("value_list",dinfo)
#             # data = serialize("json", dinfo, fields=('Device_id'))
#             # return HttpResponse(data, content_type="application/json")

#             fields_to_exclude = ['model', 'pk']
                
#             data = serialize("json", dinfo)
#             data = json.loads(data)
            
#             for item in data:
#                 item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            
            
#             if not data:
#                 response_data = {
#                     'data': [],  # Include the 'data' field
#                     'status': 200,  # Add the status field
#                     'message': "Data not found"  # Add the message field
#                 }
#             else:     
#                 data = json.dumps(data[0]["fields"])
#                 data = json.loads(data)
#                 data = [data]
#                 response_data = {
#                     'data': data[0],  # Include the 'data' field
#                     'status': 200,  # Add the status field
#                     'message': "Data get successfully"  # Add the message field
#                 }
#             response_data=[response_data]
#         except Exception as e:
#                     response_data = {
#                         'data':e,  # Include the 'data' field
#                         'status': 200,  # Add the status field
#                         'message': "Exception found"  # Add the message field
#                     }
        
#         return JsonResponse(response_data, safe=False, content_type="application/json")


class updated_disp_tap1Viewset(viewsets.ModelViewSet):
	
    def dispatch(self, request, *args, **kwargs):
        try:
            fields_to_exclude = ['model', 'pk']
            data = json.loads(request.body)
            value_list=list(data.values())
            dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
            if dinfo is not None:
                did=dinfo.Device_id
                qs_sta = disp_tap1.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
                if not qs_sta:
                    data_sta = {}
                else:
                    data_sta = serialize("json", qs_sta)
                    data_sta = json.loads(data_sta)
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
                    for item in data_set:
                        item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

                    data_set = json.dumps(data_set[0]["fields"])
                    data_set = json.loads(data_set)

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
                
                }
                response_data=[response_data]
                return JsonResponse(response_data, safe=False, content_type="application/json")    
            else:
                response_data = {
                    #new code
                'data': "",  # Include the 'data' field
                'status': 500,  # Add the status field
                'message': "Unable to update", # Add the message field
                
                }
                response_data=[response_data]
                return JsonResponse(response_data, safe=False, content_type="application/json")
        except Exception as e :
            print("Exception at line 5767 updated_disp_tap1Viewset",e) 

class updated_disp_tap2Viewset(viewsets.ModelViewSet):
	
    def dispatch(self, request, *args, **kwargs):
        try:
            fields_to_exclude = ['model', 'pk']
            data = json.loads(request.body)
            value_list=list(data.values())
            dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
            if dinfo is not None:
                did=dinfo.Device_id
                qs_sta = disp_tap2.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
                if not qs_sta:
                    data_sta = {}
                else:
                    data_sta = serialize("json", qs_sta)
                    data_sta = json.loads(data_sta)
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
                    for item in data_set:
                        item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

                    data_set = json.dumps(data_set[0]["fields"])
                    data_set = json.loads(data_set)

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
                
                }
                response_data=[response_data]
                return JsonResponse(response_data, safe=False, content_type="application/json")    
            else:
                response_data = {
                    #new code
                'data': "",  # Include the 'data' field
                'status': 500,  # Add the status field
                'message': "Unable to update", # Add the message field
                
                }
                response_data=[response_data]
                return JsonResponse(response_data, safe=False, content_type="application/json")
        except Exception as e:
            print("Exception at line 5834 updated_disp_tap2Viewset",e) 


# class updated_disp_tap3Viewset(viewsets.ModelViewSet):
	
#     def dispatch(self, request, *args, **kwargs):
#         try:
#             fields_to_exclude = ['model', 'pk']
#             data = json.loads(request.body)
#             value_list=list(data.values())

#             dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
#             if dinfo is not None:
#                 did=dinfo.Device_id
#                 qs_sta = disp_tap3.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
#                 if not qs_sta:
#                     data_sta = {}
#                 else:
#                     data_sta = serialize("json", qs_sta)
#                     data_sta = json.loads(data_sta)
#                     for item in data_sta:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
#                     data_sta = json.dumps(data_sta[0]["fields"])
#                     data_sta = json.loads(data_sta)
                
#                 qs_set = disp_tap3.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
#                 if not qs_set:
#                     data_set = {}
#                 else:
#                     data_set = serialize("json", qs_set)
#                     data_set = json.loads(data_set)
#                     for item in data_set:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

#                     data_set = json.dumps(data_set[0]["fields"])
#                     data_set = json.loads(data_set)

#                 last_error=Errors.objects.filter(service='tap3')
#                 if not last_error:
#                     last_error={}
#                 else:
#                     last_error = serialize("json", last_error)
#                     last_error = json.loads(last_error)
#                     for item in last_error:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
                    
#                     last_error = json.dumps(last_error[0]["fields"])
#                     last_error = json.loads(last_error)

#                 data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
#                 response_data = {
#                     #new code
#                 'data': data_final,  # Include the 'data' field
#                 'status': 200,  # Add the status field
#                 'message': "Data get successful", # Add the message field
                
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json")    
#             else:
#                 response_data = {
#                     #new code
#                 'data': "",  # Include the 'data' field
#                 'status': 500,  # Add the status field
#                 'message': "Unable to update", # Add the message field
                
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json")
#         except Exception as e :
#             print("Exception at line 5902 updated_disp_tap3Viewset",e) 



# class updated_disp_tap4Viewset(viewsets.ModelViewSet):
	
#     def dispatch(self, request, *args, **kwargs):
#         try:
#             fields_to_exclude = ['model', 'pk']
#             data = json.loads(request.body)
#             value_list=list(data.values())
#             dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
#             if dinfo is not None:
#                 did=dinfo.Device_id
#                 qs_sta = disp_tap4.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
#                 if not qs_sta:
#                     data_sta = {}
#                 else:
#                     data_sta = serialize("json", qs_sta)
#                     data_sta = json.loads(data_sta)
#                     for item in data_sta:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
#                     data_sta = json.dumps(data_sta[0]["fields"])
#                     data_sta = json.loads(data_sta)
#                 qs_set = disp_tap4.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
#                 if not qs_set:
#                     data_set = {}
#                 else:
#                     data_set = serialize("json", qs_set)
#                     data_set = json.loads(data_set)
#                     for item in data_set:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

#                     data_set = json.dumps(data_set[0]["fields"])
#                     data_set = json.loads(data_set)

#                 last_error=Errors.objects.filter(service='tap4')
#                 if not last_error:
#                     last_error={}
#                 else:
#                     last_error = serialize("json", last_error)
#                     last_error = json.loads(last_error)
#                     for item in last_error:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
                    
#                     last_error = json.dumps(last_error[0]["fields"])
#                     last_error = json.loads(last_error)

#                 data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
#                 response_data = {
#                     #new code
#                 'data': data_final,  # Include the 'data' field
#                 'status': 200,  # Add the status field
#                 'message': "Data get successful", # Add the message field
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json")    
#             else:
#                 response_data = {
#                     #new code
#                 'data': "",  # Include the 'data' field
#                 'status': 500,  # Add the status field
#                 'message': "Unable to update", # Add the message field
                
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json")
#         except Exception as e :
#             print("Exception at line 5968 updated_disp_tap4Viewset",e) 


                
# class updated_disp_cnd_consenViewset(viewsets.ModelViewSet):
	 
#     def dispatch(self, request, *args, **kwargs):
#         try:
#             fields_to_exclude = ['model', 'pk']
#             data = json.loads(request.body)
#             value_list=list(data.values())

#             dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
#             if dinfo is not None:
#                 did=dinfo.Device_id
#                 qs_sta = disp_cnd_consen.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
#                 if not qs_sta:
#                     data_sta = {}
#                 else:
#                     data_sta = serialize("json", qs_sta)
#                     data_sta = json.loads(data_sta)
#                     for item in data_sta:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
#                     data_sta = json.dumps(data_sta[0]["fields"])
#                     data_sta = json.loads(data_sta)
                
#                 qs_set = disp_cnd_consen.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
#                 if not qs_set:
#                     data_set = {}
#                 else:
#                     data_set = serialize("json", qs_set)
#                     data_set = json.loads(data_set)
#                     for item in data_set:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

#                     data_set = json.dumps(data_set[0]["fields"])
#                     data_set = json.loads(data_set)

#                 last_error=Errors.objects.filter(service='cnd_consen')
#                 if not last_error:
#                     last_error={}
#                 else:
#                     last_error = serialize("json", last_error)
#                     last_error = json.loads(last_error)
#                     for item in last_error:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
                    
#                     last_error = json.dumps(last_error[0]["fields"])
#                     last_error = json.loads(last_error)

#                 data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
#                 response_data = {
#                     #new code
#                 'data': data_final,  # Include the 'data' field
#                 'status': 200,  # Add the status field
#                 'message': "Data get successful", # Add the message field
                
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json")  

#             else:
#                 response_data = {
#                     #new code
#                 'data': "",  # Include the 'data' field
#                 'status': 500,  # Add the status field
#                 'message': "Unable to update", # Add the message field
                
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json")
#         except Exception as e :
#             print("Exception at line 6038 updated_disp_cnd_consenViewset",e)  
        
# class updated_disp_tds_consenViewset(viewsets.ModelViewSet):
    
#     def dispatch(self, request, *args, **kwargs):
#         try:
#             fields_to_exclude = ['model', 'pk']
#             data = json.loads(request.body)
#             value_list=list(data.values())

#             dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
#             if dinfo is not None:
#                 did=dinfo.Device_id
#                 qs_sta = disp_tds_consen.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
#                 if not qs_sta:
#                     data_sta = {}
#                 else:
#                     data_sta = serialize("json", qs_sta)
#                     data_sta = json.loads(data_sta)
#                     for item in data_sta:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
#                     data_sta = json.dumps(data_sta[0]["fields"])
#                     data_sta = json.loads(data_sta)
                
#                 qs_set = disp_tds_consen.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
#                 if not qs_set:
#                     data_set = {}
#                 else:
#                     data_set = serialize("json", qs_set)
#                     data_set = json.loads(data_set)
#                     for item in data_set:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

#                     data_set = json.dumps(data_set[0]["fields"])
#                     data_set = json.loads(data_set)

#                 last_error=Errors.objects.filter(service='tds_consen')
#                 if not last_error:
#                     last_error={}
#                 else:
#                     last_error = serialize("json", last_error)
#                     last_error = json.loads(last_error)
#                     for item in last_error:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
                    
#                     last_error = json.dumps(last_error[0]["fields"])
#                     last_error = json.loads(last_error)

#                 data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
#                 response_data = {
#                     #new code
#                 'data': data_final,  # Include the 'data' field
#                 'status': 200,  # Add the status field
#                 'message': "Data get successful", # Add the message field
                
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json")  

#             else:
#                 response_data = {
#                     #new code
#                 'data': "",  # Include the 'data' field
#                 'status': 500,  # Add the status field
#                 'message': "Unable to update", # Add the message field
                
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json")
#         except Exception as e :
#             print("Exception at line 6108 updated_disp_tds_consenViewset",e)    
      
# class updated_treat_F_flowsenViewset(viewsets.ModelViewSet):
	
    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         fields_to_exclude = ['model', 'pk']
    #         data = json.loads(request.body)
    #         value_list=list(data.values())

    #         dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
    #         if dinfo is not None:
    #             did=dinfo.Device_id
    #             qs_sta = treat_F_flowsen.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
    #             if not qs_sta:
    #                 data_sta = {}
    #             else:
    #                 data_sta = serialize("json", qs_sta)
    #                 data_sta = json.loads(data_sta)
    #                 for item in data_sta:
    #                     item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
    #                 data_sta = json.dumps(data_sta[0]["fields"])
    #                 data_sta = json.loads(data_sta)
                
    #             qs_set = treat_F_flowsen.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
    #             if not qs_set:
    #                 data_set = {}
    #             else:
    #                 data_set = serialize("json", qs_set)
    #                 data_set = json.loads(data_set)
    #                 for item in data_set:
    #                     item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

    #                 data_set = json.dumps(data_set[0]["fields"])
    #                 data_set = json.loads(data_set)

    #             last_error=Errors.objects.filter(service='F_flowsen')
    #             if not last_error:
    #                 last_error={}
    #             else:
    #                 last_error = serialize("json", last_error)
    #                 last_error = json.loads(last_error)
    #                 for item in last_error:
    #                     item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
                    
    #                 last_error = json.dumps(last_error[0]["fields"])
    #                 last_error = json.loads(last_error)

    #             data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
    #             response_data = {
    #                 #new code
    #             'data': data_final,  # Include the 'data' field
    #             'status': 200,  # Add the status field
    #             'message': "Data get successful", # Add the message field
                
    #             }
    #             response_data=[response_data]
    #             return JsonResponse(response_data, safe=False, content_type="application/json") 

    #         else:
    #             response_data = {
    #                 #new code
    #             'data': "",  # Include the 'data' field
    #             'status': 500,  # Add the status field
    #             'message': "Unable to update", # Add the message field
                
    #             }
    #             response_data=[response_data]
    #             return JsonResponse(response_data, safe=False, content_type="application/json")
    #     except Exception as e :
    #         print("Exception at line 6178",e)     
        
# class getDeviceID(viewsets.ModelViewSet):
# 	
#     def dispatch(self, request, *args, **kwargs):
#         try:
#             did = 0
#             data_dict = json.loads(request.body)
#             value_list = list(data_dict.values())
#             dinfo = device_info.objects.filter(componant_name=value_list[2], unit_type=value_list[1], company_id=value_list[0])
#             fields_to_exclude = ['model', 'pk']
                
#             data = serialize("json", dinfo)
#             data = json.loads(data)
            
#             for item in data:
#                 item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
            
            
#             if not data:
#                 response_data = {
#                     'data': [],  # Include the 'data' field
#                     'status': 200,  # Add the status field
#                     'message': "Data not found"  # Add the message field
#                 }
#             else:     
#                 data = json.dumps(data[0]["fields"])
#                 data = json.loads(data)
#                 data = [data]
#                 response_data = {
#                     'data': data[0],  # Include the 'data' field
#                     'status': 200,  # Add the status field
#                     'message': "Data get successfully"  # Add the message field
#                 }
#             response_data=[response_data]
#         except Exception as e:
#                     response_data = {
#                         'data':e,  # Include the 'data' field
#                         'status': 200,  # Add the status field
#                         'message': "Exception found"  # Add the message field
#                     }
        
#         return JsonResponse(response_data, safe=False, content_type="application/json")

# class updated_treat_P_flowsenViewset(viewsets.ModelViewSet):
	
#     def dispatch(self, request, *args, **kwargs):
#         try:
#             fields_to_exclude = ['model', 'pk']
#             data = json.loads(request.body)
#             value_list=list(data.values())
#             dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
#             if dinfo is not None:
#                 did=dinfo.Device_id
#                 qs_sta = treat_P_flowsen.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
#                 if not qs_sta:
#                     data_sta = {}
#                 else:
#                     data_sta = serialize("json", qs_sta)
#                     data_sta = json.loads(data_sta)
#                     for item in data_sta:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
#                     data_sta = json.dumps(data_sta[0]["fields"])
#                     data_sta = json.loads(data_sta)
                
#                 qs_set = treat_P_flowsen.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
#                 if not qs_set:
#                     data_set = {}
#                 else:
#                     data_set = serialize("json", qs_set)
#                     data_set = json.loads(data_set)
#                     for item in data_set:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

#                     data_set = json.dumps(data_set[0]["fields"])
#                     data_set = json.loads(data_set)

#                 last_error=Errors.objects.filter(service='P_flowsen')
#                 if not last_error:
#                     last_error={}
#                 else:
#                     last_error = serialize("json", last_error)
#                     last_error = json.loads(last_error)
#                     for item in last_error:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
                    
#                     last_error = json.dumps(last_error[0]["fields"])
#                     last_error = json.loads(last_error)

#                 data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
#                 response_data = {
#                     #new code
#                 'data': data_final,  # Include the 'data' field
#                 'status': 200,  # Add the status field
#                 'message': "Data get successful", # Add the message field
                
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json") 

#             else:
#                 response_data = {
#                     #new code
#                 'data': "",  # Include the 'data' field
#                 'status': 500,  # Add the status field
#                 'message': "Unable to update", # Add the message field
                
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json")
#         except Exception as e :
#             print("Exception at line 6289 updated_treat_P_flowsenViewset",e)     
       
# class updated_disp_flowsen1Viewset(viewsets.ModelViewSet):
	
#     def dispatch(self, request, *args, **kwargs):
#         try:
#             fields_to_exclude = ['model', 'pk']
#             data = json.loads(request.body)
#             value_list=list(data.values())

#             dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
#             if dinfo is not None:
#                 did=dinfo.Device_id
#                 qs_sta = disp_flowsen1.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
#                 if not qs_sta:
#                     data_sta = {}
#                 else:
#                     data_sta = serialize("json", qs_sta)
#                     data_sta = json.loads(data_sta)
#                     for item in data_sta:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
#                     data_sta = json.dumps(data_sta[0]["fields"])
#                     data_sta = json.loads(data_sta)
                
#                 qs_set = disp_flowsen1.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
#                 if not qs_set:
#                     data_set = {}
#                 else:
#                     data_set = serialize("json", qs_set)
#                     data_set = json.loads(data_set)
#                     for item in data_set:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

#                     data_set = json.dumps(data_set[0]["fields"])
#                     data_set = json.loads(data_set)

#                 last_error=Errors.objects.filter(service='flowsen1')
#                 if not last_error:
#                     last_error={}
#                 else:
#                     last_error = serialize("json", last_error)
#                     last_error = json.loads(last_error)
#                     for item in last_error:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
                    
#                     last_error = json.dumps(last_error[0]["fields"])
#                     last_error = json.loads(last_error)

#                 data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
#                 response_data = {
#                     #new code
#                 'data': data_final,  # Include the 'data' field
#                 'status': 200,  # Add the status field
#                 'message': "Data get successful", # Add the message field 
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json")   

#             else:
#                 response_data = {
#                     #new code
#                 'data': "",  # Include the 'data' field
#                 'status': 500,  # Add the status field
#                 'message': "Unable to update", # Add the message field
                
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json")
#         except Exception as e :
#             print("Exception at line 6358 updated_disp_flowsen1Viewset",e)   
        
# class updated_disp_flowsen2Viewset(viewsets.ModelViewSet):
	
#     def dispatch(self, request, *args, **kwargs):
#         try:
#             fields_to_exclude = ['model', 'pk']
#             data = json.loads(request.body)
#             value_list=list(data.values())

#             dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
#             if dinfo is not None:
#                 did=dinfo.Device_id
#                 qs_sta = disp_flowsen2.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
#                 if not qs_sta:
#                     data_sta = {}
#                 else:
#                     data_sta = serialize("json", qs_sta)
#                     data_sta = json.loads(data_sta)
#                     for item in data_sta:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
#                     data_sta = json.dumps(data_sta[0]["fields"])
#                     data_sta = json.loads(data_sta)
                
#                 qs_set = disp_flowsen2.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
#                 if not qs_set:
#                     data_set = {}
#                 else:
#                     data_set = serialize("json", qs_set)
#                     data_set = json.loads(data_set)
#                     for item in data_set:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

#                     data_set = json.dumps(data_set[0]["fields"])
#                     data_set = json.loads(data_set)

#                 last_error=Errors.objects.filter(service='flowsen2')
#                 if not last_error:
#                     last_error={}
#                 else:
#                     last_error = serialize("json", last_error)
#                     last_error = json.loads(last_error)
#                     for item in last_error:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
                    
#                     last_error = json.dumps(last_error[0]["fields"])
#                     last_error = json.loads(last_error)

#                 data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
#                 response_data = {
#                     #new code
#                 'data': data_final,  # Include the 'data' field
#                 'status': 200,  # Add the status field
#                 'message': "Data get successful", # Add the message field
                
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json") 

#             else:
#                 response_data = {
#                     #new code
#                 'data': "",  # Include the 'data' field
#                 'status': 500,  # Add the status field
#                 'message': "Unable to update", # Add the message field
                
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json")
#         except Exception as e :
#             print("Exception at line 6428 updated_disp_flowsen2Viewset",e)     
     
# class updated_disp_flowsen3Viewset(viewsets.ModelViewSet):
	
#     def dispatch(self, request, *args, **kwargs):
#         try:
#             fields_to_exclude = ['model', 'pk']
#             data = json.loads(request.body)
#             value_list=list(data.values())
                    
#             dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
#             if dinfo is not None:
#                 did=dinfo.Device_id

#                 qs_sta = disp_flowsen3.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
#                 if not qs_sta:
#                     data_sta = {}
#                 else:
#                     data_sta = serialize("json", qs_sta)
#                     data_sta = json.loads(data_sta)
#                     for item in data_sta:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
#                     data_sta = json.dumps(data_sta[0]["fields"])
#                     data_sta = json.loads(data_sta)
                
#                 qs_set = disp_flowsen3.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
#                 if not qs_set:
#                     data_set = {}
#                 else:
#                     data_set = serialize("json", qs_set)
#                     data_set = json.loads(data_set)
#                     for item in data_set:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

#                     data_set = json.dumps(data_set[0]["fields"])
#                     data_set = json.loads(data_set)

#                 last_error=Errors.objects.filter(service='flowsen3')
#                 if not last_error:
#                     last_error={}
#                 else:
#                     last_error = serialize("json", last_error)
#                     last_error = json.loads(last_error)
#                     for item in last_error:
#                         item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
                    
#                     last_error = json.dumps(last_error[0]["fields"])
#                     last_error = json.loads(last_error)

#                 data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
#                 response_data = {
#                     #new code
#                 'data': data_final,  # Include the 'data' field
#                 'status': 200,  # Add the status field
#                 'message': "Data get successful", # Add the message field
                
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json")  

#             else:
#                 response_data = {
#                     #new code
#                 'data': "",  # Include the 'data' field
#                 'status': 500,  # Add the status field
#                 'message': "Unable to update", # Add the message field
                
#                 }
#                 response_data=[response_data]
#                 return JsonResponse(response_data, safe=False, content_type="application/json")
#         except Exception as e :
#             print("Exception at line 6499 updated_disp_flowsen3Viewset",e)    
     
# class updated_disp_flowsen4Viewset(viewsets.ModelViewSet):
	
    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         fields_to_exclude = ['model', 'pk']
    #         data = json.loads(request.body)
    #         value_list=list(data.values())
       
    #         dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
    #         if dinfo is not None:
    #             did=dinfo.Device_id
    #             qs_sta = disp_flowsen4.objects.filter(device_id=did,message_type="updsta").order_by('-id')[:1:1]
    #             if not qs_sta:
    #                 data_sta = {}
    #             else:
    #                 data_sta = serialize("json", qs_sta)
    #                 data_sta = json.loads(data_sta)
    #                 for item in data_sta:
    #                     item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
    #                 data_sta = json.dumps(data_sta[0]["fields"])
    #                 data_sta = json.loads(data_sta)
                
    #             qs_set = disp_flowsen4.objects.filter(device_id=did,message_type="updset").order_by('-id')[:1:1]
    #             if not qs_set:
    #                 data_set = {}
    #             else:
    #                 data_set = serialize("json", qs_set)
    #                 data_set = json.loads(data_set)
    #                 for item in data_set:
    #                     item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}

    #                 data_set = json.dumps(data_set[0]["fields"])
    #                 data_set = json.loads(data_set)

    #             last_error=Errors.objects.filter(service='flowsen4')
    #             if not last_error:
    #                 last_error={}
    #             else:
    #                 last_error = serialize("json", last_error)
    #                 last_error = json.loads(last_error)
    #                 for item in last_error:
    #                     item['fields'] = {k: v for k, v in item['fields'].items() if k not in fields_to_exclude}
                    
    #                 last_error = json.dumps(last_error[0]["fields"])
    #                 last_error = json.loads(last_error)

    #             data_final = {'data_sta':data_sta,'data_set':data_set,'error':last_error}
    #             response_data = {
    #                 #new code
    #             'data': data_final,  # Include the 'data' field
    #             'status': 200,  # Add the status field
    #             'message': "Data get successful", # Add the message field
                
    #             }
    #             response_data=[response_data]
    #             return JsonResponse(response_data, safe=False, content_type="application/json") 

    #         else:
    #             response_data = {
    #                 #new code
    #             'data': "",  # Include the 'data' field
    #             'status': 500,  # Add the status field
    #             'message': "Unable to update", # Add the message field
                
    #             }
    #             response_data=[response_data]
    #             return JsonResponse(response_data, safe=False, content_type="application/json")
    #     except Exception as e :
    #         print("Exception at line 6569 updated_disp_flowsen4Viewset",e)     
      
class cnd_YearlyViewset(viewsets.ModelViewSet):
	
	queryset = cnd_repo_yearly.objects.all()
	
	serializer_class = cnd_YearlySerializer       
class cnd_HourlyViewset(viewsets.ModelViewSet):
	
	queryset = cnd_repo_hourly.objects.all()
	
	serializer_class = cnd_HourlySerializer       
class cnd_MonthlyViewset(viewsets.ModelViewSet):
	
	queryset = cnd_repo_monthly.objects.all()
	
	serializer_class = cnd_MonthlySerializer        
class cnd_DailyViewset(viewsets.ModelViewSet):
	
	queryset = cnd_repo_daily.objects.all()
	
	serializer_class = cnd_DailySerializer
class tds_YearlyViewset(viewsets.ModelViewSet):
	
	queryset = tds_repo_yearly.objects.all()
	
	serializer_class = tds_YearlySerializer       
class tds_HourlyViewset(viewsets.ModelViewSet):
	
	queryset = tds_repo_hourly.objects.all()
	
	serializer_class = tds_HourlySerializer        
class tds_MonthlyViewset(viewsets.ModelViewSet):
	
	queryset = tds_repo_monthly.objects.all()
	
	serializer_class = tds_MonthlySerializer        
class tds_DailyViewset(viewsets.ModelViewSet):
	
	queryset = tds_repo_daily.objects.all()
	
	serializer_class = tds_DailySerializer
class rwp_YearlyViewset(viewsets.ModelViewSet):
	
	queryset = rwp_repo_yearly.objects.all()
	
	serializer_class = rwp_YearlySerializer        
class rwp_HourlyViewset(viewsets.ModelViewSet):
	
	queryset = rwp_repo_hourly.objects.all()
	
	serializer_class = rwp_HourlySerializer        
class rwp_MonthlyViewset(viewsets.ModelViewSet):
	
	queryset = rwp_repo_monthly.objects.all()
	
	serializer_class = rwp_MonthlySerializer        
class rwp_DailyViewset(viewsets.ModelViewSet):
	
	queryset = rwp_repo_daily.objects.all()
	
	serializer_class = rwp_DailySerializer
class hpp_YearlyViewset(viewsets.ModelViewSet):
	
	queryset = hpp_repo_yearly.objects.all()
	
	serializer_class = hpp_YearlySerializer       
class hpp_HourlyViewset(viewsets.ModelViewSet):
	
	queryset = hpp_repo_hourly.objects.all()
	
	serializer_class = hpp_HourlySerializer        
class hpp_MonthlyViewset(viewsets.ModelViewSet):
	
	queryset = hpp_repo_monthly.objects.all()
	
	serializer_class = hpp_MonthlySerializer       
class hpp_DailyViewset(viewsets.ModelViewSet):
	
	queryset = hpp_repo_daily.objects.all()
	
	serializer_class = hpp_DailySerializer
class panel_YearlyViewset(viewsets.ModelViewSet):
	
	queryset = hpp_repo_yearly.objects.all()
	
	serializer_class = hpp_YearlySerializer        
class panel_HourlyViewset(viewsets.ModelViewSet):
	
	queryset = panel_repo_hourly.objects.all()
	
	serializer_class = panel_HourlySerializer        
class panel_MonthlyViewset(viewsets.ModelViewSet):
	
	queryset = panel_repo_monthly.objects.all()
	
	serializer_class = panel_MonthlySerializer       
class panel_DailyViewset(viewsets.ModelViewSet):
	
	queryset = panel_repo_daily.objects.all()
	
	serializer_class = panel_DailySerializer
class F_flowsen_YearlyViewset(viewsets.ModelViewSet):
	
	queryset = F_flowsen_repo_yearly.objects.all()
	
	serializer_class = F_flowsen_YearlySerializer
class P_flowsen_YearlyViewset(viewsets.ModelViewSet):
	
	queryset = P_flowsen_repo_yearly.objects.all()
	
	serializer_class = P_flowsen_YearlySerializer       
class F_flowsen_HourlyViewset(viewsets.ModelViewSet):
	
	queryset = F_flowsen_repo_hourly.objects.all()
	
	serializer_class = F_flowsen_HourlySerializer       
class P_flowsen_HourlyViewset(viewsets.ModelViewSet):
	
	queryset = P_flowsen_repo_hourly.objects.all()
	
	serializer_class = P_flowsen_HourlySerializer       
class F_flowsen_MonthlyViewset(viewsets.ModelViewSet):
	
	queryset = F_flowsen_repo_monthly.objects.all()
	
	serializer_class = F_flowsen_MonthlySerializer        
class P_flowsen_MonthlyViewset(viewsets.ModelViewSet):
	
	queryset = P_flowsen_repo_monthly.objects.all()
	
	serializer_class = P_flowsen_MonthlySerializer        
class F_flowsen_DailyViewset(viewsets.ModelViewSet):
	
	queryset = F_flowsen_repo_daily.objects.all()
	
	serializer_class = F_flowsen_DailySerializer              
class P_flowsen_DailyViewset(viewsets.ModelViewSet):
	
	queryset = P_flowsen_repo_daily.objects.all()
	
	serializer_class = P_flowsen_DailySerializer       
class ampv1_YearlyViewset(viewsets.ModelViewSet):
	
	queryset = ampv1_repo_yearly.objects.all()
	
	serializer_class = ampv1_YearlySerializer        
class ampv1_HourlyViewset(viewsets.ModelViewSet):
	
	queryset = ampv1_repo_hourly.objects.all()
	
	serializer_class = ampv1_HourlySerializer        
class ampv1_MonthlyViewset(viewsets.ModelViewSet):
	
	queryset = ampv1_repo_monthly.objects.all()
	
	serializer_class = ampv1_MonthlySerializer        
class ampv1_DailyViewset(viewsets.ModelViewSet):
	
	queryset = ampv1_repo_daily.objects.all()
	
	serializer_class = ampv1_DailySerializer               
class ampv2_YearlyViewset(viewsets.ModelViewSet):
	
	queryset = ampv2_repo_yearly.objects.all()
	
	serializer_class = ampv2_YearlySerializer        
class ampv2_HourlyViewset(viewsets.ModelViewSet):
	
	queryset = ampv2_repo_hourly.objects.all()
	
	serializer_class = ampv2_HourlySerializer       
class ampv2_MonthlyViewset(viewsets.ModelViewSet):
	
	queryset = ampv2_repo_monthly.objects.all()
	
	serializer_class = ampv2_MonthlySerializer       
class ampv2_DailyViewset(viewsets.ModelViewSet):
	
	queryset = ampv2_repo_daily.objects.all()
	
	serializer_class = ampv2_DailySerializer             
class ampv3_YearlyViewset(viewsets.ModelViewSet):
	
	queryset = ampv3_repo_yearly.objects.all()
	
	serializer_class = ampv3_YearlySerializer
                       
class ampv3_HourlyViewset(viewsets.ModelViewSet):
	
	queryset = ampv3_repo_hourly.objects.all()
	
	serializer_class = ampv3_HourlySerializer
        
class ampv3_MonthlyViewset(viewsets.ModelViewSet):
	
	queryset = ampv3_repo_monthly.objects.all()
	
	serializer_class = ampv3_MonthlySerializer
        
class ampv3_DailyViewset(viewsets.ModelViewSet):
	
	queryset = ampv3_repo_daily.objects.all()
	
	serializer_class = ampv3_DailySerializer       
        
class ampv4_YearlyViewset(viewsets.ModelViewSet):
	
	queryset = ampv4_repo_yearly.objects.all()
	
	serializer_class = ampv4_YearlySerializer
                        
class ampv4_HourlyViewset(viewsets.ModelViewSet):
	
	queryset = ampv4_repo_hourly.objects.all()
	
	serializer_class = ampv4_HourlySerializer
        
class ampv4_MonthlyViewset(viewsets.ModelViewSet):
	
	queryset = ampv4_repo_monthly.objects.all()
	
	serializer_class = ampv4_MonthlySerializer
        
class ampv4_DailyViewset(viewsets.ModelViewSet):
	
	queryset = ampv4_repo_daily.objects.all()
	
	serializer_class = ampv4_DailySerializer       
        
class ampv5_YearlyViewset(viewsets.ModelViewSet):
	
	queryset = ampv5_repo_yearly.objects.all()
	
	serializer_class = ampv5_YearlySerializer
                       
class ampv5_HourlyViewset(viewsets.ModelViewSet):
	
	queryset = ampv5_repo_hourly.objects.all()
	
	serializer_class = ampv5_HourlySerializer
        
class ampv5_MonthlyViewset(viewsets.ModelViewSet):
	
	queryset = ampv5_repo_monthly.objects.all()
	
	serializer_class = ampv5_MonthlySerializer
        
class ampv5_DailyViewset(viewsets.ModelViewSet):
	
	queryset = ampv5_repo_daily.objects.all()
	
	serializer_class = ampv5_DailySerializer       
class tap1_YearlyViewset(viewsets.ModelViewSet):
	
	queryset = tap1_repo_yearly.objects.all()
	
	serializer_class = tap1_YearlySerializer
                       
class tap1_HourlyViewset(viewsets.ModelViewSet):
	
	queryset = tap1_repo_hourly.objects.all()
	
	serializer_class = tap1_HourlySerializer
        
class tap1_MonthlyViewset(viewsets.ModelViewSet):
    
    queryset = tap1_repo_monthly.objects.all()
    
    serializer_class = tap1_MonthlySerializer
    authentication_classes = [JWTAuthentication]
class MyTokenObtainPairView(TokenObtainPairView):
    pass

class MyTokenRefreshView(TokenRefreshView):
    pass
        
class tap1_DailyViewset(viewsets.ModelViewSet):
	
	queryset = tap1_repo_daily.objects.all()
	
	serializer_class = tap1_DailySerializer       
class tap2_YearlyViewset(viewsets.ModelViewSet):
	
	queryset = tap2_repo_yearly.objects.all()
	
	serializer_class = tap2_YearlySerializer
                    
class tap2_HourlyViewset(viewsets.ModelViewSet):
	
	queryset = tap2_repo_hourly.objects.all()
	
	serializer_class = tap2_HourlySerializer
        
class tap2_MonthlyViewset(viewsets.ModelViewSet):
	
	queryset = tap2_repo_monthly.objects.all()
	
	serializer_class = tap2_MonthlySerializer
        
class tap2_DailyViewset(viewsets.ModelViewSet):
	
	queryset = tap2_repo_daily.objects.all()
	
	serializer_class = tap2_DailySerializer       
class tap3_YearlyViewset(viewsets.ModelViewSet):
	
	queryset = tap3_repo_yearly.objects.all()
	
	serializer_class = tap3_YearlySerializer
                
class tap3_HourlyViewset(viewsets.ModelViewSet):
	
	queryset = tap3_repo_hourly.objects.all()
	
	serializer_class = tap3_HourlySerializer
        
class tap3_MonthlyViewset(viewsets.ModelViewSet):
	
	queryset = tap3_repo_monthly.objects.all()
	
	serializer_class = tap3_MonthlySerializer
        
class tap3_DailyViewset(viewsets.ModelViewSet):
	
	queryset = tap3_repo_daily.objects.all()
	
	serializer_class = tap3_DailySerializer       
class tap4_YearlyViewset(viewsets.ModelViewSet):
	
	queryset = tap4_repo_yearly.objects.all()
	
	serializer_class = tap4_YearlySerializer
                        
class tap4_HourlyViewset(viewsets.ModelViewSet):
	
	queryset = tap4_repo_hourly.objects.all()
	
	serializer_class = tap4_HourlySerializer
        
class tap4_MonthlyViewset(viewsets.ModelViewSet):
	
	queryset = tap4_repo_monthly.objects.all()
	
	serializer_class = tap4_MonthlySerializer
        
class tap4_DailyViewset(viewsets.ModelViewSet):
	
	queryset = tap4_repo_daily.objects.all()
	
	serializer_class = tap4_DailySerializer       
        
class cnd_consen_YearlyViewset(viewsets.ModelViewSet):
	
	queryset = cnd_consen_repo_yearly.objects.all()
	
	serializer_class = cnd_consen_YearlySerializer
                        
class tds_consen_YearlyViewset(viewsets.ModelViewSet):
	
	queryset = tds_consen_repo_yearly.objects.all()
	
	serializer_class = tds_consen_YearlySerializer
                       
class cnd_consen_HourlyViewset(viewsets.ModelViewSet):
	
	queryset = cnd_consen_repo_hourly.objects.all()
	
	serializer_class = cnd_consen_HourlySerializer
class tds_consen_HourlyViewset(viewsets.ModelViewSet):
	
	queryset = tds_consen_repo_hourly.objects.all()
	
	serializer_class = tds_consen_HourlySerializer
        
class cnd_consen_MonthlyViewset(viewsets.ModelViewSet):
	
	queryset = cnd_consen_repo_monthly.objects.all()
	
	serializer_class = cnd_consen_MonthlySerializer
class tds_consen_MonthlyViewset(viewsets.ModelViewSet):
	
	queryset = tds_consen_repo_monthly.objects.all()
	
	serializer_class = tds_consen_MonthlySerializer
        
class cnd_consen_DailyViewset(viewsets.ModelViewSet):
	
	queryset = cnd_consen_repo_daily.objects.all()
	
	serializer_class = cnd_consen_DailySerializer
class tds_consen_DailyViewset(viewsets.ModelViewSet):
	
	queryset = tds_consen_repo_daily.objects.all()
	
	serializer_class = tds_consen_DailySerializer

class atm_YearlyViewset(viewsets.ModelViewSet):
	
	queryset = atm_repo_yearly.objects.all()
	
	serializer_class = atm_YearlySerializer
                       
class atm_HourlyViewset(viewsets.ModelViewSet):
	
	queryset = atm_repo_hourly.objects.all()
	
	serializer_class = atm_HourlySerializer
        
class atm_MonthlyViewset(viewsets.ModelViewSet):
	
	queryset = atm_repo_monthly.objects.all()
	
	serializer_class = atm_MonthlySerializer
        
class atm_DailyViewset(viewsets.ModelViewSet):
	
	queryset = atm_repo_daily.objects.all()
	
	serializer_class = atm_DailySerializer
class flowsen1_YearlyViewset(viewsets.ModelViewSet):
	
	queryset = flowsen1_repo_yearly.objects.all()
	
	serializer_class = flowsen1_YearlySerializer
                       
class flowsen1_HourlyViewset(viewsets.ModelViewSet):
	
	queryset = flowsen1_repo_hourly.objects.all()
	
	serializer_class = flowsen1_HourlySerializer
        
class flowsen1_MonthlyViewset(viewsets.ModelViewSet):
	
	queryset = flowsen1_repo_monthly.objects.all()
	
	serializer_class = flowsen1_MonthlySerializer
        
class flowsen1_DailyViewset(viewsets.ModelViewSet):
	
	queryset = flowsen1_repo_daily.objects.all()
	
	serializer_class = flowsen1_DailySerializer   

class flowsen2_YearlyViewset(viewsets.ModelViewSet):
	
	queryset = flowsen2_repo_yearly.objects.all()
	
	serializer_class = flowsen2_YearlySerializer
                        
class flowsen2_HourlyViewset(viewsets.ModelViewSet):
	
	queryset = flowsen2_repo_hourly.objects.all()
	
	serializer_class = flowsen2_HourlySerializer
        
class flowsen2_MonthlyViewset(viewsets.ModelViewSet):
	
	queryset = flowsen2_repo_monthly.objects.all()
	
	serializer_class = flowsen2_MonthlySerializer
        
class flowsen2_DailyViewset(viewsets.ModelViewSet):
	
	queryset = flowsen2_repo_daily.objects.all()
	
	serializer_class = flowsen2_DailySerializer   

class flowsen3_YearlyViewset(viewsets.ModelViewSet):
	
	queryset = flowsen3_repo_yearly.objects.all()
	
	serializer_class = flowsen3_YearlySerializer
                       
class flowsen3_HourlyViewset(viewsets.ModelViewSet):
	
	queryset = flowsen3_repo_hourly.objects.all()
	
	serializer_class = flowsen3_HourlySerializer
        
class flowsen3_MonthlyViewset(viewsets.ModelViewSet):
	
	queryset = flowsen3_repo_monthly.objects.all()
	
	serializer_class = flowsen3_MonthlySerializer
        
class flowsen3_DailyViewset(viewsets.ModelViewSet):
	
	queryset = flowsen1_repo_daily.objects.all()
	
	serializer_class = flowsen1_DailySerializer   

class flowsen4_YearlyViewset(viewsets.ModelViewSet):
	
	queryset = flowsen4_repo_yearly.objects.all()
	
	serializer_class = flowsen4_YearlySerializer
                       
class flowsen4_HourlyViewset(viewsets.ModelViewSet):
	
	queryset = flowsen4_repo_hourly.objects.all()
	
	serializer_class = flowsen4_HourlySerializer
        
class flowsen4_MonthlyViewset(viewsets.ModelViewSet):
	
	queryset = flowsen4_repo_monthly.objects.all()
	
	serializer_class = flowsen4_MonthlySerializer
        
class flowsen4_DailyViewset(viewsets.ModelViewSet):
	
	queryset = flowsen4_repo_daily.objects.all()
	
	serializer_class = flowsen4_DailySerializer

# # import mongoengine
# # mongoengine.connect(db=waterinn, host=localhost:27017, username=username, password=pwc)
class TopicViewSet(viewsets.ModelViewSet):
	
	queryset = topics.objects.all()
	
	serializer_class = TopicSerializer
        
        
class DeviceViewset(viewsets.ModelViewSet):
	
	queryset = device_info.objects.all()
	
	serializer_class = DeviceSerializer
        
class keyViewset(viewsets.ModelViewSet):
	
	queryset = key_info.objects.all()
	
	serializer_class = KeySerializer
        
        
class GraphViewset(viewsets.ModelViewSet):
	
	queryset = graph_info.objects.all()
	
	serializer_class = GraphSerializer
class TopicViewSet(viewsets.ModelViewSet):
	
	queryset = topics.objects.all()
	
	serializer_class = TopicSerializer
        
class DeviceViewset(viewsets.ModelViewSet):
	
	queryset = device_info.objects.all()
	
	serializer_class = DeviceSerializer
        
class keyViewset(viewsets.ModelViewSet):
	
	queryset = key_info.objects.all()
	
	serializer_class = KeySerializer
        
# class RwpstateViewset(viewsets.ModelViewSet):
        
        # queryset = Rwp_state.objects.all()
        
        # serializer_class = RwpstateSerializer

        # deviceid=0
        # def dispatch(self, request, *args, **kwargs):
        #     try:
        #         data_dict = json.loads(request.body)
        #         unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]  # Example of unwanted keys
                
        #         value_list=list(data_dict.values())
        #         #print("datadict:",data_dict)
        #         dinfo=device_info.objects.filter(unit_type=value_list[1],company_id=request.user.company_id).first()
        #         deviceid=dinfo.Device_id
        #         for key in unwanted_keys:
        #             if key in data_dict:
        #                 del data_dict[key]
        #         #print("datadict1:",data_dict)
        #         for key in data_dict:
        #             data_dict[key] = str(data_dict[key])
        #         if deviceid:
        #             mqttc.publish(f'wc1/{deviceid}/chgsta/rwp',str(data_dict).replace(' ',''))
        #             #print("***$$$@",str(data_dict).replace(' ',''))
        #             dd=dateandtime()
        #             e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} rwp status change has been requested - status:{value_list[3]}"
        #             erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='rwp',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
        #             erro.save()
        #         else:
        #             pass

        #     except Exception as e:
        #         pass  
        #     return super().dispatch(request)    
        # def perform_create(self, serializer):
        #     try:
        #         serializer.save()  # Save the data to the database
        #         ddid=Rwp_state.objects.filter(device_id='').update(device_id=deviceid)
        #         ddid.save()
        #     except Exception as e:
        #         pass    
        # def desptroy(self, request):
        #     try:
        #         instance = self.get_object()
        #         self.perform_destroy(instance)
        #     except Http404:
        #         pass

did=0
# class rwpsettingViewset(viewsets.ModelViewSet):
    # queryset = rwp_setting.objects.all()
    # serializer_class = rwpsettingSerializer
    # def dispatch(self, request, *args, **kwargs):
        
    #     try:
    #         data_dict = json.loads(request.body)
    #         unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name"]  # Example of unwanted keys
    #         value_list=list(data_dict.values())
    #         dinfo=device_info.objects.filter(unit_type=value_list[1],company_id=request.user.company_id).first()
    #         deviceid=dinfo.Device_id

    #         for key in unwanted_keys:
    #             if key in data_dict:
    #                 del data_dict[key]
    #         for key in data_dict:
    #                 data_dict[key] = str(data_dict[key])
    #         if deviceid:
    #             mqttc.publish(f'wc1/{deviceid}/chgset/rwp',str(data_dict).replace(' ',''))
    #             dd=dateandtime()
    #             e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} rwp settings change has been requested - over load current:{value_list[3]}, span:{value_list[4]}, dry run current:{value_list[5]}"
    #             erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='rwp',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
    #             erro.save()
    #         else:
    #             pass
            
    #     except Exception as e:
    #         dd=dateandtime()
    #         e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} Hpp has a fault-{e}"
    #         erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='hpp',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
    #         erro.save()
    #     return super().dispatch(request)    
    # def perform_create(self, serializer):
    #     try:
    #         data_dict = serializer.validated_data
    #         # unwanted_keys = ["unit_type", "water_treatment", "company_id", "componant_nam,"site_name"e"]
    #         # Get the device information based on the provided values
    #         dinfo = device_info.objects.filter(componant_name=data_dict['componant_name'],
    #                                            unit_type=data_dict['unit_type'],
    #                                           company_id=data_dict['company_id']).last()
    #         deviceid=0
    #         if dinfo:
    #             did = dinfo.Device_id
    #             deviceid=did
    #             cmpname = dinfo.componant_name
    #         serializer.save()  # Save the data to the database
    #         ddid=rwp_setting.objects.filter(device_id='').update(device_id=deviceid)
    #         ddid.save()
            
    #     except Exception as e:
    #         print("Exception at line 6937:")
    # def desptroy(self, request):
    #     try:
    #         instance = self.get_object()
    #         self.perform_destroy(instance)
    #     except Http404:
    #         pass
# class hppstateViewset(viewsets.ModelViewSet):
	
#         queryset = hpp_state.objects.all()

        
#         serializer_class = hppstateSerializer

#         deviceid=0
#         def dispatch(self, request, *args, **kwargs):
#             try:
#                 data_dict = json.loads(request.body)
#                 unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]  # Example of unwanted keys
                
#                 value_list=list(data_dict.values())
                
#                 dinfo=device_info.objects.filter(unit_type=value_list[1],company_id=request.user.company_id).first()
                
#                 global deviceid
#                 deviceid=dinfo.Device_id
#                 for key in unwanted_keys:
#                     if key in data_dict:
#                         del data_dict[key]
#                 for key in data_dict:
#                     data_dict[key] = str(data_dict[key])
#                 if deviceid:
#                     mqttc.publish(f'wc1/{deviceid}/chgsta/hpp',str(data_dict).replace(' ',''))
#                     dd=dateandtime()
#                     e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} Hpp status change has been requested - status:{value_list[3]}"
#                     erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='hpp',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
#                     erro.save()
#                 else:
#                     pass    

#             except Exception as e:
#                 dd=dateandtime()
#                 e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} Hpp has a fault-{e}"
#                 erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='hpp',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
#                 erro.save()   
#             return super().dispatch(request)    
#         def perform_create(self, serializer):
#             try:

#                 serializer.save()  # Save the data to the database
#                 ddid=hpp_state.objects.filter(device_id='').update(device_id=deviceid)
#                 ddid.save()
#             except Exception as e:
#                 pass     
#         def desptroy(self, request):
#             try:
#                 instance = self.get_object()
#                 self.perform_destroy(instance)
#             except Http404:
#                 pass   
# class hppsettingViewset(viewsets.ModelViewSet):
        
        # queryset = hpp_setting.objects.all()
        
        # serializer_class = hppsettingSerializer

        # deviceid=0
        # def dispatch(self, request, *args, **kwargs):
            
        #     try:
        #         data_dict = json.loads(request.body)
        #         unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]  # Example of unwanted keys
                
        #         value_list=list(data_dict.values())
                
        #         dinfo=device_info.objects.filter(unit_type=value_list[1],company_id=request.user.company_id).first()
                
        #         global deviceid
        #         deviceid=dinfo.Device_id

        #         for key in unwanted_keys:
        #             if key in data_dict:
        #                 del data_dict[key]
        #         for key in data_dict:
        #             data_dict[key] = str(data_dict[key])
        #         if deviceid:
        #             mqttc.publish(f'wc1/{deviceid}/chgset/hpp',str(data_dict).replace(' ',''))
        #             dd=dateandtime()
        #             e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} Hpp settings change has been requested - over load current:{value_list[3]}, span:{value_list[4]}, dry run current:{value_list[5]}"
        #             erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='hpp',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
        #             erro.save()
        #         else:
        #             pass    

        #     except Exception as e:
        #         pass    
        #     return super().dispatch(request)    
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

class device_infoViewset(viewsets.ModelViewSet):
        
        def dispatch(self, request, *args, **kwargs):
            fields_to_exclude = ['model', 'pk']

            data = json.loads(request.body)
            u_id=data['user_id']
            dinfo = device_info.objects.filter(company_id=data['company_id'])
            allsites=[]
            for si in dinfo:
                allsites.append(si.site_name)
            allsiteset=set(allsites)
            allsitelist=list(allsiteset)
            sites=[]
            raw_sql = "SELECT iwater_site.site_name FROM iwater_site INNER JOIN iwater_site_permissions ON iwater_site.id=iwater_site_permissions.site_id WHERE iwater_site_permissions.user_id=%s"

            try:
                # Execute the raw SQL query and fetch the results
                with connection.cursor() as cursor:
                    cursor.execute(raw_sql,[u_id])
                    results = cursor.fetchall()
                for result in results:
                    sites.append(result[0])
            except Exception as e:
                print("exception at line 7085")
            if data['user_role']== "super_admin" or data['user_role']== "administrator":

                siteset=set(allsites)
                siteset=list(siteset)
            else:
                siteset=set(sites)
                siteset=list(siteset)
            response_data = {
                #new code
            'data': siteset,  # Include the 'data' field
            'status': 200,  # Add the status field
            'message': "Data get successful", # Add the message field
            
            }
            response_data=[response_data]
            return JsonResponse(response_data, safe=False, content_type="application/json")           
# class cndsettingViewset(viewsets.ModelViewSet):
	
#         queryset = cnd_setting.objects.all()
#         serializer_class = cndsettingSerializer

#         deviceid =0
#         def dispatch(self, request, *args, **kwargs):
#             try:
#                 data_dict = json.loads(request.body)
#                 unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]  # Example of unwanted keys
#                 value_list=list(data_dict.values())
#                 dinfo=device_info.objects.filter(unit_type=value_list[1],company_id=request.user.company_id).first()
                
#                 did = 0
#                 cmpname = ''
#                 global deviceid
#                 deviceid=dinfo.Device_id

#                 for key in unwanted_keys:
#                     if key in data_dict:
#                         del data_dict[key]
#                 for key in data_dict:
#                     data_dict[key] = str(data_dict[key])
#                 if deviceid:
#                     mqttc.publish(f'wc1/{deviceid}/chgset/cnd_sen',str(data_dict).replace(' ',''))
#                     dd=dateandtime()
#                     e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} cnd settings change has been requested - span:{value_list[3]}, trip_setpoint:{value_list[4]}, atert_setpoint:{value_list[5]}"
#                     erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='cnd',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
#                     erro.save()
#                 else:
#                     pass    
#             except Exception as e:
#                 pass
#             return super().dispatch(request)    
#         def perform_create(self, serializer):
#             try:
#                 serializer.save()  # Save the data to the database
#                 ddid=cnd_setting.objects.filter(device_id='').update(device_id=deviceid)
#                 ddid.save()
#             except Exception as e:
#                 pass        
#         def desptroy(self, request):
#             try:
#                 instance = self.get_object()
#                 self.perform_destroy(instance)
#             except Http404:
#                 pass
        
# class tdssettingViewset(viewsets.ModelViewSet):
        
#         queryset = tds_setting.objects.all()

        
#         serializer_class = tdssettingSerializer

#         deviceid=0
#         def dispatch(self, request, *args, **kwargs):
        
#             try:
#                 data_dict = json.loads(request.body)
#                 unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]  # Example of unwanted keys
                
#                 value_list=list(data_dict.values())
#                 dinfo=device_info.objects.filter(unit_type=value_list[1],company_id=request.user.company_id).first()
                
#                 global deviceid
#                 deviceid=dinfo.Device_id
#                 for key in unwanted_keys:
#                     if key in data_dict:
#                         del data_dict[key]
#                 for key in data_dict:
#                     data_dict[key] = str(data_dict[key])
#                 if deviceid:
#                     mqttc.publish(f'wc1/{deviceid}/chgset/tds_sen',str(data_dict).replace(' ',''))
#                     dd=dateandtime()
#                     e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tds settings change has been requested - span:{value_list[3]}, trip_setpoint:{value_list[4]}, atert_setpoint:{value_list[5]}"
#                     erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='tds',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
#                     erro.save()
#                 else:
#                     pass    
#             except Exception as e:
#                 pass    
#             return super().dispatch(request)    
#         def perform_create(self, serializer):
#             try:
#                 serializer.save()  # Save the data to the database
#                 ddid=tds_setting.objects.filter(device_id='').update(device_id=deviceid)
#                 ddid.save()
#             except Exception as e:
#                 pass        
#         def desptroy(self, request):
#             try:
#                 instance = self.get_object()
#                 self.perform_destroy(instance)
#             except Http404:
#                 pass
    
# class FflowsensettingViewset(viewsets.ModelViewSet):
        
#         queryset = F_flowsen_setting.objects.all()

        
#         serializer_class = FflowsensettingSerializer

#         deviceid=0
#         def dispatch(self, request, *args, **kwargs):
        
#             try:
#                 data_dict = json.loads(request.body)
#                 unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]  # Example of unwanted keys
                
#                 value_list=list(data_dict.values())
                
#                 dinfo=device_info.objects.filter(unit_type=value_list[1],company_id=request.user.company_id).first()
                
#                 global deviceid
#                 deviceid=dinfo.Device_id
#                 for key in unwanted_keys:
#                     if key in data_dict:
#                         del data_dict[key]
#                 for key in data_dict:
#                     data_dict[key] = str(data_dict[key])
#                 if deviceid:
#                     mqttc.publish(f'wc1/{deviceid}/chgset/F_flowsen',str(data_dict).replace(' ',''))
#                     dd=dateandtime()
#                     e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} Fflowsen settings change has been requested - flow factor:{value_list[3]}"
#                     erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='Fflowsen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
#                     erro.save()
#                 else:
#                     pass    

#             except Exception as e:
#                 pass    
#             return super().dispatch(request)    
#         def perform_create(self, serializer):
#             try:
#                 serializer.save()  # Save the data to the database
#                 ddid=F_flowsen_setting.objects.filter(device_id='').update(device_id=deviceid)
#                 ddid.save()
#             except Exception as e:
#                 pass        
#         def desptroy(self, request):
#             try:
#                 instance = self.get_object()
#                 self.perform_destroy(instance)
#             except Http404:
#                 pass
        
# class PflowsensettingViewset(viewsets.ModelViewSet):
	
#         queryset = P_flowsen_setting.objects.all()

        
#         serializer_class =PflowsensettingSerializer

#         deviceid=0
#         def dispatch(self, request, *args, **kwargs):
        
#             try:
#                 data_dict = json.loads(request.body)
#                 unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]  # Example of unwanted keys
                
#                 value_list=list(data_dict.values())
                
#                 dinfo=device_info.objects.filter(unit_type=value_list[1],company_id=request.user.company_id).first()
                
#                 global deviceid
#                 deviceid=dinfo.Device_id
#                 for key in unwanted_keys:
#                     if key in data_dict:
#                         del data_dict[key]
#                 for key in data_dict:
#                     data_dict[key] = str(data_dict[key])
#                 if deviceid:
#                     mqttc.publish(f'wc1/{deviceid}/chgset/P_flowsen',str(data_dict).replace(' ',''))
#                     dd=dateandtime()
#                     e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} Pflowsen settings change has been requested - flow factor:{value_list[3]}"
#                     erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='Pflowsen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
#                     erro.save()
#                 else:
#                     pass    

#             except Exception as e:
#                 pass    
#             return super().dispatch(request)    
#         def perform_create(self, serializer):
#             try:
#                 serializer.save()  # Save the data to the database
#                 ddid=P_flowsen_setting.objects.filter(device_id='').update(device_id=deviceid)
#                 ddid.save()
#             except Exception as e:
#                 pass        
#         def desptroy(self, request):
#             try:
#                 instance = self.get_object()
#                 self.perform_destroy(instance)
#             except Http404:
#                 pass
# class panelsettingViewset(viewsets.ModelViewSet):
	
#         queryset = panel_setting.objects.all()

        
#         serializer_class = panelsettingSerializer

#         deviceid=0
#         def dispatch(self, request, *args, **kwargs):
        
#             try:
#                 data_dict = json.loads(request.body)
#                 unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]  # Example of unwanted keys
                
#                 value_list=list(data_dict.values())
                
#                 dinfo=device_info.objects.filter(unit_type=value_list[1],company_id=request.user.company_id).first()
                
#                 global deviceid
#                 deviceid=dinfo.Device_id
#                 for key in unwanted_keys:
#                     if key in data_dict:
#                         del data_dict[key]
#                 changesrt=data_dict['srt']
#                 changesrt=changesrt.split(":")
#                 hrtominit=int(changesrt[0])*60
#                 data_dict['srt']=hrtominit+int(changesrt[1])
#                 for key in data_dict:
#                     data_dict[key] = str(data_dict[key])
#                 if deviceid:
#                     mqttc.publish(f'wc1/{deviceid}/chgset/panel',str(data_dict).replace(' ',''))
#                     dd=dateandtime()
#                     e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} panel settings change has been requested - mode:{value_list[3]}, under voltage:{value_list[6]}, over voltage:{value_list[7]}, span:{value_list[8]}, no.of multiport valve:{value_list[4]}, sensor type:{value_list[5]}, service time:{value_list[9]}, backwash time:{value_list[10]}, rinse time:{value_list[11]}"
#                     erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='panel',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
#                     erro.save()
#                 else:
#                     pass        

#             except Exception as e:
#                 pass    
#             return super().dispatch(request)    
#         def perform_create(self, serializer):
#             try:
#                 serializer.save()  # Save the data to the database
#                 ddid=panel_setting.objects.filter(device_id='').update(device_id=deviceid)
#                 ddid.save()
#             except Exception as e:
#                 pass        
#         def desptroy(self, request):
#             try:
#                 instance = self.get_object()
#                 self.perform_destroy(instance)
#             except Http404:
#                 pass

# class atmsettingViewset(viewsets.ModelViewSet):
	
#         queryset = atm_setting.objects.all()
#         serializer_class = atmsettingSerializer
#         deviceid=0
#         def dispatch(self, request, *args, **kwargs):
#             try:
#                 data_dict = json.loads(request.body)
#                 unwanted_keys = ["unit_type", "water_treatment","componant_name","site_name","device_id","ntt"]  # Example of unwanted keys
                
#                 value_list=list(data_dict.values())
#                 print("value_list ", value_list)
#                 dinfo=device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
#                 print("dinfo in ATM",dinfo)
#                 deviceid = None
#                 deviceid=dinfo.Device_id
#                 for key in unwanted_keys:
#                     if key in data_dict:
#                         del data_dict[key]
#                 for key in data_dict:
#                     data_dict[key] = str(data_dict[key])
#                 if deviceid:
#                     mqttc.publish(f'wc1/{deviceid}/chgset/atm',str(data_dict).replace(' ',''))
#                     dd=dateandtime()
#                     e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} atm settings change has been requested - over no. Of  tap:{value_list[3]}, no. Of volume:{value_list[4]}, volume1:{value_list[5]}, volume2:{value_list[6]}, volume3:{value_list[7]}, volume4:{value_list[8]}, rate1:{value_list[9]}, rate2:{value_list[10]}, rate3:{value_list[11]}, rate4:{value_list[12]}"
#                     erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='atm',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
#                     erro.save()
#                 else:
#                     pass     

#             except Exception as e:
#                 print("Error in processing atm setting incomplete request ",e)    
#             return super().dispatch(request)   
         
#         def perform_create(self, serializer):
#             try:
#                 serializer.save()  # Save the data to the database
#                 ddid=atm_setting.objects.filter(device_id='').update(device_id=deviceid)
#                 ddid.save()
#             except Exception as e:
#                 pass        
#         def desptroy(self, request):
#             try:
#                 instance = self.get_object()
#                 self.perform_destroy(instance)
#             except Http404:
#                 pass
        
# class cnd_consensettingViewset(viewsets.ModelViewSet):
    
#         queryset = cnd_consen_setting.objects.all()

        
#         serializer_class = cnd_consensettingSerializer

#         deviceid=0
#         def dispatch(self, request, *args, **kwargs):
        
#             try:
#                 data_dict = json.loads(request.body)
#                 unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]  # Example of unwanted keys
                
#                 value_list=list(data_dict.values())
                
#                 dinfo=device_info.objects.filter(unit_type=value_list[1],company_id=request.user.company_id).first()
                
#                 global deviceid
#                 deviceid=dinfo.Device_id

#                 for key in unwanted_keys:
#                     if key in data_dict:
#                         del data_dict[key]
#                 for key in data_dict:
#                     data_dict[key] = str(data_dict[key])
#                 if deviceid:
#                     mqttc.publish(f'wc1/{deviceid}/chgset/cnd_consen',str(data_dict).replace(' ',''))
#                     dd=dateandtime()
#                     e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} cnd_consen settings change has been requested - span:{value_list[3]}, atert_setpoint:{value_list[4]}"
#                     erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='cnd_consen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
#                     erro.save()
#                 else:
#                     pass    

#             except Exception as e:
#                 pass    
#             return super().dispatch(request)    
#         def perform_create(self, serializer):
#             try:
#                 serializer.save()  # Save the data to the database
#                 ddid=cnd_consen_setting.objects.filter(device_id='').update(device_id=deviceid)
#                 ddid.save()
#             except Exception as e:
#                 pass        
#         def desptroy(self, request):
#             try:
#                 instance = self.get_object()
#                 self.perform_destroy(instance)
#             except Http404:
#                 pass
# class tds_consensettingViewset(viewsets.ModelViewSet):
    
#         queryset = tds_consen_setting.objects.all()

        
#         serializer_class = tds_consensettingSerializer

#         deviceid=0
#         def dispatch(self, request, *args, **kwargs):
        
#             try:
#                 data_dict = json.loads(request.body)
#                 unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]  # Example of unwanted keys
                
#                 value_list=list(data_dict.values())
                
#                 dinfo=device_info.objects.filter(unit_type=value_list[1],company_id=request.user.company_id).first()
                
#                 global deviceid
#                 deviceid=dinfo.Device_id
#                 for key in unwanted_keys:
#                     if key in data_dict:
#                         del data_dict[key]
#                 for key in data_dict:
#                     data_dict[key] = str(data_dict[key])
#                 if deviceid:
#                     mqttc.publish(f'wc1/{deviceid}/chgset/tds_consen',str(data_dict).replace(' ',''))
#                     dd=dateandtime()
#                     e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tds_consen settings change has been requested - span:{value_list[3]}, atert_setpoint:{value_list[4]}"
#                     erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='tds_consen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
#                     erro.save()
#                 else:
#                     pass    

#             except Exception as e:
#                 pass    
#             return super().dispatch(request)    
#         def perform_create(self, serializer):
#             try:
#                 serializer.save()  # Save the data to the database
#                 ddid=tds_setting.objects.filter(device_id='').update(device_id=deviceid)
#                 ddid.save()
#             except Exception as e:
#                 pass        
#         def desptroy(self, request):
#             try:
#                 instance = self.get_object()
#                 self.perform_destroy(instance)
#             except Http404:
#                 pass
# class ampv1stateViewset(viewsets.ModelViewSet):
        
#         queryset = ampv1_state.objects.all()

        
#         serializer_class = ampv1stateSerializer

#         deviceid=0
#         def dispatch(self, request, *args, **kwargs):
        
#             try:
#                 data_dict = json.loads(request.body)
#                 unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]  # Example of unwanted keys
                
#                 value_list=list(data_dict.values())
                
#                 dinfo=device_info.objects.filter(unit_type=value_list[1],company_id=request.user.company_id).first()
                
#                 global deviceid
#                 deviceid=dinfo.Device_id
#                 for key in unwanted_keys:
#                     if key in data_dict:
#                         del data_dict[key]
#                 for key in data_dict:
#                     data_dict[key] = str(data_dict[key])
#                 if deviceid:
#                     mqttc.publish(f'wc1/{deviceid}/chgsta/ampv1',str(data_dict).replace(' ',''))
#                     dd=dateandtime()
#                     e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} ampv1 status change has been requested - position:{value_list[3]}"
#                     erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='ampv1',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
#                     erro.save()
#                 else:
#                     pass    

#             except Exception as e:
#                 pass    
#             return super().dispatch(request)    
#         def perform_create(self, serializer):
#             try:
#                 serializer.save()  # Save the data to the database
#                 ddid=ampv1_state.objects.filter(device_id='').update(device_id=deviceid)
#                 ddid.save()
#             except Exception as e:
#                 pass        
#         def desptroy(self, request):
#             try:
#                 instance = self.get_object()
#                 self.perform_destroy(instance)
#             except Http404:
#                 pass
        
# class ampv1settingViewset(viewsets.ModelViewSet):
# # 	
#         queryset = ampv1_setting.objects.all()

        
#         serializer_class = ampv1settingSerializer

#         deviceid=0
#         def dispatch(self, request, *args, **kwargs):
        
#             try:
#                 data_dict = json.loads(request.body)
#                 unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]  # Example of unwanted keys
                
#                 value_list=list(data_dict.values())
                
#                 dinfo=device_info.objects.filter(unit_type=value_list[1],company_id=request.user.company_id).first()
                
#                 global deviceid
#                 deviceid=dinfo.Device_id
#                 for key in unwanted_keys:
#                     if key in data_dict:
#                         del data_dict[key]
#                 changesrt=data_dict['srt']
#                 changesrt=changesrt.split(":")
#                 hrtominit=int(changesrt[0])*60
#                 data_dict['srt']=hrtominit+int(changesrt[1])
#                 for key in data_dict:
#                     data_dict[key] = str(data_dict[key])
#                 if deviceid:
#                     mqttc.publish(f'wc1/{deviceid}/chgset/ampv1',str(data_dict).replace(' ',''))
#                     dd=dateandtime()
#                     e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} ampv1 settings change has been requested - service time:{value_list[8]}, backwash time:{value_list[9]}, rins time:{value_list[10]}, motor on delay time:{value_list[11]}, output1:{value_list[12]}, output2:{value_list[13]}, output3:{value_list[14]}, input1:{value_list[4]}, input2:{value_list[5]}, input3:{value_list[6]}, pressure switch input:{value_list[7]}, sensor type:{value_list[3]}"
#                     erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='ampv1',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
#                     erro.save()
#                 else:
#                     pass    

#             except Exception as e:
#                 pass    
#             return super().dispatch(request)    
#         def perform_create(self, serializer):
#             try:
#                 serializer.save()  # Save the data to the database
#                 ddid=ampv1_setting.objects.filter(device_id='').update(device_id=deviceid)
#                 ddid.save()
#             except Exception as e:
#                 pass        
#         def desptroy(self, request):
#             try:
#                 instance = self.get_object()
#                 self.perform_destroy(instance)
#             except Http404:
#                 pass
# class ampv2stateViewset(viewsets.ModelViewSet):
        
#         queryset = ampv2_state.objects.all()

        
#         serializer_class = ampv2stateSerializer

#         deviceid=0
#         def dispatch(self, request, *args, **kwargs):
        
#             try:
#                 data_dict = json.loads(request.body)
#                 unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]  # Example of unwanted keys
                
#                 value_list=list(data_dict.values())
                
#                 dinfo=device_info.objects.filter(unit_type=value_list[1],company_id=request.user.company_id).first()
                
#                 global deviceid
#                 deviceid=dinfo.Device_id
#                 for key in unwanted_keys:
#                     if key in data_dict:
#                         del data_dict[key]
#                 for key in data_dict:
#                     data_dict[key] = str(data_dict[key])
#                 if deviceid:
#                     mqttc.publish(f'wc1/{deviceid}/chgsta/ampv2',str(data_dict).replace(' ',''))
#                     dd=dateandtime()
#                     e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} ampv2 status change has been requested - position:{value_list[3]}"
#                     erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='ampv2',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
#                     erro.save()
#                 else:
#                     pass    
#             except Exception as e:
#                 pass    
#             return super().dispatch(request)    
#         def perform_create(self, serializer):
#             try:
#                 serializer.save()  # Save the data to the database
#                 ddid=ampv2_state.objects.filter(device_id='').update(device_id=deviceid)
#                 ddid.save()
#             except Exception as e:
#                 pass        
#         def desptroy(self, request):
#             try:
#                 instance = self.get_object()
#                 self.perform_destroy(instance)
#             except Http404:
#                 pass
# class ampv2settingViewset(viewsets.ModelViewSet):
	
#         queryset = ampv2_setting.objects.all()

        
#         serializer_class = ampv2settingSerializer

#         deviceid=0
#         def dispatch(self, request, *args, **kwargs):
        
#             try:
#                 data_dict = json.loads(request.body)
#                 unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]  # Example of unwanted keys
                
#                 value_list=list(data_dict.values())
                
#                 dinfo=device_info.objects.filter(unit_type=value_list[1],company_id=request.user.company_id).first()
                
#                 global deviceid
#                 deviceid=dinfo.Device_id
#                 for key in unwanted_keys:
#                     if key in data_dict:
#                         del data_dict[key]
#                 changesrt=data_dict['srt']
#                 changesrt=changesrt.split(":")
#                 hrtominit=int(changesrt[0])*60
#                 data_dict['srt']=hrtominit+int(changesrt[1])
#                 for key in data_dict:
#                     data_dict[key] = str(data_dict[key])
#                 if deviceid:
#                     mqttc.publish(f'wc1/{deviceid}/chgset/ampv2',str(data_dict).replace(' ',''))
#                     dd=dateandtime()
#                     e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} ampv2 settings change has been requested - service time:{value_list[8]}, backwash time:{value_list[9]}, rins time:{value_list[10]}, motor on delay time:{value_list[11]}, output1:{value_list[12]}, output2:{value_list[13]}, output3:{value_list[14]}, input1:{value_list[4]}, input2:{value_list[5]}, input3:{value_list[6]}, pressure switch input:{value_list[7]}, sensor type:{value_list[3]}"
#                     erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='ampv2',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
#                     erro.save()
#                 else:
#                     pass    
#             except Exception as e:
#                 pass    
#             return super().dispatch(request)    
#         def perform_create(self, serializer):
#             try:
#                 serializer.save()  # Save the data to the database
#                 ddid=ampv2_setting.objects.filter(device_id='').update(device_id=deviceid)
#                 ddid.save()
#             except Exception as e:
#                 pass        
#         def desptroy(self, request):
#             try:
#                 instance = self.get_object()
#                 self.perform_destroy(instance)
#             except Http404:
#                 pass

class tap1settingViewset(viewsets.ModelViewSet):
	
        queryset = tap1_setting.objects.all()
        serializer_class = tap1settingSerializer
        deviceid=0
        def dispatch(self, request, *args, **kwargs):
            try:
                data_dict = json.loads(request.body)
                unwanted_keys = ["unit_type", "water_treatment","componant_name","site_name","device_id"]  # Example of unwanted keys
                value_list=list(data_dict.values())
                dinfo=device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
                deviceid = None
                deviceid=dinfo.Device_id
                for key in unwanted_keys:
                    if key in data_dict:
                        del data_dict[key]
                for key in data_dict:
                    data_dict[key] = str(data_dict[key])
                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/tap1',str(data_dict).replace(' ',''))
                    dd=dateandtime()
                    e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tap1 settings change has been requested - pulse1:{value_list[3]}, pulse2:{value_list[4]}, pulse3:{value_list[5]}, pulse4:{value_list[6]}"
                    erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='tap1',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()
                else:
                    pass    

            except Exception as e:
                print("Error in tap1setting ",e)    
            return super().dispatch(request)  \
              
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
	
        queryset = tap2_setting.objects.all()
        serializer_class = tap2settingSerializer
        deviceid = 0
        def dispatch(self, request, *args, **kwargs):
        
            try:
                data_dict = json.loads(request.body)
                unwanted_keys = ["unit_type", "water_treatment","componant_name","site_name","device_id"]  # Example of unwanted keys
                value_list=list(data_dict.values())
                dinfo=device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
                deviceid = None
                deviceid=dinfo.Device_id
                for key in unwanted_keys:
                    if key in data_dict:
                        del data_dict[key]
                for key in data_dict:
                    data_dict[key] = str(data_dict[key])
                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/tap2',str(data_dict).replace(' ',''))
                    dd=dateandtime()
                    e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tap2 settings change has been requested - pulse1:{value_list[1]}, pulse2:{value_list[2]}, pulse3:{value_list[3]}, pulse4:{value_list[4]}"
                    erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='tap2',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()
                else:
                    pass    

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


# class tap3settingViewset(viewsets.ModelViewSet):
	
#         queryset = tap3_setting.objects.all()

        
#         serializer_class = tap3settingSerializer

#         deviceid=0
#         def dispatch(self, request, *args, **kwargs):
        
#             try:
#                 data_dict = json.loads(request.body)
#                 unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]  # Example of unwanted keys
                
#                 value_list=list(data_dict.values())
                
#                 dinfo=device_info.objects.filter(unit_type=value_list[1],company_id=request.user.company_id).first()
                
#                 global deviceid
#                 deviceid=dinfo.Device_id
#                 for key in unwanted_keys:
#                     if key in data_dict:
#                         del data_dict[key]
#                 for key in data_dict:
#                     data_dict[key] = str(data_dict[key])
#                 if deviceid:
#                     mqttc.publish(f'wc1/{deviceid}/chgset/tap3',str(data_dict).replace(' ',''))
#                     dd=dateandtime()
#                     e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tap3 settings change has been requested - pulse1:{value_list[3]}, pulse2:{value_list[4]}, pulse3:{value_list[5]}, pulse4:{value_list[6]}"
#                     erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='tap3',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
#                     erro.save()
#                 else:
#                     pass    

#             except Exception as e:
#                 pass    
#             return super().dispatch(request)    
#         def perform_create(self, serializer):
#             try:
#                 serializer.save()  # Save the data to the database
#                 ddid=tap3_setting.objects.filter(device_id='').update(device_id=deviceid)
#                 ddid.save()
#             except Exception as e:
#                 pass        
#         def desptroy(self, request):
#             try:
#                 instance = self.get_object()
#                 self.perform_destroy(instance)
#             except Http404:
#                 pass
# class tap4settingViewset(viewsets.ModelViewSet):
	
        # queryset = tap4_setting.objects.all()

        
        # serializer_class = tap4settingSerializer

    
        # deviceid=0
        # def dispatch(self, request, *args, **kwargs):
        #     try:
        #         data_dict = json.loads(request.body)
        #         unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]  # Example of unwanted keys
        #         value_list=list(data_dict.values())
        #         global deviceid
        #         dinfo=device_info.objects.filter(unit_type=value_list[1],company_id=request.user.company_id).first()
        #         deviceid=dinfo.Device_id
        #         for key in unwanted_keys:
        #             if key in data_dict:
        #                 del data_dict[key]
        #         for key in data_dict:
        #             data_dict[key] = str(data_dict[key])
        #         if deviceid:
        #             mqttc.publish(f'wc1/{deviceid}/chgset/tap4',str(data_dict).replace(' ',''))
        #             dd=dateandtime()
        #             e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tap4 settings change has been requested - pulse1:{value_list[3]}, pulse2:{value_list[4]}, pulse3:{value_list[5]}, pulse4:{value_list[6]}"
        #             erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='tap4',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
        #             erro.save()
        #         else:
        #             logger.info("device id not found")


        #     except Exception as e:
        #         pass    
        #     return super().dispatch(request)    
        # def perform_create(self, serializer):
        #     try:
        #         serializer.save()  # Save the data to the database
        #         ddid=tap4_setting.objects.filter(device_id='').update(device_id=deviceid)
        #         ddid.save()
        #     except Exception as e:
        #         pass        
        # def desptroy(self, request):
        #     try:
        #         instance = self.get_object()
        #         self.perform_destroy(instance)
        #     except Http404:
        #         pass
