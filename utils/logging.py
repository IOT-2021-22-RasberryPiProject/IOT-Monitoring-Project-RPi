import logging
import time


logging.basicConfig(filename='logs.log',
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

LOGGER = logging.getLogger(__name__)


def log_fps(func):
    def _wrapper(*args, **kwargs):
        start_time = time.time()
        return_value = func(*args, **kwargs)
        end_time = time.time()
        fps = round(1 / (end_time - start_time), 2)
        LOGGER.debug(f'FPS:{fps}')
        return return_value
    return _wrapper


if __name__ == '__main__':
    @log_fps
    def dummy(i):
        print('Dunno')
        time.sleep(i)

    dummy(5)
    dummy(7)        
