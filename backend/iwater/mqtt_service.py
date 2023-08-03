import os
import json
from pathlib import Path

import environ
import paho.mqtt.client as mqtt
import mysql.connector
from connection.alpn_mqtt import *

from .iw_logger import logger

env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, 'init_water_app/.env'))
environ.Env.read_env()

DB_NAME = env("DATABASE_NAME")
USER = env("DATABASE_USER")
PASSWORD = env("DATABASE_PASS")
HOST = env("DATABASE_HOST")
PORT = env("DATABASE_PORT")


# import datetime as dt
# import time
# import smtplib
#
# def send_email():
#     email_user = 'tony.joy.tm@gmail.com'
#     server = smtplib.SMTP ('smtp.gmail.com', 587)
#     server.starttls()
#     server.login(email_user, 'xhawroxjuxjwgkvz')
#
#     #EMAIL
#     message = 'sending this from python!'
#     server.sendmail(email_user, email_user, message)
#     server.quit()
#
# def send_email_at(send_time):
#     print(send_time.timestamp() - time.time())
#     time.sleep(send_time.timestamp() - time.time())
#     send_email()
#     print('email sent')
#
# first_email_time = dt.datetime.now()# dt.datetime(2022,10,26,3,0,0) # set your sending time in UTC
# interval = dt.timedelta(minutes=1) # set the interval for sending the email
#
# send_time = first_email_time+interval
# while True:
#     send_email_at(send_time)
#     send_time = send_time + interval


# select company_id from iwater_subscription where days_to_expire<=358;
# +------------+
# | company_id |
# +------------+
# |         30 |
# +------------+
# 1 row in set (0.03 sec)
#
# mysql> select * from iwater_user where company_id=30 and is_admin=True;

class Client:

    def __init__(self, ):
        # _data_mqtt = settings.settings_get_mqttSettings()
        # _topic = "IW/V1/OTP"
        _topic = "wc/v1/OTP"
        # mqttc = mqtt.Client()
        # mqttc.subscribe('wc/#')
        # _username = _data_mqtt['_username']
        # _password = _data_mqtt['_password']
        # _hostname = "broker.mqttdashboard.com"
        # _port = 1883
        _port = 443

        # logger.info("MQTT - Credentials: username: {}, hostname: {}, port: {}".format(_username, _hostname, _port))
        # self.client = mqtt.Client()
        self.client = mqtt.Client()
        self.topic = _topic
        # if _clientID != "":
        # self.client = mqtt.Client(client_id="")

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # connect to HiveMQ Cloud on port
        # self.client.connect(_hostname, _port, 3600)
        self.client.connect(aws_iot_endpoint, _port, 3600)
        # mqttc.connect(aws_iot_endpoint, port=443)

        self.client.loop_start()

    def on_message(self, client, userdata, message):

        data = json.loads(str(message.payload.decode('utf-8')))
        logger.info("MQTT data {}".format(data))
        site_id = str(data["token"]).lstrip("0")
        print(site_id)
        device_id = data["deviceid"]
        panelid = data["panelid"] if data["panelid"] else None
        atmid = data["atmid"] if data["atmid"] else None
        logger.info("site_id {}".format(site_id))
        logger.info("panelid {}".format(panelid))
        logger.info("atmid {}".format(atmid))
        cnx = mysql.connector.connect(user=USER, host=HOST, database=DB_NAME, passwd=PASSWORD)
        cursor = cnx.cursor()
        try:
            if panelid and atmid:
                logger.info("Both")

                add_device = "insert into iwater_device (device_name1, serial_no1, device_name2, serial_no2, site_id) " \
                             "values (%s ,%s, %s, %s, %s);"
                device_data = (device_id, panelid, device_id, atmid, site_id)
                print(device_data)
                cursor.execute(add_device, device_data)
                update_site = "update  iwater_site set is_treatment_unit=1 where id=%s;"
                site_data = (site_id,)
                cursor.execute(update_site, site_data)
                print("updated is_treatment_unit")

                update_site = "update  iwater_site set is_dispensing_unit=1 where id=%s;"
                site_data = (site_id,)
                cursor.execute(update_site, site_data)
                print("updated is_dispensing_unit")

                update_subscription = "update  iwater_subscription set is_treatment_unit=1 where site_id=%s;"
                site_data = (site_id,)
                cursor.execute(update_subscription, site_data)

                get_company_id = "select company_id from  iwater_subscription where is_treatment_unit=1 and site_id=%s;"
                site_data = (site_id,)
                cursor.execute(get_company_id, site_data)
                company_id = cursor.fetchone()[0]
                print(company_id)

                update_subscription = "insert  into iwater_subscription (is_treatment_unit, is_dispensing_unit, site_id, company_id) " \
                             "values (%s, %s, %s);"
                subscription_data = ("0", "1", site_id, company_id)
                cursor.execute(update_subscription, subscription_data)

            elif panelid:
                logger.info("panelid")
                add_device = "insert into iwater_device (device_name1, serial_no1, site_id) values (%s, %s, %s);"
                device_data = (device_id, panelid, site_id)
                cursor.execute(add_device, device_data)

                update_site = "update  iwater_site set is_treatment_unit=1 where id=%s;"
                site_data = (site_id,)
                cursor.execute(update_site, site_data)

                update_subscription = "update  iwater_subscription set is_treatment_unit=1 where site_id=%s;"
                site_data = (site_id,)
                cursor.execute(update_subscription, site_data)

            elif atmid:
                logger.info("atmid")
                add_device = "insert into iwater_device (device_name1, serial_no1, site_id) values (%s, %s, %s);"
                device_data = (device_id, atmid, site_id)
                cursor.execute(add_device, device_data)

                update_site = "update  iwater_site set is_dispensing_unit=1 where id=%s;"
                site_data = (site_id,)
                cursor.execute(update_site, site_data)

                update_subscription = "update  iwater_subscription set is_dispensing_unit=1 where site_id=%s;"
                site_data = (site_id,)
                cursor.execute(update_subscription, site_data)
                # cnx.commit()
            cnx.commit()
        except Exception as err:
            print(err)
            logger.error("MQTT - {}".format(err))

    def on_connect(self, client, userdata, flags, rc):
        logger.info("MQTT - connected")
        self.subscribe(self.topic)

    def subscribe(self, topic):
        self.client.subscribe(topic)
        logger.info("MQTT - Subscribed to topic '" + topic)

    def publish(self, topic, payload):
        logger.info("MQTT - Published message '" + str(payload) + "' on topic '" + topic)
        self.client.publish(topic, payload=payload)
        # self.client.loop_stop()

    def stop(self):
        logger.info("MQTT - Disconnecting from mqtt broker and cleaning up")
        self.client.disconnect()






# mqttc = mqtt.Client()
#     ssl_context= ssl_alpn()
#     mqttc.tls_set_context(context=ssl_context)
#     logger.info("start connect")
#     mqttc.connect(aws_iot_endpoint, port=443)
#     logger.info("connect success")
    
#     mqttc.subscribe('wc/#')
#     mqttc.loop_start()


#
#
# # The callback for when the client receives a CONNACK response from the server.
# def on_connect(client, userdata, flags, rc):
#     logger.info("connected")
#     logger.info("Connected with result code "+str(rc))
#
#     # Subscribing in on_connect() means that if we lose the connection and
#     # reconnect then subscriptions will be renewed.
#     client.subscribe("IW/V1/OTP")
#     # client.subscribe("testtopic/1")
#
#
# # The callback for when a PUBLISH message is received from the server.
# def on_message(client, userdata, msg):
#     import json
#     data = json.loads(str(msg.payload.decode('utf-8')))
#     logger.info("MQTT data {}".format(data))
#     # logger.info(msg.topic + " " + data)
#     site_id = data["token"]
#     device_id = data["deviceid"]
#     panelid = data["panelid"] if data["panelid"] else None
#     atmid = data["atmid"] if data["atmid"] else None
#     logger.info("site_id {}".format(site_id))
#     logger.info("panelid {}".format(panelid))
#     logger.info("atmid {}".format(atmid))
#
#     try:
#         if panelid and atmid:
#             add_device = "insert into iwater_device (device_name1, serial_no1, device_name2, serial_no2, site_id) " \
#                          "values (%s ,%s, %s, %s, %s);"
#             device_data = (device_id, panelid, device_id, atmid, site_id)
#             cursor.execute(add_device, device_data)
#
#             update_site = "update  iwater_site set is_treatment_unit=1 where id=%s;"
#             site_data = (site_id,)
#             cursor.execute(update_site, site_data)
#
#             update_site = "update  iwater_site set is_dispensing_unit=1 where id=%s;"
#             site_data = (site_id,)
#             cursor.execute(update_site, site_data)
#
#             update_subscription = "update  iwater_subscription set is_treatment_unit=1 where site_id=%s;"
#             site_data = (site_id,)
#             cursor.execute(update_subscription, site_data)
#
#             update_subscription = "update  iwater_subscription set is_dispensing_unit=1 where site_id=%s;"
#             site_data = (site_id,)
#             cursor.execute(update_subscription, site_data)
#
#             logger.info("Both")
#         elif panelid:
#             add_device = "insert into iwater_device (device_name1, serial_no1, site_id) values (%s, %s, %s);"
#             device_data = (device_id, panelid, site_id)
#             cursor.execute(add_device, device_data)
#
#             update_site = "update  iwater_site set is_treatment_unit=1 where id=%s;"
#             site_data = (site_id,)
#             cursor.execute(update_site, site_data)
#
#             update_subscription = "update  iwater_subscription set is_treatment_unit=1 where site_id=%s;"
#             site_data = (site_id,)
#             cursor.execute(update_subscription, site_data)
#
#             # cnx.commit()
#
#         elif atmid:
#             add_device = "insert into iwater_device (device_name1, serial_no1, site_id) values (%s, %s, %s);"
#             device_data = (device_id, atmid, site_id)
#             cursor.execute(add_device, device_data)
#
#             update_site = "update  iwater_site set is_dispensing_unit=1 where id=%s;"
#             site_data = (site_id,)
#             cursor.execute(update_site, site_data)
#
#             update_subscription = "update  iwater_subscription set is_dispensing_unit=1 where site_id=%s;"
#             site_data = (site_id,)
#             cursor.execute(update_subscription, site_data)
#             # cnx.commit()
#         cnx.commit()
#     except Exception as err:
#         logger.info(err)
#
#
# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message
#
# client.connect("broker.mqttdashboard.com", 1883, 60)
# client.publish("my/test/topic", "iwater_test")
#
# cnx = mysql.connector.connect(user=USER, host=HOST, database=DB_NAME, passwd=PASSWORD)
# cursor = cnx.cursor()
#
#
# # cursor.close()
# # cnx.close()
# client.loop_forever()
