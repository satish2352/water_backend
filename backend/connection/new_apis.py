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
from django.forms.models import model_to_dict
from django.http import HttpRequest


def dateandtime():
    year=datetime.today().strftime('%Y')
    month=datetime.today().strftime('%m')
    day=datetime.today().strftime('%d')
    hour=datetime.now().strftime('%H')
    minit=datetime.now().strftime('%M')
    second=datetime.now().strftime('%S')
    return year,month,day,hour,minit,second

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
            print("Error in tap1setting ",e)    

@api_view(['POST'])
def newtap2settingViewset(request):
    if request.method == 'POST':
        try:
            data_dict = json.loads(request.body)
            unwanted_keys = ["unit_type", "water_treatment","componant_name","site_name","device_id"]
            value_list=list(data_dict.values())
            dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
            if dinfo is not None:
                
                for key in unwanted_keys:
                            if key in data_dict.keys():
                                del data_dict[key]
                
                deviceid = None
                deviceid=dinfo.Device_id
                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/tap2',str(data_dict).replace(' ',''))
                    dd=dateandtime()
                    e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tap2 settings change has been requested - pulse1:{value_list[2]}, pulse2:{value_list[3]}, pulse3:{value_list[4]}, pulse4:{value_list[5]}"
                    erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='tap2',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()

                    obj = tap2_setting.objects.create(**data_dict)
                    obj.unit_type = value_list[0]
                    obj.componant_name = value_list[1]
                    obj.device_id = deviceid
                    obj.company_id = request.user.company_id
                    obj.save()
                return Response({"message": "NEW TAP-2 API 200"})
        except Exception as e:
            print("Error in tap2setting ",e)    

@api_view(['POST'])
def newtap3settingViewset(request):
    if request.method == 'POST':
        try:
            data_dict = json.loads(request.body)
            unwanted_keys = ["unit_type", "water_treatment","componant_name","site_name","device_id"]
            value_list=list(data_dict.values())
            dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
            if dinfo is not None:
                obj = tap3_setting.objects.create(**data_dict)
                for key in unwanted_keys:
                            if key in data_dict.keys():
                                del data_dict[key]
                
                deviceid = None
                deviceid=dinfo.Device_id
                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/tap3',str(data_dict).replace(' ',''))
                    dd=dateandtime()
                    e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tap3 settings change has been requested - pulse1:{value_list[2]}, pulse2:{value_list[3]}, pulse3:{value_list[4]}, pulse4:{value_list[5]}"
                    erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='tap3',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()

                    obj.unit_type = value_list[0]
                    obj.componant_name = value_list[1]
                    obj.device_id = deviceid
                    obj.company_id = request.user.company_id
                    obj.save()
                return Response({"message": "NEW TAP-3 API 200"})
        except Exception as e:
            print("Error in tap3setting ",e)    

@api_view(['POST'])
def newtap4settingViewset(request):
    if request.method == 'POST':
        try:
            data_dict = json.loads(request.body)
            unwanted_keys = ["unit_type", "water_treatment","componant_name","site_name","device_id"]
            value_list=list(data_dict.values())
            dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
            if dinfo is not None:
                obj = tap4_setting.objects.create(**data_dict)
                for key in unwanted_keys:
                            if key in data_dict.keys():
                                del data_dict[key]
                
                deviceid = None
                deviceid=dinfo.Device_id
                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/tap4',str(data_dict).replace(' ',''))
                    dd=dateandtime()
                    e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tap4 settings change has been requested - pulse1:{value_list[2]}, pulse2:{value_list[3]}, pulse3:{value_list[4]}, pulse4:{value_list[5]}"
                    erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='tap4',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()

                    obj.unit_type = value_list[0]
                    obj.componant_name = value_list[1]
                    obj.device_id = deviceid
                    obj.company_id = request.user.company_id
                    obj.save()
                return Response({"message": "NEW TAP-4 API 200"})
        except Exception as e:
            print("Error in tap4setting ",e)    


#updates api for tap
@api_view(['POST'])
def updated_disp_Tap1Viewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = list(data.values())
        print("value_list:", value_list)

        dinfo = device_info.objects.filter(unit_type=value_list[0], company_id=request.user.company_id).first()

        if dinfo:
            did = dinfo.Device_id
            qs_sta = disp_tap1.objects.filter(device_id=did, message_type="updsta").values('p1','p2','p3','p4','updated_at','created_at').order_by('-id')[:1:1]
            if qs_sta is not None:
                qs_set = disp_tap1.objects.filter(device_id=did, message_type="updset").values('p1','p2','p3','p4','updated_at','created_at').order_by('-id')[:1:1]
            else:
                qs_set ={}
            last_error = Errors.objects.filter(service='tap1')

            data_final = {'data_sta': qs_sta[0], 'data_set': qs_set[0], 'error': last_error}
            response_data = {
                'data': data_final,
                'status': 200,
                'message': "Data get successful",
            }
            return Response(response_data, status=status.HTTP_200_OK)

        else:
            response_data = {
                'data': "",
                'status': 404,
                'message': "Device not found",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    except json.JSONDecodeError as e:
        print("JSON Decode Error in updated_disp_Tap1Viewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in updated_disp_Tap1Viewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def updated_disp_Tap2Viewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = list(data.values())
        dinfo = device_info.objects.filter(unit_type=value_list[0], company_id=request.user.company_id).first()

        if dinfo is not None:
            did = dinfo.Device_id
            qs_sta = disp_tap2.objects.filter(device_id=did, message_type="updsta").order_by('-id')[:1:1]
            if not qs_sta:
                data_sta = {}
            else:
                data_sta = json.loads(qs_sta[0].to_json(exclude=fields_to_exclude))

            qs_set = disp_tap2.objects.filter(device_id=did, message_type="updset").order_by('-id')[:1:1]
            if not qs_set:
                data_set = {}
            else:
                data_set = json.loads(qs_set[0].to_json(exclude=fields_to_exclude))

            last_error = Errors.objects.filter(service='tap2')
            if not last_error:
                last_error = {}
            else:
                last_error = json.loads(last_error[0].to_json(exclude=fields_to_exclude))

            data_final = {'data_sta': data_sta, 'data_set': data_set, 'error': last_error}
            response_data = {
                'data': data_final,
                'status': 200,
                'message': "Data get successful",
            }
            return Response(response_data, status=status.HTTP_200_OK)

        else:
            response_data = {
                'data': "",
                'status': 500,
                'message': "Unable to update",
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        print("Exception in updated_disp_tap2Viewset", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def updated_disp_tap3Viewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = list(data.values())
        dinfo = device_info.objects.filter(unit_type=value_list[0], company_id=request.user.company_id).first()

        if dinfo is not None:
            did = dinfo.Device_id
            qs_sta = disp_tap3.objects.filter(device_id=did, message_type="updsta").order_by('-id')[:1:1]
            if not qs_sta:
                data_sta = {}
            else:
                data_sta = json.loads(qs_sta[0].to_json(exclude=fields_to_exclude))

            qs_set = disp_tap3.objects.filter(device_id=did, message_type="updset").order_by('-id')[:1:1]
            if not qs_set:
                data_set = {}
            else:
                data_set = json.loads(qs_set[0].to_json(exclude=fields_to_exclude))

            last_error = Errors.objects.filter(service='tap3')
            if not last_error:
                last_error = {}
            else:
                last_error = json.loads(last_error[0].to_json(exclude=fields_to_exclude))

            data_final = {'data_sta': data_sta, 'data_set': data_set, 'error': last_error}
            response_data = {
                'data': data_final,
                'status': 200,
                'message': "Data get successful",
            }
            return Response(response_data, status=status.HTTP_200_OK)

        else:
            response_data = {
                'data': "",
                'status': 500,
                'message': "Unable to update",
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        print("Exception in updated_disp_tap3Viewset", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def updated_disp_tap4Viewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = list(data.values())
        dinfo = device_info.objects.filter(unit_type=value_list[0], company_id=request.user.company_id).first()

        if dinfo is not None:
            did = dinfo.Device_id
            qs_sta = disp_tap4.objects.filter(device_id=did, message_type="updsta").order_by('-id')[:1:1]
            if not qs_sta:
                data_sta = {}
            else:
                data_sta = json.loads(qs_sta[0].to_json(exclude=fields_to_exclude))

            qs_set = disp_tap4.objects.filter(device_id=did, message_type="updset").order_by('-id')[:1:1]
            if not qs_set:
                data_set = {}
            else:
                data_set = json.loads(qs_set[0].to_json(exclude=fields_to_exclude))

            last_error = Errors.objects.filter(service='tap4')
            if not last_error:
                last_error = {}
            else:
                last_error = json.loads(last_error[0].to_json(exclude=fields_to_exclude))

            data_final = {'data_sta': data_sta, 'data_set': data_set, 'error': last_error}
            response_data = {
                'data': data_final,
                'status': 200,
                'message': "Data get successful",
            }
            return Response(response_data, status=status.HTTP_200_OK)

        else:
            response_data = {
                'data': "",
                'status': 500,
                'message': "Unable to update",
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        print("Exception in updated_disp_tap4Viewset", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def updated_disp_AtmViewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = list(data.values())
        dinfo = device_info.objects.filter(unit_type=value_list[0], company_id=request.user.company_id).first()

        if dinfo is not None:
            did = dinfo.Device_id
            qs_sta = disp_atm.objects.filter(device_id=did, message_type="updsta").order_by('-id')[:1:1]
            last_error = Errors.objects.filter(service='atm')
            
            if not qs_sta:
                data_sta = {}
            else:
                data_sta = qs_sta[0].__dict__
                data_sta = {k: v for k, v in data_sta.items() if k not in fields_to_exclude}

            qs_set = disp_atm.objects.filter(device_id=did, message_type="updset").order_by('-id')[:1:1]
            
            if not qs_set:
                data_set = {}
            else:
                data_set = qs_set[0].__dict__
                data_set = {k: v for k, v in data_set.items() if k not in fields_to_exclude}

            if not last_error:
                last_error = {}
            else:
                last_error = last_error[0].__dict__
                last_error = {k: v for k, v in last_error.items() if k not in fields_to_exclude}

            data_final = {'data_sta': data_sta, 'data_set': data_set, 'error': last_error}
            response_data = {
                'data': data_final,
                'status': 200,
                'message': "Data get successful",
            }
            return Response(response_data, status=status.HTTP_200_OK)

        else:
            response_data = {
                'data': "",
                'status': 500,
                'message': "Unable to update",
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        print("Exception in updated_disp_atmViewset", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def atm_setting_Viewset(request):
    if request.method == 'POST':
        try:
            data_dict = json.loads(request.body)
            unwanted_keys = ["unit_type", "water_treatment","componant_name","site_name","device_id","ntt"]
            value_list=list(data_dict.values())
            dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
            if dinfo is not None:
                obj = atm_setting.objects.create(**data_dict)
                for key in unwanted_keys:
                            if key in data_dict.keys():
                                del data_dict[key]
                
                deviceid = None
                deviceid=dinfo.Device_id
                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/atm',str(data_dict).replace(' ',''))
                    dd=dateandtime()
                    e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} atm settings change has been requested - over no. Of  tap:{value_list[3]}, no. Of volume:{value_list[4]}, volume1:{value_list[5]}, volume2:{value_list[6]}, volume3:{value_list[7]}, volume4:{value_list[8]}, rate1:{value_list[9]}, rate2:{value_list[10]}, rate3:{value_list[11]}, rate4:{value_list[12]}"
                    erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='atm',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()

                    obj.unit_type = value_list[0]
                    obj.componant_name = value_list[1]
                    obj.device_id = deviceid
                    obj.company_id = request.user.company_id
                    obj.save()
                return Response({"message": "NEW ATM API 200"})
        except Exception as e:
            print("Error in atmsetting ",e)    



#cnd_sen
@api_view(['POST'])
def cnd_senViewset(request):
    if request.method == 'POST':
        try:
            data_dict = json.loads(request.body)
            unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]
            value_list=list(data_dict.values())
            dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
            if dinfo is not None:
                obj = cnd_setting.objects.create(**data_dict)
                for key in unwanted_keys:
                    if key in data_dict.keys():
                        del data_dict[key]
                
                deviceid = None
                deviceid=dinfo.Device_id
                print("deviceid ",deviceid)
                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/cnd_sen',str(data_dict).replace(' ',''))
                    dd=dateandtime()
                    e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} cnd settings change has been requested - span:{value_list[3]}, trip_setpoint:{value_list[4]}, atert_setpoint:{value_list[5]}"
                    erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='cnd',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()

                    obj.unit_type = value_list[0]
                    obj.componant_name = value_list[1]
                    obj.device_id = deviceid
                    obj.company_id = request.user.company_id
                    obj.save()
                return Response({"message": "NEW CND_SEN SETTING API 200"})
        except Exception as e:
            print("Error in CND_SEN SETTING API  ",e)