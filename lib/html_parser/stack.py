class Stack():
	class Element():
		def __init__(self, content, prev = None):
			self.content = content
			self.prev = prev 
	
	def __init__(self):
		self.iterator = None

	def push(self, elem):
		new_elem = self.Element(elem, self.iterator)	
		self.iterator = new_elem	
		
	def pop(self):
		if self.iterator == None:
			raise ValueError("Cannot pop from empty stack")
		result = self.iterator.content
		self.iterator = self.iterator.prev
		return result
	
	def display(self):
		iterator = self.iterator
		while iterator != None:
			print(iterator.content)
			iterator = iterator.prev

	def empty(self):
		return self.iterator == None
