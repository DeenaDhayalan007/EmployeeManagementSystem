from django import forms
from django.db import models
from django.forms import ModelForm, fields, widgets
from .models import *

stats = [
            ('approve','Approved'),
            ('reject' , 'Rejected'),
            ('pending' , 'Pending'),
            ('Cancel' , 'Cancel'),
        ]

class EmployeeForm(ModelForm):
    class Meta:
        model = EmployeeDetils
        fields = "__all__"
        widgets={
            'user':forms.TextInput(attrs={'class':'form-control','placeholder':'Venue Name'}),
            'Employee_id':forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'bio':forms.TextInput(attrs={'class':'form-control','placeholder':'Zip Code'}),
            'phone_no':forms.TextInput(attrs={'class':'form-control','placeholder':'Web Address'}),
            'blood_group':forms.TextInput(attrs={'class':'form-control','placeholder':'Phone'}),
            'Permanent_Address':forms.TextInput(attrs={'class':'form-control','placeholder':'Phone'}),
            'Current_Address':forms.TextInput(attrs={'class':'form-control','placeholder':'Phone'}),
            
        }

class AdminForm(ModelForm):
    class Meta:
        model = Admin
        fields =( "role" ,  )




       