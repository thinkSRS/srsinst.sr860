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


class SetReferenceToDualTask(Task):
    """
Change the reference source to the dual mode.
    """
    InstName = 'inst to control'
    InternalFrequency = 'Internal Frequency (Hz)'
    Phase = 'phase (degree)'
    Harmonic = 'harmonic'
    TriggerMode = 'external trigger mode'
    TriggerInput = 'external trigger input'
    HarmonicsDual = 'harmonic dual'

    input_parameters = {
        InstName:          InstrumentInput(),
        InternalFrequency: CommandInput('ref.internal_frequency'),
        Phase:             CommandInput('ref.phase'),
        Harmonic:          CommandInput('ref.harmonic'),
        TriggerMode:       CommandInput('ref.trigger_mode'),
        TriggerInput:      CommandInput('ref.trigger_input'),
        HarmonicsDual:     CommandInput('ref.harmonic_dual'),
    }

    def setup(self):
        self.logger = self.get_logger(__name__)
        self.params = self.get_all_input_parameters()
        self.lockin = get_sr860(self, self.params[self.InstName])
        self.delay = 0.5

    def test(self):
        self.lockin.ref.reference_source = Keys.Dual
        time.sleep(self.delay)

        frequency = self.lockin.ref.frequency
        phase = self.lockin.ref.phase
        harmonic = self.lockin.ref.harmonic
        trigger_mode = self.lockin.ref.timebase_mode
        trigger_input = self.lockin.ref.trigger_input
        harmonic_dual = self.lockin.ref.harmonic_dual

        self.logger.info('Reference source is set to {}.'.format(self.lockin.ref.reference_source))
        self.logger.info('internal frequency: {:.6e} Hz, phase: {:.3f} degree, harmonic order to detect: {}'
                         .format(frequency, phase, harmonic))
        self.logger.info('Trigger mode: {}, trigger input: {}, harmonic dual: {}'
                         .format(trigger_mode, trigger_input, harmonic_dual))

    def cleanup(self):
        pass
