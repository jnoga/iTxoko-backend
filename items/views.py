from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.utils import simplejson
import datetime
import utils
from items.models import Item

def index(request):
    return HttpResponse("Blank Page - Updated")

def login():
	username = request.POST['username']
	password = request.POST['password']
	ans = {}
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			#login(request, user)
			# Redirect to a success page.
			ans={
				"username": user.username,
				"campus": user.campus
			}
		else:
			# Return a 'disabled account' error message
			ans={
				"error": "disabled account"
			}
	else:
		# Return an 'invalid login' error message.
		ans={
			"error": "invalid login"
		}
	return HttpResponse(simplejson.dumps(ans), mimetype='application/json')

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