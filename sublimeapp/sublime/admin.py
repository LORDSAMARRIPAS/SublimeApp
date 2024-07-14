from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Event, Review, Cart, Transaction, TransactionItem

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id",
                    "username",
                    "first_name",
                    "last_name",
                    "email",
                    "user_type",
                    "profile_image",
                    )

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Review)

class EventAdmin(admin.ModelAdmin):
    list_display = ("id",
                    "creator_id",
                    "image",
                    "name",
                    "description", 
                    "location", 
                    "edatetime", 
                    "price", 
                    "available",  
                    "sold",
                    "status",)
admin.site.register(Event, EventAdmin)

class CartAdmin(admin.ModelAdmin):
    pass
admin.site.register(Cart, CartAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id",
                    "date", 
                    "total_price", 
                    "user", 
                    "completed",
                    )
admin.site.register(Transaction, TransactionAdmin)

class TransactionItemAdmin(admin.ModelAdmin):
    list_display = ("id",
                    "quantity", 
                    "price", 
                    "event",
                    "user", 
                    )
admin.site.register(TransactionItem, TransactionItemAdmin)





