import time
import logging

from srsgui import Task
from srsgui import InstrumentInput, ListInput
from srsinst.sr860 import SR860, get_sr860

from srsinst.sr860.instruments.components import Aux
from srsinst.sr860.instruments.keys import Keys


class AutoFunctionTask(Task):
    """
    Run one of the auto functions: auto phase, auto range, or auto scale.
    """

    InstName = 'inst to change'
    FunctionSelection = 'Select Auto function to run'
    Functions = ['Phase', 'Range', 'Scale']

    input_parameters = {
        InstName:       InstrumentInput(),
        FunctionSelection: ListInput(Functions)
    }

    def setup(self):
        self.logger = logging.getLogger(__file__)
        self.lockin = get_sr860(self, self.get_input_parameter(self.InstName))
        self.params = self.get_all_input_parameters()

    def test(self):
        chosen = self.params[self.FunctionSelection]
        if chosen == 'Phase':
            self.lockin.auto.set_phase()
        elif chosen == 'Range':
            self.lockin.auto.set_range()
        elif chosen == 'Scale':
            self.lockin.auto.set_scale()
        else:
            self.logger.error('unknown option "{}"'.format(chosen))

        self.logger.info(self.params)
        self.logger.info('Auto {} has run.'.format(chosen))

    def cleanup(self):
        pass
