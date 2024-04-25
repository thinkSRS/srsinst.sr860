
from .instruments.vxi11interface import Vxi11Interface
from .instruments.visainterface import VisaInterface

from .instruments.sr860 import SR860

# SR860 is available with other names
SR865 = SR860
SR865A = SR860

from .instruments.keys import Keys

from .instruments.get_instruments import get_sr860

__version__ = "0.2"