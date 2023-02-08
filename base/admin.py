from django.contrib import admin

# Register your models here.
from . import models




class UserAdmin(admin.ModelAdmin):
    list_display=("id","first_name","last_name","email","location","account_type","phone")
    ordering = ['first_name']
    search_fields = ['first_name']



class BikeAdmin(admin.ModelAdmin):
    list_display=("id","name","description","price","owner",)
    ordering = ['name']
    search_fields = ['name']


class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "amount", "is_finished",
                    "is_successful","bike", "trans_id", 'date_created', 'date_modified')



class RentalsAdmin(admin.ModelAdmin):
    list_display=("bike","owner","customer","date_of_renting","date_of_return","paid")


admin.site.register(models.Rentals,RentalsAdmin)
admin.site.register(models.PaymentTransaction, PaymentTransactionAdmin)
admin.site.register(models.Wallet)


admin.site.register(models.User,UserAdmin),
admin.site.register(models.Bike,BikeAdmin),
# admin.site.register(models.)
