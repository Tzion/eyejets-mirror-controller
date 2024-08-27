
import time
from SPIDevice import SPI
import argparse
import numpy as np

calibration_config = {
    'X': '0.0',
    'Y': '2.0',
    'offset-x': '-1.1',
    'offset-y': '-2.7'
}
mocked_config = {
    'X': '0.0',
    'Y': '0.0',
    'offset-x': '-1.5',
    'offset-y': '-3.0'
}

class MR_E_2:
    _port = ''
    _endian = '>'
    _type_int = 'I'
    _type_flt = 'f'
    _int = _endian + _type_int
    _flt = _endian + _type_flt
    
    sysclk = 18000000
    clkdiv = 16
    def __init__(self, bus, device, freq0, amp_x, freq1=None, amp_y=None, offset_x=0.0, offset_y=0.0, waveform=2, trigger=2):
        self.freq0 = freq0
        self.amp_x = amp_x
        self.freq1 = freq1
        self.amp_y = amp_y
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.waveform = waveform
        self.trigger  = trigger

        self.sig_gen_chnl_1 = 0x60
        if (freq1 is None) != (amp_y is None):
            raise ValueError("Both freq1 and amp1 should be set or unset")
        if freq1 is None and amp_y is None:
            self.freq1 = freq0
            self.amp_y = amp_x
            self.sig_gen_chnl_2 = self.sig_gen_chnl_1
        else:
            self.sig_gen_chnl_2 = 0x61
        
        self.spi = SPI(bus=bus, device=device)
        self.spi._spi_comm.max_speed_hz = self.sysclk//self.clkdiv

    def start(self):
        print("Setting registers values")
        ans = self.spi.set_values(0x40, 0x00, 0x40, 0x05, self.sig_gen_chnl_1, self.sig_gen_chnl_2, self._int)   # Signal-Gen set as input
        print(ans)        

        ans = self.spi.set_values(0x40, 0x02, 0x40, 0x07, 0xC0, 0xC1, self._int)   # both X and Y control stage is set to CALIBRATED PID (match to UnitType of Signal generator value=XY)
        # ans = self.spi.set_values(0x40,0x02, 0x40, 0x07, 0xB0, 0xB1, self._int)   # X and Y axises control stage is set to open loop (so called OPEN LOOP)
        print(ans)
        
        ans = self.spi.set_values(self.sig_gen_chnl_1, 0x00, self.sig_gen_chnl_2, 0x00, 2, 2, self._int)         # Signal-Gen Unit - This must match the Singal Flow Manager's Control Stage's value
        print(ans)
        
        ans = self.spi.set_values(self.sig_gen_chnl_1, 0x02, self.sig_gen_chnl_2, 0x02, self.waveform, self.waveform, self._int)         # Signal-Gen Shape
        print(ans)        
        
        ans = self.spi.set_values(self.sig_gen_chnl_1, 0x03, self.sig_gen_chnl_2, 0x03, self.freq0, self.freq1, self._flt) # Signal-Gen Frequency
        print(ans)
        
        ans = self.spi.set_values(self.sig_gen_chnl_1, 0x04, self.sig_gen_chnl_2, 0x04, self.amp_x, self.amp_y, self._flt)   # Signal-Gen Amplitude
        print(ans)
        
        # Currently offset equals for both X and Y - may need to seperate to axes
        ans = self.spi.set_values(self.sig_gen_chnl_1, 0x05, self.sig_gen_chnl_2, 0x05, self.offset_x, self.offset_y, self._flt)  # Offset
        print(ans)

        ans = self.spi.set_values(self.sig_gen_chnl_1, 0x09, self.sig_gen_chnl_2, 0x09, self.trigger, self.trigger, self._int)  # External trigger
        print(ans)

        print("Staring signal generator")
        # import ipdb; ipdb.set_trace()
        ans = self.spi.set_values(self.sig_gen_chnl_1, 0x01, self.sig_gen_chnl_2, 0x01, 1, 1, self._int)         # Signal-Gen Run
        print(ans)

    def stop(self):
        print("Stopping signal generator")              
        ans = self.spi.set_values(self.sig_gen_chnl_1, 0x01, self.sig_gen_chnl_2, 0x01, 0, 0, self._int)  # Signal-Gen Stop
        print(ans)
        
    
def convert_polar_to_cartesian(angle_deg):
    xy_amplitude = np.tan(angle_deg * 2 * np.pi/180)/ np.tan(50*np.pi/180)
    return xy_amplitude
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--start',action='store_true', help='Start the signal generator - run until stop command')
    parser.add_argument('--stop', action='store_true', help='Stop the signal generator')
    parser.add_argument('--debug', action='store_true', help='Pause (breaking point) with debugger')
    parser.add_argument('--x', type=float, help='Angle (in degrees) of axis X', default=calibration_config['X'])
    parser.add_argument('--y', type=float, help='Angle (in degrees) of axis Y', default=calibration_config['Y'])
    parser.add_argument('--freq', type=float, help='Frequency (Hertz) of the movement of the mirror (for both axes!)', default=1)
    parser.add_argument('--offset-x', type=float, help='Offset of generated signal in X axis', default=calibration_config['offset-x'], dest='offset_x')
    parser.add_argument('--offset-y', type=float, help='Offset of generated signal in Y axis', default=calibration_config['offset-y'], dest='offset_y')
    parser.add_argument('--waveform', type=int, choices=[0, 1, 2, 3, 4, 5], help='Waveform type: 0-Sine, 1-Triangle, 2-Square, 3-Sawtooth, 4-Pulse, 5-Staircase', default=2)
    parser.add_argument('--trigger', type=int, choices=[0, 1, 2], help='0=Disabled, 1=Falling edge, 2=Rising edge', default=2)
    args = parser.parse_args()

    x_amplitude = convert_polar_to_cartesian(args.x)
    y_amplitude = convert_polar_to_cartesian(args.y)
    offset_x = convert_polar_to_cartesian(args.offset_x)
    offset_y = convert_polar_to_cartesian(args.offset_y)
    mre2 = MR_E_2(bus=0, device=0, freq0=args.freq, amp_x=x_amplitude, freq1=args.freq, amp_y=y_amplitude, offset_x=offset_x, offset_y=offset_y, waveform=args.waveform, trigger=args.trigger)

    # mre2 = MR_E_2(bus=0, device=0, freq0=1, amp0=0.390996311772799, freq1=1, amp1=0.390996311772799)
    # mre2 = MR_E_2(bus=0, device=0, freq0=.25, amp0=0.0, freq1=0.2, amp1=0.2)
    # mre2 = MR_E_2(bus=0, device=0, freq0=.1, amp0=0.8390996311772799) # X axis 22.5 degrees
    # mre2 = MR_E_2(bus=0, device=0, freq0=0.0, amp0=0.0, freq1=1, amp1=0.8390996311772799) # Y axis 22.5 degrees
    # mre2 = MR_E_2(bus=0, device=0, freq0=.1, amp0=0.38239973293519464) # 12.25 degrees 


    if args.debug:
        import ipdb;
        ipdb.set_trace()
    elif args.stop:
        mre2.stop()
    elif args.start:
        print(f'Starting mirror movement with arguments: {args}')
        mre2.start()
    else:
        mre2.start()
        time.sleep(5)
        mre2.stop()
#
