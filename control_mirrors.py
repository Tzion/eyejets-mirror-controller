
import time
from SPIDevice import SPI
import argparse

class MR_E_2:
    _port = ''
    _endian = '>'
    _type_int = 'I'
    _type_flt = 'f'
    _int = _endian + _type_int
    _flt = _endian + _type_flt
    
    sysclk = 18000000
    clkdiv = 16
    def __init__(self, bus, device, freq0, amp0, freq1=None, amp1=None):
        self.freq0 = freq0
        self.amp0 = amp0
        self.freq1 = freq1
        self.amp1 = amp1
        self.sig_gen_chnl_1 = 0x60
        if (freq1 is None) != (amp1 is None):
            raise ValueError("Both freq1 and amp1 should be set or unset")
        if freq1 is None and amp1 is None:
            self.freq1 = freq0
            self.amp1 = amp0
            self.sig_gen_chnl_2 = self.sig_gen_chnl_1
        else:
            self.sig_gen_chnl_2 = 0x61
        
        self.spi = SPI(bus=bus, device=device)
        self.spi._spi_comm.max_speed_hz = self.sysclk//self.clkdiv

    def start(self):
        print("Setting registers values")
        ans = self.spi.set_values(0x40, 0x00, 0x40, 0x05, self.sig_gen_chnl_1, self.sig_gen_chnl_2, self._int)   # Signal-Gen set as input
        print(ans)        

        ans = self.spi.set_values(0x40,0x02, 0x40, 0x07, 0xC0, 0xB1, self._int)   # X axis closed loop, Y axis open loop
        print(ans)
        
        ans = self.spi.set_values(self.sig_gen_chnl_1, 0x00, self.sig_gen_chnl_2, 0x00, 2, 2, self._int)         # Signal-Gen Unit
        print(ans)
        
        ans = self.spi.set_values(self.sig_gen_chnl_1, 0x02, self.sig_gen_chnl_2, 0x02, 4, 4, self._int)         # Signal-Gen Shape
        print(ans)        
        
        ans = self.spi.set_values(self.sig_gen_chnl_1, 0x03, self.sig_gen_chnl_2, 0x03, self.freq0, self.freq1, self._flt) # Signal-Gen Frequency
        print(ans)
        
        ans = self.spi.set_values(self.sig_gen_chnl_1, 0x04, self.sig_gen_chnl_2, 0x04, self.amp0, self.amp1, self._flt)   # Signal-Gen Amplitude
        print(ans)
        
        ans = self.spi.set_values(self.sig_gen_chnl_1, 0x09, self.sig_gen_chnl_2, 0x09, 2, 2, self._int)         # External trigger set to rising edge
        print(ans)

        print("Staring signal generator")
        # import ipdb; ipdb.set_trace()
        ans = self.spi.set_values(self.sig_gen_chnl_1, 0x01, self.sig_gen_chnl_2, 0x01, 1, 1, self._int)         # Signal-Gen Run
        print(ans)

    def stop(self):
        print("Stopping signal generator")              
        ans = self.spi.set_values(self.sig_gen_chnl_1, 0x01, self.sig_gen_chnl_2, 0x01, 0, 0, self._int)  # Signal-Gen Stop
        print(ans)
        
        
if __name__ == '__main__':
    mre2 = MR_E_2(bus=0, device=0, freq0=.1, amp0=0.4, freq1=0.1, amp1=0.2)
    # mre2 = MR_E_2(bus=0, device=0, freq0=.2, amp0=1)
    parser = argparse.ArgumentParser()
    parser.add_argument('--start',action='store_true', help='Start the signal generator - run until stop command')
    parser.add_argument('--stop', action='store_true', help='Stop the signal generator')
    args = parser.parse_args()

    if args.stop:
        mre2.stop()
    elif args.start:
        mre2.start()
    else:
        mre2.start()
        time.sleep(5)
        mre2.stop()

