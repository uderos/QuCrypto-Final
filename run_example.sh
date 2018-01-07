
ps aux | grep python | grep Test | awk {'print $2'} | xargs kill -9

#OPTIONS = "-m trace --trace trace"

python $OPTIONS aliceTest.py &
python $OPTIONS bobTest.py &
python $OPTIONS eveTest.py &
