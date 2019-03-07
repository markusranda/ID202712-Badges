# Generated by Django 2.1.7 on 2019-03-07 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badges', '0004_remove_badges_is_showcase_of'),
        ('users', '0002_auto_20190305_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='showcase_badge',
            field=models.ManyToManyField(blank=True, related_name='is_showcase_badge', to='badges.Badges'),
        ),
    ]
