# Generated by Django 4.2.8 on 2023-12-08 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tictactoe', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='player_1_moves',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='player_2_moves',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
