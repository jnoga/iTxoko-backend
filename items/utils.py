# -*- coding: latin-1 -*-
#Util functions python file
from utilclasses import MuTimeTableParser, MuCoursesListParser
import urllib
from items.models import Course
from django.utils import encoding
from items.models import Item

#FACEBOOK_API_KEY = '271906152892747'
#FACEBOOK_SECRET_KEY = '73ec426b46c6157b8b45401fda377e6f'

#parses MU Course Links
def parseCoursesLink(url):
	f = urllib.urlopen(url)
	html = f.read()
	f.close()
	parser = MuCoursesListParser()
	parser.feed(html)
	return parser.coursesLinks

#parses RSS entries into db items
def parseRSSEntries(url):
	try:
		import RssLib
		rss = RssLib.RssLib(url).read()
		#print(rss)
		for i in range(0, (len(rss)-1)):
			#auxi = Item.objects.get(title=rss['title'][0])
			it = Item(title=rss['title'][i],
				desc=rss['description'][i],
				author=rss['author'][i],
				category='rss',
				link=rss['link'][i],
				img="",
				pub_date=rss['pubDate'][i])
			it.save()
	except Exception as ex:
		print("Exception: %s" %ex)
		return 0
	return 1

#parses Twitter tweets into db items
def parseTweets(username):
	try:
		from twython import Twython
		twitter = Twython()
		tweets = twitter.getUserTimeline( screen_name = username )
		#print (tweets)
		for t in tweets:
			it = Item(title=t["text"],
				desc=t["text"],
				author=t["user"]["name"],
				category="twitter",
				link="",
				img=t["user"]["profile_image_url_https"],
				pub_date=t["created_at"])
			it.save()
	except Exception, e:
		print("Exception: %s" %e)
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
		print e
		return 0

#check RSS, FB or TW entry exists in DB
def checkEnty(code):
	try:

		return 1
	except Exception, e:
		print e
		return 0
		
#parse Facebook Entry
def parseFBEntries(url):
	try:
		from urllib2 import urlopen
		from simplejson import loads

		FACEBOOK_ACCESS_TOKEN = 'AAAAAAITEghMBANASYFB9sIq5ZBbdd7NyML2FWB1UujSLd22XUqsYY9EaxZCTBIfd0vUeZAebi5qmhjnZAYEZAvZATwDZB3KCxPXVCZAAmyZAZAehnXRYscJbE3'

		entries = loads(urlopen(url+FACEBOOK_ACCESS_TOKEN).read())
		#print(entries)
		for f in entries["data"]:
			#print(type(f))
			#print(f.find("picture"))
			title=""
			desc=""
			link=""
			picture=""

			if "story" in f:
				title=f["story"]
			elif "message" in f:
				title=f["message"]
							
			if "message" in f:
				desc=f["message"]
			elif "name" in f:
				desc=f["name"]
			
			if "link" in f:
				link=f["link"]
			
			if "picture" in f:
				picture=f["picture"]
			elif "icon" in f:
				picture=f["icon"]

			it = Item(title=title,
				desc=desc,
				author=f["from"]["name"],
				category=f["type"],
				link=link,
				img=picture,
				pub_date=f["created_time"])
			print(it)
			#it.save()
			
	except Exception, e:
		print("Exception: %s" %e)
		return 0
	
	return 1

#gets the access token from facebook
def fbAccessToken():
	
	return null

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



