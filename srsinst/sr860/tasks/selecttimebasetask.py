
from srsgui import Task
from srsgui import BoolInput, IntegerListInput, FloatListInput, InstrumentInput, CommandInput
from srsinst.sr860 import SR860, get_sr860

from srsinst.sr860.instruments.components import Signal, Reference
from srsinst.sr860.instruments.keys import Keys


class SelectTimebaseTask(Task):
    """
The internal timebase provides 25 ppm + 30 uHz accuracy. For better accuracy, \
you can connect an external 10 MHz clock to the timebase input/output connector \
on the rear panel, and select external timebase. Selecting the external source
without an external 10 MHz clock will automatically run with the internal oscillator.
    """

    InstName = 'inst to control'
    TimebaseMode = 'timebase mode'
    TimebaseSource = 'timebase source'

    input_parameters = {
        InstName:       InstrumentInput(),
        TimebaseSource: CommandInput('ref.timebase_source'),
    }

    def setup(self):
        self.logger = self.get_logger(__name__)
        self.params = self.get_all_input_parameters()
        self.lockin = get_sr860(self, self.params[self.InstName])

    def test(self):
        if self.params[self.TimebaseSource] == Keys.External:
            self.lockin.ref.timebase_mode = Keys.Auto
            self.lockin.ref.timebase_source = Keys.External
            self.logger.info('Timebase is set to Auto / External.')
        else:
            self.lockin.ref.timebase_mode = Keys.Internal
            self.lockin.ref.timebase_source = Keys.Internal
            self.logger.info('Timebase is set to the internal oscillator.')

    def cleanup(self):
        pass
