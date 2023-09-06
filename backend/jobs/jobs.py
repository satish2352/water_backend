from django.conf import settings
import json
import paho.mqtt.client as mqtt
from iwater.iw_logger import logger
from connection.views import MqttClient,mqttc


def schedule_api():
    global mqttc
    # logger.info("Scheduling data")
    if mqttc is None:
        mqttc = MqttClient()
        print("in schedule_api MQTT client oject created in scheduler in job file")
        logger.info("mqtt object Not found so created")
    # elif mqttc.connected_flag == False:
    #     mqttc.reconnect()
    #     logger.info("mqtt reconnected from scheduler")