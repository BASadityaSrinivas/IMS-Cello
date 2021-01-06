from django import forms
from celloApp.models import *
from django.conf import settings
import datetime
from sql import *
from os import listdir
from os.path import isfile, join



class RawMaterialForm(forms.ModelForm):
    class Meta:
        model = CelloTypes
        fields = ['color', 'quantityInStock']

class ProcessedForm(forms.ModelForm):
    usedJumbo = forms.IntegerField(min_value=0, label='Jumbo(s) used', initial=0)
    usedJumboColor = forms.ChoiceField(choices=CelloTypes.choices_Color, label='Jumbo Color')
    date = forms.DateField(widget=forms.SelectDateWidget(), initial=datetime.date.today)
    quantity = forms.IntegerField(required=False, initial=0)
    color = forms.ChoiceField(choices=CelloTypes.choices_Color)
    length = forms.ChoiceField(choices=OrderCello.choices_Length)
    width = forms.ChoiceField(choices=OrderCello.choices_Width)
    class Meta:
        model = Processed
        fields = ['color','length','width','quantity','date']

class CustomerAddForm(forms.ModelForm):
    cName = forms.CharField(label='Customer Name') # widget=forms.TextInput(attrs={'placeholder': 'Name'}) - For placeholder
    address = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'cols':25}))
    class Meta:
        model = CustomerMaster
        fields = ['cName','address','email','gstIN']


class OrderForm(forms.Form):
    color = forms.ChoiceField(choices=CelloTypes.choices_Color)
    length = forms.ChoiceField(choices=OrderCello.choices_Length)
    width = forms.ChoiceField(choices=OrderCello.choices_Width)
    quantity = forms.IntegerField()

class CustomerForm(forms.ModelForm):

    date = forms.DateField(widget=forms.SelectDateWidget(), initial=datetime.date.today)
    cName = forms.ModelChoiceField(queryset=CustomerMaster.objects.values_list('cName'))

    class Meta:
        model = OrderTable
        fields = ['cName','status','payment','date']

class CustomerEditFormStatus(forms.ModelForm):
    oID = forms.ModelChoiceField(queryset=OrderTable.objects.order_by('oID').values_list('oID').filter(status__in=['New', 'In Progress']), label="Order ID")
    field_order = ['oID', 'status']
    class Meta:
        model = OrderTable
        fields = ['oID', 'status']

class CustomerEditFormPayment(forms.ModelForm):
    oID = forms.ModelChoiceField(queryset=OrderTable.objects.order_by('oID').values_list('oID').filter(payment__exact='Not Paid'), label="Order ID")
    field_order = ['oID', 'payment']
    class Meta:
        model = OrderTable
        fields = ['oID', 'payment']

class ClearFilesForm(forms.Form):
    choices_Files = [
        ('entry.csv', 'entry.csv'),
        ('jumboWhite.csv', 'jumboWhite.csv'),
        ('jumboBrown.csv', 'jumboBrown.csv'),
        ('jumboOther.csv', 'jumboOther.csv'),
        ('order.csv', 'order.csv'),
    ]
    file = forms.ChoiceField(choices=choices_Files, label="Clear File ")

class ProcessCSVformWhite(forms.Form):
    white_process_csv = []

    for i in range(6):
        str1 = OrderCello.choices_Length[i][0][:-2] + '_0.5' + '.csv'
        white_process_csv.append((str1,str1))

    for i in range(1,6):
        for j in range(6):
            str1 = OrderCello.choices_Length[j][0][:-2] + '_' + OrderCello.choices_Width[i][0][:-2] + '.csv'
            white_process_csv.append((str1,str1))

    white = forms.ChoiceField(choices=white_process_csv)

class ProcessCSVformBrown(forms.Form):
    brown_process_csv = []

    for i in range(6):
        str1 = OrderCello.choices_Length[i][0][:-2] + '_0.5' + '.csv'
        brown_process_csv.append((str1,str1))

    for i in range(1,6):
        for j in range(6):
            str1 = OrderCello.choices_Length[j][0][:-2] + '_' + OrderCello.choices_Width[i][0][:-2] + '.csv'
            brown_process_csv.append((str1,str1))

    brown = forms.ChoiceField(choices=brown_process_csv)

class ProcessCSVformOther(forms.Form):
    other_process_csv = []

    for i in range(6):
        str1 = OrderCello.choices_Length[i][0][:-2] + '_0.5' + '.csv'
        other_process_csv.append((str1,str1))

    for i in range(1,6):
        for j in range(6):
            str1 = OrderCello.choices_Length[j][0][:-2] + '_' + OrderCello.choices_Width[i][0][:-2] + '.csv'
            other_process_csv.append((str1,str1))

    other = forms.ChoiceField(choices=other_process_csv)
