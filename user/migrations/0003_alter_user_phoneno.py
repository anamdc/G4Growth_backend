# Generated by Django 4.0.2 on 2022-02-08 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_is_banned_alter_user_referral_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phoneno',
            field=models.BigIntegerField(unique=True),
        ),
    ]
