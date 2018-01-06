from SimulaQron.cqc.pythonLib.cqc import *
import udr_utils as udr


def run_protocol(Bob):
	# Retrieve test global parameters
	[ n ] = udr.get_exercise_params() 

	# Receive bb84 qbits from Alice
	qbit_list = recv_qbit_list(Bob, n)

	#Generate a set of random classical bits (theta)
	theta_bob = udr.generate_random_bits(n)

	# Measure Alice's bb84 qbits
	x = measure_bb84_qbit_list(qbit_list, theta_bob):

	# Send Alice an acknowledge message
	Bob.sendClassical("Alice", udr.CommId.ReckAck)

	# Receive Alices's basis string
	theta_alice = Bob.recvClassical()

	# Send Alice out basis string
	Bob.sendClassical("Alice", theta_bob)

	#Discard bits measured in different basis
	x1 = udr.discard_bits(x, theta_list_alice, theta_list_bob):
	n1 = size(x1)
	if not n1 > 1:
		print("Bob: only %d bits left after basis check" % n1)
		return udr.ProtocolResult.BasisCheckFailure 

	# Receive test string indexes and values from Alice
	idx_test_list = Bob.recvClassical()
	xt_alice = Bob.recvClassical()

	# Generate the test list and send it to Alice
	nt = size(idx_test_list)
	xt_bob = generate_sublist_from_idx(x1, idx_test_list)
	Bob.sendClassical("Alice", xt_bob)

	# Peform error check
	if not xt_alice == xt_bob:
		print("Bob: Error check failure: {}:{}".format(xt_bob, xt_alice))
		return udr.ProtocolResult.ErrorCheckFailure 


#####################################################################################################
#
# main
#
def main():

	# Initialize the connection
	Bob=CQCConnection("Bob")
	Bob.startClassicalServer()

	# Run the protocol
	rc = run_protocol(Bob)

	# Display results
	udr.print_result("Bob", rc)

#	# Receive qubit from Alice (via Eve)
#	q=Bob.recvQubit()
#	print("Bob retrived a qbit from Alice. q={} type={}".format(q, type(q)))
#
#	# Retreive key
#	k=q.measure()
#	
#	print("Bob qbit measured value is {}".format(k))
#
#	# Receive classical encoded message from Alice
#	enc=Bob.recvClassical()[0]
#
#	# Calculate message
#	m=(enc+k)%2
#
#	print("Bob retrived the message m={} from Alice.".format(m))

	# Stop the connection
	Bob.close()


##################################################################################################
main()

