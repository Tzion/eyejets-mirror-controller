import optoMDC
import optoMDC._connections
from optoMDC.tools.definitions import UnitType, WaveformShape

board = optoMDC.connectmre2()

board.Logger.GetSamplingFrequency()
