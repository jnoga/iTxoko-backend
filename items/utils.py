# -*- coding: utf-8 -*-
#Util functions python file
from utilclasses import MuTimeTableParser, MuCoursesListParser, ContentDataImgParser
import urllib
import hashlib
from items.models import Course
from django.utils import encoding
from items.models import Item

#parse POP Mails into db items
def parsePOPMail(server, username, passw, from_filter):
	try:
		import poplib
		from email.parser import Parser
		
		pop_conn = poplib.POP3_SSL(server)
		pop_conn.user(username)
		pop_conn.pass_(passw)
		
		messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
		messages = ["\n".join(mssg[1]) for mssg in messages]
		messages = [Parser().parsestr(mssg) for mssg in messages]

		for message in messages:

			if from_filter in message['from']:
				body = ""
				flag = 1
				for part in message.get_payload():
					if flag:
						#print part.as_string()
						part.__delitem__('Content-Type')
						#print part['Content-Type']
						body = body + part.as_string()
						flag = 0
				#print body
	
				it = Item(title=message['subject'],
					desc=body[:2000],
					author=message['from'],
					category='mail',
					link="",
					img="",
					pub_date=message['date'])
				checkAndSaveEntry(it)
				"""
				for msg in message.get_payload():
					print msg
				"""
	
		pop_conn.quit()
		return 1
	except Exception, e:
		print("Exception: %s" %e)
		return 0

#parses MU Course Links
def parseCoursesLink(url):
	f = urllib.urlopen(url)
	html = f.read()
	f.close()
	parser = MuCoursesListParser()
	parser.feed(html)
	return parser.coursesLinks

#parse text to unicode
def texto2Unicode(data):
	try:
		"""
		from kitchen.text.converters import to_unicode
		from kitchen.i18n import get_translation_object

		translations = get_translation_object('TextTreater')
		_ = translations.ugettext
		b_ = translations.lgettext
		"""
		#aux = (u'%s') % to_unicode(data, 'utf-8')
		aux = data.encode("utf-8")

		return aux
	except Exception, e:
		print 'ExceptionTextConverter: ', e
		return data

#parses RSS entries into db items
def parseRSSEntries(url):
	try:
		import RssLib
		rss = RssLib.RssLib(url).read()
		
		for i in range(0, (len(rss)-1)):
			#auxi = Item.objects.get(title=rss['title'][0])
			parser = ContentDataImgParser()
			parser.feed(rss['description'][i])
			it = Item(title=texto2Unicode(rss['title'][i]),
				desc=texto2Unicode(parser.plainData),
				author=texto2Unicode(rss['author'][i]),
				#category=texto2Unicode(rss['category'][i]),
				category=texto2Unicode('rss'),
				link=texto2Unicode(rss['link'][i]),
				img=parser.img,
				pub_date=texto2Unicode(rss['pubDate'][i]))
			checkAndSaveEntry(it)
	except Exception as ex:
		print("ExceptionRSS: %s" %ex)
		return 0
	return 1

#parses Twitter tweets into db items
def parseTweets(username, hashtag):
	try:
		from twython import Twython
		twitter = Twython()
		if(username is not None):
			tweets = twitter.getUserTimeline( screen_name = username )
			for t in tweets:
				it = Item(title=texto2Unicode(t["text"]),
					desc=texto2Unicode(t["text"]),
					author=texto2Unicode(t["user"]["screen_name"]),
					category=texto2Unicode("twitter"),
					link="",
					img=texto2Unicode(t["user"]["profile_image_url_https"]),
					pub_date=texto2Unicode(t["created_at"]))
				checkAndSaveEntry(it)
		if(hashtag is not None):
			twhash = twitter.search(q = hashtag)
			for t in twhash["results"]:
				it = Item(title=texto2Unicode(t["text"]),
					desc=texto2Unicode(t["text"]),
					author=texto2Unicode(t["from_user"]),
					category=texto2Unicode("twitter"),
					link="",
					img=texto2Unicode(t["profile_image_url_https"]),
					pub_date=texto2Unicode(t["created_at"]))
				checkAndSaveEntry(it)
	except Exception, e:
		print("ExceptionTW: %s" %e)
		return 0
	return 1

#parses MU Timetable into a TimeTable object
def parseTimeTable(url):
	f = urllib.urlopen(url)
	# Read from the object, storing the page's contents in 's'.
	s = f.read()
	f.close()

	parser = MuTimeTableParser()
	parser.feed(s)

	#Create Course Model
	checkCourse(parser.tableInfo[3])
	c = Course(code=parser.tableInfo[3], room=parser.tableInfo[5], name=parser.tableInfo[4])
	c.save()
	#Create week days for course and fullfill them
	d = c.weekday_set.create(data=parser.tableInfo[0], 
				valid_data=parser.tableInfo[2], 
				day="Astelehena/Lunes")
	d.classinfo_set.create(hour=parser.timeTable[0][1],
							subject=parser.timeTable[0][2],
							prof=parser.timeTable[0][3],
							room=parser.timeTable[0][4])
	d.classinfo_set.create(hour=parser.timeTable[0][5],
							subject=parser.timeTable[0][6],
							prof=parser.timeTable[0][7],
							room=parser.timeTable[0][8])
	d.classinfo_set.create(hour=parser.timeTable[0][9],
							subject=parser.timeTable[0][10],
							prof=parser.timeTable[0][11],
							room=parser.timeTable[0][12])
	d.classinfo_set.create(hour=parser.timeTable[0][13],
							subject=parser.timeTable[0][14],
							prof=parser.timeTable[0][15],
							room=parser.timeTable[0][16])
	d.classinfo_set.create(hour=parser.timeTable[0][17],
							subject=parser.timeTable[0][18],
							prof=parser.timeTable[0][19],
							room=parser.timeTable[0][20])
	d = c.weekday_set.create(data=parser.tableInfo[0], 
				valid_data=parser.tableInfo[2], 
				day="Asteartea/Martes")
	d.classinfo_set.create(hour=parser.timeTable[1][1],
							subject=parser.timeTable[1][2],
							prof=parser.timeTable[1][3],
							room=parser.timeTable[1][4])
	d.classinfo_set.create(hour=parser.timeTable[1][5],
							subject=parser.timeTable[1][6],
							prof=parser.timeTable[1][7],
							room=parser.timeTable[1][8])
	d.classinfo_set.create(hour=parser.timeTable[1][9],
							subject=parser.timeTable[1][10],
							prof=parser.timeTable[1][11],
							room=parser.timeTable[1][12])
	d.classinfo_set.create(hour=parser.timeTable[1][13],
							subject=parser.timeTable[1][14],
							prof=parser.timeTable[1][15],
							room=parser.timeTable[1][16])
	d.classinfo_set.create(hour=parser.timeTable[1][17],
							subject=parser.timeTable[1][18],
							prof=parser.timeTable[1][19],
							room=parser.timeTable[1][20])
	d = c.weekday_set.create(data=parser.tableInfo[0], 
				valid_data=parser.tableInfo[2], 
				day=u'Asteazkena/Miércoles')
	d.classinfo_set.create(hour=parser.timeTable[2][1],
							subject=parser.timeTable[2][2],
							prof=parser.timeTable[2][3],
							room=parser.timeTable[2][4])
	d.classinfo_set.create(hour=parser.timeTable[2][5],
							subject=parser.timeTable[2][6],
							prof=parser.timeTable[2][7],
							room=parser.timeTable[2][8])
	d.classinfo_set.create(hour=parser.timeTable[2][9],
							subject=parser.timeTable[2][10],
							prof=parser.timeTable[2][11],
							room=parser.timeTable[2][12])
	d.classinfo_set.create(hour=parser.timeTable[2][13],
							subject=parser.timeTable[2][14],
							prof=parser.timeTable[2][15],
							room=parser.timeTable[2][16])
	d.classinfo_set.create(hour=parser.timeTable[2][17],
							subject=parser.timeTable[2][18],
							prof=parser.timeTable[2][19],
							room=parser.timeTable[2][20])
	d = c.weekday_set.create(data=parser.tableInfo[0], 
				valid_data=parser.tableInfo[2], 
				day="Osteguna/Jueves")
	d.classinfo_set.create(hour=parser.timeTable[3][1],
							subject=parser.timeTable[3][2],
							prof=parser.timeTable[3][3],
							room=parser.timeTable[3][4])
	d.classinfo_set.create(hour=parser.timeTable[3][5],
							subject=parser.timeTable[3][6],
							prof=parser.timeTable[3][7],
							room=parser.timeTable[3][8])
	d.classinfo_set.create(hour=parser.timeTable[3][9],
							subject=parser.timeTable[3][10],
							prof=parser.timeTable[3][11],
							room=parser.timeTable[3][12])
	d.classinfo_set.create(hour=parser.timeTable[3][13],
							subject=parser.timeTable[3][14],
							prof=parser.timeTable[3][15],
							room=parser.timeTable[3][16])
	d.classinfo_set.create(hour=parser.timeTable[3][17],
							subject=parser.timeTable[3][18],
							prof=parser.timeTable[3][19],
							room=parser.timeTable[3][20])
	d = c.weekday_set.create(data=parser.tableInfo[0], 
				valid_data=parser.tableInfo[2], 
				day="Ostirala/Viernes")
	d.classinfo_set.create(hour=parser.timeTable[4][1],
							subject=parser.timeTable[4][2],
							prof=parser.timeTable[4][3],
							room=parser.timeTable[4][4])
	d.classinfo_set.create(hour=parser.timeTable[4][5],
							subject=parser.timeTable[4][6],
							prof=parser.timeTable[4][7],
							room=parser.timeTable[4][8])
	d.classinfo_set.create(hour=parser.timeTable[4][9],
							subject=parser.timeTable[4][10],
							prof=parser.timeTable[4][11],
							room=parser.timeTable[4][12])
	d.classinfo_set.create(hour=parser.timeTable[4][13],
							subject=parser.timeTable[4][14],
							prof=parser.timeTable[4][15],
							room=parser.timeTable[4][16])
	d.classinfo_set.create(hour=parser.timeTable[4][17],
							subject=parser.timeTable[4][18],
							prof=parser.timeTable[4][19],
							room=parser.timeTable[4][20])
	c.save()
	return c

#check that MU course exists in DB
def checkCourse(code):
	try:
		c=Course.objects.get(code=code)
		c.delete()
		return 1
	except Exception, e:
		print 'ExceptionTT: ', e
		return 0

#check RSS, FB, Mail or TW entry exists in DB
def checkAndSaveEntry(item):

	m = hashlib.md5(item.title+item.author+item.pub_date).hexdigest()

	try:
		it = Item.objects.get(hashmd5=m)
		#exists...
		return it
	except Exception, e:
		#does not exist
		print 'ExceptionSaveIT: ', e
		item.hashmd5 = m
		item.save()
		return item

#parse POP Mails into db items
def parsePOPMail(server, username, passw, filter):
	try:
		import poplib
		from email.parser import Parser
		
		pop_conn = poplib.POP3_SSL(server)
		pop_conn.user(username)
		pop_conn.pass_(passw)
		
		messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
		messages = ["\n".join(mssg[1]) for mssg in messages]
		messages = [Parser().parsestr(mssg) for mssg in messages]
		for message in messages:
			if filter in message['from']:
				
				body = ""
				for part in message.get_payload():
					body = body + part.as_string()
	
				it = Item(title=message['subject'],
					desc=body[:200],
					author=message['from'],
					category='mail',
					link="",
					img="",
					pub_date=message['date'])
				#checkAndSaveEntry(it)
				it.save()
				"""
				
				for msg in message.get_payload():
					print msg
				"""
		
		"""
		for field, val in messages[0]:
			print 'Field: ', field
			print 'Value: ', val
	
		"""
		pop_conn.quit()
		return 1
	except Exception, e:
		print("Exception: %s" %e)
		return 0



