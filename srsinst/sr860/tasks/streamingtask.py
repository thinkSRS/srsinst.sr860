
import time
import logging

from srsgui import Task
from srsgui import IntegerInput, FloatInput, ListInput, IntegerListInput

from srsinst.sr860 import SR860, get_sr860
from srsinst.sr860.instruments.components import DataStream

from srsinst.sr860.plots.twobytwosharexplot import TwoByTwoShareXPlot


class StreamingTask(Task):
    Duration = 'duration'
    Channels = 'Channels'
    DataFormat = 'data format'
    PacketSize = 'packet size'
    Rate = 'rate divider'
    Port = 'udp port'

    input_parameters = {
        Duration: IntegerInput(3600, ' s', 1, 360000, 1),
        Channels: ListInput(list(DataStream.ChannelDict.keys()), 1),
        DataFormat: ListInput(list(DataStream.FormatDict.keys())),
        PacketSize: IntegerListInput([1024, 512, 256, 128]),
        Rate: IntegerInput(4, '  (2^n) ', 0, 20, 1),
        Port: IntegerInput(1865, '', 1024, 65535, 1)
    }

    def setup(self):
        self.logger = logging.getLogger(__file__)
        self.lia = get_sr860(self)
        print(self.lia.query_text('*idn?'))

        self.lia.stream.enable = False
        self.lia.stream.option = 2
        self.lia.stream.channel = self.input_parameters[self.Channels].text
        self.lia.stream.format = self.input_parameters[self.DataFormat].text
        self.lia.stream.packet_size = self.input_parameters[self.PacketSize].get_value()
        self.lia.stream.rate = self.get_input_parameter(self.Rate)
        self.lia.stream.port = self.get_input_parameter(self.Port)

        self.duration_value = self.get_input_parameter(self.Duration)
        self.max_rate = self.lia.stream.max_rate
        self.sample_rate = self.max_rate / 2 ** self.lia.stream.rate
        self.packet_size = self.lia.stream.packet_size
        self.logger.info('Channels: {}, Data format: {}, Packet_size: {}, Rate: {:.3f} Hz, Port: {}'
                         .format(self.lia.stream.channel,
                                 self.lia.stream.format,
                                 self.packet_size,
                                 self.sample_rate,
                                 self.lia.stream.port,
                                 )
                         )

        self.plot = TwoByTwoShareXPlot(self.figure, self.lia.stream.data)

        # Mark the time 0
        self.init_time = time.time()

    def test(self):
        if self.get_input_parameter(self.Channels) == 0:
            raise ValueError('Channel X is not allowed,Choose other multiple channels')

        self.last_p_id = 0
        self.lia.stream.start()
        try:
            while time.time() - self.init_time < self.duration_value:
                if not self.is_running():
                    break

                block, p_id = self.lia.stream.receive_packet()
                self.lia.stream.data.add_data_block(*block)

                if self.last_p_id and p_id - self.last_p_id > 1:
                    self.logger.warning('{} missing packet(s) before ID:{}'
                                        .format(p_id - self.last_p_id - 1, p_id))
                self.last_p_id = p_id
                self.notify_data_available()
        except Exception as e:
            self.logger.error(e)

    def update(self, data):
        if self.plot.request_plot_update():
            self.request_figure_update()

    def cleanup(self):
        self.lia.stream.stop()
