# Generated by Django 4.0.2 on 2022-04-11 05:47

from django.db import migrations, models
import django.db.models.deletion
import g4growth.storage_backends


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('cover_img', models.FileField(blank=True, null=True, storage=g4growth.storage_backends.PublicMediaStorage, upload_to='')),
                ('status', models.CharField(choices=[('active', 'ACTIVE'), ('inactive', 'INACTIVE'), ('deleted', 'DELETED')], default='active', max_length=8)),
                ('total_videos', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('file', models.FileField(blank=True, null=True, storage=g4growth.storage_backends.MediaStorage, upload_to='')),
                ('status', models.CharField(choices=[('active', 'ACTIVE'), ('inactive', 'INACTIVE'), ('deleted', 'DELETED')], default='active', max_length=8)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
            ],
        ),
        migrations.CreateModel(
            name='VideoUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_purchased', models.DateTimeField(auto_now_add=True)),
                ('is_watched', models.BooleanField(default=False)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
                ('videoid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.video')),
            ],
        ),
        migrations.CreateModel(
            name='CourseUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_purchased', models.DateTimeField(auto_now_add=True)),
                ('percentage', models.IntegerField(default=0)),
                ('payment_ss', models.ImageField(blank=True, null=True, storage=g4growth.storage_backends.PublicMediaStorage, upload_to='')),
                ('is_verified', models.BooleanField(default=False)),
                ('is_processed', models.BooleanField(default=False)),
                ('courseid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
    ]
