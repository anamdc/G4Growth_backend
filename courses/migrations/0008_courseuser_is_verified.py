# Generated by Django 4.0.2 on 2022-02-18 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_alter_courseuser_courseid_alter_courseuser_userid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseuser',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]