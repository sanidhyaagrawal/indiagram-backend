# Generated by Django 3.0.8 on 2020-08-03 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_v1', '0009_auto_20200803_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_details',
            name='complete_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='user_details',
            name='country_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='tokenised_contact_info',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
