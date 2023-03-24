
from srsgui import Task
from srsgui import BoolInput, IntegerListInput, FloatListInput, InstrumentInput, CommandInput
from srsinst.sr860 import SR860, get_sr860

from srsinst.sr860.instruments.components import Signal
from srsinst.sr860.instruments.keys import Keys


class SignalToVoltageModeTask(Task):
    """
It sets the input mode to the voltage inout mode. \
Make sure the signal is connected to the voltage input connector A or \
both A and B on the front panel.
    """
    InstName = 'inst to change'
    InputMode = 'input mode'
    InputCoupling = 'input coupling'
    InputShield = 'input shield'
    InputRange = 'input range (V)'
    InputSens = 'input sensitivity (V)'
    TimeConstant = 'time constant (s)'
    FilterSlope = 'filter slope (dB/oct)'
    SyncFilter = 'synchronous filter'
    AdvancedFilter = 'advanced filter'

    input_parameters = {
        InstName:       InstrumentInput(),
        InputMode:      CommandInput('signal.voltage_input_mode', Signal.voltage_input_mode),
        InputCoupling:  CommandInput('signal.voltage_input_coupling', Signal.voltage_input_coupling),
        InputShield:    CommandInput('signal.voltage_input_shield', Signal.voltage_input_shield),
        InputRange:     CommandInput('signal.voltage_input_range', Signal.voltage_input_range),
        InputSens:      CommandInput('signal.voltage_sensitivity', Signal.voltage_sensitivity),
        TimeConstant:   CommandInput('signal.time_constant', Signal.time_constant),
        FilterSlope:    CommandInput('signal.filter_slope', Signal.filter_slope),
        SyncFilter:     CommandInput('signal.sync_filter', Signal.sync_filter),
        AdvancedFilter: CommandInput('signal.advanced_filter', Signal.advanced_filter)
    }

    def setup(self):
        self.logger = self.get_logger(__name__)
        self.params = self.get_all_input_parameters()
        self.lockin = get_sr860(self, self.params[self.InstName])

    def test(self):
        # Change to Voltage mode
        self.lockin.signal.input_mode = Keys.Voltage
        self.logger.info(self.params)
        self.logger.info('Input mode change to the voltage mode')

    def cleanup(self):
        pass
