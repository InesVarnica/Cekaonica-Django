# Generated by Django 4.0.6 on 2022-07-10 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0017_alter_posjeta_utrošak'),
    ]

    operations = [
        migrations.AlterField(
            model_name='šifrarnikutrošak',
            name='naziv',
            field=models.CharField(max_length=100),
        ),
    ]
