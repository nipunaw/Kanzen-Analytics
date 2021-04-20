# Generated by Django 3.1.6 on 2021-04-16 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('anime_name', models.CharField(max_length=75, primary_key=True, serialize=False, unique=True)),
                ('anime_order', models.IntegerField(default=0)),
            ],
        ),
    ]
