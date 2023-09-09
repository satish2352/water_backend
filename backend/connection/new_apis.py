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
            qs_set = disp_tap1.objects.filter(device_id=did, message_type="updset").values('p1','p2','p3','p4','updated_at','created_at').order_by('-id')[:1:1]
            last_error = Errors.objects.filter(service='tap1')
            last_error = model_to_dict(last_error[0], exclude=fields_to_exclude) if last_error else {}

            data_final = {'data_set': qs_set[0], 'error': last_error}
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
        print("value_list:", value_list)

        dinfo = device_info.objects.filter(unit_type=value_list[0], company_id=request.user.company_id).first()

        if dinfo:
            did = dinfo.Device_id
            qs_set = disp_tap2.objects.filter(device_id=did, message_type="updset").values('p1','p2','p3','p4','updated_at','created_at').order_by('-id')[:1:1]
            last_error = Errors.objects.filter(service='tap2')
            last_error = model_to_dict(last_error[0], exclude=fields_to_exclude) if last_error else {}

            data_final = {'data_set': qs_set[0], 'error': last_error}
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
        print("JSON Decode Error in updated_disp_Tap2Viewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in updated_disp_Tap2Viewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def updated_disp_tap3Viewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = list(data.values())
        print("value_list:", value_list)

        dinfo = device_info.objects.filter(unit_type=value_list[0], company_id=request.user.company_id).first()

        if dinfo:
            did = dinfo.Device_id
            qs_set = disp_tap3.objects.filter(device_id=did, message_type="updset").values('p1','p2','p3','p4','updated_at','created_at').order_by('-id')[:1:1]
            last_error = Errors.objects.filter(service='tap3')
            last_error = model_to_dict(last_error[0], exclude=fields_to_exclude) if last_error else {}

            data_final = {'data_set': qs_set[0], 'error': last_error}
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
        print("JSON Decode Error in updated_disp_Tap3Viewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in updated_disp_Tap3Viewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def updated_disp_tap4Viewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = list(data.values())
        print("value_list:", value_list)

        dinfo = device_info.objects.filter(unit_type=value_list[0], company_id=request.user.company_id).first()

        if dinfo:
            did = dinfo.Device_id
            qs_set = disp_tap4.objects.filter(device_id=did, message_type="updset").values('p1','p2','p3','p4','updated_at','created_at').order_by('-id')[:1:1]
            last_error = Errors.objects.filter(service='tap4')
            last_error = model_to_dict(last_error[0], exclude=fields_to_exclude) if last_error else {}

            data_final = {'data_set': qs_set[0], 'error': last_error}
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
        print("JSON Decode Error in updated_disp_Tap4Viewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in updated_disp_Tap4Viewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def updated_disp_AtmViewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = list(data.values())
        print("value_list:", value_list)

        dinfo = device_info.objects.filter(unit_type=value_list[0], company_id=request.user.company_id).first()

        if dinfo:
            did = dinfo.Device_id
            qs_sta = disp_atm.objects.filter(device_id=did, message_type="updsta").values('sts','ndv','nta','tmp','whr','custid','created_at','updated_at').order_by('-id')[:1:1]
            qs_set = disp_atm.objects.filter(device_id=did, message_type="updset").values('ntp','nov','vl1','vl2','vl3','vl4','re1','re2','re3','re4','created_at','updated_at').order_by('-id')[:1:1]
            last_error = Errors.objects.filter(service='atm')
            last_error = model_to_dict(last_error[0], exclude=fields_to_exclude) if last_error else {}

            data_final = {'data_sta': qs_sta[0],'data_set': qs_set[0], 'error': last_error}
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
        print("JSON Decode Error in updated_disp_atmViewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in updated_disp_atmViewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def atm_setting_Viewset(request):
    if request.method == 'POST':
        try:
            data_dict = json.loads(request.body)
            unwanted_keys = ["unit_type","componant_name"]
            value_list=data_dict
            print("value_list value_list",request.body)
            print("value_list value_list['tap']",value_list['ntp'])
            dinfo = device_info.objects.filter(unit_type=value_list['unit_type'],company_id=request.user.company_id).first()
            if dinfo is not None:
                print("dinfo dinfo",dinfo)
                for key in unwanted_keys:
                    if key in data_dict.keys():
                        del data_dict[key]

                for key, value in data_dict.items():
                    data_type = type(value)
                    print("data_type",data_type)
                    if data_type != 'str':
                        data_dict[key] = str(value)
                    value.replace('"', "'")
                    value.replace('', "'")

                deviceid = None
                deviceid=dinfo.Device_id
                print("deviceid ",deviceid)
                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/atm',str(data_dict).replace(' ',''))
                    dd=dateandtime()
                    e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} atm settings change has been requested - over no. Of  ntp:{value_list['ntp']}, no. Of volume:{value_list['nov']}, volume1:{value_list['vl1']}, volume2:{value_list['vl2']}, volume3:{value_list['vl3']}, volume4:{value_list['vl4']}, rate1:{value_list['re1']}, rate2:{value_list['re2']}, rate3:{value_list['re3']}, rate4:{value_list['re4']}"
                    erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='atm',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()
                    try:
                        value_list_final = {}
                        value_list_final['ntp']=value_list['ntp']
                        value_list_final['nov']=value_list['nov']
                        value_list_final['vl1']=value_list['vl1']
                        value_list_final['vl2']=value_list['vl2']
                        value_list_final['vl3']=value_list['vl3']
                        value_list_final['vl4']=value_list['vl4']
                        value_list_final['re1']=value_list['re1']
                        value_list_final['re2']=value_list['re2']
                        value_list_final['re3']=value_list['re3']
                        value_list_final['re4']=value_list['re4']
                        value_list_final['componant_name'] = 'atm'
                        value_list_final['device_id'] = deviceid
                        value_list_final['company_id'] = request.user.company_id
                        atm_setting.objects.create(**value_list_final)
                        return Response({"message": "NEW ATM SETTING API 200"})
                    except Exception as e:
                        print("error while saving atm record   ",e)
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

@api_view(['POST'])
def newupdated_treat_cnd_senViewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = list(data.values())

        dinfo = device_info.objects.filter(unit_type=value_list[0], company_id=request.user.company_id).first()

        if dinfo:

            did = dinfo.Device_id
            qs_sta = treat_cnd_sen.objects.filter(device_id=did, message_type="updsta").values('cnd','created_at','updated_at').order_by('-id')[:1:1]

            qs_set = treat_cnd_sen.objects.filter(device_id=did, message_type="updset").values('spn','tsp','asp','created_at','updated_at').order_by('-id')[:1:1]
           

            last_error = Errors.objects.filter(service='cnd_sen')
            last_error = model_to_dict(last_error[0], exclude=fields_to_exclude) if last_error else {}

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
        print("JSON Decode Error in updated_disp_cnd_senViewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in updated_disp_cnd_senViewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#cnd_consen
@api_view(['POST'])
def newcnd_consensettingViewset(request):
    if request.method == 'POST':
        try:
            data_dict = json.loads(request.body)
            unwanted_keys = ["unit_type","componant_name"]
            value_list=data_dict
            try:
                dinfo = device_info.objects.filter(unit_type=value_list['unit_type'],company_id=request.user.company_id).first()
            except Exception as e:
                print("device not found  ",e)
            else:
                for key in unwanted_keys:
                    if key in data_dict.keys():
                        del data_dict[key]
                        
                deviceid = None
                deviceid=dinfo.Device_id
                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/cnd_consen',str(data_dict).replace(' ',''))
                    dd=dateandtime()
                    e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} cnd_consen settings change has been requested - span:{value_list['spn']}, atert_setpoint:{value_list['asp']}"
                    erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='cnd_consen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()
                    try:
                        value_list['componant_name'] = 'cnd_consen'
                        value_list['device_id'] = deviceid
                        value_list['company_id'] = request.user.company_id
                        cnd_consen_setting.objects.create(**value_list)
                        return Response({"message": "NEW CND_CONSEN SETTING API 200"})
                    except Exception as e:
                        print("error while saving cnd sen record   ",e)
                
        except Exception as e:
            print("Error in cnd_consen SETTING API  ",e)


@api_view(['POST'])
def newupdated_disp_cnd_consenViewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = list(data.values())

        dinfo = device_info.objects.filter(unit_type=value_list[0], company_id=request.user.company_id).first()

        if dinfo:

            did = dinfo.Device_id
            qs_sta = disp_cnd_consen.objects.filter(device_id=did, message_type="updsta").values('cnd','created_at','updated_at').order_by('-id')[:1:1]
            # data_sta = model_to_dict(qs_sta[0], exclude=fields_to_exclude) if qs_sta else {}

            qs_set = disp_cnd_consen.objects.filter(device_id=did, message_type="updset").values('spn','asp','created_at','updated_at').order_by('-id')[:1:1]
            #

            last_error = Errors.objects.filter(service='cnd_consen')
            last_error = model_to_dict(last_error[0], exclude=fields_to_exclude) if last_error else {}

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
        print("JSON Decode Error in updated_disp_cnd_consenViewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in updated_disp_cnd_consenViewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#panel
@api_view(['POST'])
def newpanelsettingViewset(request):
    if request.method == 'POST':
        try:
            data_dict = json.loads(request.body)
            unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]
            value_list=list(data_dict.values())
            dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
            if dinfo is not None:
                obj = panel_setting.objects.create(**data_dict)
                for key in unwanted_keys:
                    if key in data_dict.keys():
                        del data_dict[key]
                
                deviceid = None
                deviceid=dinfo.Device_id
                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/panel',str(data_dict).replace(' ',''))
                    dd=dateandtime()
                    e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} panel settings change has been requested - mode:{value_list[3]}, under voltage:{value_list[6]}, over voltage:{value_list[7]}, span:{value_list[8]}, no.of multiport valve:{value_list[4]}, sensor type:{value_list[5]}, service time:{value_list[9]}, backwash time:{value_list[10]}, rinse time:{value_list[11]}"
                    erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='panel',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()

                    obj.unit_type = value_list[0]
                    obj.componant_name = value_list[1]
                    obj.device_id = deviceid
                    obj.company_id = request.user.company_id
                    obj.save()
                return Response({"message": "newpanelsetting API 200"})
        except Exception as e:
            print("Error in newpanelsetting API  ",e)


@api_view(['POST'])
def newupdated_treat_panelViewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = list(data.values())

        dinfo = device_info.objects.filter(unit_type=value_list[0], company_id=request.user.company_id).first()

        if dinfo:

            did = dinfo.Device_id
            qs_sta = treat_panel.objects.filter(device_id=did, message_type="updsta").values('sts','rtl','ttl','lps','hps','dgp','ipv','err','created_at','updated_at').order_by('-id')[:1:1]

            qs_set = treat_panel.objects.filter(device_id=did, message_type="updset").values('mod','unv','ovv','spn','nmv','stp','srt','bkt','rst','created_at','updated_at').order_by('-id')[:1:1]
           

            last_error = Errors.objects.filter(service='panel')
            last_error = model_to_dict(last_error[0], exclude=fields_to_exclude) if last_error else {}

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
        print("JSON Decode Error in updated_treat_panelViewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in updated_treat_panelViewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#FeedFlowSensor
@api_view(['POST'])
def newFflowsensettingViewset(request):
    if request.method == 'POST':
        try:
            data_dict = json.loads(request.body)
            unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]
            value_list=list(data_dict.values())
            dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
            if dinfo is not None:
                obj = F_flowsen_setting.objects.create(**data_dict)
                for key in unwanted_keys:
                    if key in data_dict.keys():
                        del data_dict[key]
                
                deviceid = None
                deviceid=dinfo.Device_id
                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/F_flowsen',str(data_dict).replace(' ',''))
                    dd=dateandtime()
                    e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} Fflowsen settings change has been requested - flow factor:{value_list[3]}"
                    erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='Fflowsen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()

                    obj.unit_type = value_list[0]
                    obj.componant_name = value_list[1]
                    obj.device_id = deviceid
                    obj.company_id = request.user.company_id
                    obj.save()
                return Response({"message": "newFflowsensettingViewset API 200"})
        except Exception as e:
            print("Error in newFflowsensettingViewset API  ",e)


@api_view(['POST'])
def newupdated_treat_F_flowsenViewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = list(data.values())

        dinfo = device_info.objects.filter(unit_type=value_list[0], company_id=request.user.company_id).first()

        if dinfo:

            did = dinfo.Device_id
            qs_sta = treat_F_flowsen.objects.filter(device_id=did, message_type="updsta").values('fr1','created_at','updated_at').order_by('-id')[:1:1]

            qs_set = treat_F_flowsen.objects.filter(device_id=did, message_type="updset").values('ff2','created_at','updated_at').order_by('-id')[:1:1]
           

            last_error = Errors.objects.filter(service='F_flowsen')
            last_error = model_to_dict(last_error[0], exclude=fields_to_exclude) if last_error else {}

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
        print("JSON Decode Error in updated_treat_F_flowsenViewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in updated_treat_F_flowsenViewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#P_FlowSensor
@api_view(['POST'])
def newPflowsensettingViewset(request):
    if request.method == 'POST':
        try:
            data_dict = json.loads(request.body)
            unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]
            value_list=list(data_dict.values())
            dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
            if dinfo is not None:
                obj = P_flowsen_setting.objects.create(**data_dict)
                for key in unwanted_keys:
                    if key in data_dict.keys():
                        del data_dict[key]
                
                deviceid = None
                deviceid=dinfo.Device_id
                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/P_flowsen',str(data_dict).replace(' ',''))
                    dd=dateandtime()
                    e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} Fflowsen settings change has been requested - flow factor:{value_list[3]}"
                    erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='Pflowsen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    erro.save()

                    obj.unit_type = value_list[0]
                    obj.componant_name = value_list[1]
                    obj.device_id = deviceid
                    obj.company_id = request.user.company_id
                    obj.save()
                return Response({"message": "newPflowsensettingViewset API 200"})
        except Exception as e:
            print("Error in newPflowsensettingViewset API  ",e)


@api_view(['POST'])
def newupdated_treat_P_flowsenViewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = list(data.values())

        dinfo = device_info.objects.filter(unit_type=value_list[0], company_id=request.user.company_id).first()

        if dinfo:

            did = dinfo.Device_id
            qs_sta = treat_P_flowsen.objects.filter(device_id=did, message_type="updsta").values('fr2','created_at','updated_at').order_by('-id')[:1:1]

            qs_set = treat_P_flowsen.objects.filter(device_id=did, message_type="updset").values('ff2','created_at','updated_at').order_by('-id')[:1:1]
           

            last_error = Errors.objects.filter(service='P_flowsen')
            last_error = model_to_dict(last_error[0], exclude=fields_to_exclude) if last_error else {}

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
        print("JSON Decode Error in updated_treat_P_flowsenViewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in updated_treat_P_flowsenViewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
