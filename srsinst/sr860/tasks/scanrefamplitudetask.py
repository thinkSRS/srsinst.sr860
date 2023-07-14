##! 
##! Copyright(c) 2023 Stanford Research Systems, All rights reserved
##! Subject to the MIT License
##! 

from srsgui import Task
from srsgui import BoolInput, IntegerListInput, FloatListInput, InstrumentInput, CommandInput
from srsinst.sr860 import SR860, get_sr860

from srsinst.sr860.instruments.components import Scan
from srsinst.sr860.instruments.keys import Keys

from srsinst.sr860.tasks.scanfrequencytask import ScanFrequencyTask


class ScanRefAmplitudeTask(ScanFrequencyTask):
    """

    """
    ScanName = 'Reference Amplitude'
    ScanParameter = Keys.ReferenceAmplitude
    ScanAttenuationCommand = 'scan.amplitude_attenuation_mode'
    ScanAttenuationInstance = Scan.amplitude_attenuation_mode
    ScanBeginCommand = 'scan.amplitude_range["begin"]'
    ScanEndCommand = 'scan.amplitude_range["end"]'
    # ScanCommandInstance = Scan.amplitude_range

    InstName = 'inst to change'
    ScanScale = 'Scan Scale'
    ScanEndMode = 'End Mode'
    ScanAttenuation = 'Attenuation Mode'
    ScanPeriod = 'Scan period (s)'
    ScanInterval = 'Scan Interval (s)'
    ScanBegin = 'Scan Begin Value (V)'
    ScanEnd = 'Scan End Value (V)'

    input_parameters = {
        InstName:        InstrumentInput(),
        ScanScale:       CommandInput('scan.scale'),
        ScanEndMode:     CommandInput('scan.end_mode'),
        ScanPeriod:      CommandInput('scan.period'),
        ScanAttenuation: CommandInput(ScanAttenuationCommand),
        ScanInterval:    CommandInput('scan.interval'),
        ScanBegin:       CommandInput(ScanBeginCommand),
        ScanEnd:         CommandInput(ScanEndCommand),
    }
