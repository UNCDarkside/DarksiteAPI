# Generated by Django 2.1.4 on 2018-12-20 00:40

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfoPanel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='A unique identifier for the panel.', primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField(default=0, help_text='An integer describing position of the panel in relation to other panels.', verbose_name='order')),
                ('text', models.TextField(help_text='The text to display in the panel.', verbose_name='text')),
                ('title', models.CharField(help_text='The title of the panel.', max_length=100, verbose_name='title')),
                ('media', models.ForeignKey(blank=True, help_text='The media to show in the panel.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='cms.MediaResource', verbose_name='media resource')),
            ],
            options={
                'verbose_name': 'info panel',
                'verbose_name_plural': 'info panels',
                'ordering': ('order',),
            },
        ),
    ]
