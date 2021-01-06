from django.db import models

# Create your models here.
import datetime

class CelloTypes(models.Model):
    choices_Color = [
        ('White', 'White'),
        ('Brown', 'Brown'),
        ('Other', 'Other')
    ]

    color = models.CharField(max_length=20, blank=False, choices=choices_Color, primary_key=True)
    quantityInStock = models.IntegerField(verbose_name='Quantity')

class OrderCello(models.Model):
    choices_Length = [
        ('30 m', '30 m'),
        ('50 m', '50 m'),
        ('60 m', '60 m'),
        ('100 m', '100 m'),
        ('150 m', '150 m'),
        ('200 m', '200 m'),
    ]

    choices_Width = [
        ('1/2 \"', '1/2 \"'),
        ('1 \"', '1 \"'),
        ('1.5 \"', '1.5 \"'),
        ('2 \"', '2 \"'),
        ('2.5 \"', '2.5 \"'),
        ('3 \"', '3 \"'),
    ]

    color = models.CharField(max_length=10, choices=CelloTypes.choices_Color)
    length = models.CharField(max_length=10, choices=choices_Length)
    width = models.CharField(max_length=10, choices=choices_Width)
    quantity = models.IntegerField()

    class Meta:
        abstract = True

class CustomerMaster(models.Model):
    cID = models.IntegerField(unique=True, primary_key=True)
    cName = models.CharField(max_length=40)
    address = models.TextField()
    email = models.EmailField()
    gstIN = models.CharField(max_length=15)

class OrderTable(models.Model):
    choices_Status = [
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Abandoned', 'Abandoned'),
    ]

    choices_Paymnent = [
        ('Not Paid', 'Not Paid'),
        ('In Transit', 'In Transit'),
        ('Paid', 'Paid'),
    ]

    oID = models.IntegerField(unique=True, primary_key=True)
    cName = models.CharField(max_length=40)
    orderDetails = models.CharField(max_length=1000)
    status = models.CharField(max_length=20, choices=choices_Status, default='New')
    payment = models.CharField(max_length=20, choices=choices_Paymnent, default='Not Paid')
    date = models.DateField(default=datetime.date.today)

class Processed(OrderCello):
    date = models.DateField(default=datetime.date.today)

class loginTable(models.Model):
    userN = models.CharField(max_length=10)
    passW = models.CharField(max_length=10)

class usersTable(models.Model):
    userNames = models.CharField(max_length=10)
    passwords = models.CharField(max_length=10)

class tempTableProcess(models.Model):
    order = models.CharField(max_length=1000)

class tempTableOrder(models.Model):
    order = models.CharField(max_length=1000)
