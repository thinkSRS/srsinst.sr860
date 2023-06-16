
from srsgui.inst.exceptions import InstCommunicationError
from srsgui.inst.communications.interface import Interface

try:
    import pyvisa
    VISA_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    VISA_AVAILABLE = False


class VisaInterface(Interface):
    """Interface to use VISA"""

    NAME = 'visa'

    if VISA_AVAILABLE:
        rm = pyvisa.ResourceManager()
    else:
        rm = None

    def __init__(self):
        super(VisaInterface, self).__init__()
        self.type = VisaInterface.NAME
        self._visa = None
        self._resource_name = None
        self._is_connected = False

        if not VISA_AVAILABLE:
            raise ImportError("PyVisa is not installed. Install PyVisa to use VISA interface")

    def connect(self, resource):
        try:
            self._visa = self.rm.open_resource(resource)
            self._resource_name = resource
        except Exception as e:
            raise InstCommunicationError('Failed to connect {}'.format(resource))
        else:
            self._is_connected = True

            if self._connect_callback:
                self._connect_callback('Connected VISA: {}'
                                       .format(self._resource_name))

    def disconnect(self):
        self._visa.close()
        self._is_connected = False
        self._resource_name = None
        if self._disconnect_callback:
            self._disconnect_callback('Disconnected VISA: {}'.format(self._resource_name))

    @staticmethod
    def parse_parameter_string(param_string):
        connect_parameters = []
        params = param_string.split(':', 1)
        interface_type = params[0].strip().lower()
        if interface_type != VisaInterface.NAME:
            return None
        if len(params) <= 1:
            raise ValueError('Not enough parameters in "{}"'.format(param_string))
        else:
            connect_parameters.append(interface_type)  # 'visa'
            connect_parameters.append(params[1])  # resource string
        return connect_parameters

    def _send(self, cmd):
        self._visa.write(cmd)

    def _write_binary(self, binary_array):
        if type(binary_array) not in (bytes, bytearray):
            raise TypeError('_write_binary requires bytes or bytearray')
        self._visa.write_raw(binary_array)

    def _recv(self):
        reply = self._visa.read()
        return reply

    def _read_binary(self, length=-1):
        reply = self._visa.read_bytes(length)
        return reply

    def query_text(self, cmd):
        with self.get_lock():
            reply = self._visa.query(cmd)
        if self._query_callback:
            self._query_callback('Queried Cmd: {} Reply: {}'.format(cmd, reply))

        return reply

    def clear_buffer(self):
        self._visa.clear()

    def get_visa_instrument(self):
        return self._visa

    def get_info(self):
        return {'type': self.type,
                'resource_name': self._resource_name,
                }

    def set_timeout(self, timeout):
        self._timeout = timeout
        if self._visa:
            self._visa.timeout = self._timeout * 1000

    def get_timeout(self):
        return self._timeout

    @classmethod
    def find(cls):
        if not VISA_AVAILABLE:
            return ['No PyVisa installed']
        if not cls.rm:
            return []

        raw_items = cls.rm.list_resources()
        items = []
        for item in raw_items:
            if not item.startswith('ASRL'):
                items.append(item)
        return items


