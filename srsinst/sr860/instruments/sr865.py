
from .sr860 import SR860


class SR865(SR860):
    _IdString = 'SR86[A]?,'  # Regular expression including SR865 and SR865A
    MaxFrequency = 2e6

    def __init__(self, interface_type=None, *args):
        super().__init__(interface_type, *args)
        self.ref.__class__.internal_frequency.maximum = self.MaxFrequency
        self.ref.__class__.frequency.maximum = self.MaxFrequency
