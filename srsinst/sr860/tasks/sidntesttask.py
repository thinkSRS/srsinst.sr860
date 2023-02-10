
import time
import logging
import socket
import struct
import threading

from srsgui import Task
from srsgui import IntegerInput, ListInput
from srsinst.sr860 import SR860, get_sr860


class SidnTask(Task):
    """
    Check the time taken for 100 *IDN queries
    to check communication speed
    """

    input_parameters = {}
    Repeat = 100

    def setup(self):
        self.logger = logging.getLogger(__file__)
        self.lia = get_sr860(self)
        
        print(self.lia.query_text('*idn?'))

        # Mark the time 0
        self.init_time = time.time()

    def test(self):
        start_time = time.time()
        for i in range(self.Repeat):
            print(self.lia.query_text('*idn?'))
        finish_time = time.time()
        print('Time for {} *idn: {}'.format(self.Repeat, finish_time - start_time))

    def cleanup(self):
        pass

