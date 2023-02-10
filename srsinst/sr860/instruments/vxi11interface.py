
import logging
import vxi11

from srsgui.inst import Interface
from srsgui.inst import InstCommunicationError

logger = logging.getLogger(__file__)


class Vxi11Interface(Interface):
    
    NAME = 'vxi11'

    def __init__(self):
        super().__init__()
        self.type = Vxi11Interface.NAME
        self._vxi = None
        self._ip_address = ''
        self._timeout = 20
        
    def connect(self, ip_address):
        try:
            self._vxi = vxi11.Instrument(ip_address)
            print(self._vxi.ask('*IDN?'))
            self._ip_address = ip_address
            self._is_connected = True
            if self._connect_callback:
                self._connect_callback('Connected VXI11 to {}'
                                       .format(self._ip_address))

        except Exception as e:
            logger.error(e)

    def disconnect(self):
        self._vxi.close()
        self._is_connected = False
        if self._disconnect_callback:
            self._disconnect_callback('Disconnected VXI11 from : {}'.format(self._ip_address))

    @staticmethod
    def parse_parameter_string(param_string):
        connect_parameters = []
        params = param_string.split(':')
        num = len(params)
        interface_type = params[0].strip().lower()
        if interface_type != Vxi11Interface.NAME:
            return None
        if num > 2:
            raise ValueError('Too many parameters in "{}"'.format(param_string))
        if num > 1:
            connect_parameters.append(interface_type)  # 'serial'
            connect_parameters.append(params[1])  # IP address
        return connect_parameters

    def _send(self, cmd):
        self._vxi.write(cmd)

    def _recv(self):
        reply = self._vxi.read()
        return reply

    def _read_binary(self, length=-1):
        """
        Read a fixed number of bytes. VXI11 read_raw returns all the data contained
        in the last packet that covers the length of data.
        It could return larger than the specified size of data.
        """
        reply = self._vxi.read_raw(length)
        return reply

    def query_text(self, cmd):
        with self.get_lock():
            reply = self._vxi.ask(cmd)
        if self._query_callback:
            self._query_callback('Queried Cmd: {} Reply: {}'.format(cmd, reply))

        return reply

    def set_timeout(self, timeout):
        self._timeout = timeout
        if self._vxi:
            self._vxi.timeout = timeout * 1000

    def get_timeout(self):
        return self._timeout

    def clear_buffer(self):
        self._vxi.clear()

    def get_info(self):
        return {'type': self.type,
                'ip_address': self._ip_address,
                }
