# Generated by Django 5.0.1 on 2024-01-25 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_record_id', models.CharField(blank=True, max_length=50, null=True)),
                ('cui', models.CharField(blank=True, max_length=200, null=True)),
                ('denumire', models.CharField(blank=True, max_length=200, null=True)),
                ('adresa', models.CharField(blank=True, max_length=200, null=True)),
                ('nrRegCom', models.CharField(blank=True, max_length=200, null=True)),
                ('telefon', models.CharField(blank=True, max_length=200, null=True)),
                ('fax', models.CharField(blank=True, max_length=200, null=True)),
                ('codPostal', models.CharField(blank=True, max_length=200, null=True)),
                ('act', models.CharField(blank=True, max_length=200, null=True)),
                ('stare_inregistrare', models.CharField(blank=True, max_length=200, null=True)),
                ('data_inregistrare', models.CharField(blank=True, max_length=200, null=True)),
                ('cod_CAEN', models.CharField(blank=True, max_length=200, null=True)),
                ('iban', models.CharField(blank=True, max_length=200, null=True)),
                ('statusRO_e_Factura', models.CharField(blank=True, max_length=200, null=True)),
                ('organFiscalCompetent', models.CharField(blank=True, max_length=200, null=True)),
                ('forma_de_proprietate', models.CharField(blank=True, max_length=200, null=True)),
                ('forma_organizare', models.CharField(blank=True, max_length=200, null=True)),
                ('forma_juridica', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]