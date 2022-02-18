# Generated by Django 4.0.2 on 2022-02-16 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '__first__'),
        ('courses', '0006_courseuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseuser',
            name='courseid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
        migrations.AlterField(
            model_name='courseuser',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
        migrations.AlterField(
            model_name='videouser',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
    ]