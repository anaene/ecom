from django.contrib import admin

from .models import *

# Register your models here.
# test username rocktman
# password for all test user Gbd#21JSDs@
admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderProduct)
