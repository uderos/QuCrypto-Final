
from SimulaQron.cqc.pythonLib.cqc import *

import udr_utils as udr
import statistics

def test1():
	print("test1() - BEGIN")
	[ n ] = udr.get_exercise_params()
	print("n={}".format(n))

	for i in range(1,16):
		qbl = udr.generate_random_bits(i)
		mean = statistics.mean(qbl)
		print("rnd_bits_{}: {} mean={}".format(i,qbl,mean))


def main():
	test1()


main()

