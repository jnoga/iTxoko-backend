from django.http import HttpResponseRedirect
from django.http import HttpResponse
import utils
<<<<<<< HEAD
import urllib
import urllib2
import cookielib
import re
import mechanize
from items.models import Item
=======
from items.models import Account
>>>>>>> 8bcb2dc31b3989c2e997d23f35bd2ab6847c6c9e



def index(request):
	try:
		for ac in Account.objects.filter(active=True):
			if ac.account_type == 'tw':
				utils.parseTweets(ac.username, ac.content_filter)

			elif ac.account_type == 'tt':
				links = utils.parseCoursesLink(ac.server_url)
				for link in links:
					utils.parseTimeTable(link)

			elif ac.account_type == 'rss':
				utils.parseRSSEntries(ac.server_url)

			elif ac.account_type == 'mail':
				utils.parsePOPMail(ac.server_url, ac.username, ac.password, ac.content_filter)

	except Exception, e:
		return HttpResponse("UpdateException: %s" %e)

	return HttpResponse("Data Updated")


def updateRss(request) :
	try:
<<<<<<< HEAD
		utils.parseRSSEntries('http://www.meneame.net/rss2.php?meta=0')
=======
		for ac in Account.objects.filter(active=True, account_type='rss'):
			utils.parseRSSEntries(ac.server_url)
>>>>>>> 8bcb2dc31b3989c2e997d23f35bd2ab6847c6c9e
	except Exception as ex:
		return HttpResponse("Exception: %s" %ex)
	
	return HttpResponse("udpateRss")

def updateTw(request):
	try:
		for ac in Account.objects.filter(active=True, account_type='tw'):
			utils.parseTweets(ac.username, ac.content_filter)
	except Exception, e:
		return HttpResponse("Exception: %s" %e)
	
	return HttpResponse("updateTw")

"""
def prevUpdateFb(request):
	try:
		pass
	except Exception, e:
		return HttpResponse("Exception: %s" %e)
	
	return HttpResponse("prevUpdateFb")

def updateFb(request):
	try:
		utils.parseFBEntries('https://graph.facebook.com/me/feed?access_token=')			
	except Exception, e:
		return HttpResponse("Exception: %s" %e)
	
	return HttpResponse("updateFb")
"""

def updateTT(request):

	"""
	ua = "Mozilla/5.0 (compatible; Konqueror/3.5.8; Linux)"  
	h = {"User-Agent": ua}  
	r = urllib2.Request("https://campus.eps.mondragon.edu/campus/", headers=h)  
	f = urllib2.urlopen(r)  
	print f.read() 
	"""

	try:
<<<<<<< HEAD
		links = utils.parseCoursesLink('http://campus.eps.mondragon.edu/pls/hor/wwwHor.Lista?pPer=11218&pObj=C&pTipo=2&pCols=1')
		for link in links:
			utils.parseTimeTable(link)
=======
		for ac in Account.objects.filter(active=True, account_type='tt'):
			links = utils.parseCoursesLink(ac.server_url)
			for link in links:
				utils.parseTimeTable(link)
>>>>>>> 8bcb2dc31b3989c2e997d23f35bd2ab6847c6c9e
	except Exception, e:
		return HttpResponse("Exception: %s" %e)

	return HttpResponse("updateTT")

def updateMail(request):
	try:
<<<<<<< HEAD
		utils.parsePOPMail('pop.1and1.es', 'jnogales@gukere.com', '$jn0gal3s', 'contacto@gukere.com')
	except Exception, e:
		return HttpResponse("Exception: %s" %e)
	return HttpResponse("updateMail")

=======
		for ac in Account.objects.filter(active=True, account_type='mail'):
			utils.parsePOPMail(ac.server_url, ac.username, ac.password, ac.content_filter)
	except Exception, e:
		return HttpResponse("Exception: %s" %e)
	return HttpResponse("updateMail")
>>>>>>> 8bcb2dc31b3989c2e997d23f35bd2ab6847c6c9e
