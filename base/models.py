from django.db import models
from django.contrib.auth import models as auth_models
import uuid
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# from __future__ import unicode_literals
# Create your models here.

class UserManager(auth_models.BaseUserManager):
    def create_user(self, first_name:str, last_name:str, email:str, password:str = None,is_staff=False,is_superUser=False)->"User":
        if not email:
            raise ValueError ("User Must Have an Email")
        if not first_name:
            raise ValueError ("User Must Have a First Name")
        if not last_name:
            raise ValueError ("User Must Have a Last Name")

        user=self.model(email=self.normalize_email(email))
        user.first_name=first_name
        user.last_name=last_name
        user.set_password(password)
        user.is_active=True
        user.is_staff=is_staff
        user.is_superuser=is_superUser
        user.save()


        return user
    def create_superuser(self, first_name:str, last_name:str, email:str, password:str)->"User":
        user=self.create_user(first_name=first_name, last_name=last_name, email=email,password=password, is_superUser=True, is_staff=True,)

        user.save()
        return user


class User(auth_models.AbstractUser):
    first_name=models.CharField(verbose_name="First Name",max_length=200)
    last_name=models.CharField(verbose_name="Last Name",max_length=250)
    email=models.EmailField(verbose_name="Email",max_length=255,unique=True)
    password=models.CharField(max_length=255)
    phone=models.CharField(max_length=50)
    avatar=models.ImageField(upload_to="uploads",blank=True,null=True)
    location=models.CharField(max_length=255,blank=False,null=False)
    account_type=models.CharField(max_length=20,verbose_name="accout-type")
    username=None
    


    objects = UserManager()

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=["first_name","last_name"]


    # @property

    # def token(self):
    #     token= jwt.encode({"email":self.email,"location":self.location,"exp":datetime.utcnow() + timedelta(hours=24)},settings.SECRET_KEY,algorithms=['HS256'] )

    #     return token


    def __str__(self):
        return  self.email

class Bike(models.Model):
    name=models.CharField(max_length=500)
    description=models.CharField(max_length=500)
    price=models.CharField(max_length=500)
    image=models.ImageField(upload_to="uploads",blank=True,null=True)
    owner=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    rent_status=models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name



class Rentals(models.Model):
    bike=models.ForeignKey(Bike,on_delete=models.DO_NOTHING)
    owner=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="owner")
    customer=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="customer")
    date_of_renting=models.DateField(auto_now_add=True,null=True,blank=True)
    
    date_of_return=models.DateField()
    paid=models.BooleanField(default=False)

class RepairServices(models.Model):
    owner=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    issue=models.TextField(max_length=500)
    bike=models.ForeignKey(Bike,on_delete=models.DO_NOTHING)
    date=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=20,blank=True,null=True)



# Create your models here.
class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, blank=True)
    is_deleted = models.BooleanField(default=False, blank=True)

    class Meta:
        abstract = True


class PaymentTransaction(models.Model):
    phone_number = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    is_finished = models.BooleanField(default=False)
    is_successful = models.BooleanField(default=False)
    trans_id = models.CharField(max_length=30)
    bike=models.CharField(max_length=5,null=True,blank=True)
    order_id = models.CharField(max_length=200)
    checkout_request_id = models.CharField(max_length=100)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)

    content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.SET_NULL)
    object_id = models.PositiveIntegerField(default=0)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "{} {}".format(self.phone_number, self.amount)


class Wallet(BaseModel):
    phone_number = models.CharField(max_length=30)
    available_balance = models.DecimalField(('available_balance'), max_digits=6, decimal_places=2, default=0)
    actual_balance = models.DecimalField(('actual_balance'), max_digits=6, decimal_places=2, default=0)
    date_modified = models.DateTimeField(auto_now=True, null=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return self.phone_number
