# Generated by Django 2.1.4 on 2019-05-17 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keyword_meter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ghresultkeywordmeter',
            name='status',
            field=models.CharField(choices=[(0, 'has not check'), (1, 'checked by our algorithm'), (2, 'checked by random algorithm'), (3, 'checked by both')], default=0, max_length=50, verbose_name='Check Status'),
        ),
    ]
