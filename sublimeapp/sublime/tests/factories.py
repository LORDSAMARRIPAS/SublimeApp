import factory
from django.contrib.auth.models import User
from sublime.models import Review, CustomUser, Event, Notification

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
    username = "FactoryUser"
    email = "user@ubc.ca"
    password = "456userpw546"
    first_name = "Factory"
    last_name = "User"    
    


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review
    event_id = 2
    user_id = factory.SubFactory(UserFactory)
    title = "Factory Test title"
    review_txt = "Test Review"
    rating = 5


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event
    creator = factory.SubFactory(UserFactory)
    description = "Factory Test Event"
    location = "Factory Test Location"
    edatetime = "2020-12-12 12:00:00"
    price = 10.00
    available = 100
    status = 'pending'

class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification
    user_id = factory.SubFactory(UserFactory)
    message = "Factory Test Notification"
    read = False
    