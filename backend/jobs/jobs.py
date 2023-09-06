from django.conf import settings
import json
import paho.mqtt.client as mqtt
from iwater.iw_logger import logger
from connection.views import MqttClient,mqttc


def schedule_api():
    global mqttc
    # logger.info("Scheduling data")

   
    if mqttc is None:
        try:
            mqttc = MqttClient()
            print("MqttClient object created from views in connection app")
        except Exception as e:
            print(" error in connection views while creating mqtt object ",e)

    # elif mqttc.connected_flag == False:
    #     mqttc.reconnect()
    #     logger.info("mqtt reconnected from scheduler")