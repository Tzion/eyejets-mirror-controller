import numpy as np
import time

import optoMDC
import optoMDC._connections
from optoMDC.tools.definitions import UnitType, WaveformShape

# connect to the mirror (COM port detected automatically)
mre2 = optoMDC.connectmre2()

# set calibrated closed loop PID values for both channels
for channel in [mre2.Mirror.Channel_0, mre2.Mirror.Channel_1]:
    for pid in [channel.XYPID]:
        pid.set_register("kp", 20)
        pid.set_register("ki", 0.03)
        pid.set_register("kd", 800)

# Setup logger (See Firmware manual for register values)
mre2.Logger.set_register('logged_register_0', 0xe802) # current A: 0xe802
mre2.Logger.set_register('logged_register_1', 0xe902) # current B: 0xe902
mre2.Logger.set_register('logged_register_2', 0x2300) # OF A: 0x2300
mre2.Logger.set_register('logged_register_3', 0x2301) # OF B: 0x2301
mre2.Logger.set_register('logged_register_4', 0x2302) # X: 0x2302
mre2.Logger.set_register('logged_register_5', 0x2303) # Y: 0x2303

logger_numDataPoints = 200 # maximum is 5000
logger_sampleRate = 2000 # maximum is 10000
mre2.Logger.SetSamplingFrequency(logger_sampleRate)

# set control mode to calibrated closed loop on x axis (channel 0)
mre2.Mirror.Channel_0.SetControlMode(UnitType.XY)
# set control mode to open loop on y axis (channel 1)
mre2.Mirror.Channel_1.SetControlMode(UnitType.CURRENT)
# use static input on both axes
mre2.Mirror.Channel_0.StaticInput.SetAsInput()
mre2.Mirror.Channel_1.StaticInput.SetAsInput()

halfStep_deg = 10 # mechanical
halfStep_xy = np.tan(halfStep_deg*2*np.pi/180)/np.tan(50*np.pi/180) # conversion from mech. angle to x,y coordinate

mre2.Mirror.Channel_0.StaticInput.SetXY(-halfStep_xy)
mre2.Mirror.Channel_1.StaticInput.SetCurrent(0)
time.sleep(0.2)

# Perform step from x = -halfStep_xy to x = halfStep_xy
mre2.Logger.RunLogger() # triggers data aquisition
mre2.Mirror.Channel_0.StaticInput.SetXY(halfStep_xy) # change of setpoint

time.sleep(logger_numDataPoints / logger_sampleRate + 0.1)
mre2.Logger.StopLogger() # stop logger after all samples are collected

mre2.Mirror.Channel_0.StaticInput.SetXY(0)

# time will be linearly spaced at the given sampling rate
t = np.linspace(0, logger_numDataPoints/logger_sampleRate, num=logger_numDataPoints, endpoint=False) # in s

# get data from MR-E-2 (takes a while to transmit over serial connection)
cA = mre2.Logger.GetLog(0, 0, logger_numDataPoints)
cB = mre2.Logger.GetLog(1, 0, logger_numDataPoints)
ofA = mre2.Logger.GetLog(2, 0, logger_numDataPoints)
ofB = mre2.Logger.GetLog(3, 0, logger_numDataPoints)
x = mre2.Logger.GetLog(4, 0, logger_numDataPoints)
y = mre2.Logger.GetLog(5, 0, logger_numDataPoints)
import ipdb; ipdb.set_trace()