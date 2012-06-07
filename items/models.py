from django.db import models
from django.contrib.auth.models import User
import datetime

class UserProfile(models.Model):
	user = models.OneToOneField(User)

	campus = models.CharField(max_length=50)
	loghash = models.CharField(max_length=50)
		
class Item(models.Model) :
	title = models.CharField(max_length=200)
	desc = models.CharField(max_length=1000)
	author = models.CharField(max_length=50)
	link = models.CharField(max_length=300)
	img = models.CharField(max_length=300)
	category = models.CharField(max_length=300)
	pub_date = models.CharField(max_length=200)
	save_date = models.DateTimeField(("Date"), auto_now_add = True)


	def __unicode__(self):
		return self.title
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
		
		