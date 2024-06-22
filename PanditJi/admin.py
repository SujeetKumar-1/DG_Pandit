from django.contrib import admin
from .models import *

class List_dis(admin.ModelAdmin):
    list_display=('name','email', 'user_type', 'password')

class service_list(admin.ModelAdmin):
    list_display=("title", 'fee', 'description', 'service_img')

class profileData(admin.ModelAdmin):
    list_display=("pname", 'phone', 'faddress', 'photo')

class bookingData(admin.ModelAdmin):
    list_display=("ritual", "P_user", "N_user", "email", "phone", "destination", "ritual_date", "ritual_time")

admin.site.register(UserAccount)
admin.site.register(People, List_dis)
admin.site.register(Pandit, List_dis)
admin.site.register(serviceData, service_list)
admin.site.register(panditProfileData, profileData)
admin.site.register(Bookings, bookingData)



