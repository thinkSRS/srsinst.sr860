import time
import math
import numpy as np
from srsgui import Task
from srsinst.sr860.plots.twobytwosharexplot import TwoByTwoShareXPlot
from srsinst.sr860.instruments.components import DataStreamBuffer

class SimulatedPlotTask(Task):
    input_parameters={}

    def setup(self):
        # storage for data generation
        self.dr = 1e-3
        self.dt = 1e-3

        self.figure = self.get_figure()
        self.data = DataStreamBuffer(10000000)
        self.plot = TwoByTwoShareXPlot(self.figure, self.data)

    def test(self):
        while True:
            if not self.is_running():
                break

            r, th = self.calc_chunk()
            time.sleep(0.001)

            x = r * np.sin(th)
            y = r * np.cos(th)

            self.data.add_data_block(x, y, r, th)
            self.notify_data_available()  # parent calls update() method

    def update(self, data):
        if self.plot.request_plot_update():
            self.request_figure_update()

    def cleanup(self):
        pass

    def calc_chunk(self):
        block_size = 256
        r = np.empty(block_size)
        t = np.empty(block_size)
        for i in range(block_size):
            self.dr += 1e-4
            self.dt += 1e-3
            r[i] = 2 + math.sin(self.dr)
            t[i] = math.pi / 2.0 + 1.0 * math.sin(self.dt)
        return r, t
