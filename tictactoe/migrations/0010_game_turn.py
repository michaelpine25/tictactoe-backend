# Generated by Django 4.2.8 on 2023-12-15 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tictactoe', '0009_alter_game_player_1_moves_alter_game_player_2_moves'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='turn',
            field=models.IntegerField(default=1),
        ),
    ]