# Generated by Django 4.1.7 on 2023-04-04 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0010_mypolygon_node'),
    ]

    operations = [
        migrations.AddField(
            model_name='mypolygon',
            name='status',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
