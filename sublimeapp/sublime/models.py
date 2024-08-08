from django.contrib.auth.models import AbstractUser # type: ignore
from django.db import models # type: ignore
from django.conf import settings # type: ignore
from django.utils.timezone import now # type: ignore
import uuid
from django.utils import timezone # type: ignore
from datetime import datetime, timedelta

def get_current_datetime():
    return timezone.now()


# Custom User model extending the default AbstractUser
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('organizer', 'Event Organizer'),
        ('customer', 'Customer'),
        ('admin', 'Admin'),  # Add 'admin' type for internal use
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, blank=True, null=True)
    profile_image = models.ImageField(upload_to='sublime/images/', null=True, blank=True, default='default_profile_image.png')
    email_verified = models.BooleanField(default=False)
    email_verification_code = models.CharField(max_length=6, blank=True, null=True)
    verification_code_expiry = models.DateTimeField(null=True, blank=True)
    postal_code = models.CharField(max_length=12, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # If the user is a superuser, ignore the current user_type and set it to 'admin'
        if self.is_superuser:
            self.user_type = 'admin'
        super(CustomUser, self).save(*args, **kwargs)

    # Properties
    @property
    def is_organizer(self):
        return self.user_type == 'organizer'

    @property
    def is_customer(self):
        return self.user_type == 'customer'

    @property
    def is_admin(self):
        return self.user_type == 'admin' or self.is_superuser

    def set_verification_code(self):
        # Simplified code generation, ensure uniqueness or handle potential collisions as needed
        self.email_verification_code = str(uuid.uuid4().int)[:6]
        self.verification_code_expiry = timezone.now() + timedelta(hours=1)
        self.save()

    def verify_email(self, code):
        if timezone.now() > self.verification_code_expiry:
            return False, "Code expired"
        if self.email_verification_code == code:
            self.email_verified = True
            self.email_verification_code = None  # Invalidate the code
            self.verification_code_expiry = None  # Clear the expiry
            self.save()
            return True, "Email verified successfully"
        return False, "Invalid code"
    # Added custom field to Django User model
    
class UserProfile(models.Model):
    TYPE_CHOICES = (
        (1, 'User'),
        (2, 'Organizer'),
        (3, 'Admin'),  # New admin type

    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, default=1)

    def __str__(self):
        return self.user.username
      
# Event model
class Event(models.Model):    
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_images/',null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    location = models.CharField(max_length=200)
    edatetime = models.DateTimeField(default=now, verbose_name="Event Date")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.PositiveIntegerField(verbose_name="Number of Tickets")
    sold = models.PositiveIntegerField(default=0)
    
    #Event status Verification that crucial for events to be put into lists for approval after its created! 
    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')    

    class Meta:
        ordering = ['edatetime']

    def __str__(self):
        return f"Event {self.id} by {self.creator}"

    def is_available(self):
        return self.available > self.sold
    
    def quantity_available(self):
        return self.available - self.sold

    def button_disable(self):
        return "" if self.is_available() else "disabled"
    
    def quantity_available(self):
        return self.available - self.sold
    
    #event status is pending
    def is_pending(self):
        return self.status == 'P'
    
    #event status is approved
    def is_approved(self):
        return self.status == 'A'
    
    #event status is rejected
    def is_rejected(self):
        return self.status == 'R'
    
    #event status friendly name
    def get_status_display(self):
        for status, display in self.STATUS_CHOICES:
            if status == self.status:
                return display
        return None
    
    def notify(self):
        from sublime.signals import event_updated, event_rejected
        if self.is_approved():
            event_updated.send(sender=self, event_id=self.id,  name=self.name, creator=self.creator)        
        if self.is_rejected():            
            event_rejected.send(sender=self, event_id=self.id, name=self.name, creator=self.creator)
        

    
    
class Review(models.Model):
    rating_choices = [(i, str(i)) for i in range(1, 6)]

    # Change this to a ForeignKey relation
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    rating = models.PositiveIntegerField(choices=rating_choices, default=5)
    review_txt = models.TextField(max_length=1000)
    date = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} - by {self.user_id.username if self.user_id else 'Unknown'}"
    
    def get_event_display(self):
        return self.event.name if self.event else "N/A"
# Cart Table
class Cart(models.Model):
    quantity = models.PositiveIntegerField(default=0)
    user_id = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Cart id = {self.id}   User id = {self.user_id.id}   Event id = {self.event_id.id}"
    
    def get_total_item_price(self):
        total = self.quantity * self.event_id.price
        return total
    
    def quantity_available(self):
        return self.event_id.available - self.event_id.sold
    
    
class TransactionItem(models.Model):
    user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
     
    
    def __str__(self):
        return str(self.id) 


class Transaction(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    # User can have more than one transactions
    user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Transaction has been processed
    completed = models.BooleanField(default=False)
    items = models.ManyToManyField(TransactionItem)

    def __str__(self):
        return  f"Transaction id = {self.id}   User id = {self.user.id}   date = {self.date}"
    
# Class for admin event rejection details
class EventRejection(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    reason = models.TextField(max_length=500)
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.event_id)
    
#create a Notification model
class Notification(models.Model):
    recepient = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    date = models.DateTimeField(default=datetime.now)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.user)
    
    def is_read(self):
        return self.read
    
    def set_read(self):
        self.read = True
        self.save()

class Registered(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return str(self.user + " for " + self.event)
    

