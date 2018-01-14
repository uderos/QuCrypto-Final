# QuCrypto-Final by uders 
ubehome@gmail.com

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



