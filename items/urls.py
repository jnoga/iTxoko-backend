from django.conf.urls.defaults import *
#from django.views.generic import DetailView, ListView
#from items.models import Item

urlpatterns = patterns('',
    url(r'^$', 'items.views.index'),
    #url(r'^$', include(item_resource.urls)),
    url(r'rss/','items.views.updateRss'),
    url(r'tw/','items.views.updateTw'),
    #url(r'prevfb/','items.views.prevUpdateFb'),
    #url(r'fb/','items.views.updateFb'),
    url(r'tt/','items.views.updateTT'),
    url(r'mail/', 'items.views.updateMail'),
    #url(r'^$',
    #    ListView.as_view(
    #        queryset=Item.objects.order_by('-pub_date')[:5],
    #        context_object_name='latest_entrada_list',
    #        template_name='feeds/index.html'))
)
