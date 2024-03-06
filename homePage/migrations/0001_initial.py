# Generated by Django 5.0.1 on 2024-03-06 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HomeBackground',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='userAvatar.png', upload_to='homePage/')),
                ('title', models.CharField(blank=True, default='Title', max_length=200, null=True)),
                ('description', models.TextField(blank=True, default='Description', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HomeLayout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('position', models.IntegerField()),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
            ],
        ),
    ]
