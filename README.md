### Hardware setup
Connect the SPI connectors from the Raspberry Pi to the Optotune controller (see the pinout scheme of  [Optotune documentation](https://static1.squarespace.com/static/5d9dde8d550f0a5f20b60b6a/t/668e93651084e76f30bf388e/1720619877947/Optotune+MR-E-2+Development+Kit+Rev2.pdf)

### Softwrae Setup
Install virtual environment:
    ```
    python3 -m venv venv 
    source venv/bin/activate
    pip3 install -r requirements.txt
    ```
    * if installing the requirements fails - install optotune packages manually from ./packages/ folder

### Usage
Activate the virtual environment.
Control the mirror by executing:
``` python control_mirror.py ```

for help:
``` python control_mirror.py --help ```
