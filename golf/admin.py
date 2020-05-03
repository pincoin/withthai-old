from django.contrib import admin

from . import models


class HolidayAdmin(admin.ModelAdmin):
    list_display = ('holiday', 'country', 'title')
    list_filter = ('holiday', 'country')
    search_fields = ('title',)
    ordering = ('-holiday',)
    date_hierarchy = 'holiday'


class AreaAdmin(admin.ModelAdmin):
    list_display = ('title_english', 'title_thai', 'title_korean', 'position')
    ordering = ('position',)


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('title_english', 'title_thai', 'title_korean', 'area', 'position')
    list_filter = ('area__title_english',)
    ordering = ('area__position', 'position',)


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('title_english', 'title_thai', 'title_korean', 'province', 'position')
    list_filter = ('province__title_english',)
    ordering = ('province__position', 'position',)


class ClubAdmin(admin.ModelAdmin):
    list_display = ('title_english', 'title_thai', 'title_korean')
    prepopulated_fields = {'slug': ('title_english',)}
    list_filter = ('district__province__title_english', 'hole')


class PriceAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Holiday, HolidayAdmin)
admin.site.register(models.Area, AreaAdmin)
admin.site.register(models.Province, ProvinceAdmin)
admin.site.register(models.District, DistrictAdmin)
admin.site.register(models.Club, ClubAdmin)
admin.site.register(models.Price, PriceAdmin)
