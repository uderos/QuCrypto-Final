#!/usr/bin/env python

import socket
import time
from ipcCommon import ipcCommon

class ipcClient:
	def __init__(self, name, tcp_addr, tcp_port):
		self.name = name
		self.tcp_addr = tcp_addr
		self.tcp_port = tcp_port
		self.tcp_socket = None
		self.buffer_size = 4096
		self.null_char = chr(0)

	def sendMessage(self, destination, message):
		self.__connect_to_server()
		server_msg = "{}|{}|{}|{}".format(
			ipcCommon.get_cmd_send_message(), self.name, destination, message);
		print("ipcClient({}) ==> '{}'".format(self.name, server_msg))
		self.tcp_socket.sendall(server_msg.encode())
		self.close()

	def getMessage(self, from_who, timeOut = 5):
		server_msg_out = "{}|{}|{}".format(
			ipcCommon.get_cmd_get_message() ,from_who, self.name)
		for i in range(timeOut):
			self.__connect_to_server()
			print("ipcClient({}) ==> '{}'".format(self.name, server_msg_out))
			self.tcp_socket.sendall(server_msg_out.encode())
			raw_msg_in = self.tcp_socket.recv(self.buffer_size)
			#print("ipcClient({}) RawReply: '{}'".format(self.name, raw_msg_in))
			if not ((raw_msg_in is None) or (len(raw_msg_in) <= 1)):
				msg_in = raw_msg_in.decode()
				if msg_in[0] == self.null_char:
					msg_in = None
				print("ipcClient({}) <== '{}'".format(self.name, msg_in))
				return msg_in
			self.close()
			time.sleep(1)
		self.close()
		return None # TBD - throw exception?

	def clearServer(self):
		self.__connect_to_server()
		server_msg = ipcCommon.get_cmd_clear_server()
		print("ipcClient({}) ==> '{}'".format(self.name, server_msg))
		self.tcp_socket.sendall(server_msg.encode())
		self.close()

	def stopServer(self):
		self.__connect_to_server()
		server_msg = ipcCommon.get_cmd_stop_server()
		print("ipcClient({}) ==> '{}'".format(self.name, server_msg))
		self.tcp_socket.sendall(server_msg.encode())
		self.close()

	def close(self):
		if not self.tcp_socket is None:
			self.tcp_socket.shutdown(socket.SHUT_RDWR)
			self.tcp_socket.close()
			self.tcp_socket = None

	def __connect_to_server(self):
		if self.tcp_socket is None:
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.connect((self.tcp_addr, self.tcp_port))
				self.tcp_socket = s
			except Exception as e:
				raise RuntimeError("Unable to connect to server: {}".format(e))

