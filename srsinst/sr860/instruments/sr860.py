
from .vxi11interface import Vxi11Interface
from .visainterface import VisaInterface

from srsgui import Instrument
from srsgui.inst import TcpipInterface, SerialInterface
from srsgui.task.inputs import IntegerListInput, BoolInput, \
                               Ip4Input, IntegerInput, FindListInput

from .components import Reference, Reference2M, Reference4M,\
                        Signal, Output, Aux, Auto, \
                        Display, Chart, FFT, \
                        Scan, Scan2M, Scan4M,\
                        DataTransfer, DataCapture, DataStream,\
                        Status


class SR860(Instrument):
    _IdString = 'SR86[05][A]?,'  # Regular expression including SR860, SR865 and SR865A
    MaxFrequency = Reference.MaxFrequency
    
    available_interfaces = [
        [
            Vxi11Interface,
            {
                'ip_address': Ip4Input('192.168.1.10'),
            }
        ],
        [
            VisaInterface,
            {
                'resource': FindListInput(),
            }
        ],
        [
            TcpipInterface,
            {
                'ip_address': Ip4Input('192.168.1.10'),
                'port': 23
            }
        ],
        [
            SerialInterface,
            {
                'port': FindListInput(),
                'baud_rate': IntegerListInput([9600, 19200, 38400, 115200,
                                               230400, 460800], 3)
            }
        ],
    ]

    def __init__(self, interface_type=None, *args):
        super().__init__(interface_type, *args)

        self.ref = Reference(self)
        self.signal = Signal(self)
        self.output = Output(self)
        self.aux = Aux(self)
        self.auto = Auto(self)
        self.display = Display(self)
        self.chart = Chart(self)
        self.fft = FFT(self)
        self.scan = Scan(self)
        self.data = DataTransfer(self)
        self.capture = DataCapture(self)
        self.stream = DataStream(self)
        self.status = Status(self)

        # Exclude components from capture_commands()
        self.exclude_capture.append(self.display)
        self.exclude_capture.append(self.chart)
        self.exclude_capture.append(self.fft)

    def connect(self, interface_type, *args):
        super().connect(interface_type, *args)
        if isinstance(self.comm, TcpipInterface):
            print(self.query_text(''))  # Read out the initial string

    def check_id(self):
        """
        Check if the instrument is one of SR860 series and adjust
        the maximum frequency depending on the models.
        """
        ids = super().check_id()
        if ids[0] is None:
            return ids
        if 'SR865A' in ids[0]:
            self.MaxFrequency = Reference4M.MaxFrequency
            if type(self.ref) is not Reference4M:
                self.ref = Reference4M(self)
                self.scan = Scan4M(self)
        elif 'SR865' in ids[0]:
            self.MaxFrequency = Reference2M.MaxFrequency
            if type(self.ref) is not Reference2M:
                self.ref = Reference2M(self)
                self.scan = Scan2M(self)
        elif 'SR860' in ids[0]:
            self.MaxFrequency = Reference.MaxFrequency
            if type(self.ref) is not Reference:
                self.ref = Reference(self)
                self.scan = Scan(self)
        return ids

    def reset(self):
        self.send('*RST')

    def get_status(self):
        st = 'Frequency: {:.6e} Hz\n'.format(self.ref.frequency) + \
             ' Phase: {:.6f} deg\n'.format(self.ref.phase) + \
             ' Amplitude: {:.4f} V\n'.format(self.ref.sine_out_amplitude) + \
             ' DC level: {:.4f} V\n'.format(self.ref.sine_out_offset) + \
             ' Harmonic: {}\n\n'.format(self.ref.harmonic) + \
             self.status.get_status_text()
        return st

    allow_run_button = [reset]