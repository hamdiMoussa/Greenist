# Generated by Django 4.1.7 on 2023-04-11 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0024_rename_wfi_mypolygon_fwi'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mypolygon',
            name='FWI',
        ),
        migrations.RemoveField(
            model_name='mypolygon',
            name='status',
        ),
        migrations.AddField(
            model_name='node',
            name='FWI',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='node',
            name='status',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
