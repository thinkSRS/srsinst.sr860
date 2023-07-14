##! 
##! Copyright(c) 2023 Stanford Research Systems, All rights reserved
##! Subject to the MIT License
##! 

import time

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
        self.logger = self.get_logger(__name__)
        self.lockin = get_sr860(self)
        
        print(self.lockin.query_text('*idn?'))

        print('Start capturing commands...')
        capture = self.lockin.capture_commands(True)
        self.session_handler.add_dict_to_file('command capture', capture)
        print('Finished capturing commands...')

        # Mark the time 0
        self.init_time = time.time()

    def test(self):
        start_time = time.time()
        for i in range(self.Repeat):
            print(self.lockin.query_text('*idn?'))
        finish_time = time.time()
        print('Time for {:.3f} *idn: {} s'.format(self.Repeat, finish_time - start_time))

    def cleanup(self):
        pass

