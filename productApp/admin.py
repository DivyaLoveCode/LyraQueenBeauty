from django.contrib import admin
from .models import LoginUser, Enquiry, Order

# Register your models here.
admin.site.register(LoginUser)
admin.site.register(Enquiry)
admin.site.register(Order)
