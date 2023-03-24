import time

from srsgui import Task
from srsgui import BoolInput, IntegerListInput, FloatListInput, InstrumentInput, CommandInput
from srsinst.sr860 import SR860, get_sr860

from srsinst.sr860.instruments.components import Signal, Reference
from srsinst.sr860.instruments.keys import Keys


class ConfigureReferenceTask(Task):
    """
The task shows all parameters in Reference component
Adjust values and press the Apply button.
    """
    InstName = 'inst to change'
    TimebaseMode = 'timebase mode'
    TimebaseSource = 'timebase source'
    InternalFrequency = 'internal F (Hz)'
    Phase = 'phase (degree)'
    Harmonics = 'harmonics'
    HarmonicsDual = 'harmonics dual'
    BladeSlots = 'blade slots (/rev.)'
    BladePhase = 'blade phase (degree)'
    SineAmplitude = 'sine amplitude (V)'
    SineOffset = 'sine dc level (V)'
    SineDCMode = 'sine dc mode (V)'
    ReferenceSource = 'reference source'
    TriggerMode = 'trigger mode'
    TriggerInput = 'trigger input'

    input_parameters = {
        InstName:       InstrumentInput(),
        TimebaseMode:   CommandInput('ref.timebase_mode', Reference.timebase_mode),
        TimebaseSource: CommandInput('ref.timebase_source', Reference.timebase_source),
        InternalFrequency: CommandInput('ref.internal_frequency', Reference.internal_frequency),
        Phase: CommandInput('ref.phase', Reference.phase),
        Harmonics: CommandInput('ref.harmonics', Reference.harmonics),
        HarmonicsDual: CommandInput('ref.harmonics_dual', Reference.harmonics_dual),
        BladeSlots: CommandInput('ref.blade_slots', Reference.blade_slots),
        BladePhase: CommandInput('ref.blade_phase', Reference.blade_phase),
        SineAmplitude: CommandInput('ref.sine_out_amplitude', Reference.sine_out_amplitude),
        SineOffset: CommandInput('ref.sine_out_offset', Reference.sine_out_offset),
        SineDCMode: CommandInput('ref.sine_out_dc_mode', Reference.sine_out_dc_mode),
        ReferenceSource: CommandInput('ref.reference_source', Reference.reference_source),
        TriggerMode: CommandInput('ref.trigger_mode', Reference.trigger_mode),
        TriggerInput: CommandInput('ref.trigger_input', Reference.trigger_input),
    }

    def setup(self):
        self.logger = self.get_logger(__name__)
        self.lockin = get_sr860(self, self.get_input_parameter(self.InstName))

    def test(self):
        self.logger.info('Current Reference parameters')
        self.logger.info(self.get_all_input_parameters())

    def cleanup(self):
        pass
