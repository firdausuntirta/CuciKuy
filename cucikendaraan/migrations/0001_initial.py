# Generated by Django 5.0.6 on 2024-05-31 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('nama', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
