# Generated by Django 2.0.3 on 2018-03-23 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20180322_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='score_away',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='score_home',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]