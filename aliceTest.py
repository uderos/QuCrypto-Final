import random
import time
from SimulaQron.cqc.pythonLib.cqc import *
import udr_utils as udr
from ipcCacClient import ipcCacClient

def run_protocol(Alice, cacClient):

	# Retrieve test global parameters
	num_bb84_qbits = udr.get_config_num_qbits()

	#Generate a set of random classical bits (x)
	x = udr.generate_random_bits(num_bb84_qbits)
	udr.dbg_print("Alice: x={}".format(x))

	#Generate a set of random classical bits (theta)
	theta_alice = udr.generate_random_bits(num_bb84_qbits)

	#Generate the set of bb84 qbits
	qbits_list = udr.create_bb84_states(Alice, x, theta_alice)

	#Send the qbits to Bob (via Eve)
	udr.dbg_print("Alice: sending {} qbits to Bob via Eve".format(num_bb84_qbits))
	udr.send_qbit_list(Alice, "Eve", qbits_list)

	# Wait for acknowledge from Bob
	udr.dbg_print("Alice: waiting for Bob's acknowledge")
	cacClient.getAck('Bob')
	
	# Send Bob our basis string
	udr.dbg_print("Alice: sending Bob the basis string")
	cacClient.sendValueList('Bob', theta_alice)

	# Receive Bob's basis string
	udr.dbg_print("Alice: waiting for Bob basis string")
	theta_bob = cacClient.getValueList('Bob')
	udr.dbg_print("Alice: got Bob basis string")
	udr.dbg_print("Alice: alice_basis={}".format(theta_alice))
	udr.dbg_print("Alice:   bob_basis={}".format(theta_bob))

	#Discard bits measured in different basis
	x1 = udr.discard_bits(x, theta_alice, theta_bob)
	udr.dbg_print("Alice: x1={}".format(x1))
	n1 = len(x1)
	if not n1 > 1:
		raise udr.bb84Error_NoBitsBasisCkeck(
			"Alice: only {} bits left after basis check".format(n1))
	
	# Generate test string indexes and test bits
	nt = n1 // 2
	idx_test_list = udr.generate_random_indexes(n1, nt)
	xt_alice = udr.generate_sublist_from_idx(x1, idx_test_list)

	# Send test string indexes and values to Bob
	udr.dbg_print("Alice: Sending Bob the test index list")
	cacClient.sendValueList('Bob', idx_test_list)
	time.sleep(2)
	udr.dbg_print("Alice: Sending Bob test bit string")
	cacClient.sendValueList('Bob', xt_alice)

	# Receive test values from Bob and peform error check
	udr.dbg_print("Alice: waiting for Bob's error checking bit list")
	xt_bob = cacClient.getValueList('Bob')
	udr.dbg_print("Alice: xt_alice={}".format(xt_alice))
	udr.dbg_print("Alice:   xt_bob={}".format(xt_bob))
	if not xt_alice == xt_bob:
		raise udr.bb84Error_TestCheck("Alice: Error check failure: {}:{}".
			format(xt_alice, xt_bob))

	# Remove test bits from bit string
	x2 = udr.generate_sublist_removing_idx(x1, idx_test_list)
	udr.dbg_print("Alice: x2={}".format(x2))
	n2 = len(x2)
	if not n2 > 0:
		raise udr.bb84Error_TestCheck("Alice: only {} bits left after error check".
			format(n2))

	# Calculate the key as xor of the remaining bits
	key_bit = udr.calculate_bit_list_xor(x2)
	udr.dbg_print("Alice: key_bit={}".format(key_bit))

	# We are done !
	return key_bit



#####################################################################################################
#
# main
#
def main():

	try:

		# Initialize the connection to the quantum channel
		Alice = CQCConnection("Alice")

		# Initialize the connection to the Classical Authenticated Channel
		cacClient = ipcCacClient('Alice')

		# Be sure Bob and Eve are running
		# (Alice is a control freak)
		cacClient.getAck('Bob')
		cacClient.getAck('Eve')

		# Run the protocol
		key = None
		if not udr.get_config_skip_protocol():
			key = run_protocol(Alice, cacClient)

		# Display results
		time.sleep(1)
		udr.print_result("Alice", key)

	except udr.bb84Error as e:
		print("\n ALICE: ##Protocol Failure## {}".format(e))

	except Exception as e:
		print("\n ALICE: ##EXCEPTION## {}".format(e))

	finally:
		# Stop the connections
		Alice.close()

		# Alice is in charge of closing the CAC channel as well
		cacClient.closeChannel()



##################################################################################################
main()

