from typing import *


class AttributeDict(dict):
    """
    Class allowing access dictionary items as properties. 
    For example:
    
    my_dict = AttributeDict({'name': 'Adam', 'salary': 30})
    print(my_dict.name)
    >> Adam
    print(my_dict.salary)
    >> 30
    my_dict.profession = 'Worker'
    print(my_dict.profession)
    >> Worker

    """
    __slots__ = () 
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


config_data = {
    'device': 'CAMERA0',
    'broker_ip': '192.168.0.192',
    'topic': 'monitoring/frame',
    'camera_id': 0,
    'frame_size': (224, 224),
    'latence': 0.00,
    'grayscale': False,
    'reverse': True
}


CONFIG = AttributeDict(config_data)

if __name__ == '__main__':
    a = AttributeDict({'A': '1'})
    a['B'] = '2'
    a.C = 20
    print(a.items())

