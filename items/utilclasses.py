
from HTMLParser import HTMLParser

class MuSubjectParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.subjectList = {}
		self.tagi = 0
		self.tdi = 0
		self.dataFlag = 0
		self.subName = ""

	def handle_starttag(self, tag, attrs):
		if tag == 'table':
			if self.tagi < 7:
				self.tagi +=1
		elif tag == 'td' and self.tdi < 2 and self.tagi == 7:
			self.tdi += 1
			self.dataFlag = 1

	def handle_endtag(self, tag):
		if tag == 'tr':
			self.tdi = 0
		elif tag == 'table' and self.tagi == 7:
			self.tagi = 0

	def handle_data(self, data):
		if self.dataFlag and self.tdi == 1:
			self.subName = data
			self.dataFlag = 0
		elif self.dataFlag and self.tdi == 2:
			self.subjectList[self.subName] = data
			self.dataFlag = 0

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
			elif attr == 'class' and val == "horarioLeyenDato":
				self.leyenFlag = 1

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
			val = "-"
			try:
				oldv = data.encode("utf8", "ignore")
				val = oldv.replace('"', '')
			except Exception, e:
				pass
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

class ContentDataImgParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.img = ""
		self.imgReady = 1
		self.plainData = ""
	
	def handle_starttag(self, tag, attrs):
		if tag == 'img' and self.imgReady:
			for attr, val in attrs:
				if attr == 'src':
					self.img = val
					self.imgReady = 0

	def handle_data(self, data):
		self.plainData += data +" "