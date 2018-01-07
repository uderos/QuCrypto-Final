
from SimulaQron.cqc.pythonLib.cqc import *
import udr_utils as udr


def measure_half_qbits(qbit_list):
	udr.dbg_print("Eve: *attack*: measuring 1/2 of Alice's qbits")
	measureInPlace = True
	flag = False
	for i in range(len(qbit_list)):
		flag = not flag
		if flag:
			qbit_list[i].measure(measureInPlace)
	
def execute_attack(attack, qbit_list):
	if attack == udr.AttackType.MeasureHalfQbits:
		measure_half_qbits(qbit_list)

def run_protocol(Eve):

	# Retrieve test global parameters
	num_bb84_qbits = udr.get_config_num_qbits()
	attack = udr.get_config_attack_type()

	# Receive Alice's bb84 qbits and forward them to Bob
	alice_qbits = udr.recv_qbit_list(Eve, num_bb84_qbits)

	execute_attack(attack, qbit_list)

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

		run_protocol(Eve)

		# Stop the connection
		Eve.close()

	except Exception as e:
		print("\n ALICE: EXCEPTION: {}".format(e))

##################################################################################################
main()

