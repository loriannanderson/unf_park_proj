from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Contact(models.Model):
    # contact_id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    desc = models.TextField(max_length=500)
    phonenumber = models.IntegerField()

    def __int__(self):
        return self.id

class Registration(models.Model):
    registration_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    student_id_num = models.CharField(max_length=15, blank=True, null=True)
    employee_id_num = models.CharField(max_length=15,blank=True, null=True)
    address_1 = models.CharField(max_length=40)
    address_2 = models.CharField(max_length=40, blank=True, null=True)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=25)
    phone = models.CharField(max_length=100, default="", blank=True, null=True)
    vehicle_make = models.CharField(max_length=50, blank=True)
    vehicle_model = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=50, blank=True)
    license_plate = models.CharField(max_length=10, blank=True)
    vehicle2_make = models.CharField(max_length=50, blank=True)
    vehicle2_model = models.CharField(max_length=50, blank=True)
    color2 = models.CharField(max_length=50, blank=True)
    license2_plate = models.CharField(max_length=10, blank=True)
    def __str__(self):
        return (self.first_name + " " + self.last_name + " - " + self.user.username)

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    image = models.ImageField(upload_to='images/images')
    #add for parking
    active = models.BooleanField(default=True)
    start_date = models.DateField(default=None, null=True)
    end_date = models.DateField(default=None, null=True)


    def __str__(self):
        return self.product_name

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # items_json = models.CharField(max_length=5000) # should remove but want to still see it for now
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=90)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=25)
    oid = models.CharField(max_length=150, blank=True)
    amountpaid = models.CharField(max_length=500, blank=True, null=True)
    paymentstatus = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    delivered = models.BooleanField(default=False)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."

