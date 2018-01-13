
class msgContainer:
	def __init__(self):
		self.data = []

	def __str__(self):
		return str(self.data)

	def __repr__(self):
		return repr(self.data)

	def clear(self):
		self.data = []

	def addMessage(self, fromNode, toNode, msg):
		for elem in self.data:
			if elem[0] == (fromNode, toNode):
				elem[1].append(msg)
				return
		new_elem = [ (fromNode, toNode), [ msg ] ]
		self.data.append(new_elem)

	def getMessage(self, fromNode, toNode):
		for elem in self.data:
			if elem[0] == (fromNode, toNode):
				msg_list = elem[1]
				if len(msg_list) == 0:
					return None
				return msg_list.pop(0)

	def dump(self):
		print("msgContainer Dump: {} elements".format(len(self.data)))
		for elem in self.data:
			print("\t{}".format(elem))
		

#############################################################################
# UNIT TESTING
#############################################################################

def utest1():
	print("\n## TEST 1")
	c = msgContainer()
	print("After construction: str='{}' repr='{}".format(str(c), repr(c)))

	c.addMessage('alice', 'bob', 'msg1')
	print("After 1st message: str='{}' repr='{}".format(str(c), repr(c)))

	c.addMessage('alice', 'bob', 'msg2')
	c.addMessage('alice', 'bob', 'msg3')
	print("After 3rd message: str='{}'".format(str(c), repr(c)))

	c.addMessage('bob', 'eve', 'msg_b_e_1')
	c.addMessage('bob', 'eve', 'msg_b_e_2')
	print("After bob=>evd msgs: {}".format(str(c), repr(c)))

def utest2():
	print("\n## TEST 2")
	c = msgContainer()
	c.addMessage('alice', 'bob', 'ab-msg1')
	c.addMessage('bob', 'eve', 'be-msg1')
	c.addMessage('alice', 'bob', 'ab-msg2')
	c.addMessage('bob', 'eve', 'be-msg2')
	c.addMessage('alice', 'bob', 'ab-msg3')
	c.addMessage('bob', 'eve', 'be-msg3')

	print("Before reading: {}".format(c))
	print("from alice to bob: {}".format(c.getMessage('alice', 'bob')))
	print("from bob to eve: {}".format(c.getMessage('bob', 'eve')))
	print("from alice to bob: {}".format(c.getMessage('alice', 'bob')))
	print("from bob to eve: {}".format(c.getMessage('bob', 'eve')))
	print("from alice to bob: {}".format(c.getMessage('alice', 'bob')))
	print("from bob to eve: {}".format(c.getMessage('bob', 'eve')))
	print("from alice to bob: {}".format(c.getMessage('alice', 'bob')))
	print("from bob to eve: {}".format(c.getMessage('bob', 'eve')))
	print("After reading: {}".format(c))

	c.addMessage('alice', 'bob', 'ab-msg4')
	c.addMessage('bob', 'eve', 'be-msg4')
	print("from alice to bob: {}".format(c.getMessage('alice', 'bob')))
	print("from bob to eve: {}".format(c.getMessage('bob', 'eve')))

	print("from eve to alice: {}".format(c.getMessage('eve', 'alice')))
	c.clear();
	print("Reading from empty container: {}".format(c.getMessage('eve', 'alice')))

def unit_test():
	utest1()
	utest2()

if __name__ == '__main__':
	unit_test()
			

	
