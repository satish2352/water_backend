from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
from .models import *
from datetime import datetime
from connection.views import mqttc
from datetime import datetime
from django.db import DatabaseError
from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

def dateandtime():
    year=datetime.today().strftime('%Y')
    month=datetime.today().strftime('%m')
    day=datetime.today().strftime('%d')
    hour=datetime.now().strftime('%H')
    minit=datetime.now().strftime('%M')
    second=datetime.now().strftime('%S')
    return year,month,day,hour,minit,second


#TAP 1
@api_view(['POST'])
def newtap1settingViewset(request):
    if request.method == 'POST':
        try:
            print("request  ",request)
            print("request body  ",request.user)
            print("request.user.company_id ",request.user.company_id)
            data_dict = json.loads(request.body)
            unwanted_keys = ["unit_type", "water_treatment","componant_name","site_name","device_id"]
            value_list=list(data_dict.values())
            print("value_list value_list",value_list)
            print("value_list[0] ",value_list[0])
            dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
            if dinfo is not None:
                print("dinfo dinfo",dinfo)
                obj = tap1_setting.objects.create(**data_dict)
                for key in unwanted_keys:
                            if key in data_dict.keys():
                                del data_dict[key]
                
                deviceid = None
                deviceid=dinfo.Device_id
                print("deviceid ",deviceid)
                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/tap1',str(data_dict).replace(' ',''))
                    dd=dateandtime()
                    print("dd dd ",dd)
                    e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tap1 settings change has been requested - pulse1:{value_list[2]}, pulse2:{value_list[3]}, pulse3:{value_list[4]}, pulse4:{value_list[5]}"
                    erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='tap1',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()

                    obj.unit_type = value_list[0]
                    obj.componant_name = value_list[1]
                    obj.device_id = deviceid
                    obj.company_id = request.user.company_id
                    obj.save()
                return Response({"message": "NEW TAP-1 API 200"})
        except Exception as e:
            print("Error in tap1setting ",e)
#RWP STATE 
@api_view(['POST'])
def rwpstateViewset(request):
    if request.method == 'POST':
        try:
            print("request  ",request)
            print("request body   ",request.user)
            print("request.user.company_id ",request.user.company_id)
            data_dict = json.loads(request.body)
            unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name"]
            value_list=list(data_dict.values())
            print("value_list value_list",value_list)
            print("value_list[0] ",value_list[0])
            dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
            if dinfo is not None:
                print("dinfo dinfo",dinfo)
                obj = Rwp_state.objects.create(**data_dict)
                for key in unwanted_keys:
                    if key in data_dict.keys():
                        del data_dict[key]
                
                deviceid = None
                deviceid=dinfo.Device_id
                print("deviceid ",deviceid)
                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/rwp',str(data_dict).replace(' ',''))
                    dd=dateandtime()
                    print("dd dd ",dd)
                    e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} Rwp state change has been requested - pulse1:{value_list[2]}, pulse2:{value_list[3]}, pulse3:{value_list[4]}, pulse4:{value_list[5]}"
                    erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='tap1',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()

                    obj.unit_type = value_list[0]
                    obj.componant_name = value_list[1]
                    obj.device_id = deviceid
                    obj.company_id = request.user.company_id
                    obj.save()
                return Response({"message": "NEW RWP STATE API 200"})
        except Exception as e:
            print("Error in RWP STATE  ",e)

#RWP SETTING
@api_view(['POST'])
def rwpsettingViewset(request):
    if request.method == 'POST':
        try:
            print("request  ",request)
            print("request body   ",request.user)
            print("request.user.company_id ",request.user.company_id)
            data_dict = json.loads(request.body)
            unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name"]
            value_list=list(data_dict.values())
            print("value_list value_list",value_list)
            print("value_list[0] ",value_list[0])
            dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
            if dinfo is not None:
                print("dinfo dinfo",dinfo)
                obj = rwp_setting.objects.create(**data_dict)
                for key in unwanted_keys:
                    if key in data_dict.keys():
                        del data_dict[key]
                
                deviceid = None
                deviceid=dinfo.Device_id
                print("deviceid ",deviceid)
                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/rwp',str(data_dict).replace(' ',''))
                    dd=dateandtime()
                    print("dd dd ",dd)
                    e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} Rwp Setting change has been requested - pulse1:{value_list[2]}, pulse2:{value_list[3]}, pulse3:{value_list[4]}, pulse4:{value_list[5]}"
                    erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='rwp_setting',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()

                    obj.unit_type = value_list[0]
                    obj.componant_name = value_list[1]
                    obj.device_id = deviceid
                    obj.company_id = request.user.company_id
                    obj.save()
                return Response({"message": "NEW RWP setting API 200"})
        except Exception as e:
            print("Error in RWP SETTING  ",e)


#AMPV 1 STATE
@api_view(['POST'])
def ampv1stateViewset(request):
    if request.method == 'POST':
        try:
            print("request  ",request)
            print("request body   ",request.user)
            print("request.user.company_id ",request.user.company_id)
            data_dict = json.loads(request.body)
            unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]
            value_list=list(data_dict.values())
            print("value_list value_list",value_list)
            print("value_list[0] ",value_list[0])
            dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
            if dinfo is not None:
                print("dinfo dinfo",dinfo)
                obj = ampv1_state.objects.create(**data_dict)
                for key in unwanted_keys:
                    if key in data_dict.keys():
                        del data_dict[key]
                
                deviceid = None
                deviceid=dinfo.Device_id
                print("deviceid ",deviceid)
                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/ampv-1',str(data_dict).replace(' ',''))
                    dd=dateandtime()
                    print("dd dd ",dd)
                    e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} Ampv-1 state change has been requested - pulse1:{value_list[2]}, pulse2:{value_list[3]}, pulse3:{value_list[4]}, pulse4:{value_list[5]}"
                    erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='ampv-1_state',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()

                    obj.unit_type = value_list[0]
                    obj.componant_name = value_list[1]
                    obj.device_id = deviceid
                    obj.company_id = request.user.company_id
                    obj.save()
                return Response({"message": "NEW AMPV-1 State API 200"})
        except Exception as e:
            print("Error in AMPV-1 State  ",e)

#AMPV 1 SETTING
@api_view(['POST'])
def ampv1settingViewset(request):
    if request.method == 'POST':
        try:
            print("request  ",request)
            print("request body   ",request.user)
            print("request.user.company_id ",request.user.company_id)
            data_dict = json.loads(request.body)
            unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]
            value_list=list(data_dict.values())
            print("value_list value_list",value_list)
            print("value_list[0] ",value_list[0])
            dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
            if dinfo is not None:
                print("dinfo dinfo",dinfo)
                obj = ampv1_state.objects.create(**data_dict)
                for key in unwanted_keys:
                    if key in data_dict.keys():
                        del data_dict[key]
                
                deviceid = None
                deviceid=dinfo.Device_id
                print("deviceid ",deviceid)
                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/ampv-1',str(data_dict).replace(' ',''))
                    dd=dateandtime()
                    print("dd dd ",dd)
                    e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} Ampv-1 setting change has been requested - pulse1:{value_list[2]}, pulse2:{value_list[3]}, pulse3:{value_list[4]}, pulse4:{value_list[5]}"
                    erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='ampv-1_setting',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()

                    obj.unit_type = value_list[0]
                    obj.componant_name = value_list[1]
                    obj.device_id = deviceid
                    obj.company_id = request.user.company_id
                    obj.save()
                return Response({"message": "NEW AMPV-1 SETTING API 200"})
        except Exception as e:
            print("Error in AMPV-1 SETTING  ",e)

#AMPV 2 STATE
@api_view(['POST'])
def ampv2stateViewset(request):
    if request.method == 'POST':
        try:
            print("request  ",request)
            print("request body   ",request.user)
            print("request.user.company_id ",request.user.company_id)
            data_dict = json.loads(request.body)
            unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]
            value_list=list(data_dict.values())
            print("value_list value_list",value_list)
            print("value_list[0] ",value_list[0])
            dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
            if dinfo is not None:
                print("dinfo dinfo",dinfo)
                obj = ampv1_state.objects.create(**data_dict)
                for key in unwanted_keys:
                    if key in data_dict.keys():
                        del data_dict[key]
                
                deviceid = None
                deviceid=dinfo.Device_id
                print("deviceid ",deviceid)
                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/ampv-2',str(data_dict).replace(' ',''))
                    dd=dateandtime()
                    print("dd dd ",dd)
                    e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} Ampv-2 state change has been requested - pulse1:{value_list[2]}, pulse2:{value_list[3]}, pulse3:{value_list[4]}, pulse4:{value_list[5]}"
                    erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='ampv-2_state',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()

                    obj.unit_type = value_list[0]
                    obj.componant_name = value_list[1]
                    obj.device_id = deviceid
                    obj.company_id = request.user.company_id
                    obj.save()
                return Response({"message": "NEW AMPV-2 State API 200"})
        except Exception as e:
            print("Error in AMPV-2 STATE  ",e)

#AMPV 2 SETTING
@api_view(['POST'])
def ampv2settingViewset(request):
    if request.method == 'POST':
        try:
            print("request  ",request)
            print("request body   ",request.user)
            print("request.user.company_id ",request.user.company_id)
            data_dict = json.loads(request.body)
            unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]
            value_list=list(data_dict.values())
            print("value_list value_list",value_list)
            print("value_list[0] ",value_list[0])
            dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
            if dinfo is not None:
                print("dinfo dinfo",dinfo)
                obj = ampv1_state.objects.create(**data_dict)
                for key in unwanted_keys:
                    if key in data_dict.keys():
                        del data_dict[key]
                
                deviceid = None
                deviceid=dinfo.Device_id
                print("deviceid ",deviceid)
                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/ampv-2',str(data_dict).replace(' ',''))
                    dd=dateandtime()
                    print("dd dd ",dd)
                    e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} Ampv-2 setting change has been requested - pulse1:{value_list[2]}, pulse2:{value_list[3]}, pulse3:{value_list[4]}, pulse4:{value_list[5]}"
                    erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='ampv-2_setting',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()

                    obj.unit_type = value_list[0]
                    obj.componant_name = value_list[1]
                    obj.device_id = deviceid
                    obj.company_id = request.user.company_id
                    obj.save()
                return Response({"message": "NEW AMPV-2 SETTING API 200"})
        except Exception as e:
            print("Error in AMPV-2 setting  ",e)


#HPP STATE
@api_view(['POST'])
def hppstateViewset(request):
    if request.method == 'POST':
        try:
            print("request  ",request)
            print("request body   ",request.user)
            print("request.user.company_id ",request.user.company_id)
            data_dict = json.loads(request.body)
            unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]
            value_list=list(data_dict.values())
            print("value_list value_list",value_list)
            print("value_list[0] ",value_list[0])
            dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
            if dinfo is not None:
                print("dinfo dinfo",dinfo)
                obj = ampv1_state.objects.create(**data_dict)
                for key in unwanted_keys:
                    if key in data_dict.keys():
                        del data_dict[key]
                
                deviceid = None
                deviceid=dinfo.Device_id
                print("deviceid ",deviceid)
                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/hpp',str(data_dict).replace(' ',''))
                    dd=dateandtime()
                    print("dd dd ",dd)
                    e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} hpp state change has been requested - pulse1:{value_list[2]}, pulse2:{value_list[3]}, pulse3:{value_list[4]}, pulse4:{value_list[5]}"
                    erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='hpp_state',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()

                    obj.unit_type = value_list[0]
                    obj.componant_name = value_list[1]
                    obj.device_id = deviceid
                    obj.company_id = request.user.company_id
                    obj.save()
                return Response({"message": "NEW HPP STATE API 200"})
        except Exception as e:
            print("Error in HPP STATE  ",e)


#HPP SETTING
@api_view(['POST'])
def hppsettingViewset(request):
    if request.method == 'POST':
        try:
            print("request  ",request)
            print("request body   ",request.user)
            print("request.user.company_id ",request.user.company_id)
            data_dict = json.loads(request.body)
            unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]
            value_list=list(data_dict.values())
            print("value_list value_list",value_list)
            print("value_list[0] ",value_list[0])
            dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
            if dinfo is not None:
                print("dinfo dinfo",dinfo)
                obj = ampv1_state.objects.create(**data_dict)
                for key in unwanted_keys:
                    if key in data_dict.keys():
                        del data_dict[key]
                
                deviceid = None
                deviceid=dinfo.Device_id
                print("deviceid ",deviceid)
                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/hpp',str(data_dict).replace(' ',''))
                    dd=dateandtime()
                    print("dd dd ",dd)
                    e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} hpp setting change has been requested - pulse1:{value_list[2]}, pulse2:{value_list[3]}, pulse3:{value_list[4]}, pulse4:{value_list[5]}"
                    erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='hpp_setting',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()

                    obj.unit_type = value_list[0]
                    obj.componant_name = value_list[1]
                    obj.device_id = deviceid
                    obj.company_id = request.user.company_id
                    obj.save()
                return Response({"message": "NEW HPP SETTING API 200"})
        except Exception as e:
            print("Error in HPP SETTING  ",e)

            
