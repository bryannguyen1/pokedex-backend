# Generated by Django 3.2.4 on 2021-07-02 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_pokemonentry_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pokemonentry',
            old_name='owner',
            new_name='user',
        ),
    ]
