# Generated by Django 4.0.2 on 2022-02-22 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0002_referrer_referee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]