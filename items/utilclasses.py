
from HTMLParser import HTMLParser

# create a subclass and override the handler methods
class MuTimeTableParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.tableInfo = []
		self.timeTable = [[], [], [], [], []]
		self.i = 0
		self.titFlag = 0
		self.diaFlag = 0
		self.excepFlag = 0
		self.celdaFlag = 0

	def handle_starttag(self, tag, attrs):
		for attr, val in attrs:
			if attr == 'class' and val == "horarioTitDato":
				self.titFlag = 1
			elif attr == 'class' and val == "horarioDia":
				self.diaFlag = 1
			elif attr == 'class' and val == "HorarioExcep":
				self.excepFlag = 1
			elif attr == 'class' and (val == "HorarioRes" or val == "HorarioCelda"):
				self.celdaFlag = 1

	def handle_data(self, data):
		if self.i > 4:
			self.i = 0

		if self.titFlag:
			self.tableInfo.append(data)
			self.titFlag = 0
		elif self.diaFlag:
			self.timeTable[self.i].append(data)
			self.i += 1
			self.diaFlag = 0
		elif self.excepFlag:
			self.timeTable[self.i].append(data)
			self.i += 1
			self.excepFlag = 0
		elif self.celdaFlag:
			#print "Data appended: ", data
			val = "-"
			try:
				oldv = data.encode("utf8", "ignore")
				val = oldv.replace('"', '')
			except Exception, e:
				pass
				#print "Data exception : ", e
			self.timeTable[self.i].append(val)
			self.i += 1
			self.celdaFlag = 0

class MuCoursesListParser(HTMLParser):
	"""docstring for MuCoursesListParser"""
	def __init__(self):
		HTMLParser.__init__(self)
		self.coursesLinks = []
	
	def handle_starttag(self, tag, attrs):
		if tag == 'a':
			for attr, val in attrs:
				if attr == 'href':
					self.coursesLinks.append('http://intranet.eps.mondragon.edu/pls/hor/'+val)

		
			