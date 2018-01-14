#!/usr/bin/env python


class ipcCommon:
	""" Utlilty static class.
		It provides common constants and utility functions.
	"""

	def __init__(self):
		pass

	def get_tcp_address():
		return 'localhost'

	def get_tcp_port_number():
		return 5005
	
	def get_cmd_send_message():
		return str('SendMsg')

	def get_cmd_get_message():
		return str('GetMsg')

	def get_cmd_clear_server():
		return str('ClearMsgContainer')

	def get_cmd_stop_server():
		return str('StopServer')

	def send_string(session_socket, msg_str):
		out_str = msg_str + ipcCommon.__get_etx_char()
		session_socket.sendall(out_str.encode())

	def recv_data(session_socket):
		data = bytearray()
		etx = ord(ipcCommon.__get_etx_char())
		keep_reading = True
		while keep_reading:
			keep_reading = False
			temp_data = session_socket.recv(256)
			if temp_data:
				keep_reading = True
				nbytes = len(temp_data)
				if nbytes > 0 and temp_data[nbytes-1] == etx:
					nbytes -= 1
					keep_reading = False
				for i in range(nbytes):
					data.append(temp_data[i])
				temp_data= None
		return data

	def __get_etx_char():
		return chr(0x03)

