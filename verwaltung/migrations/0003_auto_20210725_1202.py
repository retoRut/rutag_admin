# Generated by Django 3.2.5 on 2021-07-25 10:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('verwaltung', '0002_auto_20210725_1200'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rentreceipts',
            old_name='betrag',
            new_name='amount',
        ),
        migrations.AlterField(
            model_name='investment',
            name='datum',
            field=models.DateField(default=datetime.datetime(2021, 7, 25, 10, 2, 8, 700723, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='rent',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2021, 7, 25, 10, 2, 8, 694726, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='rent',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2021, 7, 25, 10, 2, 8, 694726, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='rentprofile',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2021, 7, 25, 10, 2, 8, 696725, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='rentprofile',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2021, 7, 25, 10, 2, 8, 696725, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='rentreceipts',
            name='datum',
            field=models.DateField(default=datetime.datetime(2021, 7, 25, 10, 2, 8, 701723, tzinfo=utc)),
        ),
    ]
