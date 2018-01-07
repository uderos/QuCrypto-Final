
from SimulaQron.cqc.pythonLib.cqc import *
import udr_utils as udr


#def transfer_qbits(Eve, n, destination):
#	print("Eve: forwarding {} qbits to {}".format(n, destination))
#	for i in range(n):
#		q = Eve.recvQubit();
#		Eve.sendQubit(q, destination)


def run_protocol(Eve):

	# Retrieve test global parameters
	[ n ] = udr.get_exercise_params()

	# Receive Alice's bb84 qbits and forward them to Bob
	alice_qbits = udr.recv_qbit_list(Eve, n)

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

