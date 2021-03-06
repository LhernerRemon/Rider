# Generated by Django 2.2.12 on 2020-06-24 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which  the object was created', verbose_name='Created at')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date time on which  the object was last modified', verbose_name='Modified at')),
                ('available_seats', models.PositiveSmallIntegerField(default=1)),
                ('comments', models.TextField(blank=True)),
                ('departure_location', models.CharField(max_length=255)),
                ('departure_date', models.DateTimeField()),
                ('arrival_location', models.CharField(max_length=255)),
                ('arrival_date', models.DateTimeField()),
                ('rating', models.FloatField(null=True)),
                ('is_active', models.BooleanField()),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
    ]
