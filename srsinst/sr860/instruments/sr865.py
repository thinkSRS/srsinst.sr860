
from .sr860 import SR860


class SR865(SR860):
    _IdString = 'SR86[A]?,'  # Regular expression including SR865 and SR865A
    MaxFreqeuency = 2e6