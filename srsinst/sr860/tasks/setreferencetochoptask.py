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


class SetReferenceToChopTask(Task):
    """
Change the reference source to the internal oscillator and servo \
SR530 chopper connected to the aux output channel 4 in the rear panel.
    """
    InstName = 'lock-in to control'
    InternalFrequency = 'internal F (Hz)'
    Phase = 'phase (degree)'
    Harmonic = 'harmonic to detect'

    BladeSlots = 'blade slots (/rev.)'
    BladePhase = 'blade phase (degree)'
    RunAutoPhase = "run auto phase"

    input_parameters = {
        InstName:          InstrumentInput(),
        InternalFrequency: CommandInput('ref.internal_frequency'),
        Phase:             CommandInput('ref.phase'),
        Harmonic:          CommandInput('ref.harmonic'),
        BladeSlots:        CommandInput('ref.blade_slots'),
        BladePhase:        CommandInput('ref.blade_phase'),
        RunAutoPhase:      BoolInput()
    }

    def setup(self):
        self.logger = self.get_logger(__name__)
        self.params = self.get_all_input_parameters()
        self.lockin = get_sr860(self, self.params[self.InstName])
        self.delay = 0.5

    def test(self):
        self.lockin.ref.reference_source = Keys.Chop
        time.sleep(self.delay)
        auto = self.params[self.RunAutoPhase]
        if auto:
            self.lockin.ref.auto_phase()
            time.sleep(self.delay)

        frequency = self.lockin.ref.frequency
        phase = self.lockin.ref.phase
        harmonic = self.lockin.ref.harmonic
        blade_slots = self.lockin.ref.blade_slots
        blade_phase = self.lockin.ref.blade_phase

        self.logger.info('Reference source is set to {} mode.'.format(self.lockin.ref.reference_source))
        self.logger.info('frequency: {:.6e} Hz, phase: {:.3f} degree, harmonic order to detect: {}'
                         .format(frequency, phase, harmonic))
        self.logger.info('Blade slots: {}, blade phase: {} degree'.format(blade_slots, blade_phase))

    def cleanup(self):
        pass
