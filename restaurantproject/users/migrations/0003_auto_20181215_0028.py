# Generated by Django 2.1.2 on 2018-12-14 23:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20181214_2321'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menistavka',
            old_name='nijeUPOnudi',
            new_name='nijeUPonudi',
        ),
    ]
