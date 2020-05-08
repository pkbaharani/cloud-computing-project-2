# Generated by Django 3.0.5 on 2020-05-08 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralFound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('displayflag', models.BooleanField(default=True)),
                ('postid', models.CharField(default=None, max_length=250)),
                ('username', models.CharField(max_length=250)),
                ('itemtype', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=250)),
                ('imagelink', models.CharField(max_length=500)),
                ('campuslocation', models.CharField(max_length=250)),
                ('address', models.CharField(default='', max_length=250)),
                ('timestamp', models.DateField(blank=True, default=None, null=True, verbose_name='Time Stamp')),
            ],
        ),
        migrations.CreateModel(
            name='GeneralLost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('displayflag', models.BooleanField(default=True)),
                ('postid', models.CharField(default=None, max_length=250)),
                ('username', models.CharField(max_length=250)),
                ('itemtype', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=250)),
                ('imagelink', models.CharField(max_length=500)),
                ('campuslocation', models.CharField(max_length=250)),
                ('address', models.CharField(default='', max_length=250)),
                ('timestamp', models.DateField(blank=True, default=None, null=True, verbose_name='Time Stamp')),
            ],
        ),
        migrations.CreateModel(
            name='SensitiveFound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('displayflag', models.BooleanField(default=True)),
                ('postid', models.CharField(default=None, max_length=250)),
                ('username', models.CharField(default='', max_length=250)),
                ('cardtype', models.CharField(default='', max_length=250)),
                ('description', models.CharField(default='', max_length=250)),
                ('campuslocation', models.CharField(default='', max_length=250)),
                ('address', models.CharField(default='', max_length=250)),
                ('fourdigit', models.IntegerField(default=0)),
                ('color', models.CharField(default='', max_length=250)),
                ('timestamp', models.DateField(blank=True, default=None, null=True, verbose_name='Time Stamp')),
            ],
        ),
        migrations.CreateModel(
            name='SensitiveLost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('displayflag', models.BooleanField(default=True)),
                ('postid', models.CharField(default=None, max_length=250)),
                ('username', models.CharField(default='', max_length=250)),
                ('cardtype', models.CharField(default='', max_length=250)),
                ('description', models.CharField(default='', max_length=250)),
                ('campuslocation', models.CharField(default='', max_length=250)),
                ('address', models.CharField(default='', max_length=250)),
                ('fourdigit', models.IntegerField(default=0)),
                ('color', models.CharField(default='', max_length=250)),
                ('timestamp', models.DateField(blank=True, default=None, null=True, verbose_name='Time Stamp')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=250)),
                ('emailid', models.CharField(max_length=250)),
                ('password', models.CharField(max_length=250)),
            ],
        ),
    ]
