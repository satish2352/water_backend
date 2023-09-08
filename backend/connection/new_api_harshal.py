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

def dateandtime():
    year=datetime.today().strftime('%Y')
    month=datetime.today().strftime('%m')
    day=datetime.today().strftime('%d')
    hour=datetime.now().strftime('%H')
    minit=datetime.now().strftime('%M')
    second=datetime.now().strftime('%S')
    return year,month,day,hour,minit,second



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
    
#RwP UPDATE
@api_view(['POST'])
def newupdated_treat_rwp_Viewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = list(data.values())

        dinfo = device_info.objects.filter(unit_type=value_list[0], company_id=request.user.company_id).first()

        if dinfo:

            did = dinfo.Device_id
            qs_sta = treat_rwp.objects.filter(device_id=did, message_type="updsta").values("sts","crt","olc","drc","spn","created_at","updated_at").order_by('-id')[:1:1]
            # data_sta = model_to_dict(qs_sta[0], exclude=fields_to_exclude) if qs_sta else {}




            qs_set = treat_rwp.objects.filter(device_id=did, message_type="updset").values("sts","crt","olc","drc","spn","created_at","updated_at").order_by('-id')[:1:1]
            # data_set = model_to_dict(qs_set[0], exclude=fields_to_exclude) if qs_set else {}

            last_error = Errors.objects.filter(service='rwp')
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
        print("JSON Decode Error in newupdated_treat_rwp_Viewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in newupdated_treat_rwp_Viewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
                obj = ampv1_setting.objects.create(**data_dict)
                for key in unwanted_keys:
                    if key in data_dict.keys():
                        del data_dict[key]
                
                deviceid = None
                deviceid=dinfo.Device_id
                print("deviceid ",deviceid)
                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/ampv1',str(data_dict).replace(' ',''))
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
                return Response({"message": "NEW AMPV1 SETTING API 200"})
        except Exception as e:
            print("Error in AMPV1 SETTING  ",e)
#APMV1 UPDATE
@api_view(['POST'])
def newupdated_treat_ampv1_Viewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = list(data.values())

        dinfo = device_info.objects.filter(unit_type=value_list[0], company_id=request.user.company_id).first()

        if dinfo:

            did = dinfo.Device_id
            qs_sta = treat_ampv1.objects.filter(device_id=did, message_type="updsta").values("pos","rmt","cct","srt","bkt","rst","mot""stp","op1","op2","op3","ip1","ip2","ip3","psi","created_at","updated_at").order_by('-id')[:1:1]
            # data_sta = model_to_dict(qs_sta[0], exclude=fields_to_exclude) if qs_sta else {}

            qs_set = treat_ampv1.objects.filter(device_id=did, message_type="updset").values("pos","rmt","cct","srt","bkt","rst","mot""stp","op1","op2","op3","ip1","ip2","ip3","psi","created_at","updated_at").order_by('-id')[:1:1]
            # data_set = model_to_dict(qs_set[0], exclude=fields_to_exclude) if qs_set else {}

            last_error = Errors.objects.filter(service='ampv1')
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
        print("JSON Decode Error in newupdated_treat_ampv1_Viewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in newupdated_treat_ampv1_Viewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                obj = ampv2_state.objects.create(**data_dict)
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
                obj = ampv2_setting.objects.create(**data_dict)
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

#AMPV2 UPDATE
@api_view(['POST'])
def newupdated_treat_ampv2_Viewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = list(data.values())

        dinfo = device_info.objects.filter(unit_type=value_list[0], company_id=request.user.company_id).first()

        if dinfo:

            did = dinfo.Device_id
            qs_sta = treat_ampv2.objects.filter(device_id=did, message_type="updsta").values("pos","rmt","cct","srt","bkt","rst","mot""stp","op1","op2","op3","ip1","ip2","ip3","psi","created_at","updated_at").order_by('-id')[:1:1]
            # data_sta = model_to_dict(qs_sta[0], exclude=fields_to_exclude) if qs_sta else {}

            qs_set = treat_ampv2.objects.filter(device_id=did, message_type="updset").values("pos","rmt","cct","srt","bkt","rst","mot""stp","op1","op2","op3","ip1","ip2","ip3","psi","created_at","updated_at").order_by('-id')[:1:1]
            # data_set = model_to_dict(qs_set[0], exclude=fields_to_exclude) if qs_set else {}

            last_error = Errors.objects.filter(service='ampv2')
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
        print("JSON Decode Error in newupdated_treat_ampv2_Viewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in newupdated_treat_ampv2_Viewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
                obj = hpp_state.objects.create(**data_dict)
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
                obj = hpp_setting.objects.create(**data_dict)
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
        
#HPP UPDATE
@api_view(['POST'])
def newupdated_treat_hpp_Viewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = list(data.values())

        dinfo = device_info.objects.filter(unit_type=value_list[0], company_id=request.user.company_id).first()

        if dinfo:

            did = dinfo.Device_id
            qs_sta = treat_hpp.objects.filter(device_id=did, message_type="updsta").values("sts","crt","olc","drc","spn","created_at","updated_at").order_by('-id')[:1:1]
            # data_sta = model_to_dict(qs_sta[0], exclude=fields_to_exclude) if qs_sta else {}

            qs_set = treat_hpp.objects.filter(device_id=did, message_type="updset").values("sts","crt","olc","drc","spn","created_at","updated_at").order_by('-id')[:1:1]
            # data_set = model_to_dict(qs_set[0], exclude=fields_to_exclude) if qs_set else {}

            last_error = Errors.objects.filter(service='hpp')
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
        print("JSON Decode Error in newupdated_treat_hpp_Viewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in newupdated_treat_hpp_Viewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


            
#Flowsen 1 UPDATE
@api_view(['POST'])
def newupdated_disp_flowsen1_Viewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = list(data.values())

        dinfo = device_info.objects.filter(unit_type=value_list[0], company_id=request.user.company_id).first()

        if dinfo:

            did = dinfo.Device_id
            qs_sta = disp_flowsen1.objects.filter(device_id=did, message_type="updsta").values("fr","created_at","updated_at").order_by('-id')[:1:1]
            data_sta = model_to_dict(qs_sta[0], exclude=fields_to_exclude) if qs_sta else {}

            last_error = Errors.objects.filter(service='flowsen1')
            last_error = model_to_dict(last_error[0], exclude=fields_to_exclude) if last_error else {}

            data_final = {'data_sta': qs_sta[0], 'error': last_error}
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
        print("JSON Decode Error in newupdated_disp_flowsen1_Viewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in newupdated_disp_flowsen1_Viewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#Flowsen 2 UPDATE
@api_view(['POST'])
def newupdated_disp_flowsen2_Viewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = list(data.values())

        dinfo = device_info.objects.filter(unit_type=value_list[0], company_id=request.user.company_id).first()

        if dinfo:

            did = dinfo.Device_id
            qs_sta = disp_flowsen2.objects.filter(device_id=did, message_type="updsta").values("fr","created_at","updated_at").order_by('-id')[:1:1]
            data_sta = model_to_dict(qs_sta[0], exclude=fields_to_exclude) if qs_sta else {}

            last_error = Errors.objects.filter(service='flowsen2')
            last_error = model_to_dict(last_error[0], exclude=fields_to_exclude) if last_error else {}

            data_final = {'data_sta': qs_sta[0], 'error': last_error}
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
        print("JSON Decode Error in newupdated_disp_flowsen2_Viewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in newupdated_disp_flowsen2_Viewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#Flowsen 3 UPDATE
@api_view(['POST'])
def newupdated_disp_flowsen3_Viewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = list(data.values())

        dinfo = device_info.objects.filter(unit_type=value_list[0], company_id=request.user.company_id).first()

        if dinfo:

            did = dinfo.Device_id
            qs_sta = disp_flowsen3.objects.filter(device_id=did, message_type="updsta").values("fr","created_at","updated_at").order_by('-id')[:1:1]
            data_sta = model_to_dict(qs_sta[0], exclude=fields_to_exclude) if qs_sta else {}

            last_error = Errors.objects.filter(service='flowsen3')
            last_error = model_to_dict(last_error[0], exclude=fields_to_exclude) if last_error else {}

            data_final = {'data_sta': qs_sta[0], 'error': last_error}
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
        print("JSON Decode Error in newupdated_disp_flowsen3_Viewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in newupdated_disp_flowsen3_Viewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#Flowsen 4 UPDATE
@api_view(['POST'])
def newupdated_disp_flowsen4_Viewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = list(data.values())

        dinfo = device_info.objects.filter(unit_type=value_list[0], company_id=request.user.company_id).first()

        if dinfo:

            did = dinfo.Device_id
            qs_sta = disp_flowsen4.objects.filter(device_id=did, message_type="updsta").values("fr","created_at","updated_at").order_by('-id')[:1:1]
            data_sta = model_to_dict(qs_sta[0], exclude=fields_to_exclude) if qs_sta else {}

            last_error = Errors.objects.filter(service='flowsen4')
            last_error = model_to_dict(last_error[0], exclude=fields_to_exclude) if last_error else {}

            data_final = {'data_sta': qs_sta[0], 'error': last_error}
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
        print("JSON Decode Error in newupdated_disp_flowsen4_Viewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in newupdated_disp_flowsen4_Viewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)