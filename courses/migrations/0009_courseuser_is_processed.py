# Generated by Django 4.0.2 on 2022-02-25 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_courseuser_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseuser',
            name='is_processed',
            field=models.BooleanField(default=False),
        ),
    ]
