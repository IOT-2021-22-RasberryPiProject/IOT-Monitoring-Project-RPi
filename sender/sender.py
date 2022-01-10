from typing import *
import time
import binascii

import cv2
import numpy as np
from paho.mqtt.client import Client
import json

from config import AttributeDict
from utils import log_fps



class Sender:

    def __init__(self, config: AttributeDict) -> None:
        self._config = config

        self._client = Client()
        self._camera = cv2.VideoCapture(self._config.camera_id)
        self._try_connect(self._config.broker_ip)


    def start(self) -> None:
        try:
            while True:
                self._inner_read()
        except KeyboardInterrupt:
            self._camera.release()
            self._client.disconnect()
            print('Disconected')

    @log_fps
    def _inner_read(self) -> None:
        _, frame = self._camera.read()
        if frame is not None:
            if self._config.reverse:
                frame = np.flipud(frame)
            message = self._get_message(frame)
            self._client.publish(self._config.topic, message)
            time.sleep(self._config.latence)
    
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

    