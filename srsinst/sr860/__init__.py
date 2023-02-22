
from .instruments.vxi11interface import Vxi11Interface
from .instruments.visainterface import VisaInterface

from .instruments.sr860 import SR860
from .instruments.sr865 import SR865
from .instruments.sr865a import SR865A

from .instruments.get_instruments import get_sr860, get_sr865, get_sr865a

__version__ = "0.0.10"