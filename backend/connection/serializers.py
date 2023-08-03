# import serializer from rest_framework
from rest_framework import serializers

# import model from models.py
from .models import *

# # Create a model serializer
# class GeeksSerializer(serializers.HyperlinkedModelSerializer):
# 	# specify model and fields
# 	class Meta:
# 		model = GeeksModel
# 		fields = ('Topic',)


# class TopicSerializer(serializers.HyperlinkedModelSerializer):
# 	class Meta:
# 		model = MyObject
# 		fields = ('__all__')
# class DeviceSerializer(serializers.HyperlinkedModelSerializer):
# 	class Meta:
# 			model = Decice_details
# 			fields = ('__all__')


# class NewDeviceSerializer(serializers.HyperlinkedModelSerializer):
# 	# specify model and fields
# 	class Meta:
# 		model = NewDecice_details
# 		fields = ('__all__')

class TopicSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = topics
		fields=('__all__')




# # Create a model serializer
# class GeeksSerializer(serializers.HyperlinkedModelSerializer):
# 	# specify model and fields
# 	class Meta:
# 		model = GeeksModel
# 		fields = ('Topic',)


# class YourModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Errors
#         fields = '__all__'
class TopicSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = topics
		fields=('__all__')

class DeviceSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = device_info
		fields='__all__'

class KeySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = key_info
		fields='__all__'

class cnd_YearlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = cnd_repo_yearly
		fields='__all__'

class cnd_HourlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = cnd_repo_hourly
		fields='__all__'

class cnd_MonthlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = cnd_repo_monthly
		fields='__all__'

class cnd_DailySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = cnd_repo_daily
		fields='__all__'

class tds_YearlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tds_repo_yearly
		fields='__all__'

class tds_HourlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tds_repo_hourly
		fields='__all__'

class tds_MonthlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tds_repo_monthly
		fields='__all__'

class tds_DailySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tds_repo_daily
		fields='__all__'


class rwp_DailySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = rwp_repo_daily
		fields='__all__'

class rwp_HourlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = rwp_repo_hourly
		fields='__all__'

class rwp_MonthlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = rwp_repo_monthly
		fields='__all__'

class rwp_YearlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = rwp_repo_yearly
		fields='__all__'


class hpp_DailySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = hpp_repo_daily
		fields='__all__'

class hpp_HourlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = hpp_repo_hourly
		fields='__all__'

class hpp_MonthlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = hpp_repo_monthly
		fields='__all__'

class hpp_YearlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = hpp_repo_yearly
		fields='__all__'

class panel_DailySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = panel_repo_daily
		fields='__all__'

class panel_HourlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = panel_repo_hourly
		fields='__all__'

class panel_MonthlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = panel_repo_monthly
		fields='__all__'

class panel_YearlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = panel_repo_yearly
		fields='__all__'


class F_flowsen_DailySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = F_flowsen_repo_daily
		fields='__all__'
class P_flowsen_DailySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = P_flowsen_repo_daily
		fields='__all__'

class F_flowsen_HourlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = F_flowsen_repo_hourly
		fields='__all__'
class P_flowsen_HourlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = P_flowsen_repo_hourly
		fields='__all__'

class F_flowsen_MonthlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = F_flowsen_repo_monthly
		fields='__all__'
class P_flowsen_MonthlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = P_flowsen_repo_monthly
		fields='__all__'

class F_flowsen_YearlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = F_flowsen_repo_yearly
		fields='__all__'

class P_flowsen_YearlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = P_flowsen_repo_yearly
		fields='__all__'



class ampv1_DailySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ampv1_repo_daily
		fields='__all__'

class ampv1_HourlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ampv1_repo_hourly
		fields='__all__'

class ampv1_MonthlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ampv1_repo_monthly
		fields='__all__'

class ampv1_YearlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ampv1_repo_yearly
		fields='__all__'
class ampv2_DailySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ampv2_repo_daily
		fields='__all__'

class ampv2_HourlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ampv2_repo_hourly
		fields='__all__'

class ampv2_MonthlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ampv2_repo_monthly
		fields='__all__'

class ampv2_YearlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ampv2_repo_yearly
		fields='__all__'
class ampv3_DailySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ampv3_repo_daily
		fields='__all__'

class ampv3_HourlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ampv3_repo_hourly
		fields='__all__'

class ampv3_MonthlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ampv3_repo_monthly
		fields='__all__'

class ampv3_YearlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ampv3_repo_yearly
		fields='__all__'
class ampv4_DailySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ampv4_repo_daily
		fields='__all__'

class ampv4_HourlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ampv4_repo_hourly
		fields='__all__'

class ampv4_MonthlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ampv4_repo_monthly
		fields='__all__'

class ampv4_YearlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ampv4_repo_yearly
		fields='__all__'
class ampv5_DailySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ampv5_repo_daily
		fields='__all__'

class ampv5_HourlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ampv5_repo_hourly
		fields='__all__'

class ampv5_MonthlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ampv5_repo_monthly
		fields='__all__'

class ampv5_YearlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ampv5_repo_yearly
		fields='__all__'

class tap1_DailySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tap1_repo_daily
		fields='__all__'

class tap1_HourlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tap1_repo_hourly
		fields='__all__'

class tap1_MonthlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tap1_repo_monthly
		fields='__all__'

class tap1_YearlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tap1_repo_yearly
		fields='__all__'
class tap2_DailySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tap2_repo_daily
		fields='__all__'

class tap2_HourlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tap2_repo_hourly
		fields='__all__'

class tap2_MonthlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tap2_repo_monthly
		fields='__all__'

class tap2_YearlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tap2_repo_yearly
		fields='__all__'
class tap3_DailySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tap3_repo_daily
		fields='__all__'

class tap3_HourlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tap3_repo_hourly
		fields='__all__'

class tap3_MonthlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tap3_repo_monthly
		fields='__all__'

class tap3_YearlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tap3_repo_yearly
		fields='__all__'
class tap4_DailySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tap4_repo_daily
		fields='__all__'

class tap4_HourlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tap4_repo_hourly
		fields='__all__'

class tap4_MonthlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tap4_repo_monthly
		fields='__all__'

class tap4_YearlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tap4_repo_yearly
		fields='__all__'

class tds_consen_DailySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = cnd_consen_repo_daily
		fields='__all__'
class cnd_consen_DailySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tds_consen_repo_daily
		fields='__all__'
class cnd_consen_HourlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = cnd_consen_repo_hourly
		fields='__all__'
class tds_consen_HourlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tds_consen_repo_hourly
		fields='__all__'

class cnd_consen_MonthlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = cnd_consen_repo_monthly
		fields='__all__'
class tds_consen_MonthlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tds_consen_repo_monthly
		fields='__all__'

class cnd_consen_YearlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = cnd_consen_repo_yearly
		fields='__all__'
class tds_consen_YearlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tds_consen_repo_yearly
		fields='__all__'

class atm_DailySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = atm_repo_daily
		fields='__all__'
class atm_HourlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = atm_repo_hourly
		fields='__all__'

class atm_MonthlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = atm_repo_monthly
		fields='__all__'

class atm_YearlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = atm_repo_yearly
		fields='__all__'



class GraphSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = graph_info
		fields='__all__'

class DeviceSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = device_info
		fields='__all__'

class KeySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = key_info
		fields='__all__'


class SerchinfoSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = device_info
		fields='__all__'
		# fields=['company_name',]
class rwpsettingSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = rwp_setting
		fields=['drc','olc','spn','unit_type','company_name','componant_name']
	# 	print("hi am from serilization")
	# 	fields=['olc','drc','spn','unit_type','company_name','componant_name']

	# 	def get_author_serializer(self):
	# 		# here write the logic to compute the value based on object
	# 		print("hi ok satish 1")
	# 		return 1

	# 	def get_publisher_serializer(self):
	# 		# here write the logic to compute the value based on object
	# 		print("hi ok satish 1")
	# 		return 2
	# rss=Meta()
	# rss.get_author_serializer()
	# rss.get_publisher_serializer()

class RwpstateSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Rwp_state
		fields=['sts','unit_type','company_name','componant_name']
# class rwpsettingSerializer(serializers.HyperlinkedModelSerializer):
# 	class Meta:
# 		model = rwp_setting
# 		print("hi am from serilization")
# 		fields=['olc','drc','spn','unit_type','company_name','componant_name']


class hppstateSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = hpp_state
		fields=['sts','unit_type','company_name','componant_name']
class hppsettingSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = hpp_setting
		fields=['drc','olc','spn','unit_type','company_name','componant_name']

class cndsettingSerializer(serializers.HyperlinkedModelSerializer):
	# new_field = serializers.CharField()
	class Meta:
		model = cnd_setting
		fields=['spn','tsp','asp','unit_type','company_name','componant_name']

class tdssettingSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tds_setting
		fields=['spn','tsp','asp','unit_type','company_name','componant_name']
class FflowsensettingSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = F_flowsen_setting
		fields=['ff1','unit_type','company_name','componant_name']

class PflowsensettingSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = P_flowsen_setting
		fields=['ff2','unit_type','company_name','componant_name']
class panelsettingSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = panel_setting
		fields=['mod','unv','ovv','spn','nmv','stp','srt','bkt','rst','unit_type','company_name','componant_name']
class atmsettingSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = atm_setting
		fields=['ntp','nov','vl1','vl2','vl3','vl4','re1','re2','re3','re4','unit_type','company_name','componant_name']
class cnd_consensettingSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = cnd_consen_setting
		fields=['spn','asp','unit_type','company_name','componant_name']
class tds_consensettingSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tds_consen_setting
		fields=['spn','asp','unit_type','company_name','componant_name']
class tap1settingSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tap1_setting
		fields=['p1','p2','p3','p4','unit_type','company_name','componant_name']
class tap2settingSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tap2_setting
		fields=['p1','p2','p3','p4','unit_type','company_name','componant_name']
class tap3settingSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tap3_setting
		fields=['p1','p2','p3','p4','unit_type','company_name','componant_name']
class tap4settingSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = tap4_setting
		fields=['p1','p2','p3','p4','unit_type','company_name','componant_name']
class ampv1stateSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ampv1_state
		fields=['pos','unit_type','company_name','componant_name']
class ampv1settingSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ampv1_setting
		fields=['srt','bkt','rst','mot','stp','op1','op2','op3','ip1','ip2','ip3','psi','unit_type','company_name','componant_name']
class ampv2stateSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ampv2_state
		fields=['pos','unit_type','company_name','componant_name']
class ampv2settingSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ampv2_setting
		fields=['srt','bkt','rst','mot','stp','op1','op2','op3','ip1','ip2','ip3','psi','unit_type','company_name','componant_name']
class flowsen1_DailySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = flowsen1_repo_daily
		fields='__all__'
class flowsen1_HourlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = flowsen1_repo_hourly
		fields='__all__'

class flowsen1_MonthlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = flowsen1_repo_monthly
		fields='__all__'

class flowsen1_YearlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = flowsen1_repo_yearly
		fields='__all__'


class flowsen2_DailySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = flowsen2_repo_daily
		fields='__all__'
class flowsen2_HourlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = flowsen2_repo_hourly
		fields='__all__'

class flowsen2_MonthlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = flowsen2_repo_monthly
		fields='__all__'

class flowsen2_YearlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = flowsen2_repo_yearly
		fields='__all__'


class flowsen3_DailySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = flowsen3_repo_daily
		fields='__all__'
class flowsen3_HourlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = flowsen3_repo_hourly
		fields='__all__'

class flowsen3_MonthlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = flowsen3_repo_monthly
		fields='__all__'

class flowsen3_YearlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = flowsen3_repo_yearly
		fields='__all__'


class flowsen4_DailySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = flowsen4_repo_daily
		fields='__all__'
class flowsen4_HourlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = flowsen4_repo_hourly
		fields='__all__'

class flowsen4_MonthlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = flowsen4_repo_monthly
		fields='__all__'

class flowsen4_YearlySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = flowsen4_repo_yearly
		fields='__all__'
#all data form minit tables used for fornt end

class all_panelSerializer(serializers.ModelSerializer):
	class Meta:
		model = treat_panel
		fields = '__all__'
class all_cndSerializer(serializers.ModelSerializer):
	class Meta:
		model = treat_cnd_sen
		fields = '__all__'
class all_tdsSerializer(serializers.ModelSerializer):
	class Meta:
		model = treat_tds_sen
		fields = '__all__'
class all_rwpSerializer(serializers.ModelSerializer):
	class Meta:
		model = treat_rwp
		fields = '__all__'
class all_hppSerializer(serializers.ModelSerializer):
	class Meta:
		model = treat_hpp
		fields = '__all__'
class all_ampv1Serializer(serializers.ModelSerializer):
	class Meta:
		model = treat_ampv1
		fields = '__all__'
class all_ampv2Serializer(serializers.ModelSerializer):
	class Meta:
		model = treat_ampv2
		fields = '__all__'
class all_ampv3Serializer(serializers.ModelSerializer):
    class Meta:
        model = treat_ampv3
        fields = '__all__'
class all_ampv4Serializer(serializers.ModelSerializer):
	class Meta:
		model = treat_ampv4
		fields = '__all__'

class all_ampv5Serializer(serializers.ModelSerializer):
	class Meta:
		model = treat_ampv5
		fields = '__all__'
class all_hppSerializer(serializers.ModelSerializer):
	class Meta:
		model = treat_hpp
		fields = '__all__'
class all_F_flowsenSerializer(serializers.ModelSerializer):
	class Meta:
		model = treat_F_flowsen
		fields = '__all__'
class all_P_flowsenSerializer(serializers.ModelSerializer):
	class Meta:
		model = treat_P_flowsen
		fields = '__all__'
class all_cnd_consenSerializer(serializers.ModelSerializer):
	class Meta:
		model = disp_cnd_consen
		fields = '__all__'

class all_tds_consenSerializer(serializers.ModelSerializer):
	class Meta:
		model = disp_tds_consen
		fields = '__all__'

class all_atmSerializer(serializers.ModelSerializer):
	class Meta:
		model = disp_atm
		fields = '__all__'

class all_tap1Serializer(serializers.ModelSerializer):
	class Meta:
		model = disp_tap1
		fields = '__all__'
class all_tap2Serializer(serializers.ModelSerializer):
	class Meta:
		model = disp_tap2
		fields = '__all__'
class all_tap3Serializer(serializers.ModelSerializer):
	class Meta:
		model = disp_tap3
		fields = '__all__'
class all_tap4Serializer(serializers.ModelSerializer):
	class Meta:
		model = disp_tap4
		fields = '__all__'
class all_flowsen1Serializer(serializers.ModelSerializer):
	class Meta:
		model = disp_flowsen1
		fields = '__all__'
class all_flowsen2Serializer(serializers.ModelSerializer):
	class Meta:
		model = disp_flowsen2
		fields = '__all__'
class all_flowsen3Serializer(serializers.ModelSerializer):
	class Meta:
		model = disp_flowsen3
		fields = '__all__'
class all_flowsen4Serializer(serializers.ModelSerializer):
	class Meta:
		model = disp_flowsen4
		fields = '__all__'

class last_ten_errors(serializers.ModelSerializer):
	class Meta:
		model = Errors
		fields = '__all__'