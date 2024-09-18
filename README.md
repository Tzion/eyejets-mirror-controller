## Hardware setup (how to connect the wires)
1. Connect the SPI connectors from the Raspberry Pi to the Optotune controller (see the pinout scheme of  [Optotune documentation](https://static1.squarespace.com/static/5d9dde8d550f0a5f20b60b6a/t/668e93651084e76f30bf388e/1720619877947/Optotune+MR-E-2+Development+Kit+Rev2.pdf)).  
        
    The relevant connectors are MOSI, MISO, CLK, GND, CE0/NSS, according to this scheme:

        Raspberry pi ::::: Optotune controller
            MOSI <-----------> MOSI
            MISO <-----------> MISO
             CLK <-----------> CLK
             CE0 <-----------> NSS  
             GND <-----------> GND

2. Connect the trigger signal from the light enginge (Maradin) to the Optotune controller.  

    The relevant connectors are TRIG, GND, according to this scheme:

        Maradin ::::: Optotune controller
         TRIG <-----------> TRIG
         GND <------------> GND



## Softwrae Setup (need to be done only once- when installing the software for the first time)
Install the virtual environment:  
```bash
python3 -m venv venv  
source venv/bin/activate  
pip3 install -r requirements.txt  
```
- if installing the requirements fails - install Optotune packages manually from ./packages/ folder

<br><br>


## Usage
Activate the virtual environment:  
> source ~/eyejets-mirror-controller/venv/bin/activate  

Control the mirror by executing the script with the wanted parameters:
> python control_mirrors.py

*for help with the parameters execute:
> python control_mirrors.py --help

<br><br>
### Connecting to the Raspberry Pi
You can either connect wirely (using mouse keyboard and a display) or wirelessly (using SSH).

For wireless connection:
1. **Make sure the Raspberry Pi is connected to the same network as your computer.**
2. Find the IP address of the Raspberry Pi (you can use the command `hostname -I` from the raspberry pi, or `ping raspberrypi.local` from a computer on the same network).
3. Connect to the Raspberry Pi using SSH: `ssh pi@<IP_ADDRESS>`. The default password is `raspberry`.