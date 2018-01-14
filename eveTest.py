
from SimulaQron.cqc.pythonLib.cqc import *
import udr_utils as udr
from ipcCacClient import ipcCacClient


def measure_all_qbits(qbit_list):
	""" Utility function: measure all the qubit of the specified list """
	udr.dbg_print("Eve: *attack*: measuring all of Alice's qbits")
	measureInPlace = True
	for qbit in qbit_list:
		qbit.measure(measureInPlace)
	
def measure_half_qbits(qbit_list):
	""" Utility function: measure half the qubit of the specified list """
	udr.dbg_print("Eve: *attack*: measuring 1/2 of Alice's qbits")
	measureInPlace = True
	flag = False
	for i in range(len(qbit_list)):
		flag = not flag
		if flag:
			qbit_list[i].measure(measureInPlace)
	
def execute_attack(attack, qbit_list):
	""" Execute the attack requested by the user via command line """
	if attack == udr.AttackType.NoAttack:
		udr.dbg_print("Eve: no attack")
	elif attack == udr.AttackType.MeasureAllQbits:
		measure_all_qbits(qbit_list)
	elif attack == udr.AttackType.MeasureHalfQbits:
		measure_half_qbits(qbit_list)
	else:
		raise RuntimeError("Eve: invalid attack code={}".format(attack))

def run_protocol(Eve, cacClient):

	# Retrieve test global parameters
	num_bb84_qbits = udr.get_config_num_qbits()
	attack = udr.get_config_attack_type()

	# Receive Alice's bb84 qbits and forward them to Bob
	alice_qbits = udr.recv_qbit_list(Eve, num_bb84_qbits)

	execute_attack(attack, alice_qbits)

	udr.dbg_print("Eve: received Alice's qbits - forwarding to Bob")

	# Forward Alice's qbits to Bob
	udr.send_qbit_list(Eve, "Bob", alice_qbits)

	udr.dbg_print("Eve: THE END")




#####################################################################################################
#
# main
#
def main():

	try:

		# Initialize the connection
		Eve=CQCConnection("Eve")

		# Initialize the connection to the Classical Authenticated Channel
		cacClient = ipcCacClient('Eve')
		
		# Tell Alice we are running
		# (Alice is such a control freak ...)
		cacClient.sendAck('Alice')

		# Run the protocol
		key = None
		if not udr.get_config_skip_protocol():
			key = run_protocol(Eve, cacClient)
	
	except Exception as e:
		print("\n EVE: EXCEPTION: {}".format(e))


	finally:
		# Stop the connection
		Eve.close()

##################################################################################################
main()

