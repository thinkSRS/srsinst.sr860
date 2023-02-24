import time
import logging

from srsgui import Task
from srsgui import BoolInput, IntegerListInput, FloatListInput, InstrumentInput, CommandInput
from srsinst.sr860 import SR860, get_sr860

from srsinst.sr860.instruments.components import Signal, Reference
from srsinst.sr860.instruments.keys import Keys


class SetReferenceToExternalTask(Task):
    """
Change the reference source to the external.
    """
    InstName = 'inst to control'
    TriggerMode = 'trigger mode'
    TriggerInput = 'trigger input'
    Phase = 'phase (degree)'
    Harmonic = 'harmonic to detect'
    RunAutoPhase = "run auto phase"

    input_parameters = {
        InstName: InstrumentInput(),
        TriggerMode: CommandInput('ref.trigger_mode', Reference.trigger_mode),
        TriggerInput: CommandInput('ref.trigger_input', Reference.trigger_input),
        Phase: CommandInput('ref.phase', Reference.phase),
        Harmonic: CommandInput('ref.harmonic', Reference.harmonic),
        RunAutoPhase: BoolInput()
    }

    def setup(self):
        self.logger = logging.getLogger(__file__)
        self.params = self.get_all_input_parameters()
        self.lockin = get_sr860(self, self.params[self.InstName])
        self.delay = 0.5

    def test(self):
        self.lockin.ref.reference_source = Keys.External
        time.sleep(self.delay)
        auto = self.params[self.RunAutoPhase]
        if auto:
            self.lockin.ref.auto_phase()
            time.sleep(self.delay)

        frequency = self.lockin.ref.frequency
        phase = self.lockin.ref.phase
        harmonic = self.lockin.ref.harmonic
        trigger_mode = self.lockin.ref.timebase_mode
        trigger_input = self.lockin.ref.trigger_input

        self.logger.info('Reference source is set to {}.'.format(self.lockin.ref.reference_source))
        self.logger.info('Trigger mode: {}, trigger input: {}'.format(trigger_mode, trigger_input))
        self.logger.info('frequency: {:.6e} Hz, phase: {:.3f} degree, harmonic order to detect: {}'
                         .format(frequency, phase, harmonic))

    def cleanup(self):
        pass
