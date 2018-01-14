# QuCrypto-Final by uders (ubehome@gmail.com)

Files list:

# Classical communication library (a CAC channel)
ipcCacClient.py
ipcClient.py
ipcCommon.py
ipcServer.py
msgContainer.py

# Misc utility functions
udr_utils.py

# The player: Alice, Bob & Eve
aliceTest.py
bobTest.py
eveTest.py

# How to run the test
1. Start SimulaCron:
Change directory to ~/classes/QuCryptox-2017/src/SimulaQron
export NETSIM=~/classes/QuCryptox-2017/src
export PYTHONPATH=classes/QuCryptox-2017/src:$PYTHONPATH
sh run/startAll.sh

2. From this directory, execuot:
sh ./run_example.sh


# Configuration
- Some options can be specified in run_example.sh
- IP addresses and port numbers for classical communications are defined in ipcComon.py.
By default, all processes use 'localhost' and port 5005



