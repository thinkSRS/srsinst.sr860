
from srsgui import Task
from srsgui import BoolInput, IntegerListInput, FloatListInput, InstrumentInput, CommandInput
from srsinst.sr860 import SR860, get_sr860

from srsinst.sr860.instruments.components import Signal
from srsinst.sr860.instruments.keys import Keys


class SignalToCurrentModeTask(Task):
    """
It sets the input mode to the current inout mode. \
Make sure the signal is connected to the current input connector on the front panel.
    """
    InstName = 'inst to change'
    InputGain = 'input gain (Ohm)'
    Sensitivity = 'sensitivity (A)'
    TimeConstant = 'time constant (s)'
    FilterSlope = 'filter slope (dB/oct)'
    SyncFilter = 'synchronous filter'
    AdvancedFilter = 'advanced filter'

    input_parameters = {
        InstName:       InstrumentInput(),
        InputGain:      CommandInput('signal.current_input_gain'),
        Sensitivity:    CommandInput('signal.current_sensitivity'),
        TimeConstant:   CommandInput('signal.time_constant'),
        FilterSlope:    CommandInput('signal.filter_slope'),
        SyncFilter:     CommandInput('signal.sync_filter'),
        AdvancedFilter: CommandInput('signal.advanced_filter'),
    }

    def setup(self):
        self.logger = self.get_logger(__name__)
        self.params = self.get_all_input_parameters()
        self.lockin = get_sr860(self, self.params[self.InstName])

    def test(self):
        self.lockin.signal.input_mode = Keys.Current
        self.logger.info(self.params)
        self.logger.info('Input mode change to the current mode')

    def cleanup(self):
        pass
