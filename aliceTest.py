import random
from SimulaQron.cqc.pythonLib.cqc import *
import udr_utils as udr

def run_protocol(Alice):
	# Retrieve test global parameters
	[ n ] = udr.get_exercise_params()

	#Generate a set of random classical bits (x)
	x = udr.generate_random_bits(n)

	#Generate a set of random classical bits (theta)
	theta_alice = udr.generate_random_bits(n)

	#Generate the set of bb84 qbits
	qbits_list = udr.create_bb84_states(Alice, x, theta_alice):

	#Send the qbits to Bob (via Eve)
	udr.send_qbit_list(Alice, "Eve", qbits_list)

	# Wait for acknowledge from Bob
	ack = Alice.recvClassical()[0]
	if not ack == udr.CommId.ReckAck
		raise RuntimeError("Alice: invalid ack msg from Bob: {}:{}".
			format(ack, udr.CommId.ReckAck);
	
	# Send Bob our basis string
	Alice.sendClassical("Bob", theta_alice)

	# Receive Bob's basis string
	theta_bob = Alice.recvClassical()

	#Discard bits measured in different basis
	x1 = udr.discard_bits(x, theta_list_alice, theta_list_bob):
	n1 = size(x1)
	if not n1 > 1:
		print("Alice: only %d bits left after basis check" % n1)
		return udr.ProtocolResult.BasisCheckFailure 

	
	# Generate test string indexes and test bits
	nt = n1 // 2
	idx_test_list = udr.generate_random_indexes(n1, nt)
	xt_alice = generate_sublist_from_idx(x1, idx_test_list)

	# Send test string indexes and values to Bob
	Alice.sendClassical("Bob", idx_test_list)
	Alice.sendClassical("Bob", xt_alice)

	# Receive test values from Bob and peform error check
	xt_bob = Alice.recvClassical()
	if not xt_alice == xt_bob:
		print("Alice: Error check failure: {}:{}".format(xt_alice, xt_bob))
		return udr.ProtocolResult.ErrorCheckFailure 



#####################################################################################################
#
# main
#
def main():

	# Initialize the connection
	Alice = CQCConnection("Alice")

	# Run the protocol
	rc = run_protocol(Alice)

	# Display results
	udr.print_result("Alice", rc)

#
#
#
#	# Create a qubit
#	q=qubit(Alice)
#
#	# Encode the key in the qubit
#	if k==1:
#		q.X()
#
#	#Send qubit to Bob (via Eve)
#	print("Alice is sending qbit to Eve: k={} q={}".format(k,q))
#	Alice.sendQubit(q,"Eve")
#
#	# Encode and send a classical message m to Bob
#	m=0
#	enc=(m+k)%2
#	Alice.sendClassical("Bob",enc)
#
#	print("Alice send the message m={} to Bob".format(m))

	# Stop the connections
	Alice.close()



##################################################################################################
main()

