
import socket
from struct import unpack_from
import numpy as np

from srsgui.inst.component import Component
from srsgui.inst.commands import Command, GetCommand,\
                                 BoolCommand, BoolGetCommand,\
                                 IntCommand, IntGetCommand, IntSetCommand,\
                                 FloatCommand, FloatSetCommand, FloatGetCommand, \
                                 DictCommand, DictGetCommand

from srsgui.inst.indexcommands import IndexCommand, IndexGetCommand, \
                                      IntIndexCommand, IntIndexGetCommand, \
                                      BoolIndexCommand, BoolIndexGetCommand,\
                                      FloatIndexCommand, FloatIndexGetCommand, \
                                      DictIndexCommand
from .keys import Keys


class Reference(Component):
    MaxFrequency = 500000.0

    TimebaseModeDict = {
        Keys.Auto: 0,
        Keys.Internal: 1
    }
    TimebaseSourceDict = {
        Keys.External: 0,
        Keys.Internal: 1
    }
    BladeSlotsDict = {
        6: 0,
        30: 1
    }
    SineOutDCModeDict = {
        Keys.Common: 0,
        Keys.Difference: 1
    }
    ReferenceSourceDict = {
        Keys.Internal: 0,
        Keys.External: 1,
        Keys.Dual: 2,
        Keys.Chop: 3
    }
    TriggerModeDict = {
        Keys.Sine: 0,
        Keys.PositiveTTL: 1,
        Keys.NegativeTTL: 2
    }
    TriggerInputDict = {
        Keys.R50Ohms: 0,
        Keys.R1Meg: 1
    }
    timebase_mode = DictCommand('TBMODE', TimebaseModeDict)
    timebase_source = DictCommand('TBSTAT', TimebaseSourceDict)
    
    phase = FloatCommand('PHAS', unit='deg', min=-360000, max=360000, step=0.000001,
                                 fmt='{:6e}', default_value=0.0)

    frequency = FloatCommand('FREQ', 'Hz', 0.001, MaxFrequency, 0.0001,)
    internal_frequency = FloatCommand('FREQINT','Hz', 0.001, MaxFrequency, 0.0001)
    external_frequency = FloatGetCommand('FREQEXT')
    detection_frequency = FloatGetCommand('FREQDET')

    harmonic = IntCommand('HARM', '', 1, 99)
    harmonic_dual = IntCommand('HARMDUAL', '', 1, 99)
    
    blade_slots = DictCommand('BLADESLOTS', BladeSlotsDict)
    blade_phase = FloatCommand('BLADEPHASE')
    
    sine_out_amplitude = FloatCommand('SLVL', ' V', 0, 2.0, 1e-9)
    sine_out_offset = FloatCommand('SOFF', 'V', -5.0, 5.0, 1e-4)
    sine_out_dc_mode = DictCommand('REFM', SineOutDCModeDict)
    reference_source = DictCommand('RSRC', ReferenceSourceDict)
    
    trigger_mode = DictCommand('RTRG', TriggerModeDict)
    trigger_input = DictCommand('REFZ', TriggerInputDict)

    frequency_preset = FloatIndexCommand('PSTF', 3, 0, " V", 0.001, MaxFrequency, 0.0001)
    sine_out_amplitude_preset = FloatIndexCommand('PSTA', 3, 0, " V", 0, 2.0, 1e-9)
    sine_out_offset_preset = FloatIndexCommand('PSTL', 3, 0, " V", -5.0, 5.0, 1e-4)

    def auto_phase(self):
        self.comm.send('APHS')


class Signal(Component):
    InputModeDict = {
        Keys.Voltage: 0,
        Keys.Current: 1
    }
    VoltageInputModeDict = {
        Keys.AOnly: 0,
        Keys.AMinusB: 1
    }
    VoltageInputCouplingDict = {
        Keys.AC: 0,
        Keys.DC: 1
    }
    VoltageInputShieldDict = {
        Keys.Float:  0,
        Keys.Ground: 1
    }
    VoltageInputRangeDict = {
        1.0:  0,
        0.3:  1,
        0.1:  2,
        0.03: 3,
        0.01: 4
    }
    CurrentInputGainDict = {
        1e6: 0,
        1e8: 1
    }
    VoltageSensitivityDict = {1.0: 0}
    CurrentSensitivityDict = {1e-6: 0}
    index = 0
    for i in range(9):
        for j in [5.0, 2.0, 1.0]:
            index += 1
            VoltageSensitivityDict[float(f'{(j * 10 ** -(i + 1)):.1e}')] = index
            CurrentSensitivityDict[float(f'{(j * 10 ** -(i + 7)):.1e}')] = index

    TimeConstantDict = {}
    index = 0
    for i in range(11):
        for j in [1.0, 3.0]:
            TimeConstantDict[float(f'{(j * 10 ** (i - 6)):.1e}')] = index
            index += 1

    FilterSlopeDict = {
        6:  0,
        12: 1,
        18: 2,
        24: 3
    }
    OffOnDict = {Keys.Off: 0,
                 Keys.On:  1
    }

    input_mode = DictCommand('IVMD', InputModeDict)
    
    voltage_input_mode = DictCommand('ISRC', VoltageInputModeDict)
    voltage_input_coupling = DictCommand('ICPL', VoltageInputCouplingDict)

    voltage_input_shield = DictCommand('IGND', VoltageInputShieldDict)
    voltage_input_range = DictCommand('IRNG', VoltageInputRangeDict)
    voltage_sensitivity = DictCommand('SCAL', VoltageSensitivityDict)
    
    current_input_gain = DictCommand('ICUR', CurrentInputGainDict, unit='Ohm', fmt='{:0e}')
    current_sensitivity = DictCommand('SCAL', CurrentSensitivityDict, unit='A', fmt='{:0e}')
    time_constant = DictCommand('OFLT', TimeConstantDict, unit='s', fmt='{:0e}')

    strength_indicator = IntGetCommand('ILVL')
    filter_slope = DictCommand('OFSL', FilterSlopeDict, unit='dB/oct')
    sync_filter = DictCommand('SYNC', OffOnDict)
    advanced_filter = DictCommand('ADVFILT', OffOnDict)
    equivalent_noise_bandwidth = FloatCommand('ENBW')


class Output(Component):
    TypeDict = {
        Keys.XY: 0,
        Keys.RT: 1
    }
    IndexDict = {
        Keys.X: 0,
        Keys.Y: 1,
        Keys.R: 2
    }
    ChannelDict = {
        Keys.OutputCh1: 0,
        Keys.OutputCh2: 1
    }
    ExpandDict = {
        1:   0,
        10:  1,
        100: 2
    }

    type = DictIndexCommand('COUT', TypeDict, 1, 0, ChannelDict)
    expand = DictIndexCommand('CEXP', ExpandDict, 2, 0, IndexDict)
    offset = BoolIndexCommand('COFA', 2, 0, IndexDict)
    offset_percent = FloatIndexCommand('COFP', 2, 0, IndexDict)
    ratio_mode = BoolIndexCommand('CRAT', 2, 0, IndexDict)

    def auto_offset(self, index):
        self.comm.send('OAUT {}'.format(index))


class Aux(Component):
    ChannelDict = {
        Keys.Channel1: 0,
        Keys.Channel2: 1,
        Keys.Channel3: 2,
        Keys.Channel4: 3
    }

    input = FloatIndexGetCommand('OAUX', 3, 0, ChannelDict)
    output = FloatIndexCommand('AUXV', 3, 0, ChannelDict)


class Auto(Component):
    def set_phase(self):
        self.comm.send('APHS')

    def set_range(self):
        self.comm.send('ARNG')

    def set_scale(self):
        self.comm.send('ASCL')


class Display(Component):
    LayoutDict = {
        Keys.Trend:       0,
        Keys.History:     1,
        Keys.BarHistory: 2,
        Keys.FFT:         3,
        Keys.BarFFT:     4,
        Keys.Bar8:       5
    }
    ChannelDict = {
        Keys.Data1: 0,
        Keys.Data2: 1,
        Keys.Data3: 2,
        Keys.Data4: 3
    }
    ParameterDict = {
        Keys.X: 0,
        Keys.Y: 1,
        Keys.R: 2,
        Keys.Theta: 3,
        Keys.AuxInput1: 4,
        Keys.AuxInput2: 5,
        Keys.AuxInput3: 6,
        Keys.AuxInput4: 7,
        Keys.XNoise: 8,
        Keys.YNoise: 9,
        Keys.AuxOutput1: 10,
        Keys.AuxOutput2: 11,
        Keys.Phase: 12,
        Keys.SineOutputAmplitude: 13,
        Keys.DCLevel: 14,
        Keys.InternalFrequency: 15,
        Keys.ExternalFrequency: 16
    }

    blank = BoolCommand('DBLK')
    layout = DictCommand('DLAY', LayoutDict)
    config = DictIndexCommand('CDSP', ParameterDict, 3, 0, ChannelDict)
    graph_enable = BoolIndexCommand('CGRF', 3, 0, ChannelDict)

    def get_screen(self):
        raise NotImplemented('get_screen() is not implemented')


class Chart(Component):
    ChannelDict = Display.ChannelDict
    TimeDivDict = {
        0.5:       0,
        1.0:       1,
        2.0:       2,
        5.0:       3,
        10.0:      4,
        30.0:      5,
        60.0:      6,
        120.0:     7,
        300.0:     8,
        600.0:     9,
        1800.0:   10,
        3600.0:   11,
        7200.0:   12,
        21600.0:  13,
        43200.0:  14,
        86400.0:  15,
        172800.0: 16
    }
    CursorDisplayModeDict = {
        Keys.DateTime: 0,
        Keys.IntervalTime:  1
    }
    CursorReadoutModeDict = {
        Keys.Mean: 0,
        Keys.Maximum:  1,
        Keys.Minimum:  2
    }
    CursorWidthDict={
        Keys.Line:   0,
        Keys.Narrow: 1,
        Keys.Wide:   2
    }
    CursorValueDict = {
        Keys.Data1:   0,
        Keys.Data2:   1,
        Keys.Data3:   2,
        Keys.Data4:   3,
        Keys.Status:   4
    }

    time_division = DictCommand('GSPD', TimeDivDict)
    vertical_division = FloatIndexCommand('GSCL', 3, 0, ChannelDict)
    vertical_offset = FloatIndexCommand('GOFF', 3, 0, ChannelDict)
    enable = BoolIndexCommand('CGRF', 3, 0, ChannelDict)
    live = BoolCommand('GLIV')
    cursor_position = IntCommand('PCUR')
    cursor_relative = BoolCommand('CURREL')
    cursor_display_mode = DictCommand('CURDISP', CursorDisplayModeDict)
    cursor_readout_mode = DictCommand('CURBUG', CursorReadoutModeDict)
    cursor_width = DictCommand('FCRW', CursorWidthDict)
    cursor_value = IntIndexGetCommand('SCRY', 4, 0, CursorValueDict)
    cursor_date_time = GetCommand('CURDATTIM')
    cursor_interval_time = GetCommand('CURINTERVAL')

    def auto_scal(self, channel):
        self.comm.send(f'GACT {channel}')

    def auto_find(self, channel):
        self.comm.send(f'GAUF {channel}')


class FFT(Component):
    SourceDict = {
        Keys.ADC:    0,
        Keys.MIXER:  1,
        Keys.FILTER: 2
    }

    DBDivDict = {}
    index = -9
    for i in range(6):
        for j in [1.0, 2.0, 5.0]:
            DBDivDict[float(f'{(j * 10 ** (i - 3)):.1e}')] = index
            index += 1

    AverageDict = {
        1:   0,
        3:   1,
        10:  2,
        30:  3,
        100: 4
    }

    source = DictCommand('FFTR', SourceDict)
    vertical_scale = DictCommand('FFTS', DBDivDict)
    vertical_offset = FloatCommand('FFTO')
    max_span = FloatGetCommand('FFTMAXSPAN')
    span = FloatCommand('FFTSPAN')
    average = DictCommand('FFTA', AverageDict)
    live = BoolCommand('FFTL')
    cursor_width = DictCommand('FCRW', Chart.CursorWidthDict)
    cursor_frequency = FloatGetCommand('FCRX')
    cursor_value = FloatGetCommand('FCRY')

    def auto_scale(self):
        self.comm.send('FAUT')


class Scan(Component):
    ParameterDict = {
        Keys.InternalFrequency:  0,
        Keys.ReferenceAmplitude: 1,
        Keys.ReferenceOffset:    2,
        Keys.AuxOutput1:          3,
        Keys.AuxOutput2:          4
    }
    ScaleDict = {
        Keys.Linear: 0,
        Keys.Log:    1
    }
    EndDict = {
        Keys.Once:    0,
        Keys.Repeat:  1,
        Keys.UpDown: 2
    }
    AttenuationDict = {
        Keys.Auto:  0,
        Keys.Fixed: 1
    }
    IntervalDict = {
        0.008: 0,
        0.016: 1,
        0.031: 2,
        0.078: 3,
        0.155: 4,
        0.469: 5,
        0.938: 6,
        1.875: 7,
        4.688: 8,
        9.375: 9,
        28.12: 10,
        56.25: 11,
        112.5: 12,
        337.0: 13,
        675.0: 14,
        1350.0: 15,
        2700.0: 16
    }
    StateDict = {
        Keys.Off:     0,
        Keys.Reset:   1,
        Keys.Running: 2,
        Keys.Paused:  3,
        Keys.Done:    4
    }
    RangeDict = {
        Keys.BEGIN: 0,
        Keys.END:   1
    }

    parameter = DictCommand('SCNPAR', ParameterDict)
    scale = DictCommand('SCNLOG', ScaleDict)
    end_mode = DictCommand('SCNEND', EndDict)
    period = FloatCommand('SCNSEC')
    amplitude_attenuation_mode = DictCommand('SCNAMPATTN', AttenuationDict)
    offset_attenuation_mode = DictCommand('SCNDCATTN', AttenuationDict)
    interval = DictCommand('SCNINRVL', IntervalDict)
    enable = BoolCommand('SCNENBL')
    state = DictGetCommand('SCNSTATE', StateDict)
    frequency_range = FloatIndexCommand('SCNFREQ', 1, 0, RangeDict)
    amplitude_range = FloatIndexCommand('SCNAMP', 1, 0, RangeDict)
    offset_range = FloatIndexCommand('SCNDC', 1, 0, RangeDict)
    aux_out1_range = FloatIndexCommand('SCNAUX1', 1, 0, RangeDict)
    aux_out2_range = FloatIndexCommand('SCNAUX2', 1, 0, RangeDict)

    def start(self):
        self.comm.send('SCNRUN')

    def pause(self):
        self.comm.send('SCNPAUSE')

    def reset(self):
        self.comm.send('SCNRST')


class DataTransfer(Component):
    ChannelDict = Display.ChannelDict
    ParameterDict = Display.ParameterDict
    channel_config = DictIndexCommand('CDSP', ParameterDict, 3, 0, ChannelDict)
    channel_value = FloatIndexGetCommand('OUTR', 3, 0, ChannelDict)
    value = FloatIndexGetCommand('OUTP', 16, 0, ParameterDict)

    def get_values(self, p1, p2, p3=None):
        if p3:
            reply = self.comm.query_text(f'SNAP? {p1}, {p2}, {p3}')
        else:
            reply = self.comm.query_text(f'SNAP? {p1}, {p2}')
            
        return list(map(float, reply.split(',')))

    def get_channel_values(self):
        reply = self.comm.query_text('SNAPD?')
        return list(map(float, reply.split(',')))


class DataCapture(Component):
    ChannelDict = {
        Keys.X:    0,
        Keys.XY:   1,
        Keys.RT:   2,
        Keys.XYRT: 3
    }
    RunModeDict={
        Keys.Once:       0,
        Keys.Continuous: 1
    }
    TriggerModeDict ={
        Keys.Immediate:        0,
        Keys.TriggerStart:     1,
        Keys.SamplePerTrigger: 2
    }
    CaptureStateBitDict = {
        Keys.InProgress: 0,
        Keys.Triggered:  1,
        Keys.Wrapped:    2
    }
    
    buffer_size_in_kilobytes = IntCommand('CAPTURELEN')
    config = DictCommand('CAPTURECFG', ChannelDict)
    max_rate = FloatGetCommand('CAPTURERATEMAX')
    rate_divisor_exponent = IntSetCommand('CAPTURERATE')
    rate = FloatGetCommand('CAPTURERATE')
    state = IntGetCommand('CAPTURESTAT')
    data_size_in_bytes = IntGetCommand('CAPTUREBYTES')
    data_size_in_kilobytes = IntGetCommand('CAPTUREPROG')

    def start(self, run_mode=0, trigger_mode=0):
        self.comm.send('CAPTURESTART {}, {}'.format(run_mode, trigger_mode))

    def stop(self):
        self.comm.send('CAPTURESTOP')

    def get_data(self, index):
        reply = self.comm.query_text(f'CAPTUREVAL? {index}')
        return list(map(float, reply.split(',')))
        
    def get_all_data(self):
        data_type = self.config
        final_index = self.data_size_in_kilobytes
        
        with self.comm.get_lock():
            self.comm._send(f'CAPTUREGET? 0, {final_index:d}')
            buffer = self.comm._read_binary(2)
            # buffer[0] should be 35            
            digits = buffer[1] - 48
            
            buffer += self.comm._read_binary(digits)
            offset = digits + 2
            buffer_size = int(buffer[2 : offset])
            buffer += self.comm._read_binary(buffer_size)
            
        data_size  = (len(buffer) - offset) // 4
        self.unpack_format = '>{}f'.format(data_size)
        vals = unpack_from(self.unpack_format, buffer, offset)
        if data_type == Keys.X:
            column = 1
        elif data_type == Keys.XY or data_type == 'RT':
            column = 2
        elif data_type == Keys.XYRT:
            column = 4
        else:
            ValueError('Invalid data type {} in get_all_data()'.format(data_type))
            
        row = len(vals) // column
        arr = np.transpose(np.reshape(vals, (row, column)))    
        return arr


class DataStreamBuffer:
    def __init__(self, size=10000000):
        self._data_buffer_size = size
        self._data_points = 0
        self.reset(size)

    def reset(self, size=10000000):
        self._data_buffer_size = size
        self._data_points = 0
        self.time = np.empty(self._data_buffer_size)
        self.x = np.empty(self._data_buffer_size)
        self.y = np.empty(self._data_buffer_size)
        self.r = np.empty(self._data_buffer_size)
        self.th = np.empty(self._data_buffer_size)

    def get_buffer_size(self):
        return self._data_buffer_size

    def get_data_size(self):
        return self._data_points

    def add_data_block(self, x, y, r, th):
        block_size = x.size
        init = self._data_points
        final = init + block_size

        final = init + block_size
        if final > self._data_buffer_size:
            raise IndexError('Data reached the data buffer size.')

        ti = np.arange(init, final)
        self.time[init: final] = ti
        self.x[init: final] = x
        self.y[init: final] = y
        self.r[init: final] = r
        self.th[init: final] = th
        self._data_points = final


class DataStream(Component):
    ChannelDict = DataCapture.ChannelDict
    FormatDict = {
        Keys.Float32: 0,
        Keys.Int16:   1
    }
    PacketSizeDict = {
        1024: 0,
        512:  1,
        256:  2,
        128:  3
    }
    OptionBitDict = {
        Keys.LittleEndian: 1,
        Keys.DataIntegrityChecking: 2
    }

    channel = DictCommand('STREAMCH', ChannelDict)
    max_rate = FloatGetCommand('STREAMRATEMAX')
    rate = IntCommand('STREAMRATE')
    format = DictCommand('STREAMFMT', FormatDict)
    packet_size = DictCommand('STREAMPCKT', PacketSizeDict)
    port = IntCommand('STREAMPORT')
    option = IntCommand('STREAMOPTION')
    enable = BoolCommand('STREAM')

    def __init__(self, parent, buffer_size=1000000):
        super().__init__(parent)
        self.data_buffer_size = buffer_size
        self.data = DataStreamBuffer(self.data_buffer_size)

    def _prepare(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind(('', self.port))
        self.timeout = 10
        self.udp_socket.settimeout(self.timeout)
        self.prepared_channel = self.channel

        self.prepared_packet_size = self.packet_size
        self.unpack_format = '>{}h'.format(self.prepared_packet_size // 2) if self.format == 'int16' else\
                             '>{}f'.format(self.prepared_packet_size // 4)
        self.data.reset(self.data_buffer_size)

    def receive_packet(self):
        buffer, _ = self.udp_socket.recvfrom(self.prepared_packet_size + 4)
        header = unpack_from('>I', buffer)[0]
        packet_number = header & 0xff

        # from the manual page 172
        packet_content = (header >> 8) & 0x0f
        packet_size = (header >> 12) & 0x0f
        packet_rate = (header >> 16) & 0xff
        packet_status = (header >> 24) & 0xff

        vals = unpack_from(self.unpack_format, buffer, 4)

        arr = None
        if self.prepared_channel == Keys.X:
            arr = np.array(vals)

        elif self.prepared_channel == Keys.XY:
            rows = len(vals) // 2
            mat = np.transpose(np.reshape(vals, (rows, 2)))
            r = np.sqrt(np.square(mat[0]) + np.square(mat[1]))
            th = 180.0 / np.pi * np.arctan2(mat[1], mat[0])
            arr = np.append(np.append(mat, np.reshape(r, (1, rows)), axis=0),
                            np.reshape(th, (1,rows)), axis=0)

        elif self.prepared_channel == Keys.RT:
            rows = len(vals) // 2
            mat = np.transpose(np.reshape(vals, (rows, 2)))
            angle = np.pi / 180.0 * mat[1]
            x = mat[0] * np.cos(angle)
            y = mat[0] * np.sin(angle)
            arr = np.append(np.append(np.reshape(x, (1, rows)),
                                      np.reshape(y, (1, rows)), axis=0),
                            mat, axis=0)

        elif self.prepared_channel == Keys.XYRT:
            row = len(vals) // 4
            arr = np.transpose(np.reshape(vals, (row, 4)))
        else:
            raise ValueError(f'{self.prepared_channel} is not in ChannelDict')
        return arr, packet_number

    def start(self):
        self._prepare()
        self.enable = True

    def stop(self):
        self.enable = False
        self.udp_socket.close()


class Status(Component):
    SerialPollStatusBitDict = {
        Keys.ERR: 2,
        Keys.LIA: 3,
        Keys.MAV: 4,
        Keys.ESB: 5,
        Keys.SRQ: 6
    }
    EventStatusBitDict = {
        Keys.OPC: 0,
        Keys.INP: 1,
        Keys.QRY: 3,
        Keys.EXE: 4,
        Keys.CMD: 5,
        Keys.URQ: 6,
        Keys.PON: 7,
    }
    ErrorStatusBitDict = {
        Keys.CLK: 0,
        Keys.BACKUP: 1,
        Keys.VXI: 4,
        Keys.GPIB: 5,
        Keys.USBDEV: 6,
        Keys.USBHOST: 7
    }
    LiaStatusBitDict = {
        Keys.CH1OV:  0,
        Keys.CH2OV:  1,
        Keys.UNLK:   3,
        Keys.RANGE:  4,
        Keys.SYNCF:  5,
        Keys.SYNCOV: 6,
        Keys.TRIG:   7,
        Keys.DAT1OV: 8,
        Keys.DAT2OV: 9,
        Keys.DAT3OV: 10,
        Keys.DAT4OV: 11,
        Keys.DCAPFIN:12,
        Keys.SCNST:  13,
        Keys.SCNFIN: 14,
    }
    OverloadStatusBitDict = {
        Keys.Ch1OutputScale: 0,
        Keys.Ch2OutputScale: 1,
        Keys.ExternalReferenceUnlocked: 3,
        Keys.InputRange: 4,
        Keys.DataCh1Scale: 8,
        Keys.DataCh2Scale: 9,
        Keys.DataCh3Scale: 10,
        Keys.DataCh4Scale: 11,
    }

    event_enable = IntCommand('*ESE')
    event = IntGetCommand('*ESR')
    event_enable_bit = BoolIndexCommand('*ESE', 7, 0, EventStatusBitDict)
    event_bit = BoolIndexGetCommand('*ESR', 7, 0, EventStatusBitDict)

    serial_poll_enable = IntCommand('*SRE')
    serial_poll = IntGetCommand('*STB')
    serial_poll_enable_bit = BoolIndexCommand('*SRE', 7, 0, SerialPollStatusBitDict)
    serial_poll_bit = BoolIndexGetCommand('*STB', 7, 0, SerialPollStatusBitDict)

    power_on_status_clear_bit = BoolCommand('*PSC')

    error_enable = IntCommand('ERRE')
    error = IntGetCommand('ERRS')
    error_enable_bit = BoolIndexCommand('ERRE', 7, 0, ErrorStatusBitDict)
    error_bit = BoolIndexGetCommand('ERRS', 7, 0, ErrorStatusBitDict)

    lock_in_enable = IntCommand('LIAE')
    lock_in = IntGetCommand('LIAS')
    lock_in_enable_bit = BoolIndexCommand('LIAE', 14, 0, LiaStatusBitDict)
    lock_in_bit = BoolIndexGetCommand('LIAS', 14, 0, LiaStatusBitDict)

    overload = IntGetCommand('CUROVLDSTAT')

    exclude_capture = [event_enable_bit, serial_poll_enable_bit,
                       error_enable_bit, lock_in_enable_bit]

    def clear(self):
        self.comm.send('*CLS')

    def get_status_text(self):
        msg = ''
        status_byte = self.serial_poll
        if self.SerialPollStatusBitDict[Keys.ERR]:
            err = self.error
            for key, val in self.ErrorStatusBitDict.items():
                if 2 ** val & err:
                    msg += 'Error bit {}, {} is set, '.format(val, key)

        if self.SerialPollStatusBitDict[Keys.LIA]:
            lia = self.lock_in
            for key, val in self.LiaStatusBitDict.items():
                if 2 ** val & lia:
                    msg += 'LIA status bit {}, {} is set, '.format(val, key)

        if self.SerialPollStatusBitDict[Keys.ESB]:
            event = self.event
            for key, val in self.EventStatusBitDict.items():
                if 2 ** val & event:
                    msg += 'Event status bit {}, {} is set, '.format(val, key)

        ovld = self.overload
        if ovld:
            for key, val in self.OverloadStatusBitDict.items():
                if 2 ** val & ovld:
                    msg += 'Overload bit {}, {}, is set, '.format(val, key)

        if msg == '':
            msg = 'OK,'
        return msg[:-1]
