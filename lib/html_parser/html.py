import re
from stack import Stack
from dom import Element, Root

class HTML():
	# elements that can't contain anything
	void_elements = ("!doctype", "area", "base", "br", "col", "hr", "img", "input", \
			 "link", "meta", "param", "command", "keygen", "source")

	# elements that can only contain text
	text_only_elements = ("script", "style")
	
	# helper for read_tag to get tag 
	@staticmethod
	def read_tag_label(result, c, tag_content, i):
		if c == "/":
			result["closing_tag"] = True	
			i += 1
		tag = ""

		# -1 for not found any normal character yet
		#  0 for iterating through tag
		#  1 for termination
		flag = -1 
		
		# find substring that makes up tag
		# terminated by either space or forward slash				
		while flag != 1 and i < len(tag_content):
			if tag_content[i] in (" ", "/"):
				if flag != -1:
					flag = 1 
					i -= 1
			else:
				tag += tag_content[i]
				flag = 0
			i += 1

		# HTML tags are case insensitive
		tag = tag.lower()

		# cannot have an empty tag
		if tag == "":
			raise ValueError("Empty tag (2)")
		# cannot close  a tag that is supposed to be empty
		elif result["closing_tag"] is True and \
		     tag in HTML.void_elements:
			raise ValueError("Attempting to close void tag")
		result["tag"] = tag
		return i

	# helper for read_tag to get key and value for parameter 
	@staticmethod
	def read_tag_parameter(result, tag_content, i):
		# starting to find parameters
		p_key = "" 
		p_value = "" 
		flag = False

		# get parameter key
		while i < len(tag_content):
			c = tag_content[i]
			if c == "=":
				flag = True
				i += 1
				break
			elif c == " ":
				while i < len(tag_content):
					c = tag_content[i]
					if c == "=":
						flag = True
						i += 1
						break	
					elif c != " ":
						i -= 1
						break
					i += 1	
				break
			else:
				p_key += c	
			i += 1

		if flag:
			end_char = False
			# loop until content found
			while i < len(tag_content):
				c = tag_content[i]
				if c != " ":
					if c == "\"" or c == "'":
						end_char = c
						i += 1	
					else:
						end_char = " "

					# find content
					while i < len(tag_content):
						c = tag_content[i]
						if c == end_char:
							break	
						else:
							p_value += c	
						i += 1		
					if (i == len(tag_content) and \
					   tag_content[-1] != end_char) \
					   and end_char != " ":
						raise ValueError("Error: ", \
								 tag_content)
					break
				i += 1 
		result["parameters"][p_key] = p_value
		return i


	# reads content inside tag and returns dict containg
	# tag, parameters, closing_tag (bool)
	@staticmethod
	def read_tag(tag_content):
		i = 0
		result = {"tag": None, "parameters": {}, "closing_tag": False}
		first_char = True
		while i < len(tag_content):
			c = tag_content[i]
			if c != " ":
				# name of tag should be first non-space character
				if first_char is True:
					i = HTML.read_tag_label(result, c, tag_content, i)
				else:
					i = HTML.read_tag_parameter(result, tag_content, i)
				first_char = False
			i += 1	
		if result["tag"] == None: raise ValueError("Empty tag (3)")
		return result

	# "code" must be given as a string
	def __init__(self, code):
		self.source_raw = code	
			
		# create stack to keep track of elements being created
		S = Stack()

		# represent DOM as tree
		self.root = Root()
		parent = self.root

		content_index = 0

		# compile regex expressions to match to certain tags
		re_comment = re.compile("^!--(.*)--$")
		re_alphanum = re.compile("^.*[a-zA-Z0-9]+.*$")
		
		i = 0
		while i < len(code):
			c = code[i]
			if c == "<":
				# look for closing > bracket
				try:
					closing_bracket_index = code.index(">", i + 1) 
				except:
					raise ValueError("No closing angle bracket found after: ", \
							 code[i:i+5])

				# content inside tag
				tag_content = code[i + 1 : closing_bracket_index]
				i = closing_bracket_index
				
				if re_alphanum.match(tag_content) == False:
					raise ValueError("Empty tag (1)")
				# if tag is a comment
				elif tag_content[0] == "!" and re_comment.match(tag_content):
					comment_content = re_comment.findall(tag_content)
					if len(comment_content) != 1:
						raise ValueError("Broken regex match on: ", \
								 tag_content)
					comment = [2, comment_content[0]]
					parent.content.append(comment)
				else:
					tag = self.read_tag(tag_content)	
			
					# if it's a closing tag
					if tag["closing_tag"]:
						if S.empty():
							raise ValueError("Unmatched tag end") 
						parent = S.pop()
					else:
						new_element = Element(tag["tag"], tag["parameters"], \
								      parent, len(parent.content))
						parent.content.append([1, new_element])	
						if tag["tag"] not in self.void_elements:
							S.push(parent)
							parent = new_element
						
						# get content of text only elements where html tags are
						# escaped with quotes; ex. <script>text="</script>";</script>
						
						if tag["tag"] in self.text_only_elements:
							i += 1
							text = ""
							# script tag parser
							# currently just look for first </script> tag
							close_match = re.compile("^<[ ]*/[ ]*" + \
										 tag["tag"] + "[ ]*.*?>")
							while i < len(code):
								try:
									bracket_index = code.index("<", i)
								except:
									raise ValueError("Unmatched " + \
											 tag["tag"] + " tag")
								# closing tag found
								match = close_match.match(code[bracket_index:])
								if match:
									i += match.span()[1] - 1	
									break		
								else:
									text += code[i:bracket_index+1]
									i = bracket_index + 1
							parent.content.append([0, text])

			# find plain text content
			elif c != " ":
				text = ""
				while i < len(code):
					if code[i] == "<" or i == len(code) - 1:
						parent.content.append([0, text])
						i -= 1
						break
					else:
						text += code[i]
					i += 1
			i += 1

	# print hierarchy of DOM elements
	def print_DOM(self):
		self.root.display()

	def toList(self):
		return self.root.toList()

	@staticmethod
	def cleanXMLDict(L):
		if isinstance(L, dict):
			P = []
			for key in L:
				_L, valid = HTML.cleanXMLDict(L[key])
				L[key] = _L
				if not valid:
					P.append(key)
			for key in P:
				del L[key]
			
			keys = list(L.keys())
			if len(keys) == 1 and keys[0] == "TEXT":
				L = "".join(L["TEXT"])
			return (L, len(L) != 0)
		elif isinstance(L, list):
			f = lambda x: x[1]		
			g = lambda x: f(HTML.cleanXMLDict(x))
			L = [x for x in L if g(x)]
			return (L, len(L) != 0)
		elif isinstance(L, str):
			L = re.sub("[ ]*\r\n[ ]*", "", L).lstrip().rstrip()
			return (L, len(L) != 0)
		else:
			raise ValueError("Error: expected dictionary or list")

	def fromXML(self):
		L = self.root.toList()
		L, x = self.cleanXMLDict(L)	
		return L
	
	# attribute selector
	@staticmethod
	def select_helper_read_bracket(selector, elem):
		reg = re.compile("\[[ ]*([^ =~\|\^$*]+)[ ]*(=|~=|\|=|\^=|\$=|\*=)?[ ]*(\"(.*?)\"|[^\"\']+?)?\]")	
		match = reg.findall(selector)
		if len(match) != 1:
			raise ValueError("Regex match error")
		match = match[0]
		# checking if element has attribute
		if match[1] == "":
			return match[0] in elem.parameters
		value = match[2] if match[3] == "" else match[3]
		if match[1] == "=":
			return value == elem.r(match[0])
		elif match[1] == "~=":
			return value in elem.r(match[0]).split()
		elif match[1] == "^=":
			return elem.r(match[0])[0:len(value)] == value
		elif match[1] == "|=":
			hyphen_list = elem.r(match[0]).split("-")
			return len(hyphen_list) != 0 and hyphen_list[0] != value
		elif match[1] == "$=":
			return elem.r(match[0])[-len(value):] == value
		elif match[1] == "*=":
			return value in elem.r(match[0])
		else:
			raise ValueError("Regex match error")

	# runs selector on entire page, calls root selector method
	def select(self, selectors):
		return self.root.select(selectors)	

	def get_all_text(self):
		return self.root.innerHTML()
