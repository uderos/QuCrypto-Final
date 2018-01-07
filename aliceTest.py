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
	qbits_list = udr.create_bb84_states(Alice, x, theta_alice)

	#Send the qbits to Bob (via Eve)
	udr.dbg_print("Alice: sending {} qbits to Bob via Eve".format(n))
	udr.send_qbit_list(Alice, "Eve", qbits_list)

	# Wait for acknowledge from Bob
	udr.dbg_print("Alice: waiting for Bob's acknowledge")
	ack = Alice.recvClassical()[0]
	if not ack == udr.classicCmd_RecvAck:
		raise RuntimeError("Alice: invalid ack msg from Bob: {}:{}".
			format(ack, udr.classicCmd_RecvAck ));
	
	# Send Bob our basis string
	udr.dbg_print("Alice: sending Bob the basis string")
	Alice.sendClassical("Bob", theta_alice)

	# Receive Bob's basis string
	udr.dbg_print("Alice: waiting for Bob basis string")
	theta_bob = Alice.recvClassical()
	udr.dbg_print("Alice: got Bob basis string")

	#return udr.ProtocolResult.DebugAbort # UBEDEBUG

	#Discard bits measured in different basis
	x1 = udr.discard_bits(x, theta_alice, theta_bob)
	n1 = len(x1)
	if not n1 > 1:
		print("Alice: only %d bits left after basis check" % n1)
		return udr.ProtocolResult.BasisCheckFailure 

	
	# Generate test string indexes and test bits
	nt = n1 // 2
	idx_test_list = udr.generate_random_indexes(n1, nt)
	xt_alice = udr.generate_sublist_from_idx(x1, idx_test_list)

	# Send test string indexes and values to Bob
	udr.dbg_print("Alice: Sending Bob the test index list")
	Alice.sendClassical("Bob", idx_test_list)
	udr.dbg_print("Alice: Sending Bob test bit string")
	Alice.sendClassical("Bob", xt_alice)

	# Receive test values from Bob and peform error check
	udr.dbg_print("Alice: waiting for Bob's error checking bit list")
	xt_bob = Alice.recvClassical()
	if not xt_alice == xt_bob:
		print("Alice: Error check failure: {}:{}".format(xt_alice, xt_bob))
		return udr.ProtocolResult.ErrorCheckFailure 

	# Remove test bits from bit string
	x2 = udr.generate_sublist_removing_idx(x1, idx_test_list)
	n2 = len(x2)
	if not x2 > 0:
		print("Alice: only %d bits left after error check" % n1)
		return udr.ProtocolResult.NoBitsAfterErrorCheck

	# We are done !
	dbg_print("Alice: x2={}".format(x2))
	return [udr.ProtocolResult.NoBitsAfterErrorCheck, x2]



#####################################################################################################
#
# main
#
def main():

	# Initialize the connection
	Alice = CQCConnection("Alice")

	udr.dbg_print("Alice: opening classical channel with Bob")
	Alice.openClassicalChannel("Bob");
	udr.dbg_print("Alice: classical channel with Bob open")

	# Run the protocol
	rc = run_protocol(Alice)

	# Display results
	udr.print_result("Alice", rc)

	# Stop the connections
	Alice.close()



##################################################################################################
main()

