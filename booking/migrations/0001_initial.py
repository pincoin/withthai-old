# Generated by Django 3.0.7 on 2020-06-12 18:06

import booking.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import easy_thumbnails.fields
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title_english', models.CharField(max_length=255, verbose_name='Area english name')),
                ('title_thai', models.CharField(max_length=255, verbose_name='Area Thai name')),
                ('title_korean', models.CharField(max_length=255, verbose_name='Area Korean name')),
                ('slug', models.SlugField(allow_unicode=True, help_text='A short label containing only letters, numbers, underscores or hyphens for URL', max_length=255, unique=True, verbose_name='Slug')),
                ('position', models.IntegerField(db_index=True, default=0, verbose_name='Position')),
            ],
            options={
                'verbose_name': 'Area',
                'verbose_name_plural': 'Areas',
            },
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title_english', models.CharField(db_index=True, max_length=255, verbose_name='Golf club English name')),
                ('title_thai', models.CharField(db_index=True, max_length=255, verbose_name='Golf club Thai name')),
                ('title_korean', models.CharField(db_index=True, max_length=255, verbose_name='Golf club Korean name')),
                ('slug', models.SlugField(allow_unicode=True, help_text='A short label containing only letters, numbers, underscores or hyphens for URL', max_length=255, unique=True, verbose_name='Slug')),
                ('phone', models.CharField(blank=True, max_length=32, null=True, verbose_name='Phone number')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='Email address')),
                ('fax', models.CharField(blank=True, max_length=16, null=True, verbose_name='Fax number')),
                ('website', models.URLField(blank=True, max_length=255, null=True, verbose_name='Website')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Golf club address')),
                ('hole', models.IntegerField(choices=[(0, '18 Holes'), (1, '9 Holes'), (2, '27 Holes'), (3, '36 Holes')], db_index=True, default=0, verbose_name='No. of holes')),
                ('country', models.IntegerField(choices=[(1, 'Thailand'), (2, 'South Korea'), (3, 'Japan'), (4, 'China')], db_index=True, default=1, verbose_name='Country code')),
                ('green_fee_selling_price', models.DecimalField(db_index=True, decimal_places=2, help_text='THB', max_digits=11, verbose_name='Start from')),
                ('caddie_fee_selling_price', models.DecimalField(db_index=True, decimal_places=2, help_text='THB', max_digits=11, verbose_name='Caddie fee')),
                ('cart_fee_selling_price', models.DecimalField(db_index=True, decimal_places=2, help_text='THB', max_digits=11, verbose_name='Cart fee')),
                ('max_pax', models.IntegerField(default=4, verbose_name='Max PAX')),
                ('cart_required', models.IntegerField(db_index=True, default=0, verbose_name='Require golf cart')),
                ('weekdays_min_in_advance', models.IntegerField(db_index=True, default=1, verbose_name='Weekdays minimum in advance')),
                ('weekdays_max_in_advance', models.IntegerField(db_index=True, default=30, verbose_name='Weekdays maximum in advance')),
                ('weekend_min_in_advance', models.IntegerField(db_index=True, default=1, verbose_name='Weekend minimum in advance')),
                ('weekend_max_in_advance', models.IntegerField(db_index=True, default=7, verbose_name='Weekend maximum in advance')),
                ('thumbnail1', easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to=booking.models.upload_directory_path, verbose_name='Thumbnail 1')),
                ('thumbnail2', easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to=booking.models.upload_directory_path, verbose_name='Thumbnail 2')),
                ('thumbnail3', easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to=booking.models.upload_directory_path, verbose_name='Thumbnail 3')),
                ('thumbnail4', easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to=booking.models.upload_directory_path, verbose_name='Thumbnail 4')),
                ('thumbnail5', easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to=booking.models.upload_directory_path, verbose_name='Thumbnail 5')),
                ('latitude', models.DecimalField(decimal_places=6, default=0, max_digits=9, verbose_name='Latitude')),
                ('longitude', models.DecimalField(decimal_places=6, default=0, max_digits=9, verbose_name='Longitude')),
                ('position', models.IntegerField(db_index=True, default=0, verbose_name='Position')),
                ('status', models.IntegerField(choices=[(0, 'Club open'), (1, 'Club closed')], db_index=True, default=0, verbose_name='Club status')),
            ],
            options={
                'verbose_name': 'Golf club',
                'verbose_name_plural': 'Golf clubs',
            },
        ),
        migrations.CreateModel(
            name='ClubList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='Club list title')),
                ('code', models.CharField(max_length=255, verbose_name='Club list code')),
            ],
            options={
                'verbose_name': 'Golf club list',
                'verbose_name_plural': 'Golf club lists',
            },
        ),
        migrations.CreateModel(
            name='ClubOrderListMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_date', models.DateField(db_index=True, verbose_name='Round date')),
                ('round_time', models.TimeField(db_index=True, verbose_name='Round time')),
                ('pax', models.IntegerField(default=4, verbose_name='PAX')),
                ('green_fee_selling_price', models.DecimalField(decimal_places=0, default=0, help_text='THB', max_digits=11, verbose_name='Green fee selling price')),
                ('green_fee_cost_price', models.DecimalField(decimal_places=0, default=0, help_text='THB', max_digits=11, verbose_name='Green fee cost price')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.Club', verbose_name='Golf club')),
            ],
            options={
                'verbose_name': 'Golf club order list membership',
                'verbose_name_plural': 'Golf club order list membership',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('order_no', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Order no')),
                ('last_name', models.CharField(blank=True, max_length=64, verbose_name='Last name')),
                ('first_name', models.CharField(blank=True, max_length=64, verbose_name='First name')),
                ('user_agent', models.TextField(blank=True, verbose_name='User-agent')),
                ('accept_language', models.TextField(blank=True, verbose_name='Accept-language')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP address')),
                ('transaction_id', models.CharField(blank=True, max_length=64, verbose_name='Transaction ID')),
                ('status', models.IntegerField(choices=[(0, 'Booking opened'), (1, 'Booking pending'), (2, 'Booking offered'), (3, 'Payment completed'), (4, 'Booking confirmed'), (5, 'Booking unavailable'), (6, 'Payment adjustment'), (7, 'Payment adjusted'), (8, 'Refund requested'), (9, 'Refund pending'), (10, 'Refunded'), (11, 'Refunded'), (12, 'Voided')], db_index=True, default=0, verbose_name='Order status')),
                ('total_selling_price', models.DecimalField(decimal_places=0, default=0, max_digits=11, verbose_name='Total selling price')),
                ('total_cost_price', models.DecimalField(decimal_places=0, default=0, max_digits=11, verbose_name='Total cost price')),
                ('message', models.TextField(blank=True, verbose_name='Order message')),
                ('clubs', models.ManyToManyField(through='booking.ClubOrderListMembership', to='booking.Club')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='booking.Order', verbose_name='Parent order')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Booking order',
                'verbose_name_plural': 'Booking orders',
            },
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('season_start', models.DateField(verbose_name='Season start date')),
                ('season_end', models.DateField(verbose_name='Season end date')),
                ('day_of_week', models.IntegerField(choices=[(0, 'Weekday'), (1, 'Weekend')], db_index=True, default=0, verbose_name='Day of week')),
                ('slot_start', models.TimeField(verbose_name='Slot start time')),
                ('slot_end', models.TimeField(verbose_name='Slot end time')),
                ('title', models.IntegerField(choices=[(0, 'Day golf'), (1, 'Day golf 1st round'), (2, 'Day golf 2nd round'), (3, 'Twilight golf'), (4, 'Night golf')], db_index=True, default=0, verbose_name='Rate title')),
                ('green_fee_selling_price', models.DecimalField(decimal_places=2, help_text='THB', max_digits=11, verbose_name='Green fee selling price')),
                ('green_fee_cost_price', models.DecimalField(decimal_places=2, help_text='THB', max_digits=11, verbose_name='Green fee cost price')),
                ('caddie_fee_selling_price', models.DecimalField(decimal_places=2, help_text='THB', max_digits=11, verbose_name='Caddie fee selling price')),
                ('caddie_fee_cost_price', models.DecimalField(decimal_places=2, help_text='THB', max_digits=11, verbose_name='Caddie fee cost price')),
                ('cart_fee_selling_price', models.DecimalField(decimal_places=2, help_text='THB', max_digits=11, verbose_name='Cart fee selling price')),
                ('cart_fee_cost_price', models.DecimalField(decimal_places=2, help_text='THB', max_digits=11, verbose_name='Cart fee cost price')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.Club', verbose_name='Golf club')),
            ],
            options={
                'verbose_name': 'Service rate',
                'verbose_name_plural': 'Service rates',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title_english', models.CharField(max_length=255, verbose_name='Province English name')),
                ('title_thai', models.CharField(max_length=255, verbose_name='Province Thai name')),
                ('title_korean', models.CharField(max_length=255, verbose_name='Province Korean name')),
                ('slug', models.SlugField(allow_unicode=True, help_text='A short label containing only letters, numbers, underscores or hyphens for URL', max_length=255, unique=True, verbose_name='Slug')),
                ('position', models.IntegerField(db_index=True, default=0, verbose_name='Position')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.Area', verbose_name='Location area')),
            ],
            options={
                'verbose_name': 'Province',
                'verbose_name_plural': 'Provinces',
            },
        ),
        migrations.CreateModel(
            name='OrderTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('payment_method', models.IntegerField(choices=[(0, 'Credit Card'), (1, 'Bank Transfer'), (2, 'PayPal')], db_index=True, default=0, verbose_name='Payment method')),
                ('category', models.IntegerField(choices=[(0, 'Credit Card'), (1, 'Bank Transfer'), (2, 'PayPal')], db_index=True, default=0, verbose_name='Transaction category')),
                ('amount', models.DecimalField(decimal_places=0, max_digits=11, verbose_name='Amount')),
                ('transaction_date', models.DateTimeField(verbose_name='Transaction date')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.Order', verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Order transaction',
                'verbose_name_plural': 'Order transactions',
            },
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='Holiday name')),
                ('holiday', models.DateField(db_index=True, verbose_name='Holiday day')),
                ('country', models.IntegerField(choices=[(1, 'Thailand'), (2, 'South Korea'), (3, 'Japan'), (4, 'China')], db_index=True, default=1, verbose_name='Country code')),
            ],
            options={
                'verbose_name': 'Holiday',
                'verbose_name_plural': 'Holidays',
                'unique_together': {('holiday', 'country')},
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title_english', models.CharField(max_length=255, verbose_name='District English name')),
                ('title_thai', models.CharField(max_length=255, verbose_name='District Thai name')),
                ('title_korean', models.CharField(max_length=255, verbose_name='District Korean name')),
                ('slug', models.SlugField(allow_unicode=True, help_text='A short label containing only letters, numbers, underscores or hyphens for URL', max_length=255, unique=True, verbose_name='Slug')),
                ('position', models.IntegerField(db_index=True, default=0, verbose_name='Position')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.Province', verbose_name='Province')),
            ],
            options={
                'verbose_name': 'District',
                'verbose_name_plural': 'Districts',
            },
        ),
        migrations.AddField(
            model_name='cluborderlistmembership',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.Order', verbose_name='Order'),
        ),
        migrations.CreateModel(
            name='ClubListMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(verbose_name='Position')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.Club', verbose_name='Golf club')),
                ('club_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.ClubList', verbose_name='Golf club list')),
            ],
            options={
                'verbose_name': 'Golf club list membership',
                'verbose_name_plural': 'Golf club list membership',
            },
        ),
        migrations.AddField(
            model_name='clublist',
            name='clubs',
            field=models.ManyToManyField(through='booking.ClubListMembership', to='booking.Club'),
        ),
        migrations.AddField(
            model_name='club',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.District', verbose_name='District'),
        ),
    ]
