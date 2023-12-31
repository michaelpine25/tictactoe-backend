# Generated by Django 5.0 on 2023-12-07 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_1_id', models.IntegerField()),
                ('player_2_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='invitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_user_id', models.IntegerField()),
                ('recipient_user_id', models.IntegerField()),
            ],
        ),
    ]
