from django.conf.urls.defaults import patterns, include, url
from items.api import ItemResource, CourseResource, WeekDayResource, ClassInfoResource
from tastypie.api import Api
# Uncomment the next two lines to enable the admin:
from django.contrib import admin


admin.autodiscover()
rsc = Api(api_name='rsc')
rsc.register(ItemResource())
rsc.register(CourseResource())
rsc.register(WeekDayResource())
rsc.register(ClassInfoResource())

urlpatterns = patterns('',
	# Examples:
    #url(r'^$', 'kanalizador.views.home', name='home'),
    #url(r'^kanalizador/', include('kanalizador.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^refresh/', include('items.urls')),
    #url(r'^updateRss/', include('items.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(rsc.urls)),
    url(r'^update/', include('items.urls')),
)
