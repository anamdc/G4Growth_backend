# Generated by Django 4.0.2 on 2022-02-08 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_banned',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='referral_id',
            field=models.CharField(max_length=7, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='referrer_id',
            field=models.CharField(blank=True, max_length=7),
        ),
    ]
