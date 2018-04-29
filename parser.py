# parse XML files

from lib import html_parser
import os

class Parser:
	# convert file to python dictionary
	@staticmethod
	def readFile(file):
		if not os.path.exists(file):
			raise ValueError("File does not exist.")

		file = open(file, "r")
		text = file.read()
		file.close()

		parsed = html_parser.HTML(text)
		json = parsed.fromXML()
		return json

	@staticmethod
	def getDirList(dir):
		try:
			return os.listdir(dir)
		except:
			raise ValueError("Directory does not exist.")

	# convert all files in a directory to dictionary
	@staticmethod
	def convertDirJSON(dir):
		dirList = Parser.getDirList(dir)
		total = []
		length = len(dirList)
		checkpoint = length // 20
		count = 0

		print("Starting...")
		for filename in dirList:
			count += 1
			if count % checkpoint == 0:
				print(str(int(float(count) / length * 100)) + "%")
			file = (dir if dir[-1] == "/" else dir + "/") + filename
			result = Parser.readFile(file)[0]
			result["path"] = filename
			total.append(result)

		return total
