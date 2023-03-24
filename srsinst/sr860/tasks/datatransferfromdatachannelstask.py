import time

from srsgui import Task
from srsgui import FloatInput, BoolInput, ListInput, InstrumentInput, CommandInput

from srsinst.sr860 import SR860, get_sr860
from srsinst.sr860.instruments.components import Display

from srsinst.sr860.plots.timeplot import TimePlot


class DataTransferFromDataChannelsTask(Task):
    """
    Transfer data from data channels
    """
    InstName = 'inst to control'
    Channel1 = 'channel 1'
    Channel2 = 'channel 2'
    Channel3 = 'channel 3'
    Channel4 = 'channel 4'
    Delay = 'delay (s)'
    DateTime = 'time format'

    input_parameters = {
        InstName: InstrumentInput(),
        Channel1: CommandInput('display.config[0]', Display.config),
        Channel2: CommandInput('display.config[1]', Display.config),
        Channel3: CommandInput('display.config[2]', Display.config),
        Channel4: CommandInput('display.config[3]', Display.config),
        Delay: FloatInput(1, ' s', 0.0, 600, 0.1),
        DateTime: BoolInput(['Seconds', 'Date time'])
    }

    def setup(self):
        self.logger = self.get_logger(__name__)
        self.params = self.get_all_input_parameters()
        self.lockin = get_sr860(self, self.params[self.InstName])
        self.ax = self.get_figure().subplots(2, 2, sharex=True)

        ch_name = self.lockin.display.config[0]
        options = {'color': '#00d000'}
        self.ch1_plot = TimePlot(self, self.ax[0, 0], ch_name, (ch_name,), True, self.params[self.DateTime], options)
        ch_name = self.lockin.display.config[1]
        options = {'color': '#00e0e0'}
        self.ch2_plot = TimePlot(self, self.ax[0, 1], ch_name, (ch_name,), True, self.params[self.DateTime], options)
        ch_name = self.lockin.display.config[2]
        options = {'color': '#e0e000'}
        self.ch3_plot = TimePlot(self, self.ax[1, 0], ch_name, (ch_name,), True, self.params[self.DateTime], options)
        ch_name = self.lockin.display.config[3]
        options = {'color': 'orange'}
        self.ch4_plot = TimePlot(self, self.ax[1, 1], ch_name, (ch_name,), True, self.params[self.DateTime], options)

        # capture = self.lockin.capture_commands()
        # self.add_dict_to_file('command capture', capture)

    def test(self):
        self.logger.info(self.params)
        while self.is_running():
            v = self.lockin.data.get_channel_values()
            self.ch1_plot.add_data([v[0]], True)
            self.ch2_plot.add_data([v[1]], True)
            self.ch3_plot.add_data([v[2]], True)
            self.ch4_plot.add_data([v[3]], True)
            time.sleep(self.params[self.Delay])

    def cleanup(self):
        pass
