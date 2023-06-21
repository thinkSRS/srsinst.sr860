
from srsgui import Task
from srsgui import BoolInput, IntegerListInput, FloatListInput, InstrumentInput, CommandInput
from srsinst.sr860 import SR860, get_sr860

from srsinst.sr860.instruments.components import Scan
from srsinst.sr860.instruments.keys import Keys

from srsinst.sr860.tasks.scanfrequencytask import ScanFrequencyTask


class ScanAuxOut1Task(ScanFrequencyTask):
    ScanName = 'Aux output 1'
    ScanParameter = Keys.AuxOutput1
    ScanBeginCommand = 'scan.aux_out1_range["begin"]'
    ScanEndCommand = 'scan.aux_out1_range["end"]'

    InstName = 'inst to change'
    ScanScale = 'Scan Scale'
    ScanEndMode = 'End Mode'
    ScanPeriod = 'Scan period (s)'
    ScanInterval = 'Scan Interval (s)'
    ScanBegin = 'Scan Begin Value (V)'
    ScanEnd = 'Scan End Value (V)'

    input_parameters = {
        InstName:     InstrumentInput(),
        ScanScale:    CommandInput('scan.scale'),
        ScanEndMode:  CommandInput('scan.end_mode'),
        ScanPeriod:   CommandInput('scan.period'),
        ScanInterval: CommandInput('scan.interval'),
        ScanBegin:    CommandInput(ScanBeginCommand),
        ScanEnd:      CommandInput(ScanEndCommand),
    }
