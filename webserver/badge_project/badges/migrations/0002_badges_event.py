# Generated by Django 2.1.7 on 2019-02-26 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
        ('badges', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='badges',
            name='event',
            field=models.ManyToManyField(blank=True, to='events.Events'),
        ),
    ]
