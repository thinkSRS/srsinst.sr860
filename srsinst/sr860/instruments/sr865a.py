
from .sr860 import SR860


class SR865A(SR860):
    _IdString = 'SR865A'
    MaxFrequency = 4e6

    def __init__(self, interface_type=None, *args):
        super().__init__(interface_type, *args)
        self.ref.__class__.internal_frequency.maximum = self.MaxFrequency
        self.ref.__class__.frequency.maximum = self.MaxFrequency
