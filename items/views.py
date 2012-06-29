from django.http import HttpResponseRedirect
from django.http import HttpResponse
import utils
from items.models import Account

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
		for ac in Account.objects.filter(active=True, account_type='rss'):
			utils.parseRSSEntries(ac.server_url)
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

def updateTT(request):

	"""
	ua = "Mozilla/5.0 (compatible; Konqueror/3.5.8; Linux)"  
	h = {"User-Agent": ua}  
	r = urllib2.Request("https://campus.eps.mondragon.edu/campus/", headers=h)  
	f = urllib2.urlopen(r)  
	print f.read() 
	"""

	try:
		for ac in Account.objects.filter(active=True, account_type='tt'):
			links = utils.parseCoursesLink(ac.server_url)
			for link in links:
				utils.parseTimeTable(link)
	except Exception, e:
		return HttpResponse("Exception: %s" %e)

	return HttpResponse("updateTT")

def updateMail(request):
	try:
		for ac in Account.objects.filter(active=True, account_type='mail'):
			utils.parsePOPMail(ac.server_url, ac.username, ac.password, ac.content_filter)
	except Exception, e:
		return HttpResponse("Exception: %s" %e)
	return HttpResponse("updateMail")
