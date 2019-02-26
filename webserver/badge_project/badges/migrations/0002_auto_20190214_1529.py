# Generated by Django 2.1.7 on 2019-02-14 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('badges', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userbadges',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='events',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='eventbadges',
            name='badge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='badges.Badges'),
        ),
        migrations.AddField(
            model_name='eventbadges',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='badges.Events'),
        ),
        migrations.AddField(
            model_name='attendees',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='badges.Events'),
        ),
        migrations.AddField(
            model_name='attendees',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='userbadges',
            unique_together={('user', 'badge')},
        ),
        migrations.AlterUniqueTogether(
            name='eventbadges',
            unique_together={('badge', 'event')},
        ),
        migrations.AlterUniqueTogether(
            name='attendees',
            unique_together={('user', 'event')},
        ),
    ]
