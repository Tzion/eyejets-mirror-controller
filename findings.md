
- The SDK allows to set a conncetion to the device and define wave functions
- The code should be executed via raspbery pi connected to the device
- There's a conversion function from the mechanical XY to the optical XY
    `halfStep_xy = np.tan(halfStep_deg*2*np.pi/180)/np.tan(50*np.pi/180) # conversion from mech. angle to x,y coordinate`
- we can use pulse wave function - `sg1.SetShape(WaveformShape.PULSE`
- is may be possible to do it all using the com port and not use raspbery pi


##### unknown:
- what pins should be conencted from the rapsberry pi to the device?
- how to change the code to works with SPI port? (`mre2 = optoMDC.connect() ## original code example`)
