# Generated by Django 4.2.8 on 2023-12-18 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tictactoe', '0010_game_turn'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
