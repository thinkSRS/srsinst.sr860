import time
from srsgui import Task
from srsgui import BoolInput, IntegerListInput, FloatListInput, InstrumentInput, CommandInput
from srsinst.sr860 import SR860, get_sr860

from srsinst.sr860.instruments.components import Signal, Reference
from srsinst.sr860.instruments.keys import Keys


class SetReferenceToInternalTask(Task):
    """
Change the reference source to the internal oscillator.
    """
    InstName = 'inst to control'
    InternalFrequency = 'Frequency to set (Hz)'
    Phase = 'phase (degree)'
    Harmonic = 'harmonic to detect'
    RunAutoPhase = "run auto phase"

    input_parameters = {
        InstName:          InstrumentInput(),
        InternalFrequency: CommandInput('ref.internal_frequency'),
        Phase:             CommandInput('ref.phase'),
        Harmonic:          CommandInput('ref.harmonic'),
        RunAutoPhase:      BoolInput()
    }

    def setup(self):
        self.logger = self.get_logger(__name__)
        self.params = self.get_all_input_parameters()
        self.lockin = get_sr860(self, self.params[self.InstName])
        self.delay = 0.5

    def test(self):
        self.lockin.ref.reference_source = Keys.Internal
        auto = self.params[self.RunAutoPhase]
        if auto:
            self.lockin.ref.auto_phase()
            time.sleep(self.delay)

        frequency = self.lockin.ref.frequency
        phase = self.lockin.ref.phase
        harmonic = self.lockin.ref.harmonic

        self.logger.info('Reference source is set to {}.'.format(self.lockin.ref.reference_source))
        self.logger.info('frequency: {:.6e} Hz, phase: {:.3f} degree, harmonic order to detect: {}'
                         .format(frequency, phase, harmonic))

    def cleanup(self):
        pass
