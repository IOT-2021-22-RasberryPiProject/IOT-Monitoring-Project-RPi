import base64
from typing import *
import time
import binascii

import cv2
import numpy as np
from paho.mqtt.client import Client
import json

from config import AttributeDict



class Sender:

    def __init__(self, config: AttributeDict) -> None:
        self._config = config

        self._client = Client()
        self._camera = cv2.VideoCapture(self._config.camera_id)
        self._try_connect(self._config.broker_ip)


    def start(self) -> NoReturn:
        try:
            while True:
                start_time = time.time()
                _, frame = self._camera.read()
                if frame is not None:
                    message = self._get_message(frame)
                    self._client.publish(self._config.topic, message)
                    end_time = time.time()
                    print(f'FPS: {1 / (end_time - start_time)}')
        except KeyboardInterrupt:
            self._camera.release()
            self._client.disconnect()
            print('Disconected')

    
    def _get_message(self, frame: np.ndarray) -> str:
        _, buffer = cv2.imencode('.jpg', cv2.resize(frame, self._config.frame_size))
        message = {
            'device': self._config.device,
            'time': time.time(),
            'frame': binascii.b2a_base64(buffer).decode()
        }
        message_encoded = json.dumps(message)
        return message_encoded
    
    def _try_connect(self, broker_ip: str) -> None:
        try:
            self._client.connect(broker_ip)
        except Exception as e:
            print(e)

    