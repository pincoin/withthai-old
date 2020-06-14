from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from . import models


class ClubInline(admin.TabularInline):
    model = models.ClubList.clubs.through
    extra = 1


class ClubOrderInline(admin.TabularInline):
    model = models.Order.clubs.through
    raw_id_fields = ('club',)
    extra = 1


class AssetTransactionInline(admin.TabularInline):
    model = models.AssetTransaction
    ordering = ['-transaction_date', ]
    extra = 1


class ClubOrderChangeLogInline(admin.TabularInline):
    model = models.ClubOrderChangeLog
    ordering = ['-created', ]
    extra = 1


class HolidayAdmin(admin.ModelAdmin):
    list_display = ('holiday', 'country', 'title')
    list_filter = ('holiday', 'country')
    search_fields = ('title',)
    ordering = ('-holiday',)
    date_hierarchy = 'holiday'


class AreaAdmin(admin.ModelAdmin):
    list_display = ('title_english', 'title_thai', 'title_korean', 'slug', 'position')
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
    readonly_fields = ('club_link',)
    ordering = ('district', 'position',)

    def club_link(self, obj=None):
        return mark_safe('<a href="{url}">{text}</a>'.format(
            url=reverse('booking:golf-club-booking', args=(obj.slug,)),
            text='{}'.format(obj.title_english),
        ))

    club_link.short_description = _('Golf club')


class RateAdmin(admin.ModelAdmin):
    list_display = ('get_club', 'season_start', 'season_end', 'day_of_week', 'title',
                    'green_fee_selling_price', 'green_fee_cost_price',
                    'caddie_fee_selling_price', 'caddie_fee_cost_price',
                    'cart_fee_selling_price', 'cart_fee_cost_price')
    list_filter = ('club__title_english',)
    raw_id_fields = ('club',)

    def get_club(self, obj):
        return obj.club.title_english

    get_club.short_description = _('Golf club')


class ClubListAdmin(admin.ModelAdmin):
    list_display = ('title', 'code')
    inlines = [ClubInline, ]
    exclude = ('clubs',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'created', 'status',
                    'total_selling_price', 'total_cost_price')
    list_filter = ('status',)
    readonly_fields = ('order_no', 'ip_address', 'user_agent', 'accept_language', 'created', 'is_removed')
    raw_id_fields = ('user', 'parent',)
    inlines = [ClubOrderInline, AssetTransactionInline, ClubOrderChangeLogInline]
    ordering = ('-created',)


class AssetAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'balance', 'created', 'modified')
    list_filter = ('code',)


class AssetTransactionAdmin(admin.ModelAdmin):
    list_display = ('asset', 'category', 'amount', 'order', 'transaction_date')
    list_filter = ('asset', 'category')
    raw_id_fields = ('order',)
    date_hierarchy = 'transaction_date'


admin.site.register(models.Holiday, HolidayAdmin)
admin.site.register(models.Area, AreaAdmin)
admin.site.register(models.Province, ProvinceAdmin)
admin.site.register(models.District, DistrictAdmin)
admin.site.register(models.Club, ClubAdmin)
admin.site.register(models.Rate, RateAdmin)
admin.site.register(models.ClubList, ClubListAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Asset, AssetAdmin)
admin.site.register(models.AssetTransaction, AssetTransactionAdmin)
