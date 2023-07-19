##! 
##! Copyright(c) 2023 Stanford Research Systems, All rights reserved
##! Subject to the MIT License
##! 

import time

from srsgui import Task
from srsgui import BoolInput, IntegerListInput, FloatListInput, InstrumentInput, CommandInput

from srsinst.sr860 import get_sr860
from srsinst.sr860.instruments.components import Reference
from srsinst.sr860.instruments.keys import Keys as LKeys

from srsinst.sr542 import get_sr542
from srsinst.sr542.instruments.components import Config
from srsinst.sr542.instruments.keys import Keys as CKeys

# import debugpy

class SetRefToExternalWithSR542Task(Task):
    """
This task configures an SR542 to provide an External Reference to an 
SR860 lock-in, for synchronous detection of a chopped optical signal.

Preconditions:
1. Establish remote communications with SR860 and SR542 from SRSGUI.
2. Connect SR542 Outer Ref Out (Inner Ref Out, or Shaft Ref Out) to SR860 External Ref In
using a BNC cable.
3. Connect your photodetector to the lock-in input as appropriate for your
experiment.

Postconditions:
1. Chopper is configured with:
Source = Internal Freq
Internal Frequency = [set by user]
n/m = 1
Control = Outer [or set by user]
Blade Phase = [set by user]

2. Lock-in is configured with
Source = External
Trigger = Positive TTL
Ref Input Impedance = 1 MOhm
Phase = [set by user]
Harmonic = [set by user]

The chopper motor will be powered up and the frequency of the
control target will be monitored until it is phase and frequency locked
at the setpoint frequency.

Once the chopper has reached frequency and phase lock,
the chopper's frequency is compared to the frequency detected
at the lock-in's reference input. If these match within 5%,
the task is considered successful.

If the motor was initially OFF, the user is prompted if they
wish to return the motor to a OFF state.
    """
    InstName = 'Lock-in to control'
    TriggerMode = 'Trigger mode'
    TriggerInput = 'Trigger input'
    Phase = 'Lock-in phase (degrees)'
    Harmonic = 'Harmonic'
    ChopperName = 'Chopper to control'
    FrequencySource = 'Source' #  where does this show up?
    ControlTarget = 'Control'
    InternalF = 'Internal frequency'
    BladePhase = 'Chopper blade phase (degrees)'
    
    input_parameters = {
        InstName:      InstrumentInput(0),
        Phase:         CommandInput('ref.phase'),
        Harmonic:      CommandInput('ref.harmonic'),

        ChopperName: InstrumentInput(1),
        ControlTarget: CommandInput('config.control_target', Config.control_target),
        InternalF: CommandInput('config.internal_freq', Config.internal_freq),
        BladePhase: CommandInput('config.phase', Config.phase),
    }

    def setup(self):
        self.logger = self.get_logger(__name__)
        self.params = self.get_all_input_parameters()        
        self.lockin = get_sr860(self, self.params[self.InstName])
        self.chopper = get_sr542(self, self.params[self.ChopperName])
        
    def test(self):    
        # debugpy.debug_this_thread()
        self.lockin.ref.reference_source = LKeys.External
        self.lockin.ref.trigger_mode = LKeys.PositiveTTL
        self.lockin.ref.trigger_input = LKeys.R1Meg

        self.chopper.config.multiplier = 1
        self.chopper.config.divisor = 1

        initial_motor_state = self.chopper.operate.motor_state

        phase = self.lockin.ref.phase
        harmonic = self.lockin.ref.harmonic
        trigger_mode = self.lockin.ref.timebase_mode
        trigger_input = self.lockin.ref.trigger_input

        self.logger.info('Lock-in RefIn: {}.'.format(self.lockin.ref.reference_source))
        self.logger.info('Trigger mode: {}, Trigger input impedance: {}'.format(trigger_mode, trigger_input))
        self.logger.info('Phase: {:.3f} degree, harmonic: {}'
                         .format(phase, harmonic))
        
        # used through test
        timeout_s = 30
        dt_s = 1.0

        # Change the reference source to internal        
        if self.chopper.config.source != CKeys.INTERNAL:
            if self.chopper.operate.motor_state == CKeys.ON:
                reply = self.ask_question("Is it OK to turn off the chopper "
                                        "to change the reference source to internal?")
                if not reply:
                    self.logger.info("Aborted.")
                    return
                else:
                    self.chopper.operate.motor_state = CKeys.OFF                   

            t_elapsed_s = 0            
            while(self.chopper.operate.motor_state == CKeys.ON):
                self.delay(1.0)                              
                t_elapsed_s += dt_s

                if t_elapsed_s > timeout_s:
                    msg = "Timeout waiting for chopper shut down"
                    self.logger.error(msg)                
                    raise TimeoutError(msg)
            
            self.chopper.config.source = CKeys.INTERNAL

        chopper_f = lockin_f = 0.0
        if self.chopper.operate.motor_state == CKeys.OFF:
            reply = self.ask_question("Proceed to run chopper motor and "
                                      "test for frequency match between chopper target "
                                      "and lock-in reference input?")
            if reply:
                self.chopper.operate.motor_state = CKeys.ON                

        control_target = self.chopper.config.control_target        
        t_elapsed_s = 0        
        while(True):
            self.delay(dt_s)            
            t_elapsed_s += dt_s
            chopper_f = self.chopper.operate.frequency_monitor[control_target]
            freq_locked = self.chopper.status.chopper_condition_bit['FL']
            phase_locked = self.chopper.status.chopper_condition_bit['PL']
            if(freq_locked and phase_locked):
                break
            if t_elapsed_s > timeout_s:
                msg = "Timeout waiting for chopper lock"
                self.logger.error(msg)                
                raise TimeoutError(msg)

        t_elapsed_s = 0
        while(True):
            self.delay(dt_s)            
            t_elapsed_s += dt_s
            ext_unlock = self.lockin.status.lock_in_bit['UNLK']
            if(not ext_unlock):
               break
            if t_elapsed_s > timeout_s:
                msg = "Timeout waiting for lock-in Ext lock"
                self.logger.error(msg)
                raise TimeoutError(msg)
            
        lockin_f = self.lockin.data.value[LKeys.ExternalFrequency]

        self.logger.info("Chopper frequency: {:.3f} Hz\n"
                         "Lock-in external frequency: {:.3f} Hz"
                            .format(chopper_f, lockin_f))

        valid = 0.95 < chopper_f / lockin_f < 1.05
        if not valid:
            self.ask_question('Lock-in external frequency {:3f} does not match '
                                'the chopper {} frequency {:.3f}. Check connections.'
                                .format(lockin_f, self.params[self.ControlTarget], chopper_f, None), return_type = None)

        if initial_motor_state == CKeys.OFF:
            reply = self.ask_question("Do you want to stop the chopper motor?")
            if reply:
                self.chopper.operate.motor_state = CKeys.OFF                
    def cleanup(self):
        pass
