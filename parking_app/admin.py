from django.contrib import admin
from parking_app.models import Contact, Product, Orders, OrderUpdate, Registration


# Register your models here.
admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Orders)
admin.site.register(OrderUpdate)
admin.site.register(Registration)

