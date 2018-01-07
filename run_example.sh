#!/bin/sh

ps aux | grep python | grep Test | awk {'print $2'} | xargs kill -9

rm -f ./logfile.txt

NUM_BB84_QBITS=8
ATTACK_TYPE=1

CMD_LINE="$NUM_BB84_QBITS  $ATTACK_TYPE"
echo "CMD_LINE=[$CMD_LINE]"

python aliceTest.py $CMD_LINE &
python bobTest.py $CMD_LINE &
python eveTest.py $CMD_LINE &

