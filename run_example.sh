#!/bin/sh

ps aux | grep python | grep Test | awk {'print $2'} | xargs kill -9

# delete log file containing debugging messages
rm -f ./logfile.txt

###########################################################
# COMMAND LINE PARAMETERS
###########################################################

# ARGV[1]: Number of BB84 qbits used by the protocol
NUM_BB84_QBITS=10

# ARGV[2]: The type of attack played by Eve:
# 0: no attack
# 1: Eve measures all the qbits sent by Alice to Bob
# 2: Eve measures 1/2 of the qbits sent by Alice to Bob
ATTACK_TYPE=0			

# ARGV[3]: Enable/Disable random generator
# 0: Random generator enabled
# 1: Random generator disabled - it always generates 1010...
DISABLE_RANDOM=0


# Compose the commad line string
CMD_LINE="$NUM_BB84_QBITS  $ATTACK_TYPE $DISABLE_RANDOM"
echo "CMD_LINE=[$CMD_LINE]"

# Start the processes:
# 1. The classical communication server (the CAC channel)
# 2. Alice
# 3. Bob
# 4. Eve
python ipcServer.py &
sleep 1
python aliceTest.py $CMD_LINE &
python bobTest.py $CMD_LINE &
python eveTest.py $CMD_LINE &

