# Generated by Django 4.0.6 on 2022-07-07 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_alter_registarpacijenata_nalazi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registarpacijenata',
            name='MBO',
            field=models.IntegerField(blank=True, max_length=9, null=True),
        ),
    ]
