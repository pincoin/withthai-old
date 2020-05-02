from django.contrib import admin

from . import models


class HolidayAdmin(admin.ModelAdmin):
    list_display = ('holiday', 'country', 'title')
    list_filter = ('holiday', 'country')
    search_fields = ('title',)
    ordering = ('-holiday',)
    date_hierarchy = 'holiday'


class AreaAdmin(admin.ModelAdmin):
    list_display = ('title_english', 'title_thai', 'title_korean')


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('title_english', 'title_thai', 'title_korean', 'area')
    list_filter = ('area__title_english',)


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('title_english', 'title_thai', 'title_korean')
    list_filter = ('province__title_english',)


class ClubAdmin(admin.ModelAdmin):
    list_display = ('title_english', 'title_thai', 'title_korean')
    prepopulated_fields = {'slug': ('title_english',)}


class PriceAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Holiday, HolidayAdmin)
admin.site.register(models.Area, AreaAdmin)
admin.site.register(models.Province, ProvinceAdmin)
admin.site.register(models.District, DistrictAdmin)
admin.site.register(models.Club, ClubAdmin)
admin.site.register(models.Price, PriceAdmin)
