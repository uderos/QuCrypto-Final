#!/usr/bin/env python

class ipcCommon:
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

