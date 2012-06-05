from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse 
import datetime
import utils
from items.models import Item

def index(request):
    return HttpResponse("Blank Page - Updated")

def updateRss(request) :
	try:
		utils.parseRSSEntries('http://www.diariovasco.com/rss/feeds/ultima.xml')
	except Exception as ex:
		return HttpResponse("Exception: %s" %ex)
	
	return HttpResponse("udpateRss")

def updateTw(request):
	try:
		utils.parseTweets('dlacroixe')
	except Exception, e:
		return HttpResponse("Exception: %s" %e)
	
	return HttpResponse("updateTw")

def updateFb(request):
	try:
		utils.parseFBEntries('https://graph.facebook.com/me/feed?access_token=')			
	except Exception, e:
		return HttpResponse("Exception: %s" %e)
	
	return HttpResponse("updateFb")

def updateTT(request):
	try:
		links = utils.parseCoursesLink('http://intranet.eps.mondragon.edu/pls/hor/wwwHor.Lista?pPer=11217&pObj=C&pTipo=2&pCols=1')
		for link in links:
			utils.parseTimeTable(link)
	except Exception, e:
		return HttpResponse("Exception: %s" %e)

	return HttpResponse("updateTT")