import numpy as np
import time
import optoMDC
from optoMDC.tools.definitions import UnitType, WaveformShape

# connect to the mirror (COM port detected automatically)
mre2 = optoMDC.connect()

# set calibrated closed loop PID values (for x-axis only)
mre2.Mirror.Channel_0.XYPID.set_register("kp", 3)
mre2.Mirror.Channel_0.XYPID.set_register("ki", 0.01)
mre2.Mirror.Channel_0.XYPID.set_register("kd", 100)
mre2.set_value(0xC014, float(200)) # cutoff filter for derivative control


# Setup logger (See Firmware manual for register values)
mre2.Logger.set_register('logged_register_0', 0xe802) # current A: 0xe802
mre2.Logger.set_register('logged_register_1', 0xe902) # current B: 0xe902
mre2.Logger.set_register('logged_register_2', 0x2300) # OF A: 0x2300
mre2.Logger.set_register('logged_register_3', 0x2301) # OF B: 0x2301
mre2.Logger.set_register('logged_register_4', 0x2302) # X: 0x2302
mre2.Logger.set_register('logged_register_5', 0x2303) # Y: 0x2303

logger_numDataPoints = 1000 # maximum is 5000
logger_sampleRate = 10000 # maximum is 10000
mre2.Logger.SetSamplingFrequency(logger_sampleRate)

# set control mode to calibrated closed loop on x axis (channel 0)
mre2.Mirror.Channel_0.SetControlMode(UnitType.XY)
# set control mode to open loop on y axis (channel 1)
mre2.Mirror.Channel_1.SetControlMode(UnitType.CURRENT)



# use signal generator input on both axes
x_freq = 5 # Hz
FOV_x = 50 # deg
x_amp = np.tan(FOV_x/2*np.pi/180)/np.tan(50/180*np.pi) # calculate x-amplitude from desired FOV


y_freq = 275 # Hz
y_amp = 0.05 # A

sg0 = mre2.Mirror.Channel_0.SignalGenerator
sg1 = mre2.Mirror.Channel_1.SignalGenerator
sg0.SetAsInput()
sg1.SetAsInput()

sg0.SetFrequency(x_freq)
sg0.SetShape(WaveformShape.TRIANGULAR)
sg0.SetUnit(UnitType.XY.value)
sg0.SetAmplitude(x_amp)

sg1.SetFrequency(y_freq)
sg1.SetShape(WaveformShape.SINUSOIDAL)
sg1.SetUnit(UnitType.CURRENT.value)
sg1.SetAmplitude(y_amp)

sg0.Run()
sg1.Run()

time.sleep(3)

mre2.Logger.RunLogger() # start data acquisition
time.sleep(logger_numDataPoints/logger_sampleRate+0.1) # wait long enough before stopping the logger
mre2.Logger.StopLogger()

# turn off signal generator input
sg0.Stop()
sg1.Stop()

# set both axes to open loop
mre2.Mirror.Channel_0.SetControlMode(UnitType.CURRENT) 
mre2.Mirror.Channel_1.SetControlMode(UnitType.CURRENT)

# time will be linearly spaced at the given sampling rate
t = np.linspace(0, logger_numDataPoints/logger_sampleRate, num=logger_numDataPoints, endpoint=False) # in s

# get data from MR-E-2 (takes a while to transmit over serial connection)
cA = mre2.Logger.GetLog(0, 0, logger_numDataPoints) # control current coil A (x)
cB = mre2.Logger.GetLog(1, 0, logger_numDataPoints) # control current coil B (y)
ofA = mre2.Logger.GetLog(2, 0, logger_numDataPoints)# uncalibrated sensor channel A
ofB = mre2.Logger.GetLog(3, 0, logger_numDataPoints)# uncalibration sensor channel B
x = mre2.Logger.GetLog(4, 0, logger_numDataPoints) # calibrated sensor values
y = mre2.Logger.GetLog(5, 0, logger_numDataPoints) # calibrated sensor values