from django.urls import path
# from connection import views
from .new_apis import *
from . new_api_harshal import *
from django.urls import path,include
from .views import *
from .updated_api import sites_user_count
from rest_framework import routers
# from .views import MyTokenObtainPairView, MyTokenRefreshView

router = routers.DefaultRouter()
router.register(r'Topic',TopicViewSet)
router.register(r'device_info',DeviceViewset)
router.register(r'key_info',keyViewset)
router.register(r'graph_info',GraphViewset)


router.register(r'device_infoViewset',device_infoViewset,basename='device_info')
# router.register(r'cnd_setting',cndsettingViewset)
# router.register(r'tds_setting',tdssettingViewset)
# router.register(r'F_flowsen_setting',FflowsensettingViewset)
# router.register(r'P_flowsen_setting',PflowsensettingViewset)
# router.register(r'panel_setting',panelsettingViewset)
# router.register(r'atm_setting',atmsettingViewset)
# router.register(r'cnd_consen_setting',cnd_consensettingViewset)
# router.register(r'tds_consen_setting',tds_consensettingViewset)
# router.register(r'tap1_setting',tap1settingViewset)
# router.register(r'tap2_setting',tap2settingViewset)
# router.register(r'tap3_setting',tap3settingViewset)
# router.register(r'tap4_setting',tap4settingViewset)


router.register(r'cnd_hourly',cnd_HourlyViewset)
router.register(r'cnd_daily',cnd_DailyViewset)
router.register(r'cnd_monthly',cnd_MonthlyViewset)
router.register(r'cnd_yearly',cnd_YearlyViewset)
router.register(r'tds_hourly',tds_HourlyViewset)
router.register(r'tds_daily',tds_DailyViewset)
router.register(r'tds_monthly',tds_MonthlyViewset)
router.register(r'tds_yearly',tds_YearlyViewset)
router.register(r'rwp_hourly',rwp_HourlyViewset)
router.register(r'rwp_daily',rwp_DailyViewset)
router.register(r'rwp_monthly',rwp_MonthlyViewset)
router.register(r'rwp_yearly',rwp_YearlyViewset)
router.register(r'hpp_hourly',hpp_HourlyViewset)
router.register(r'hpp_daily',hpp_DailyViewset)
router.register(r'hpp_monthly',hpp_MonthlyViewset)
router.register(r'hpp_yearly',hpp_YearlyViewset)
router.register(r'panel_hourly',panel_HourlyViewset)
router.register(r'panel_daily',panel_DailyViewset)
router.register(r'panel_monthly',panel_MonthlyViewset)
router.register(r'panel_yearly',panel_YearlyViewset)
router.register(r'F_flowsen_hourly',F_flowsen_HourlyViewset)
router.register(r'P_flowsen_hourly',P_flowsen_HourlyViewset)
router.register(r'F_flowsen_daily',F_flowsen_DailyViewset)
router.register(r'P_flowsen_daily',P_flowsen_DailyViewset)
router.register(r'F_flowsen_monthly',F_flowsen_MonthlyViewset)
router.register(r'P_flowsen_monthly',P_flowsen_MonthlyViewset)
router.register(r'F_flowsen_yearly',F_flowsen_YearlyViewset)
router.register(r'P_flowsen_yearly',P_flowsen_YearlyViewset)
router.register(r'ampv1_hourly',ampv1_HourlyViewset)
router.register(r'ampv1_daily',ampv1_DailyViewset)
router.register(r'ampv1_monthly',ampv1_MonthlyViewset)
router.register(r'ampv1_yearly',ampv1_YearlyViewset)
router.register(r'ampv2_hourly',ampv2_HourlyViewset)
router.register(r'ampv2_daily',ampv2_DailyViewset)
router.register(r'ampv2_monthly',ampv2_MonthlyViewset)
router.register(r'ampv2_yearly',ampv2_YearlyViewset)
router.register(r'ampv3_hourly',ampv3_HourlyViewset)
router.register(r'ampv3_daily',ampv3_DailyViewset)
router.register(r'ampv3_monthly',ampv3_MonthlyViewset)
router.register(r'ampv3_yearly',ampv3_YearlyViewset)
router.register(r'ampv4_hourly',ampv4_HourlyViewset)
router.register(r'ampv4_daily',ampv4_DailyViewset)
router.register(r'ampv4_monthly',ampv4_MonthlyViewset)
router.register(r'ampv4_yearly',ampv4_YearlyViewset)
router.register(r'ampv5_hourly',ampv5_HourlyViewset)
router.register(r'ampv5_daily',ampv5_DailyViewset)
router.register(r'ampv5_monthly',ampv5_MonthlyViewset)
router.register(r'ampv5_yearly',ampv5_YearlyViewset)
router.register(r'tap1_hourly',tap1_HourlyViewset)
router.register(r'tap1_daily',tap1_DailyViewset)
router.register(r'tap1_monthly',tap1_MonthlyViewset)
router.register(r'tap1_yearly',tap1_YearlyViewset)
router.register(r'tap2_hourly',tap2_HourlyViewset)
router.register(r'tap2_daily',tap2_DailyViewset)
router.register(r'tap2_monthly',tap2_MonthlyViewset)
router.register(r'tap2_yearly',tap2_YearlyViewset)
router.register(r'tap3_hourly',tap3_HourlyViewset)
router.register(r'tap3_daily',tap3_DailyViewset)
router.register(r'tap3_monthly',tap3_MonthlyViewset)
router.register(r'tap3_yearly',tap3_YearlyViewset)
router.register(r'tap4_hourly',tap4_HourlyViewset)
router.register(r'tap4_daily',tap4_DailyViewset)
router.register(r'tap4_monthly',tap4_MonthlyViewset)
router.register(r'tap4_yearly',tap4_YearlyViewset)
router.register(r'atm_hourly',atm_HourlyViewset)
router.register(r'atm_daily',atm_DailyViewset)
router.register(r'atm_monthly',atm_MonthlyViewset)
router.register(r'atm_yearly',atm_YearlyViewset)
router.register(r'cnd_consen_hourly',cnd_consen_HourlyViewset)
router.register(r'tds_consen_hourly',tds_consen_HourlyViewset)
router.register(r'cnd_consen_daily',cnd_consen_DailyViewset)
router.register(r'tds_consen_daily',tds_consen_DailyViewset)
router.register(r'cnd_consen_monthly',cnd_consen_MonthlyViewset)
router.register(r'tds_consen_monthly',tds_consen_MonthlyViewset)
router.register(r'cnd_consen_yearly',cnd_consen_YearlyViewset)
router.register(r'tds_consen_yearly',tds_consen_YearlyViewset)
router.register(r'flowsen1_hourly',flowsen1_HourlyViewset)
router.register(r'flowsen1_daily',flowsen1_DailyViewset)
router.register(r'flowsen1_monthly',flowsen1_MonthlyViewset)
router.register(r'flowsen1_yearly',flowsen1_YearlyViewset)
router.register(r'flowsen2_hourly',flowsen2_HourlyViewset)
router.register(r'flowsen2_daily',flowsen2_DailyViewset)
router.register(r'flowsen2_monthly',flowsen2_MonthlyViewset)
router.register(r'flowsen2_yearly',flowsen2_YearlyViewset)
router.register(r'flowsen3_hourly',flowsen3_HourlyViewset)
router.register(r'flowsen3_daily',flowsen3_DailyViewset)
router.register(r'flowsen3_monthly',flowsen3_MonthlyViewset)
router.register(r'flowsen3_yearly',flowsen3_YearlyViewset)
router.register(r'flowsen4_hourly',flowsen4_HourlyViewset)
router.register(r'flowsen4_daily',flowsen4_DailyViewset)
router.register(r'flowsen4_monthly',flowsen4_MonthlyViewset)
router.register(r'flowsen4_yearly',flowsen4_YearlyViewset)

# router.register(r'updated_treat_cnd_sen',updated_treat_cnd_senViewset,basename='treat_cnd_sen')
# router.register(r'updated_treat_tds_sen',updated_treat_tds_senViewset,basename='treat_tds_sen')
# router.register(r'updated_treat_rwp',updated_treat_rwpViewset,basename='treat_rwp')
router.register(r'site_check',site_check,basename='site_check')
# router.register(r'updated_treat_ampv1',updated_treat_ampv1Viewset,basename='treat_ampv1')
# router.register(r'updated_treat_ampv2',updated_treat_ampv2Viewset,basename='_treat_ampv2')
# router.register(r'updated_treat_hpp',updated_treat_hppViewset,basename='_treat_hpp')
# router.register(r'updated_treat_panel',updated_treat_panelViewset,basename='treat_panel')
# router.register(r'updated_treat_F_flowsen',updated_treat_F_flowsenViewset,basename='treat_F_flowsen')
# router.register(r'updated_treat_P_flowsen',updated_treat_P_flowsenViewset,basename='treat_P_flowsen')
# router.register(r'updated_disp_cnd_consen',updated_disp_cnd_consenViewset,basename='disp_cnd_consen')
# router.register(r'updated_disp_tds_consen',updated_disp_tds_consenViewset,basename='disp_tds_consen')
# router.register(r'updated_disp_tap1',updated_disp_tap1Viewset,basename='disp_tap1')
# router.register(r'updated_disp_tap2',updated_disp_tap2Viewset,basename='disp_tap2')
# router.register(r'updated_disp_tap3',updated_disp_tap3Viewset,basename='disp_tap3')
# router.register(r'updated_disp_tap4',updated_disp_tap4Viewset,basename='disp_tap4')
# router.register(r'updated_disp_atm',updated_disp_atmViewset,basename='disp_atm')
# router.register(r'updated_disp_flowsen1',updated_disp_flowsen1Viewset,basename='disp_flowsen1')
# router.register(r'updated_disp_flowsen2',updated_disp_flowsen2Viewset,basename='disp_flowsen2')
# router.register(r'updated_disp_flowsen3',updated_disp_flowsen3Viewset,basename='disp_flowsen3')
# router.register(r'updated_disp_flowsen4',updated_disp_flowsen4Viewset,basename='disp_flowsen4')
# router.register(r'get_device_id',getDeviceID,basename='get_device_id')

router.register(r'last-records',LastRecordsView,basename='last-records')

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('tap1_setting/',newtap1settingViewset,name="tap1_setting"),
    path('tap2_setting/',newtap2settingViewset,name="tap2_setting"),
    path('tap3_setting/',newtap3settingViewset,name="tap3_setting"),
    path('tap4_setting/',newtap4settingViewset,name="tap4_setting"),
    path('updated_disp_tap1/',updated_disp_Tap1Viewset,name='updated_disp_tap1'),
    path('updated_disp_tap2/',updated_disp_Tap2Viewset,name='updated_disp_tap2'),
    path('updated_disp_tap3/',updated_disp_tap3Viewset,name='updated_disp_tap3'),
    path('updated_disp_tap4/',updated_disp_tap4Viewset,name='updated_disp_tap4'),
    path('atm_setting/',atm_setting_Viewset,name='atm_setting'),
    path('updated_disp_atm/',updated_disp_AtmViewset,name='updated_disp_atm'),
    path('cnd_setting/',cnd_senViewset,name='cnd_setting'),
    path('updated_treat_cnd_sen/',newupdated_treat_cnd_senViewset,name='updated_treat_cnd_sen'),
    path('cnd_consen_setting/',newcnd_consensettingViewset,name='cnd_consen_setting'),
    path('updated_disp_cnd_consen/',newupdated_disp_cnd_consenViewset,name='updated_disp_cnd_consen'),
    path('panel_setting/',newpanelsettingViewset,name='panel_setting'),
    path('updated_treat_panel/',newupdated_treat_panelViewset,name='updated_treat_panel'),
    path('F_flowsen_setting/',newFflowsensettingViewset,name='F_flowsen_setting'),
    path('updated_treat_F_flowsen/',newupdated_treat_F_flowsenViewset,name='updated_treat_F_flowsen'),
    path('P_flowsen_setting/',newPflowsensettingViewset,name='P_flowsen_setting'),
    path('updated_treat_P_flowsen/',newupdated_treat_P_flowsenViewset,name='updated_treat_P_flowsen'),
    # path('c',views.on_message)
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/', views.obtain_token, name='token_obtain_pair'),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    #Harshals APIS
    path('sites_user_count/',sites_user_count,name="sites_user_count"),
    path('Rwp_state/',rwpstateViewset,name="rwpstateViewset"),
    path('rwp_setting/',rwpsettingViewset,name="rwpsettingViewset"),
    path('updated_treat_rwp/',newupdated_treat_rwp_Viewset,name="updated_treat_rwp_Viewset"),
    path('ampv1_state/',ampv1stateViewset,name="ampv1stateViewset"),
    path('ampv1_setting/',ampv1settingViewset,name="ampv1settingViewset"),
    path('updated_treat_ampv1/',newupdated_treat_ampv1_Viewset,name="newupdated_treat_ampv1_Viewset"),
    path('ampv2_state/',ampv2stateViewset,name="ampv2stateViewset"),
    path('ampv2_setting/',ampv2settingViewset,name="ampv2settingViewset"),
    path('updated_treat_ampv2/',newupdated_treat_ampv2_Viewset,name="newupdated_treat_ampv2_Viewset"),
    path('hpp_state/',hppstateViewset,name="hppstateViewset"),
    path('hpp_setting/',hppsettingViewset,name="hppsettingViewset"),
    path('updated_treat_hpp/',newupdated_treat_hpp_Viewset,name="newupdated_treat_hpp_Viewset"),
    path('updated_disp_flowsen1/',newupdated_disp_flowsen1_Viewset,name="newupdated_disp_flowsen1_Viewset"),
    path('updated_disp_flowsen2/',newupdated_disp_flowsen2_Viewset,name="newupdated_disp_flowsen2_Viewset"),
    path('updated_disp_flowsen3/',newupdated_disp_flowsen3_Viewset,name="newupdated_disp_flowsen3_Viewset"),
    path('updated_disp_flowsen4/',newupdated_disp_flowsen4_Viewset,name="newupdated_disp_flowsen4_Viewset"),
]
# urlpatterns = [ 
#     # path('',views.index)
# ]