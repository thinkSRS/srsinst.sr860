from srsgui import Task
from srsgui import ListInput, InstrumentInput, CommandInput

from srsinst.sr860 import SR860, get_sr860
from srsinst.sr860.instruments.components import Display


class AssignParameterToChannel(Task):
    """
    Assign a parameter to a channel
    """
    InstName = 'inst to control'
    Channel1 = 'channel 1'
    Channel2 = 'channel 2'
    Channel3 = 'channel 3'
    Channel4 = 'channel 4'

    input_parameters = {
        InstName: InstrumentInput(),
        Channel1: CommandInput('display.config[0]'),
        Channel2: CommandInput('display.config[1]'),
        Channel3: CommandInput('display.config[2]'),
        Channel4: CommandInput('display.config[3]'),
    }

    def setup(self):
        self.logger = self.get_logger(__name__)
        self.params = self.get_all_input_parameters()
        self.lockin = get_sr860(self, self.params[self.InstName])

    def test(self):
        self.logger.info(self.params)

    def cleanup(self):
        pass



