# Generated by Django 4.1.7 on 2023-04-15 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0030_remove_node_data_data_node'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='range',
            field=models.BigIntegerField(null=True),
        ),
    ]
