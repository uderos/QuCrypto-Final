
#############################################################################
# udr_utils module - BEGIN
#############################################################################

from SimulaQron.cqc.pythonLib.cqc import *
import random
from enum import Enum, IntEnum

DBG_PRINT_ENABLED = True


classicCmd_RecvAck = 1

class ProtocolResult(Enum):
	Success = 1,
	BasisCheckFailure = 2,
	ErrorCheckFailure = 3,
	NoBitsAfterErrorCheck = 4,
	DebugAbort = 5

class Players(IntEnum):
	Alice = 0,
	Bob = 1,
	Eve = 2

def get_player_name(player):
	player_names = ["Alice", "Bob", "Eve"]
	if player < len(player_names):
		return player_names[player]
	raise RuntimeError("Invalid player: {}".format(player))


def get_exercise_params():
	n = 8 # number of qbits
	return [ n ]

def dbg_print(msg):
	f = open("logfile.txt", "a")
	f.write("{}\n".format(msg))
	f.close()
	if DBG_PRINT_ENABLED:
		print(msg)

def zz_generate_random_bits(n):
	bit_list = []
	for i in list(range(n)):
		x = random.randint(0,1)
		bit_list.append(x)
	return bit_list
		
def generate_random_bits(n):
	bit_list = []
	x = 1
	for i in list(range(n)):
		x = 1 - x
		bit_list.append(x)
	return bit_list
		
def send_qbit_list(cqcc_from, name_to, qbit_list):
	for qb in qbit_list:
		cqcc_from.sendQubit(qb, name_to)

def recv_qbit_list(cqcc_dest, n):
	qbit_list = []
	for i in range(n):
		qb = cqcc_dest.recvQubit()
		qbit_list.append(qb)
	return qbit_list

def recv_classic_list(cqcc_dest):
	raw_list = cqcc_dest.recvClassical()
	l = []
	for i in range(len(raw_list)):
		l.append(raw_list[i])
	return l

#def raw_list_to_list(raw_list):
#	l = []
#	for i in range(len(raw_list)):
#		l.append(raw_list[i])
#	return l

	

def measure_single_bb84_qbit(qbit, theta):
	if theta == 1:
		qbit.H()
	return qbit.measure()
	
def measure_bb84_qbit_list(qbit_list, theta_list):
	if not len(qbit_list) == len(theta_list):
		raise RuntimeError("Size mismatch: {}:{}".format(
			len(qbit_list), len(theta_list)))
	meas_list = []
	for i in range(len(qbit_list)):
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
	q=qubit(cqcc)

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
	if not len(x_list) == len(theta_list):
		raise RuntimeError("create_bb84_states len mismatch: {}:{}".format(
			len(x_list), len(theta_list)))
	for i in range(len(x_list)):
		q = create_bb84_single_state(cqcc, x_list[i], theta_list[i])
		qbit_list.append(q)
	return qbit_list

def discard_bits(bit_list, theta_list_1, theta_list_2):
	if not ((len(bit_list) == len(theta_list_1)) and \
		    (len(bit_list) == len(theta_list_2))):
		raise RuntimeError("create_bb84_states len mismatch: {}:{}:{}".format(
			len(bit_list), len(theta_list_1), len(theta_list_2)))
	result_list = []
	for i in range(len(bit_list)):
		if theta_list_1[i] == theta_list_2[i]:
			result_list.append(bit_list[i])
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
	l = []
	for i in range(len(full_list)):
		if idx_sublist.count(i) == 0:
			l.append(full_list[i])
	return l

def print_result(player, rc):
	if rc == ProtocolResult.Success:
		print("{} protocol result: SUCCESS".format(player))
	else:
		print("{} protocol result: {}".format(player, rc))

#############################################################################
# udr_utils module - END
#############################################################################

