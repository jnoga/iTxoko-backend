from tastypie import fields
from tastypie.resources import ModelResource
from items.models import Item
from items.models import Course
from items.models import WeekDay
from items.models import ClassInfo


class ItemResource(ModelResource):
    class Meta:
        queryset = Item.objects.all()
        resource_name = 'item'
        filtering = {
        	'id' : ['gt'],
        }

class CourseResource(ModelResource):
	weekday_set = fields.ToManyField('items.api.WeekDayResource', 'weekday_set', full=True)

	class Meta:
		queryset = Course.objects.all()
		resource_name = 'course'

class WeekDayResource(ModelResource):
	#course = fields.ToOneField(CourseResource, 'course')
	classinfo_set = fields.ToManyField('items.api.ClassInfoResource', 'classinfo_set', full=True)
	class Meta:
		queryset = WeekDay.objects.all()
		resource_name = 'weekday'

class ClassInfoResource(ModelResource):
	#weekday = fields.ToOneField(WeekDayResource, 'weekday')
	class Meta:
		queryset = ClassInfo.objects.all()
		resource_name = 'classinfo'