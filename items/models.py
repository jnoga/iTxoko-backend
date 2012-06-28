from django.db import models
import datetime

ACCOUNT_TYPES = (
	('tw', 'Twitter'),
	('rss', 'RSS'),
	('mail', 'E-mail'),
	#('fb', 'Facebook'),
	('tt', 'MU - Time Table')
)

class Account(models.Model):

	name = models.CharField(max_length=200)
	server_url = models.CharField(max_length=300, blank=True)
	username = models.CharField(max_length=100, blank=True)
	password = models.CharField(max_length=200, blank=True)
	content_filter = models.CharField(max_length=200, blank=True)
	account_type = models.CharField(max_length=4, choices=ACCOUNT_TYPES)
	save_date = models.DateTimeField("Date", auto_now_add = True)
	active = models.BooleanField()
	
	def __unicode__(self):
		return self.name
		
class Item(models.Model) :
	title = models.CharField(max_length=200)
	desc = models.CharField(max_length=2000)
	author = models.CharField(max_length=50)
	link = models.CharField(max_length=300)
	img = models.CharField(max_length=300)
	category = models.CharField(max_length=300)
	pub_date = models.CharField(max_length=200)
	save_date = models.DateTimeField(("Date"), auto_now_add = True)
	hashmd5 = models.CharField(max_length=50)

	def __unicode__(self):
		return self.hashmd5
	def was_published_today(self):
		return self.save_date.date() == datetime.date.today()
	was_published_today.short_description = 'Published today?'

class Course(models.Model):
	"""docstring for Course"""
	code = models.CharField(max_length=50)
	name = models.CharField(max_length=200)
	room  = models.CharField(max_length=50)

	def __unicode__(self):
		return self.code + ' - ' + self.name

class WeekDay(models.Model):
	"""docstring for WeekDay"""
	course = models.ForeignKey(Course)
	data = models.CharField(max_length=100)
	valid_data = models.CharField(max_length=100)
	day = models.CharField(max_length=100)

	def __unicode__(self):
		return self.valid_data + ' - ' + self.day

class ClassInfo(models.Model):
	weekday = models.ForeignKey(WeekDay)
	hour = models.CharField(max_length=50)
	subject = models.CharField(max_length=100)
	prof = models.CharField(max_length=100)
	room = models.CharField(max_length=50)

	def __unicode__(self):
		return self.hour
		
		