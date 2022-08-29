# Generated by Django 4.0.6 on 2022-07-09 21:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0013_alter_registarpacijenata_mbo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Uputnice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tip', models.CharField(choices=[('A1', 'Konzilijarni pregled'), ('A2', 'Kontrolni konzilijarni pregled'), ('C1', 'Pregled i cjelovita obrada u specijalističkoj zdravstvenoj zaštiti'), ('C2', 'Pregled i obrada kroz Objedinjeni hitni bolnički prijam'), ('D1', 'Ambulantno liječenje'), ('D2', ' Dnevna bolnica')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ŠifrarnikUtrošak',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('šifra', models.CharField(max_length=6)),
                ('naziv', models.CharField(max_length=50)),
                ('cijena', models.FloatField()),
            ],
        ),
        migrations.AlterField(
            model_name='registarpacijenata',
            name='datum_police_osiguranja',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registarpacijenata',
            name='datum_rođenja',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Utrošak',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('količina', models.IntegerField()),
                ('utrošak', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='utrošak', to='App.radilišta')),
            ],
        ),
        migrations.CreateModel(
            name='Posjeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datum', models.DateTimeField(auto_now_add=True)),
                ('nalaz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posjeta', to='App.nalaz')),
                ('naziv_radilišta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posjeta', to='App.radilišta')),
                ('uputnica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posjeta', to='App.uputnice')),
                ('utrošak', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posjeta', to='App.utrošak')),
                ('zaposlenik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posjeta', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
