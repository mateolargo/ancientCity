from ancientCity.cityBrowser.models import *
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

#class CityAdmin(admin.ModelAdmin):
#    list_display = ('name',)
#admin.site.register(City, CityAdmin)

class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'encompassing_monument',)
admin.site.register(Region, RegionAdmin)

class MonumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'region', 'description',)
admin.site.register(Monument, MonumentAdmin)

class SourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', )
admin.site.register(Source, SourceAdmin)
