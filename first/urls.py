from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns=[

   path('',views.index,name="index"),
   path('login' , views.login , name="login"),
   path('cat_signup' , views.cat_signup , name="cat_signup"),
   path('Admin1',views.Admin1,name="Admin1"),
   path('logout',views.logout,name="logout"),
   path('role' , views.role,  name="role"),
   path('getlatlon' , views.getlatlon , name="getlatlon"),
   path('TrackEmp' , views.TrackEmp , name="TrackEmp"),
   path('organize_emp' , views.organize_emp , name="organize_emp"),
   path('track/<int:id>' , views.track , name="track"),
   path('employeehome' , views.employeehome , name="employeehome"),
   path('adduser' , views.adduser , name="adduser"),
   path('editemp/<int:id>' , views.editemp , name="editemp"),
   path('viewemp' , views.viewEmp , name='viewemp'),
   path('removeuser/<int:id>' , views.removeuser , name="removeuser"),
   path('paid_time_off' , views.paid_time_off , name="paid_time_off"),
   path('adminhome',views.adminhome,name="adminhome"),
   path('aboutus',views.aboutus,name="aboutus"),
   path('contactus',views.contactus,name="contactus"),
   path('subscribe' , views.subscribe , name="subscribe")





]

