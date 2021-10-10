from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Admin(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    role = models.CharField('role',max_length=50)

    def __str__(self):
        return str(self.user)

class Address(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE )
    lat = models.DecimalField(default = 0.0 , max_digits=100 , decimal_places=10)
    lon = models.DecimalField(default = 0.0 ,max_digits=100 , decimal_places=10)
    city = models.CharField('city' , max_length=100)
    district = models.CharField('district' , max_length=100)
    state = models.CharField('State' , max_length=100)
    pincode = models.CharField('pincode' , max_length=100)
    country = models.CharField('Country',max_length=255)
    
    def __str__(self):
        return self.city+","+self.district+","+self.state+","+str(self.pincode)+"."
    
class EmployeeDetils(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    Employee_Name = models.CharField('Employee_Name' , max_length=50 , default="Employee_Name")
    Employee_id = models.CharField('Employee Id',max_length=20 , unique=True)
    bio = models.TextField(max_length=600,default="bio of this shop will be show here.")
    phone_no = models.IntegerField(null=True, default=1231231231)
    blood_group = models.CharField(max_length=10)
    Permanent_Address = models.CharField(max_length=255)
    Current_Address = models.CharField(max_length=300 )

    def __str__(self):
        return str(self.user)


#class stats(models.Model):
#    status = models.CharField('status' , max_length=50)
#    def __str__(self):
#        return self.status



class Paid_Time_Off(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    #Id = models.ForeignKey(EmployeeDetils , on_delete=False)
    Time_From = models.DateTimeField('Time_From')
    Time_To = models.DateTimeField('Time_To')
    status = models.CharField('Status' , max_length=30)

#class Leave(models.Model):
#    user = models.ForeignKey(User , on_delete=models.CASCADE)
#    Id = models.ForeignKey(EmployeeDetils , on_delete=False)
#    Time_From = models.DateTimeField('Time_From')
#    Time_To = models.DateTimeField('Time_To')
#    status = models.CharField('Status' , max_length=30 , default="Pending")

