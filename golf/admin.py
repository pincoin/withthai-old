from django.contrib import admin

from . import models


class HolidayAdmin(admin.ModelAdmin):
    list_display = ('holiday', 'country', 'title')
    list_filter = ('holiday', 'country')
    search_fields = ('title',)
    ordering = ('-holiday',)
    date_hierarchy = 'holiday'


class AreaAdmin(admin.ModelAdmin):
    pass


class ProvinceAdmin(admin.ModelAdmin):
    pass


class DistrictAdmin(admin.ModelAdmin):
    pass


class ClubAdmin(admin.ModelAdmin):
    pass


class PriceAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Holiday, HolidayAdmin)
admin.site.register(models.Area, AreaAdmin)
admin.site.register(models.Province, ProvinceAdmin)
admin.site.register(models.District, DistrictAdmin)
admin.site.register(models.Club, ClubAdmin)
admin.site.register(models.Price, PriceAdmin)
