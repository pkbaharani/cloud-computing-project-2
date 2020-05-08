# Generated by Django 3.0.5 on 2020-05-07 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lostfound', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='generalfound',
            old_name='location',
            new_name='campuslocation',
        ),
        migrations.AddField(
            model_name='generalfound',
            name='address',
            field=models.CharField(default='', max_length=250),
        ),
    ]