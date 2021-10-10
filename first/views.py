from django.http.response import HttpResponseRedirect
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User ,auth
from django.contrib import messages
from django.core.mail import send_mail

from first.utils import get_center_coordinates, get_zoom
from .models import *
from .forms import *


from . utils import get_zoom,get_center_coordinates,get_image,get_simple_plot

from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Create your views here.
def getlatlon(request):
    address = None 
    map = None
    geolocator = Nominatim(user_agent="first")
    if request.user.is_authenticated and request.user.is_active:

            import requests

            res = requests.get('https://ipinfo.io/')
            data = res.json()

            city=data['city']

            location1 = data['loc'].split(',')
            latitude = location1[0]
            longitude = location1[1]

           
            latlon = str(latitude)+","+str(longitude)
            
            location = geolocator.reverse(latlon)

            l = str(location.address)
            address = str(l)
            l = list(l.split(","))
            l= l[::-1]
            country = l[0]
            pincode = l[1]
            state = l[2]
            district = l[3]
            city = ""
            for i in range(4,len(l)):
                city  = l[i]+" " 
            lat = float(round(location.latitude , 10))
            lon = float(round(location.longitude , 10))

            m = folium.Map(width = 800,
            height=500,
            location= get_center_coordinates(lat,lon),
            zoom_start = get_zoom(0))

            folium.Marker([lat,lon],
            tooltip="Click Here For More",
            popup = city,
            icon = folium.Icon(color="blue" , icon = "cloud")).add_to(m)
            
            m = m._repr_html_()


            my_obj = list(Address.objects.filter(user = request.user))
            #print(my_obj)

            if not my_obj:
                obj = Address(
                    user=request.user,
                    lat=lat,
                    lon=lon,
                    city=city,
                    district=district,
                    state=state,
                    pincode=pincode,
                    country=country
                )

                obj.save();
            
            else:
                o = Address.objects.get(user = request.user)
                o.lat=lat
                o.lon=lon
                o.city=city
                o.district=district
                o.state=state
                o.pincode=pincode
                o.country=country
                o.save();
           
                

            b=EmployeeDetils.objects.get(user = request.user.id)
            b.Current_Address=address
            b.save();

            messages.info(request , "Thank you , Your Current Location is"+address)






    context = {
        "address" : address,
        "map" : m
    }



    return render(request , "latlon.html" , context)

def employeehome(request):
    if request.user.is_authenticated and request.user.is_active:
        a=User.objects.get( username = request.user.username)
        emp = EmployeeDetils.objects.get(user = request.user.id)

        dist={
            
            'user' : a,
            'emp' : emp,
        
        }
        return render(request,'employee_home.html',dist)
        
    else :
       messages.info(request,"Login to enter")
       return redirect("login")


def organize_emp(request):
    graph = None
    error_message = None

    if request.user.is_authenticated and request.user.is_staff and request.user.is_active:
        df = pd.DataFrame(Address.objects.all().values())

        if df.shape[0] > 0:
            if request.method == 'POST':
                base = request.POST['base']
                chart = request.POST['chart']

                graph = get_simple_plot(chart , base = base , data = df)
        else:
            error_message = "Ther is no data"

    return render(request , 'organize_emp.html' , {'graph':graph , 'error_message':error_message})
    


def adduser (request):
    if request.user.is_authenticated and request.user.is_staff and request.user.is_active:
        if request.method=='POST':
                email=request.POST['email']
                username=request.POST['username']
                first_name=request.POST['first_name']  #to differnt the Custom / employer
                last_name=request.POST['last_name'] #used to store shop name
                password1=request.POST['password1']
                password2=request.POST['password2']
                if password1==password2:
                    if User.objects.filter(username=username).exists():
                        messages.info(request,"Username is already taken!")
                        return redirect('adduser')
                    elif User.objects.filter(email=email).exists():
                        messages.info(request,"Email id is already taken!")
                        return redirect('adduser')
                    elif len(password1)<8:
                        messages.info(request,"Password length must be greater then 7")
                        return redirect('adduser')

                    else:
                        user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password1)
                        user.is_active = True
                        user.save();
                       
                        Employee_Name = request.POST['Employee_name']
                        Employee_id = request.POST['Employee_id']
                        bio = request.POST['bio']
                        phone_no = request.POST['phone_no']
                        blood_group = request.POST['blood_group']
                        Permanent_Address = request.POST['Permanent_Address']
                        Current_Address = request.POST['Current_Address']

                        obj = EmployeeDetils(
                            user=user,
                            Employee_Name=Employee_Name,
                            Employee_id=Employee_id,
                            bio=bio,
                            phone_no=phone_no,
                            blood_group=blood_group,
                            Permanent_Address=Permanent_Address,
                            Current_Address=Current_Address
                            )

                        obj.save();

                        messages.info(request,"ThankYou , Sucessfully Added Employye")

                        return redirect('adduser')
                else:
                    messages.info(request,"password not maching")
                    return redirect('adduser')

    else:
        return redirect('login')

    return render(request , "adduser.html",{})


def viewEmp(request):

        emp = list(EmployeeDetils.objects.filter().values())
        print(emp)

        employee=EmployeeDetils.objects.filter(user = request.user)
        employers =User.objects.filter(is_staff = False).values()

        

        dist={
        "employee":employee,
        "employers":employers,
        }

        return render(request,"viewemp.html",dist)


def removeuser(request,id=None):
    a = User.objects.get(id = id)
    name=a.username
    a.delete()
    msg=name+" is removed !"
    messages.info(request,msg)
    return redirect("viewemp")


def editemp(request,id=None):
    if request.method=="POST":
            a = User.objects.get(id = id)
            b=EmployeeDetils.objects.get(user = a)
            Employee_Name = request.POST['Employee_Name']
            blood_group = request.POST['blood_group']
            bio = request.POST['bio']
            phone_no = request.POST['phone_no']
            Permanent_Address=request.POST['permanent']
            if Employee_Name != "":
                b.Employee_Name=Employee_Name
            if blood_group != "":
                b.blood_group = blood_group
            if bio != "":
                b.bio=bio
            if phone_no != "":
                b.phone_no=phone_no
            if Permanent_Address != "":
                b.Permanent_Address
            b.save()
            msg=str(a.username)+" is changed sucessfully !"
            messages.info(request,msg)
            return redirect('viewemp')


    a = User.objects.get(id = id)
    b=EmployeeDetils.objects.filter(user = a).values()
    username=a.get_username()

    dist={

    "username":username,
    "i":a

    }
    return render(request,"editemp.html",dist)


def TrackEmp(request):
        employee=EmployeeDetils.objects.filter(user = request.user)
        employers =User.objects.filter(is_staff = False).values()

        dist={
        "employee":employee,
        "employers":employers,
        }

        
        return render(request,"TrackEmp.html",dist)

def track(request , id=None):
    context = {}
    a = User.objects.get(id = id)
    b=EmployeeDetils.objects.get(user = a)
    c=list(Address.objects.filter(user = a))
    if not c:
        error = "Employee has not shared live location untill now"
        context = {'error':error}
    else:
        add=Address.objects.get(user=a)
        geolocator = Nominatim(user_agent="first")
        lat = add.lat
        lon = add.lon

        


        m = folium.Map(width = 800,
        height=500,
        location= get_center_coordinates(lat,lon),
        zoom_start = get_zoom(0))

        folium.Marker([lat,lon],
        tooltip="Click Here For More",
        popup = add.city,
        icon = folium.Icon(color="blue" , icon = "cloud")).add_to(m)
        
        m = m._repr_html_()



        context = {
                "lat":lat,
                "lon":lon,
                "map":m,
                "emp":b,
            }
    return render(request , "track.html" , context)

def paid_time_off(request):
    user = User.objects.all()
    context = {
            'user' : user
        }

        
    if request.method == "POST":

        user = request.POST['user']
        Time_From_Time = request.POST["Time_From_Time"]
        Time_From_Date = request.POST["Time_From_Date"]
        Time_To_Time = request.POST["Time_To_Time"]
        Time_To_Date = request.POST["Time_To_Date"]
        status = request.POST["status"]

        from_time = str(Time_From_Date)+" "+str(Time_From_Time)+":00"
        to_time = str(Time_To_Date)+" "+str(Time_To_Time)+":00"
        user_obj = User.objects.get(username = user) 
        obj = Paid_Time_Off(
            user=user_obj,
            Time_From = from_time,
            Time_To = to_time,
            status = status
        )

        obj.save();
        message = f"ThankYou , {user} was {status}."
        messages.info(request , message)
        return redirect("paid_time_off")
   
            
    return render(request,'approve.html',context)



    

def adminhome(request):
    if request.user.is_authenticated and request.user.is_staff:
        admin=Admin.objects.filter(user = request.user)
        dist = {'admin' : admin}

       

        return render(request,'admin.html',dist)
    else :
       messages.info(request,"Login to enter")
       return redirect("login")


def logout(request):
    auth.logout(request)
    return redirect("index")

def subscribe(request):
    if request.method == 'GET':
        subscribe = request.GET['subscribe']
        return redirect('index')
    return render(request,'base.html')

def index(request):
    
    if request.user.is_authenticated:
            if request.user.is_active and request.user.is_staff:
                return redirect('adminhome')
            else:
                return redirect('employeehome')
    else:
        if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['email']
            subject = request.POST['subject']
            message = request.POST['message']
            return redirect('index')
            # send_mail(
            #     name,
            #     message,
            #     email,
            #     ['deenadhayalan0705@gmail.com']
            # )
            # if name != '' and email != '':
            #     message = "Thank You , we will contact you shortly."
            
    return render(request,'base.html')







def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None :
            auth.login(request,user)
            if user.is_active and user.is_staff :
                    return redirect('adminhome')
            else :
                return redirect('employeehome')

        else:
            messages.info(request,"Username or Password is wrong")
            return redirect("login")

    return render(request,"login.html")




def Admin1(request):
    if request.method=='POST':
        email=request.POST['email']
        username=request.POST['username']
        first_name=request.POST['first_name']  #to differnt the Custom / employer
        last_name=request.POST['last_name'] #used to store shop name
        password1=request.POST['password1']
        password2=request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username is already taken!")
                return redirect('Admin1')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email id is already taken!")
                return redirect('Admin1')
            elif len(password1)<8:
                messages.info(request,"Password length must be greater then 7")
                return redirect('Admin1')

            else:
                  user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password1)
                  user.is_active = True
                  user.is_staff = True
                  user.save();
                  #send_emailto(email) #sending email
                  role = request.POST["role"]
                  obj = Admin(user = user , role = role)
                  obj.save();
                  return redirect('adminhome')
        else:
            messages.info(request,"password not maching")
            return redirect('Admin1')


    else:
         return render(request,'admin_signup.html')


def role(request):
    if request.user.is_authenticated and request.user.is_staff and request.user.is_active:
        if request.method == "POST":
            user = request.user
            role = request.POST["role"]
            obj = role(user = user , role = role)
            obj.save();
            return redirect('adminhome')
        
            
    return render(request , 'admin_role.html')

def cat_signup(request):
    return render(request , 'cat_signup.html')



def aboutus(request):
             return render(request,'aboutus.html')


def contactus(request):
             return render(request,'contact_us.html')