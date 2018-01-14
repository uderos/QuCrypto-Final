#!/usr/bin/env python

import socket
import time

import ipcClient
from ipcCommon import ipcCommon


class ipcCacClient:
	def __init__(self, name):
		""" Class constructor - Initialize data members
			Args:
				name: name of this client
		"""
		tcp_addr = ipcCommon.get_tcp_address()
		tcp_port = ipcCommon.get_tcp_port_number()
		self.ipc_client = ipcClient.ipcClient(name, tcp_addr, tcp_port)
		self.ack_string = '#ACK#'
		self.separator = ','

	def sendValueList(self, destination, value_list):
		""" Send a list of values (bits, numbers, alpha-characters) to another
			client.

			Args:
				destination: name of the client the data has to be sent to
				value_list: list of values to be sent
		"""
		msg = ""
		separator = ""
		for v in value_list:
			msg += separator
			msg += str(v)
			separator = self.separator
		self.ipc_client.sendMessage(destination, msg)

	def getValueList(self, from_who, timeOut = 5):
		""" Receive a list of values (bits, numbers, alpha-characters) from
			another client.
			The methods performs some retries (1-second aparts).
			A runtime exception is raised if no message is received.

			Args:
				from_who: name of the client we read the values from
				timeOut: reading timeout (seconds)
			Returns:
				list of values received from the other client
		"""
		value_list = None
		msg = self.ipc_client.getMessage(from_who)
		if not msg is None:
			value_list = []
			str_list = msg.split(self.separator)
			for s in str_list:
				value_list.append(int(s))
		if value_list is None:
			raise RuntimeError("No data received from {}".format(from_who))
		return value_list

	def sendAck(self, destination):
		""" Send an acknowledge message to the specified client.
			Args:
				destination: the client the ack has to be sent to
		"""
		self.ipc_client.sendMessage(destination, self.ack_string)

	def getAck(self, from_who):
		""" Receive an acknowledge message from the specified client.
			Args:
				from_who: the client the ack has to be received from
		"""
		msg = self.ipc_client.getMessage(from_who)
		if msg is None:
			raise RuntimeError("No Ack received from {}".format(from_who))
		if not msg == self.ack_string:
			raise RuntimeError("{}: Unexpected msg from {} waiting for ack: {}".
				format(self.name, from_who, msg))

	def clearServer(self):
		""" Ask the classical communication server to clear any transient data
		"""
		self.ipc_client.clearServer()
		
	def closeChannel(self):
		""" Ask the classical communication server to terminate. """
		self.ipc_client.stopServer()

