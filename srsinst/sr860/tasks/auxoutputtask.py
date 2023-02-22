import time
import logging

from srsgui import Task
from srsgui import BoolInput, IntegerListInput, FloatListInput, InstrumentInput, CommandInput
from srsinst.sr860 import SR860, get_sr860

from srsinst.sr860.instruments.components import Aux
from srsinst.sr860.instruments.keys import Keys


class AuxOutputTask(Task):
    """
    When the task is selected, it reads the current auxiliary output values from the unit. \
Adjust the output values from the input panel, and press the adjust button. \
It will change the aux output values, even without running the task.
    """

    InstName = 'inst to change'
    Ch1 = 'channel 1 (V)'
    Ch2 = 'channel 2 (V)'
    Ch3 = 'channel 3 (V)'
    Ch4 = 'channel 4 (V)'

    input_parameters = {
        InstName: InstrumentInput(),
        Ch1:      CommandInput(f'aux.output[0]', Aux.output),
        Ch2:      CommandInput(f'aux.output[1]', Aux.output),
        Ch3:      CommandInput(f'aux.output[2]', Aux.output),
        Ch4:      CommandInput(f'aux.output[3]', Aux.output),
    }

    def setup(self):
        self.logger = logging.getLogger(__file__)
        self.lockin = get_sr860(self, self.get_input_parameter(self.InstName))

    def test(self):

        self.params = self.get_all_input_parameters()
        self.logger.info(self.params)
        self.logger.info('Set aux outputs')

    def cleanup(self):
        pass
