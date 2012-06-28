from items.models import Account
from django.contrib import admin


class ItemAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {
			'fields': ('title','desc','author','link','img','category','pub_date')
		}),
	]
	list_display = ('title', 'save_date', 'was_published_today')
	readonly_fields = ['save_date']
	list_filter = ['save_date']
	search_fields = ['title']
	date_hierarchy = 'save_date'


#admin.site.register(Item, ItemAdmin)
#admin.site.register(Course)
admin.site.register(Account)