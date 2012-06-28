from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.utils import simplejson
import datetime
import utils
import urllib
import urllib2
import cookielib
import re
import mechanize
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
		utils.parseRSSEntries('http://www.meneame.net/rss2.php?meta=0')
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

	"""
	ua = "Mozilla/5.0 (compatible; Konqueror/3.5.8; Linux)"  
	h = {"User-Agent": ua}  
	r = urllib2.Request("https://campus.eps.mondragon.edu/campus/", headers=h)  
	f = urllib2.urlopen(r)  
	print f.read() 
	"""

	try:
		links = utils.parseCoursesLink('http://campus.eps.mondragon.edu/pls/hor/wwwHor.Lista?pPer=11218&pObj=C&pTipo=2&pCols=1')
		for link in links:
			utils.parseTimeTable(link)
	except Exception, e:
		return HttpResponse("Exception: %s" %e)

	return HttpResponse("updateTT")

def updateMail(request):
	try:
		utils.parsePOPMail('pop.1and1.es', 'jnogales@gukere.com', '$jn0gal3s', 'contacto@gukere.com')
	except Exception, e:
		return HttpResponse("Exception: %s" %e)
	return HttpResponse("updateMail")

