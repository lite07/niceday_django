# Generated by Django 3.2.8 on 2021-10-17 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_contactlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactlist',
            name='description',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
