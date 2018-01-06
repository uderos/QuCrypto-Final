
#############################################################################
# udr_utils module - BEGIN
#############################################################################

from SimulaQron.cqc.pythonLib.cqc import *

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
			size(x_list), size(theta_list))
	for i in list(range(size(x_list))):
		q = create_bb84_single_state(cqcc, x_list[i], theta_list[i])
		qbit.append(q)
	return qbit_list



#############################################################################
# udr_utils module - END
#############################################################################

