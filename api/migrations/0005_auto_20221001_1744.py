# Generated by Django 3.0.8 on 2022-10-01 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20221001_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todogroup',
            name='color',
            field=models.CharField(default='#000000', max_length=10),
        ),
    ]
