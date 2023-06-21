import time

from srsgui import Task
from srsgui import BoolInput, IntegerListInput, FloatListInput, InstrumentInput, CommandInput
from srsinst.sr860 import SR860, get_sr860

from srsinst.sr860.instruments.components import Aux
from srsinst.sr860.instruments.keys import Keys


class AuxOutputTask(Task):
    """
It will change the aux output values when the Apply button is pressed, \
even without running the task.
    """

    InstName = 'inst to change'
    Ch1 = 'channel 1 (V)'
    Ch2 = 'channel 2 (V)'
    Ch3 = 'channel 3 (V)'
    Ch4 = 'channel 4 (V)'

    input_parameters = {
        InstName: InstrumentInput(),
        Ch1:      CommandInput(f'aux.output[0]'),
        Ch2:      CommandInput(f'aux.output[1]'),
        Ch3:      CommandInput(f'aux.output[2]'),
        Ch4:      CommandInput(f'aux.output[3]'),
    }

    def setup(self):
        self.logger = self.get_logger(__name__)
        self.lockin = get_sr860(self, self.get_input_parameter(self.InstName))

    def test(self):

        self.params = self.get_all_input_parameters()
        self.logger.info('Aux output values')
        self.logger.info(self.params)

    def cleanup(self):
        pass
