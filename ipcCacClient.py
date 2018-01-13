#!/usr/bin/env python

import socket
import time

import ipcClient
from ipcCommon import ipcCommon


class ipcCacClient:
	def __init__(self, name):
		tcp_addr = ipcCommon.get_tcp_address()
		tcp_port = ipcCommon.get_tcp_port_number()
		self.ipc_client = ipcClient.ipcClient(name, tcp_addr, tcp_port)
		self.ack_string = '#ACK#'
		self.separator = ','

	def sendValueList(self, destination, value_list):
		msg = ""
		separator = ""
		for v in value_list:
			msg += separator
			msg += str(v)
			separator = self.separator
		self.ipc_client.sendMessage(destination, msg)

	def getValueList(self, from_who, timeOut = 5):
		value_list = None
		msg = self.ipc_client.getMessage(from_who)
		if not msg is None:
			value_list = []
			str_list = msg.split(self.separator)
			for s in str_list:
				value_list.append(int(s))
		return value_list

	def sendAck(self, destination):
		self.ipc_client.sendMessage(destination, self.ack_string)

	def getAck(self, from_who):
		msg = self.ipc_client.getMessage(from_who)
		if msg is None:
			raise RuntimeError("No Ack received from {}".format(from_who))
		if not msg == self.ack_string:
			raise RuntimeError("{}: Unexpected msg from {} waiting for ack: {}".
				format(self.name, from_who, msg))

	def clearServer(self):
		self.ipc_client.clearServer()
		
	def closeChannel(self):
		self.ipc_client.stopServer()

