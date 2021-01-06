# Generated by Django 3.1.2 on 2020-12-10 15:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CelloTypes',
            fields=[
                ('color', models.CharField(choices=[('White', 'White'), ('Brown', 'Brown'), ('Other', 'Other')], max_length=20, primary_key=True, serialize=False)),
                ('quantityInStock', models.IntegerField(verbose_name='Quantity')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerMaster',
            fields=[
                ('cID', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('cName', models.CharField(max_length=40)),
                ('address', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('gstIN', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='loginTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userN', models.CharField(max_length=10)),
                ('passW', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='OrderTable',
            fields=[
                ('oID', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('cName', models.CharField(max_length=40)),
                ('orderDetails', models.CharField(max_length=1000)),
                ('status', models.CharField(choices=[('New', 'New'), ('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Abandoned', 'Abandoned')], default='New', max_length=20)),
                ('payment', models.CharField(choices=[('Not Paid', 'Not Paid'), ('In Transit', 'In Transit'), ('Paid', 'Paid')], default='Not Paid', max_length=20)),
                ('date', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='Processed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(choices=[('White', 'White'), ('Brown', 'Brown'), ('Other', 'Other')], max_length=10)),
                ('length', models.CharField(choices=[('30 m', '30 m'), ('50 m', '50 m'), ('60 m', '60 m'), ('100 m', '100 m'), ('150 m', '150 m'), ('200 m', '200 m')], max_length=10)),
                ('width', models.CharField(choices=[('1/2 "', '1/2 "'), ('1 "', '1 "'), ('1.5 "', '1.5 "'), ('2 "', '2 "'), ('2.5 "', '2.5 "'), ('3 "', '3 "')], max_length=10)),
                ('quantity', models.IntegerField()),
                ('date', models.DateField(default=datetime.date.today)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='tempTableOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='tempTableProcess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='usersTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userNames', models.CharField(max_length=10)),
                ('passwords', models.CharField(max_length=10)),
            ],
        ),
    ]