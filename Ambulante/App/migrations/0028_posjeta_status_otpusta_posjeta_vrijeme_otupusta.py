# Generated by Django 4.0.6 on 2022-07-16 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0027_alter_blagajna_cijena'),
    ]

    operations = [
        migrations.AddField(
            model_name='posjeta',
            name='status_otpusta',
            field=models.CharField(choices=[('K', 'Kući'), ('H', 'Hospitalizacija'), ('O', 'Opservacija'), ('PP', 'Prekinut pregled')], default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posjeta',
            name='vrijeme_otupusta',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
