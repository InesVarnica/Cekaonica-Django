# Generated by Django 4.0.6 on 2022-07-09 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0014_uputnice_šifrarnikutrošak_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='posjeta',
            name='pacijent',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='posjeta', to='App.registarpacijenata'),
            preserve_default=False,
        ),
    ]
