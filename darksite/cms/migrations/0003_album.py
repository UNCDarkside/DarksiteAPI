# Generated by Django 2.1.4 on 2018-12-22 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_infopanel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='The time the album was created at.', verbose_name='creation time')),
                ('description', models.TextField(blank=True, help_text='A description of the album.', verbose_name='description')),
                ('slug', models.SlugField(help_text='A unique slug identifying the album.', unique=True, verbose_name='slug')),
                ('title', models.CharField(help_text='The title of the album.', max_length=100, verbose_name='title')),
            ],
            options={
                'verbose_name': 'album',
                'verbose_name_plural': 'albums',
                'ordering': ('-created',),
            },
        ),
    ]
