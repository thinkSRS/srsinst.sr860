import time
import logging

from srsgui import Task
from srsgui import BoolInput, IntegerListInput, FloatListInput, InstrumentInput, CommandInput
from srsinst.sr860 import SR860, get_sr860

from srsinst.sr860.instruments.components import Scan
from srsinst.sr860.instruments.keys import Keys

from srsinst.sr860.tasks.scanfrequencytask import ScanFrequencyTask


class ScanAuxOut2Task(ScanFrequencyTask):
    ScanName = 'Aux output 2'
    ScanParameter = Keys.AuxOutput2
    ScanBeginCommand = 'scan.aux_out2_range["begin"]'
    ScanEndCommand = 'scan.aux_out2_range["end"]'
    ScanCommandInstance = Scan.aux_out2_range

    InstName = 'inst to change'
    ScanScale = 'Scan Scale'
    ScanEndMode = 'End Mode'
    ScanPeriod = 'Scan period (s)'
    ScanInterval = 'Scan Interval (s)'
    ScanBegin = 'Scan Begin Value (V)'
    ScanEnd = 'Scan End Value (V)'

    input_parameters = {
        InstName:     InstrumentInput(),
        ScanScale:    CommandInput('scan.scale', Scan.scale),
        ScanEndMode:  CommandInput('scan.end_mode', Scan.end_mode),
        ScanPeriod:   CommandInput('scan.period', Scan.period),
        ScanInterval: CommandInput('scan.interval', Scan.interval),
        ScanBegin:    CommandInput(ScanBeginCommand, ScanCommandInstance),
        ScanEnd:      CommandInput(ScanEndCommand, ScanCommandInstance),
    }