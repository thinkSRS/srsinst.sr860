import time
import logging

from srsgui import Task
from srsgui import BoolInput, IntegerListInput, FloatListInput
from srsinst.sr860 import SR860, get_sr860

from srsinst.sr860.instruments.components import Signal


class SignalToCurrentModeTask(Task):
    """
When this task runs, it sets the input mode to the current inout mode, \
reads the relevant parameters from the unit, and updates the input panel display. \
It waits until you press the Apply button.

You change parameters to the values you want, and press the Apply button. \
After it updates the parameters in the unit, and finishes the task.

Note that its input panel behaves differently from typical usage.
    """

    InputGain = 'input gain (Ohm)'
    Sensitivity = 'sensitivity (A)'
    TimeConstant = 'time constant (s)'
    FilterSlope = 'filter slope (dB/oct)'
    SyncFilter = 'synchronous filter'
    AdvancedFilter = 'advanced filter'
    OffOnList = ['Off', 'On,']
    input_parameters = {
        InputGain:      FloatListInput(Signal.CurrentInputGainDict.keys(),  '{:.0e}'),
        Sensitivity:    FloatListInput(Signal.CurrentSensitivityDict.keys(), '{:.0e}'),
        TimeConstant:   FloatListInput(Signal.TimeConstantDict.keys(), '{:.0e}', 6),
        FilterSlope:    IntegerListInput(Signal.FilterSlopeDict.keys()),
        SyncFilter:     BoolInput(OffOnList),
        AdvancedFilter: BoolInput(OffOnList)
    }

    def setup(self):
        self.logger = logging.getLogger(__file__)
        self.lockin = get_sr860(self)

        self.params = self.get_all_input_parameters()  # get values from the input panel
        self.params_before = self.get_all_input_parameters()
        print('Wait while reading current input mode parameters...')

        self.params[self.InputGain] = self.lockin.signal.current_input_gain
        self.params[self.Sensitivity] = self.lockin.signal.current_sensitivity
        self.params[self.TimeConstant] = self.lockin.signal.time_constant
        self.params[self.FilterSlope] = self.lockin.signal.filter_slope
        self.params[self.SyncFilter] = self.lockin.signal.sync_filter
        self.params[self.AdvancedFilter] = self.lockin.signal.advanced_filter

        for name in self.params:
            self.set_input_parameter(name, self.params[name])
        self.notify_parameter_changed()  # it updates the input panel.
        print(self.params)
        print('Adjust parameters and press Apply.')

    def test(self):
        while self.is_running():
            changed = False
            self.params = self.get_all_input_parameters()
            for name in self.params:
                if self.params[name] != self.params_before[name]:
                    changed = True
                    break
            if changed:
                self.lockin.signal.current_input_gain = self.params[self.InputGain]
                self.lockin.signal.current_sensitivity = self.params[self.Sensitivity]
                self.lockin.signal.time_constant = self.params[self.TimeConstant]
                self.lockin.signal.filter_slope = self.params[self.FilterSlope]
                self.lockin.signal.sync_filter = self.params[self.SyncFilter]
                self.lockin.signal.advanced_filter = self.params[self.AdvancedFilter]
                print(self.params)
                print('Parameters changed')
                break
            time.sleep(0.1)

    def cleanup(self):
        pass
