from django.dispatch import receiver, Signal
from django.urls import reverse
from sublime.models import Event, Notification, Registered


event_updated = Signal()
event_rejected = Signal()

@receiver(event_updated)
def event_updated_handler(sender,**kwargs):
    #print("Event Updated Signal Received")
    event = kwargs.get('event_id')
    creator = kwargs.get('creator')
    name = kwargs.get('name')    
    registered_msg = f"Event {name} has been updated by {creator}. Check it out!"
    creator_msg = f"Event {name} has been updated successfully"
    #send a notification event creator
    Notification.objects.create(recepient=creator, event=sender, message=creator_msg)
    #query all users who are attending the event
    attendees = Registered.objects.filter(event=event)
    for attendee in attendees:
        Notification.objects.create(recepient=attendee.user, event=sender, message=registered_msg)
    #print("Notification sent to all attendees")
   
@receiver(event_rejected)
def event_rejected_handler(sender,**kwargs):
    event = kwargs.get('event_id')
    creator = kwargs.get('creator')
    name = kwargs.get('name')
    creator_msg = f"Event {name} has been rejected. Please make necessary changes and resubmit."
    Notification.objects.create(recepient=creator, event=sender, message=creator_msg)
    #print("Notification sent to event creator")
