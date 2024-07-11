Connection fails when using the Python SDK:

code:
```
import optoMDC
mre2 = optoMDC.connectmre2()
sig_gen = mre2.Mirror.Channel_0.SignalGenerator
sig_gen.SetAmplitude(0.1)
```

Error:
boundary error
boundary error
boundary error
boundary error
Warning: Required serial read several attempts, number of attempts: 4
Exception: ('Interface Error', 'No connection')

Full Stack Trace:
>> sig_gen.SetAmplitude(0.1)

>>>

boundary error
boundary error
boundary error
boundary error
Warning: Required serial read several attempts, number of attempts: 4
---------------------------------------------------------------------------
Exception                                 Traceback (most recent call last)
Cell In[16], line 1
----> 1 sig_gen.SetAmplitude(0.1)

File ~/eyejets/MR-E-2-controller/venv_pi/lib/python3.11/site-packages/optoKummenberg/registers/InputStage.py:490, in SignalGenerator.SetAmplitude(self, value)
    489 def SetAmplitude(self, value):
--> 490     return self.set_register('amplitude', value)

File ~/eyejets/MR-E-2-controller/venv_pi/lib/python3.11/site-packages/optoKummenberg/registers/ClassAbstracts.py:25, in System.set_register(self, register_name_or_id, value, set_internal)
     23 if reg['type'] is float:
     24     value = float(value)
---> 25 response = self._board.set_value(reg, value)
     26 if isinstance(value, list):
     27     value = value[0]

File ~/eyejets/MR-E-2-controller/venv_pi/lib/python3.11/site-packages/optoKummenberg/commands.py:492, in Command.set_value(self, register, value)
    489 else:
    490     # perform encode, issue, process
    491     data = encode(*cmd_reg_val)
--> 492     response = issue_command(self, data)
    493     if not response:
    494         print('No reply received')

File ~/eyejets/MR-E-2-controller/venv_pi/lib/python3.11/site-packages/optoKummenberg/tools/command_tools.py:106, in issue_command(board, command_bytes)
    103     print("Error: Length of response is 0")
    105 if number_of_attempts > 3:
--> 106     raise Exception('Interface Error', 'No connection')
    108 board.Connection._comm_lock = True
    110 return response

Exception: ('Interface Error', 'No connection')