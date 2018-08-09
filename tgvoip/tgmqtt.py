#!/usr/bin/env python3
# Telegram VOIP calls via mqtt
# Gabriel Jacobo <gabomdq@gmail.com>
# https://mdqinc.com
# License: zlib

import logging
import argparse
import os
import json
import base64
from telegram.client import Telegram as _Telegram
from telegram.utils import AsyncResult
from tgvoip import call_start, call_stop
import paho.mqtt.client as paho_mqtt

mqtt = paho_mqtt.Client()

class Telegram(_Telegram):
    def __init__(self, mqtt_client, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mqtt = mqtt_client
        self.code = None
        self.call_id = None
        self.incoming_call_id = None
        self.add_handler(self._tghandler)

    def _call_start(self, data):
        # state['config'] is passed as a string, convert to object
        data['state']['config'] = json.loads(data['state']['config'])
        # encryption key is base64 encoded
        data['state']['encryption_key'] = base64.decodebytes(data['state']['encryption_key'].encode('utf-8'))
        # peer_tag is base64 encoded
        for conn in data['state']['connections']:
            conn['peer_tag'] = base64.decodebytes(conn['peer_tag'].encode('utf-8'))
        call_start(data)

    def voip_call(self, user_id):
        if self._authorized and self.call_id is None and self.incoming_call_id is None:
            r = self.call_method('createCall', {'user_id': user_id, 'protocol': {'udp_p2p': True, 'udp_reflector': True, 'min_layer': 65, 'max_layer': 65} })
            r.wait()
            self.call_id = r.update['id']

    def voip_call_stop(self):
        if self.call_id is not None:
            self.call_method('discardCall', {'call_id': self.call_id})

    def voip_call_answer(self):
        if self.incoming_call_id is not None:
            self.call_method('acceptCall', {'call_id': self.incoming_call_id, 'protocol': {'udp_p2p': True, 'udp_reflector': True, 'min_layer': 65, 'max_layer': 65} })

    def publish(self, topic, payload=""):
        self.mqtt.publish("telegram/" + topic, payload)

    def _tghandler(self, msg):
        #print ("UPDATE >>>", msg)
        if msg['@type'] == 'updateCall':
            data = msg['call']
            self.publish("call/%d/state" % data['id'], data['state']['@type'])
            if data['state']['@type'] == 'callStateReady':
                self.call_id = data['id']
                self.incoming_call_id = None
                self._call_start(data)
            elif data['state']['@type'] == 'callStatePending' and data['is_outgoing'] is False:
                # Incoming call
                self.publish("call/incoming", data['user_id'])
                self.incoming_call_id = data['id']
            elif data['state']['@type'] == 'callStateDiscarded':
                call_stop()
                self.call_id = None

    def _send_telegram_code(self) -> AsyncResult:
        # Wait for the code to arrive via mqtt
        self.publish("code/request")
        print ("Waiting for Telegram Auth Code via MQTT")
        while self.code is None:
            self.mqtt.loop()
        data = {
            '@type': 'checkAuthenticationCode',
            'code': str(self.code),
        }
        return self._send_data(data, result_id='updateAuthorizationState')

def mqtt_connect(client, userdata, flags, rc):
    client.subscribe("telegram/#")

# The callback for when a PUBLISH message is received from the server.
def mqtt_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    print(msg.topic+" "+payload)
    if msg.topic == "telegram/code":
        tg.code = payload
    elif msg.topic == "telegram/call":
        tg.voip_call(payload)
    elif msg.topic == "telegram/call/disconnect":
        tg.voip_call_stop()
    elif msg.topic == "telegram/call/answer":
        tg.voip_call_answer()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Config File', default='/data/options.json')
    parser.add_argument('-d', '--data', help='Data Directory (if not provided it will be configured from the options file)', default=None)
    args = parser.parse_args()
    
    with open(args.config, 'rb') as config_file:
        config = json.load(config_file)

    files_dir = args.data if args.data is not None else config['data_dir']
    files_dir = os.path.join(os.path.expanduser(files_dir), config['phone'])
    tg = Telegram(
                api_id=config['api_id'],
                api_hash=config['api_hash'],
                phone=config['phone'],
                td_verbosity=3,
                files_directory = files_dir,
                database_encryption_key=config['database_key'],
                #use_test_dc = True,
                mqtt_client = mqtt,
                )

    mqtt.on_connect = mqtt_connect
    mqtt.on_message = mqtt_message
    mqtt.connect(config['mqtt_server'])

    tg.login()
    r = tg.get_chats()
    r.wait()
    

    while True:
        mqtt.loop()


