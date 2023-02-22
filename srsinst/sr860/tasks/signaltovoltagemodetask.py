import time
import logging

from srsgui import Task
from srsgui import BoolInput, IntegerListInput, FloatListInput, InstrumentInput, CommandInput
from srsinst.sr860 import SR860, get_sr860

from srsinst.sr860.instruments.components import Signal
from srsinst.sr860.instruments.keys import Keys


class SignalToVoltageModeTask(Task):
    """
When the task is selected, the relevant parameters are read from the unit, \
and updates the input panel display. The values in the unit will change, when the \
Apply button is pressed.

When this task runs, it sets the input mode to the voltage inout mode.
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
        self.logger = logging.getLogger(__file__)
        self.lockin = get_sr860(self, self.get_input_parameter(self.InstName))

    def test(self):
        # Change to Voltage mode
        self.lockin.signal.input_mode = Keys.Voltage

        self.logger.info(self.get_all_input_parameters())
        self.logger.info('Input mode change to the voltage mode')

    def cleanup(self):
        pass
