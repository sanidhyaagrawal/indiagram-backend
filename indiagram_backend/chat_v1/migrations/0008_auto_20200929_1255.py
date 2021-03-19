# Generated by Django 3.0.8 on 2020-09-29 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_v1', '0017_user_details_showlastsseen'),
        ('chat_v1', '0007_remove_lastseen_activenow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lastseen',
            name='lastSeen',
            field=models.DateTimeField(db_index=True, editable=False),
        ),
        migrations.CreateModel(
            name='deviceLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change', models.IntegerField(default=0)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api_v1.user_details', verbose_name='user')),
            ],
        ),
    ]