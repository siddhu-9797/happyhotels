# Generated by Django 3.0.3 on 2020-02-19 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200210_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='inAdvance',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
