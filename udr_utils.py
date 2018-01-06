
#############################################################################
# udr_utils module - BEGIN
#############################################################################

from SimulaQron.cqc.pythonLib.cqc import *
import random
from enum import Enum

class CommId(Enum):
	RecvAck = 1

class ProtocolResult(Enum):
	Success = 1,
	BasisCheckFailure = 2,
	ErrorCheckFailure = 3,
	NoBitsAfterErrorCheck = 4


def get_exercise_params():
	n = 8 # number of qbits
	return [ n ]


def generate_random_bits(n):
	bit_list = []
	for i in list(range(n)):
		x = random.randint(0,1)
		bit_list.append(x)
	return bit_list
		
def send_qbit_list(cqcc_from, name_to, qbit_list):
	for qb in qbit_list:
		cqccfrom.sendQubit(qb, name_to)

def recv_qbit_list(cqcc_dest, n):
	qbit_list = []
	for i in range(n):
		qb = cqcc_dest.recvQubit()

def measure_single_bb84_qbit(qbit, theta):
	m = 0
	if theta == 0:
		return qbit.measure()
	if theta == 1:
		return qbit.H().measure()
	raise RuntimeError("Invalid theta value: {}."format(theta))
	
def measure_bb84_qbit_list(qbit_list, theta_list):
	if not size(qbit_list) == size(theta_list):
	raise RuntimeError("Size mismatch: {}:{}".format(
		size(qbit_list), size(theta_list)))
	meas_list = []
	for i in range(size(qbit_list)):
		m = measure_single_bb84_qbit(qbit_list[i], theta_list[i])
		meas_list.append(m)
	return meas_list
		

def create_bb84_single_state(cqcc, x, theta):
	""" Create a qbit in the specified BB84 state.

		Args:
			x: 		the classical bit to be encoded
			theta:	the basis to be used to encode the classical bit

		The qbit is generated as follows:
		x	theta	qbit
		0	0		|0>	
		1	0		|1>	
		0	1		|+>	
		1	1		|->	
	"""

	# Create a new qbit (default state is |0>)
	q=qubit(Alice)

	if x == 1 and theta == 0:
		q.X() # change q from |0> to |1>
	if x == 0 and theta == 1:
		q.H() # change q from |0> to |+>
	if x == 1 and theta == 1:
		q.X() # change q from |0> to |1>
		q.H() # change q from |1> to |->

	return q
		



def create_bb84_states(cqcc, x_list, theta_list):
	""" Create a list qbits in the specified BB84 states.
		Args:
			x_list:		the classical bits to be encoded
			theta_list:	the basis to be used to encode the classical bits
	"""
	qbit_list = []
	if not size(x_list) == size(theta_list):
		raise RuntimeError("create_bb84_states size mismatch: {}:{}".format(
			size(x_list), size(theta_list)))
	for i in range(size(x_list)):
		q = create_bb84_single_state(cqcc, x_list[i], theta_list[i])
		qbit.append(q)
	return qbit_list

def discard_bits(bit_list, theta_list_1, theta_list_2):
	if not ((size(bit_list) == size(theta_list_1)) and \
		    (size(bit_list) == size(theta_list_2))):
		raise RuntimeError("create_bb84_states size mismatch: {}:{}:{}".format(
			size(bit_list), size(theta_list_1), size(theta_list_2)))
	result_list = []
	for i in range(size(bits_list)):
		if theta_list_1[i] == theta_list_2[i]:
			result_list.append(bits_list[i])
	return result_list

def generate_random_indexes(list_size, sublist_size):
	l = list(range(list_size))
	random.shuffle(l)
	l = l[0:sublist_size]
	return l

def generate_sublist_from_idx(full_list, idx_sublist):
	l = []
	for i in idx_sublist:
		l.append(full_list[i])
	return l

def generate_sublist_removing_idx(full_list, idx_sublist):
	tag = "TAG"
	l1 = list(full_list)
	for i in idx_sublist:
		l[i] = tag
	l2 = [e in l1 if not e == tag]
	return l2

def print_result(player, rc):
	print("{} protocol result: {}".format(who, rc))

#############################################################################
# udr_utils module - END
#############################################################################

