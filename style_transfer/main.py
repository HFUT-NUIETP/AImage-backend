from utils.options import StyleOptions
from utils.test import *

import time

if __name__ == '__main__':
    config = StyleOptions().config

    time_begin = time.time()
    im_stylized = test_and_save(config=config)
    time_end = time.time()
    print('Time Cost: ', time_end-time_begin)
