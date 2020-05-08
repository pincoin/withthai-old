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
    prepopulated_fields = {'slug': ('title_english',)}
    ordering = ('position',)


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('title_english', 'title_thai', 'title_korean', 'slug', 'area', 'position')
    list_filter = ('area__title_english',)
    prepopulated_fields = {'slug': ('title_english',)}
    ordering = ('area', 'position',)


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('title_english', 'title_thai', 'title_korean', 'slug', 'province', 'position')
    list_filter = ('province__title_english',)
    prepopulated_fields = {'slug': ('title_english',)}
    ordering = ('province', 'position',)


class ClubAdmin(admin.ModelAdmin):
    list_display = ('title_english', 'title_thai', 'title_korean', 'district',
                    'slug', 'hole', 'green_fee_selling_price', 'position')
    list_filter = ('district__province__title_english', 'hole')
    prepopulated_fields = {'slug': ('title_english',)}
    ordering = ('district', 'position',)


class RateAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Holiday, HolidayAdmin)
admin.site.register(models.Area, AreaAdmin)
admin.site.register(models.Province, ProvinceAdmin)
admin.site.register(models.District, DistrictAdmin)
admin.site.register(models.Club, ClubAdmin)
admin.site.register(models.Rate, RateAdmin)
