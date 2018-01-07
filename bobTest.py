from SimulaQron.cqc.pythonLib.cqc import *
import udr_utils as udr


def run_protocol(Bob):
	# Retrieve test global parameters
	[ n ] = udr.get_exercise_params() 

	# Receive bb84 qbits from Alice
	udr.dbg_print("Bob: waiting for bb84 qbits from Alice")
	qbit_list = udr.recv_qbit_list(Bob, n)

	#Generate a set of random classical bits (theta)
	theta_bob = udr.generate_random_bits(n)

	# Measure Alice's bb84 qbits
	x = udr.measure_bb84_qbit_list(qbit_list, theta_bob)
	udr.dbg_print("Bob: x={}".format(x))

	# Send Alice an acknowledge message
	udr.dbg_print("Bob: sending ack to ALice")
	Bob.sendClassical("Alice", udr.classicCmd_RecvAck )

	# Receive Alices's basis string
	udr.dbg_print("Bob: waiting for Alice basis string")
	theta_alice = udr.recv_classic_list(Bob)

	# Send Alice out basis string
	udr.dbg_print("Bob: sending Alice my basis string")
	Bob.sendClassical("Alice", theta_bob)

	#return udr.ProtocolResult.DebugAbort # UBEDEBUG

	#Discard bits measured in different basis
	x1 = udr.discard_bits(x, theta_alice, theta_bob)
	udr.dbg_print("Bob: x1={}".format(x1))
	n1 = len(x1)
	if not n1 > 1:
		print("Bob: only %d bits left after basis check" % n1)
		return udr.ProtocolResult.BasisCheckFailure 

	# Receive test string indexes and values from Alice
	udr.dbg_print("Bob: waiting for Alice's test index list")
	idx_test_list = udr.recv_classic_list(Bob)
	udr.dbg_print("Bob: waiting for Alice's test bit string")
	xt_alice = udr.recv_classic_list(Bob)

	# Generate the test list and send it to Alice
	nt = len(idx_test_list)
	xt_bob = udr.generate_sublist_from_idx(x1, idx_test_list)
	udr.dbg_print("Bob: sending Alice test list")
	Bob.sendClassical("Alice", xt_bob)

	# Peform error check
	if not xt_alice == xt_bob:
		print("Bob: Error check failure: {}:{}".format(xt_bob, xt_alice))
		return udr.ProtocolResult.ErrorCheckFailure 

	# Remove test bits from bit string
	x2 = udr.generate_sublist_removing_idx(x1, idx_test_list)
	udr.dbg_print("Bob: x2={}".format(x2))
	n2 = len(x2)
	if not n2 > 0:
		print("Bob: only %d bits left after error check" % n2)
		return udr.ProtocolResult.NoBitsAfterErrorCheck

	# We are done !
	udr.dbg_print("Bob x2={}".format(x2))
	return [udr.ProtocolResult.Success, x2]


#####################################################################################################
#
# main
#
def main():

	# Initialize the connection
	Bob=CQCConnection("Bob")

	udr.dbg_print("Bob: starting classical server")
	Bob.startClassicalServer()
	udr.dbg_print("Bob: classical server started")

	# Run the protocol
	[rc, key] = run_protocol(Bob)

	# Display results
	udr.print_result("Bob", rc)

	# Stop the connection
	Bob.close()


##################################################################################################
main()

