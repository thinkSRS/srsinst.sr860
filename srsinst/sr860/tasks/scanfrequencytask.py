import time
import logging

from srsgui import Task
from srsgui import BoolInput, IntegerListInput, FloatListInput, InstrumentInput, CommandInput
from srsinst.sr860 import SR860, get_sr860

from srsinst.sr860.instruments.components import Scan
from srsinst.sr860.instruments.keys import Keys


class ScanFrequencyTask(Task):
    """

    """
    ScanName = 'Internal frequency'
    ScanParameter = Keys.InternalFrequency
    ScanBeginCommand = 'scan.frequency_range["begin"]'
    ScanEndCommand = 'scan.frequency_range["end"]'
    ScanCommandInstance = Scan.frequency_range

    InstName = 'inst to change'
    ScanScale = 'Scan Scale'
    ScanEndMode = 'End Mode'
    ScanPeriod = 'Scan period (s)'
    ScanInterval = 'Scan Interval (s)'
    ScanBegin = 'Scan Begin Value (Hz)'
    ScanEnd = 'Scan End Value (Hz)'

    input_parameters = {
        InstName:     InstrumentInput(),
        ScanScale:    CommandInput('scan.scale', Scan.scale),
        ScanEndMode:  CommandInput('scan.end_mode', Scan.end_mode),
        ScanPeriod:   CommandInput('scan.period', Scan.period),
        ScanInterval: CommandInput('scan.interval', Scan.interval),
        ScanBegin:    CommandInput(ScanBeginCommand, ScanCommandInstance),
        ScanEnd:      CommandInput(ScanEndCommand, ScanCommandInstance),
    }

    def setup(self):
        self.logger = logging.getLogger(__file__)
        self.lockin = get_sr860(self, self.get_input_parameter(self.InstName))

    def test(self):
        self.params = self.get_all_input_parameters()
        self.logger.info(self.params)
        self.lockin.scan.parameter = self.ScanParameter
        self.lockin.scan.enable = True
        self.logger.info('Scan mode change to {}'.format(self.ScanName))

    def cleanup(self):
        pass
