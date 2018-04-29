import re

# root element for entire page
# content is 2-list [(id, content)] where id
# 	0: represents normal text
#	1: represents another Element	
# 	2: represents a comment
class Root(object):
	def __init__(self):
		self.content = [] # children of element

	# print hierarchy view of DOM
	def display(self, level = 0):
		for elem in self.content:
			if elem[0] == 0: # text
				print(" " * 4 * level + elem[1])
			elif elem[0] == 1: # Element
				elem[1].display(level)
			elif elem[0] == 2: # comment
				print(" " * 4 * level + "Comment: " + elem[1])
			elif elem[0] != -1:
				raise ValueError("Unknown code")	
	
	# return string of all plain text content in Element
	# recursively get innerHTML of all children
	def innerHTML(self):
		text = ""
		for elem in self.content:
			if elem[0] == 0: # text
				text += elem[1] + " "
			elif elem[0] == 1:
				text += elem[1].innerHTML() + " "
		return text

	# filter HTML Elements by id, class, or tag
	@staticmethod
	def select_helper(selector, query, recursive = True):
		final = set()
		convert = lambda y: [x[1] for x in y if x[0] == 1]	
		if selector[0] == "*":
			return query
		elif selector[1] in (".", "#") or \
		     (selector[1] == "" and selector[2] == ""): # match tag
			while len(query) > 0:
				sel_filter = set()
				for elem in query:	
					# if class, id, tag match found	
					if (selector[1] == "." and \
					    selector[4] in elem.r("class")) or \
					   (selector[1] == "#" and \
					    selector[4] == elem.r("id")) or \
					   (selector[1] == "" and selector[2] == "" and \
					    elem.tag == selector[4]) or \
					   (selector[0][0] == "[" and \
					    HTML.select_helper_read_bracket(selector[0], elem)):
						final.add(elem)	
	
					# search children if and only if recursive True
					elif recursive:
						sel_filter.update( \
							convert(elem.content))
				query = sel_filter
		return final 

	def select(self, selectors):
		results = set()
		selectors = selectors.split(",")
		selector_pattern = re.compile("(\[.*?\]|([#.]|([>~+])[ ]*([#.]?))?([^*.#~+> \[\]]+)|[*])")
	
		for selector_group in selectors:
			selector_group = selector_pattern.findall(selector_group.lower())
			convert = lambda y: [x[1] for x in y if x[0] == 1]
			query = convert(self.content)
			for selector in selector_group:
				if selector[2] == ">":
					# rearrange selector to match pattern of id/class match
					selector = (selector[0], selector[3], "", "", selector[4])
					new_query = []
					for parent in query:
						new_query.extend(convert(parent.content))
					query = self.select_helper(selector, new_query, False)	
				elif selector[2] == "~":
					# rearrange selector to match pattern of id/class match
					selector = (selector[0], selector[3], "", "", selector[4])
					new_query = set()
					for element in query:
						for i in range(element.position + 1, \
							       len(element.parent.content)):
							elem = element.parent.content[i]	
							if elem[0] == 1:
								new_query.add(elem[1])
					query = self.select_helper(selector, new_query, False)
				elif selector[2] == "+":
					# rearrange selector to match pattern of id/class match
					selector = (selector[0], selector[3], "", "", selector[4])
					new_query = []	
					for element in query:
						if element.position < \
							len(element.parent.content) - 1 and \
						   element.parent.content[element.position + 1][0] == 1:
							new_query.append(element.parent
									.content[element.position + 1][1])
					query = self.select_helper(selector, new_query, False)
				else:
					query = self.select_helper(selector, query)
						
			results.update(query)
		return list(results)

	# convert to python dictionary
	def toList(self, acc = None, ignoreTag = False):
		if hasattr(self, "tag"):
			if acc == None:
				acc = {}

			tags = set()
			duplicate = False
			for elem in self.content:
				id, content = elem
				if id == 1:
					if content.tag in tags:
						duplicate = True
					tags.add(content.tag)	

			if duplicate:
				if (ignoreTag):
					acc["TEXT"] = []	
					x = acc
				else:
					x = dict()
					x["TEXT"] = []
					acc[self.tag] = x 
				for tag in tags:
					x[tag] = []
				for elem in self.content:
					id, content = elem
					if id == 0:
						x["TEXT"].append(content)	
					elif id == 1 and content.tag not in tags:
						content.toList(x)
					elif id == 1:
						y = dict()
						x[content.tag].append(y)
						content.toList(y, True)
			else:
				if (ignoreTag):
					acc["TEXT"] = []	
					x = acc
				else:
					x = dict()
					x["TEXT"] = []
					acc[self.tag] = x 
				for elem in self.content:
					id, content = elem
					if id == 0:
						x["TEXT"].append(content)	
					elif id == 1:
						content.toList(x)
		else:
			acc = list()
			x = acc
			for elem in self.content:
				id, content = elem
				if id == 0:
					x.append(content)	
				elif id == 1:
					x.append(content.toList())
		return acc

# represents an HTML element
# subclass of Root
class Element(Root):
	# "tag" is a string such as "div"
	# "parameters" is a dict
	def __init__(self, tag, parameters, parent, position):
		# initialize super class
		Root.__init__(self)

		self.tag = tag
		self.parameters = dict(parameters)
		self.parent = parent # parent Element
		self.position = position # index of Element in content of parent 
		if "class" in parameters:
			self.parameters["class"] = [x.lower() for x in \
						    self.parameters["class"].split()]
		if "id" in parameters:
			self.parameters["id"] = self.parameters["id"].lower()
	
	# read a parameter
	def r(self, param):
		if param == "class" and "class" not in self.parameters:
			return [] 
		if param not in self.parameters:
			return ""
		return self.parameters[param]
	
	def display(self, level = 0):
		print(" " * 4 * level + self.tag)
		super(Element, self).display(level + 1)

	# print next sibling of self or None
	def nextSibling(self):
		for i in range(self.position + 1, \
			       len(self.parent.content)):
			if self.parent.content[i][0] == 1:
				return self.parent.content[i][1]	
		return None

	# delete Element from DOM tree
	def delete(self):
		self.parent.content[self.position][0] = -1
