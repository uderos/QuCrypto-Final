
from SimulaQron.cqc.pythonLib.cqc import *

import udr_utils as udr
import statistics

def test_assert(predicate):
	if not predicate:
		print("\n ## ASSERT FAILURE ## \n")
		raise RuntimeError("Test Assertion Failure")

def test01():
	print("test01() - BEGIN")
	[ n ] = udr.get_exercise_params()
	print("n={}".format(n))

	for i in range(1,16):
		qbl = udr.generate_random_bits(i)
		mean = statistics.mean(qbl)
		print("rnd_bits_{}: {} mean={}".format(i,qbl,mean))
		test_assert(n == 8)

def test02():
	print("test02() - BEGIN")
	lbegin =   [0, 1, 2, 3, 4, 5]
	theta_1 =  [1, 1, 1, 1, 1, 1]
	theta_2 =  [1, 0, 1, 0, 1, 0] 
	lend = udr.discard_bits(lbegin, theta_1, theta_2)
	print("lbegin={} lend={}".format(lbegin, lend))
	test_assert(lend == [0, 2, 4])

def test03():
	print("test03() - BEGIN")
	list_size = 32
	sublist_size = 16
	l = udr.generate_random_indexes(list_size, sublist_size)
	print("l={}".format(l))
	test_assert(len(l) == sublist_size)
	for e in l:
		test_assert(e < list_size)

def test04():
	print("test04() - BEGIN")
	full_list = list(range(16))
	idx_sublist = [15, 1, 10, 4]
	exp_l =  [15, 1, 10, 4]
	calc_l = udr.generate_sublist_from_idx(full_list, idx_sublist)
	test_assert(calc_l == exp_l)

def test05():
	print("test05() - BEGIN")
	full_list = list(range(10))
	idx_sublist = [9, 2, 7, 4]
	exp_l = [0, 1, 3, 5, 6, 8]
	calc_l = generate_sublist_removing_idx(full_list, idx_sublist)
	test_assert(calc_l == exp_l)

def main():
	Eve=CQCConnection("Eve")

	test01()
	test02()
	test03()
	test04()
	test05()

	Eve.close()

main()

