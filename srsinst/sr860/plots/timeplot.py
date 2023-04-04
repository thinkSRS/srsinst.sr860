
import time
import logging
import numpy as np
from datetime import datetime, timedelta
from matplotlib.axes import Axes
from srsgui.task import Task

logger = logging.getLogger(__name__)


class TimePlot:
    def __init__(self, parent: Task, ax: Axes, plot_name='', data_names=('Y',), save_to_file=True,
                 use_datetime=True, plot_options=None):
        if plot_options is None:
            plot_options = {}
        if not issubclass(type(parent), Task):
            raise TypeError('Invalid parent {} is not a Task subclass'.format(type(parent)))
        # if type(ax) is not Axes or AxesSubplot:
        #    raise TypeError('ax is not a Matplotlib Axes class, but "{}"'.format(type(ax)))

        self.type = self.__class__.__name__
        self.parent = parent
        self.ax = ax
        self.name = plot_name.strip()

        self.min_value = 0
        self.max_value = 0

        self.conversion_factor = 1
        self.unit = ''
        self.use_datetime = use_datetime

        self.updated_time = 0
        self.update_period = 0.1

        self.save_to_file = False
        if hasattr(self.parent, 'session_handler') and self.parent.session_handler:
            self.save_to_file = save_to_file
        else:
            logger.error('parent has no session_handler')

        self.data_keys = data_names

        self.data = {}
        self.lines = {}

        self._data_buffer_size = 1000000  # Maximum data points per line
        self.data_points = 0  # Current data points in data buffer
        self.max_points_in_plot = 5000  # Maximum point to plot

        if self.use_datetime:
            self.time = np.zeros(self._data_buffer_size).astype('datetime64[ms]')
        else:
            self.time = np.zeros(self._data_buffer_size, dtype=np.float64)

        for key in self.data_keys:
            self.data[key] = np.zeros(self._data_buffer_size)
            self.lines[key], = self.ax.plot([1.0], [1.0], label=key, **plot_options)

        # significant digits in a number in text
        self.round_float_resolution = 4
        self.header_saved = False

        self.ax.set_title(self.name)

        self.legend = self.ax.legend()
        self.lined = {}
        for legline, origline in zip(self.legend.get_lines(), self.lines.values()):
            legline.set_picker(True)
            self.lined[legline] = origline
        self.ax.figure.canvas.mpl_connect('pick_event', self.on_pick)

        self.ax.callbacks.connect('xlim_changed', self.on_xlim_changed)
        if self.use_datetime:
            self.initial_time = datetime.now()
            self.ax.set_xlabel('Date time')
            self.ax.xaxis.set_tick_params(rotation=30)
            self.ax.set_xlim(self.initial_time, self.initial_time + timedelta(0, 1200))
        else:
            self.initial_time = time.time()
            self.ax.set_xlabel('Time (s)')
            self.ax.set_xlim(0, 300)

    def on_xlim_changed(self, event_ax):
        self.update_plot()

    def on_pick(self, event):
        """
        Toggle a line from the line corresponding in the legend
        https://matplotlib.org/stable/gallery/event_handling/legend_picking.html
        """
        legline = event.artist
        origline = self.lined[legline]
        visible = not origline.get_visible()
        origline.set_visible(visible)
        legline.set_alpha(1.0 if visible else 0.3)
        self.update_plot()

    def get_buffer_size(self):
        return self._data_buffer_size

    def set_buffer_size(self, size=10000000):
        self._data_buffer_size = size
        self.data_points = 0
        self.time = np.zeros(size)
        for key in self.data_keys:
            self.data[key] = np.zeros(size)

    def set_conversion_factor(self, factor=0.1, unit='fA'):
        old_factor = self.conversion_factor
        self.conversion_factor = factor
        self.unit = unit
        if self.parent:
            self.parent.add_details(' {:.4e} '.format(self.conversion_factor), 'Conversion factor')
            self.parent.add_details(' {} '.format(self.unit), 'Converted unit')

        factor_ratio = self.conversion_factor / old_factor
        bottom, top = self.ax.get_ylim()
        self.ax.set_ylim(bottom * factor_ratio, top * factor_ratio)
        self.ax.set_ylabel('Intensity ({})'.format(self.unit))

    def add_data(self, data_list=(0,), update_figure=False):
        if self.use_datetime:
            self.time[self.data_points] = np.datetime64(datetime.now())
        else:
            self.time[self.data_points] = time.time() - self.initial_time

        for key, point in zip(self.data_keys, data_list):
            self.data[key][self.data_points] = point * self.conversion_factor
        self.data_points += 1

        if self.data_points == 1:
            self.min_value = min(data_list) * self.conversion_factor
            self.max_value = max(data_list) * self.conversion_factor
        elif self.data_points < 5:
            temp_min_value = min(data_list) * self.conversion_factor
            temp_max_value = max(data_list) * self.conversion_factor
            self.min_value = temp_min_value if temp_min_value < self.min_value else self.min_value
            self.max_value = temp_max_value if temp_max_value > self.max_value else self.max_value

            if self.min_value == 0 and self.max_value == 0:
                min_value = -1.0
                max_value = 1.0
            else:
                min_value = self.min_value
                max_value = self.max_value

            margin = (max_value - min_value)
            self.ax.set_ylim(min_value - margin, max_value + margin)

        if update_figure:
            self.update_plot()
        self.save_data(self.time[self.data_points - 1], data_list)

    def save_data(self, timestamp, data_list):
        if not self.save_to_file:
            return
        if not self.header_saved:
            self.parent.add_dict_to_file(self.name, self.get_plot_info())
            if self.use_datetime:
                self.parent.create_table_in_file(self.name, 'Date time', *self.data_keys)
            else:
                self.parent.create_table_in_file(self.name, 'Elapsed time', *self.data_keys)
            self.header_saved = True
        # write the spectrum in to the data file
        if self.use_datetime:
            ts = str(timestamp)
        else:
            ts = self.round_float(timestamp)

        self.parent.add_to_table_in_file(self.name, ts, *map(self.round_float, data_list))

    def round_float(self, number):
        # set the resolution of the number with self.round_float_resolution
        fmt = '{{:.{}e}}'.format(self.round_float_resolution)
        return float(fmt.format(number))

    def get_plot_info(self):
        return {
            'type': self.type,
            'name': self.name,
            'xunit': 's',
            'yunit': self.unit,
            'axes_title': self.ax.get_title(),
            'axes_xlabel': self.ax.get_xlabel(),
            'axes_ylabel': self.ax.get_ylabel(),
            'axes_xlim': self.ax.get_xlim(),
            'axes_ylim': self.ax.get_ylim(),
            'axes_xsclae': self.ax.get_xscale(),
            'axes_yscale': self.ax.get_yscale(),
        }

    def update_plot(self):
        current_time = time.time()
        if current_time - self.updated_time < self.update_period:
            return

        if self.use_datetime:
            r_min, r_max = np.array(self.ax.get_xlim()) * 86400
            xl = np.array([r_min, r_max]).astype('datetime64[s]')
        else:
            xl = np.array(self.ax.get_xlim())
        index = np.searchsorted(self.time[:self.data_points], xl)
        index_step = (index[1] - index[0]) // self.max_points_in_plot
        if index_step < 1:
            index_step = 1

        index[0] = 0 if index[0] <= 0 else index[0] - 1
        index[1] = self.data_points if index[1] >= self.data_points else index[1] + 1

        s = slice(index[0], index[1], index_step)
        for key in self.data_keys:
            self.lines[key].set_xdata(self.time[s])
            self.lines[key].set_ydata(self.data[key][s])

        self.parent.request_figure_update(self.ax.figure)
        self.updated_time = current_time

    def cleanup(self):
        pass

