
from SimulaQron.cqc.pythonLib.cqc import *

import udr_utils as udr
import statistics

def test_assert(predicate):
	if not predicate:
		raise RuntimeError("Test Assertion Failure")

def test1():
	print("test1() - BEGIN")
	[ n ] = udr.get_exercise_params()
	print("n={}".format(n))

	for i in range(1,16):
		qbl = udr.generate_random_bits(i)
		mean = statistics.mean(qbl)
		print("rnd_bits_{}: {} mean={}".format(i,qbl,mean))
		test_assert(n == 8)

def test2():
	print("test2() - BEGIN")
	lbegin =   [0, 1, 2, 3, 4, 5]
	theta_1 =  [1, 1, 1, 1, 1, 1]
	theta_2 =  [1, 0, 1, 0, 1, 0] 
	lend = udr.discard_bits(lbegin, theta_1, theta_2)
	print("lbegin={} lend={}".format(lbegin, lend))
	test_assert(lend == [0, 2, 4])

def main():
	Eve=CQCConnection("Eve")

	test1()
	test2()

	Eve.close()

main()

