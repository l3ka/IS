# Generated by Django 2.1.4 on 2018-12-20 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20181220_1530'),
    ]

    operations = [
        migrations.RenameField(
            model_name='opcija',
            old_name='imeDodatneSastojke',
            new_name='imaDodatneSastojke',
        ),
    ]
