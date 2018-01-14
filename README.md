# QuCrypto - Programming Assignment
by uderos (ubehome@gmail.com)

## The Protocol
I have implemented a simple implementation of the basic B84 protocol.

"Basic" means:
- no information reconciliation
- no privacy amplification
- no noisy communications

The protocol implements the BB84 algorithm defined as "**Protocol 1 — BB84 QKD (no noise)**" in sectin 6.1 of Week 6 Lecture Notes.

Step 9 (privacy amplification) is replaced by xoring all the bits, as required in the assignment.

The only interesting thing in this implementation is that it is possible to "program" Eve:
- Eve can forward Alices's qbits to Bob without touching them
- Eve can measure 1/2 of the qbits
- Eve can measure all the qbits

##Source code
The code is also available at:
[GitHub](https://github.com/uderos/QuCrypto-Final)

- ipcCacClient.py (Classical communication library - a CAC channel)
- ipcClient.py (Classical communication library - a CAC channel)
- ipcCommon.py (Classical communication library - a CAC channel)
- ipcServer.py (Classical communication library - a CAC channel)
- msgContainer.py (Classical communication library - a CAC channel)
- udr_utils.py (Utilitiy functions)
- aliceTest.py (Alice player)
- bobTest.py (Bob Player)
- eveTest.py (Eve  player)

## How to run the test
1.Start SimulaCron:

Change directory to (your-path)/QuCryptox-2017/src/SimulaQron

export NETSIM=(your-path)/QuCryptox-2017/src

export PYTHONPATH=(your-path)/QuCryptox-2017/src:$PYTHONPATH

sh run/startAll.sh

2. From this directory, execute:
sh ./run_example.sh


## Configuration
- Some options can be specified in run_example.sh
- IP addresses and port numbers for classical communications are defined in ipcComon.py.
By default, all processes use 'localhost' and port 5005



