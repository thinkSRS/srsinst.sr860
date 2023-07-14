##! 
##! Copyright(c) 2023 Stanford Research Systems, All rights reserved
##! Subject to the MIT License
##! 

import time

from srsgui import Task
from srsgui import BoolInput, IntegerListInput, FloatListInput, InstrumentInput, CommandInput
from srsinst.sr860 import SR860, get_sr860

from srsinst.sr860.instruments.components import Signal, Reference
from srsinst.sr860.instruments.keys import Keys


class ConfigureSineOutputTask(Task):
    """
Sine output is generated based on the frequency of the selected reference source.
    """
    InstName = 'inst to control'
    SineAmplitude = 'sine amplitude (V)'
    SineOffset = 'sine dc level (V)'
    SineDCMode = 'sine dc mode'

    input_parameters = {
        InstName:      InstrumentInput(),
        SineAmplitude: CommandInput('ref.sine_out_amplitude'),
        SineOffset:    CommandInput('ref.sine_out_offset'),
        SineDCMode:    CommandInput('ref.sine_out_dc_mode'),
    }

    def setup(self):
        self.logger = self.get_logger(__name__)
        self.params = self.get_all_input_parameters()
        self.lockin = get_sr860(self, self.params[self.InstName])

    def test(self):
        amplitude = self.lockin.ref.sine_out_amplitude
        offset = self.lockin.ref.sine_out_offset
        dc_mode = self.lockin.ref.sine_out_dc_mode
        self.logger.info('Sine output amplitude: {:.3f} V, offset: {:.3f} V, dc mode: {}'
                         .format(amplitude, offset, dc_mode))

    def cleanup(self):
        pass
