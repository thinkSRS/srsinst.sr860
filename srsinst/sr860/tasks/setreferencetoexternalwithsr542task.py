
import time

from srsgui import Task
from srsgui import BoolInput, IntegerListInput, FloatListInput, InstrumentInput, CommandInput

from srsinst.sr860 import get_sr860
from srsinst.sr860.instruments.components import Reference
from srsinst.sr860.instruments.keys import Keys as LKeys

from srsinst.sr542 import get_sr542
from srsinst.sr542.instruments.components import Config
from srsinst.sr542.instruments.keys import Keys as CKeys


class SetRefToExternalWithSR542Task(Task):
    """
Use the internal frequency of SR542 as reference source. \
To use the outer track of a blade, connect the outer track \
reference output connector or inner track for chopping.
Connect
Change the reference source of SR860 to the external and .
    """
    InstName = 'Lock-in to control'
    TriggerMode = 'trigger mode'
    TriggerInput = 'trigger input'
    Phase = 'phase (degree)'
    Harmonic = 'harmonic to detect'
    ChopperName = 'Chopper to control'
    FrequencySource = 'Frequency source'
    ControlTarget = 'control target'
    InternalF = 'internal frequency'
    BladePhase = 'blade phase'

    input_parameters = {
        InstName:      InstrumentInput(0),
        Phase:         CommandInput('ref.phase'),
        Harmonic:      CommandInput('ref.harmonic'),

        ChopperName:   InstrumentInput(1),
        ControlTarget: CommandInput('config.control_target'),
        InternalF:     CommandInput('config.frequency'),
        BladePhase:    CommandInput('config.phase'),
    }

    def setup(self):
        self.logger = self.get_logger(__name__)
        self.params = self.get_all_input_parameters()
        self.lockin = get_sr860(self, self.params[self.InstName])
        self.chopper = get_sr542(self, self.params[self.ChopperName])

        if self.chopper.config.control_target not in (CKeys.INNER, CKeys.OUTER):
            msg = 'Control target should be either "{}" or "{}, NOT "{}".'\
                .format(CKeys.INNER, CKeys.OUTER, self.params[self.ControlTarget])
            raise ValueError(msg)

    def test(self):
        self.lockin.ref.reference_source = LKeys.External
        self.lockin.ref.trigger_mode = LKeys.PositiveTTL
        self.lockin.ref.trigger_input = LKeys.R1Meg

        initial_motor_state = self.chopper.operate.motor_state

        # Change the reference source to internal
        if self.chopper.operate.motor_state == CKeys.ON and self.chopper.config.source != CKeys.INTERNAL:
            reply = self.ask_question("Is it OK to turn off the chopper \n"
                                      "to change the reference source to internal?")
            if not reply:
                self.logger.info("Aborted not to turn off chopper")
                return
            else:
                self.chopper.operate.motor_state = CKeys.OFF
                time.sleep(1.0)
                self.chopper.config.source = CKeys.INTERNAL

            self.logger.info('Turning back on the chopper')
            self.chopper.operate.motor_state = CKeys.ON
            time.sleep(3.0)

        chopper_f = lockin_f = 0.0
        if self.chopper.operate.motor_state == CKeys.OFF:
            reply = self.ask_question("Is it OK to turn on the chopper \n"
                                      "to check if the frequencies are matched \n"
                                      "between lock-in and the chopper?")
            if reply:
                self.chopper.operate.motor_state = CKeys.ON
                time.sleep(3.0)

            control_target = self.chopper.config.control_target
            chopper_f = self.chopper.operate.frequency_monitor[control_target]
            while chopper_f < 0.98 * self.params[self.InternalF]:
                time.sleep(1.0)
                chopper_f = self.chopper.operate.frequency_monitor[control_target]

            lockin_f = self.lockin.data.value[LKeys.ExternalFrequency]

            self.logger.info('Chopper frequency: {:.3f} Hz Lockin external frequency: {:.3f} Hz'
                             .format(chopper_f, lockin_f))

            valid = 0.95 < chopper_f / lockin_f < 1.05
            if not valid:
                self.ask_question('The external frequency {:3f} not matching with'
                                  'the chopper {} frequency {:.3f}. Check connections'
                                  .format(lockin_f, self.params[self.ControlTarget], chopper_f, None))

        if initial_motor_state == CKeys.OFF:
            reply = self.ask_question("Do you want to turn back off the chopper?")
            if reply:
                self.chopper.operate.motor_state = CKeys.OFF

        phase = self.lockin.ref.phase
        harmonic = self.lockin.ref.harmonic
        trigger_mode = self.lockin.ref.timebase_mode
        trigger_input = self.lockin.ref.trigger_input

        self.logger.info('Lock-in reference source is set to {}.'.format(self.lockin.ref.reference_source))
        self.logger.info('Trigger mode: {}, trigger input: {}'.format(trigger_mode, trigger_input))

        self.logger.info('Phase: {:.3f} degree, harmonic order to detect: {}'
                         .format(phase, harmonic))

    def cleanup(self):
        pass
