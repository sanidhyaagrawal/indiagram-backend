# Generated by Django 3.0.8 on 2020-07-29 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_v1', '0005_auto_20200723_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_details',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
    ]