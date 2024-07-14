from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from sublime.models import Notification

#admin only decorator
def admin_only(view_func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request,*args,**kwargs)
        else:
            messages.error(request, "You do not have permission to access this page. Please login as an admin.")
            return redirect('login')  
    return wrapper


# organizer only decorator
def organizer_only(view_func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated and request.user.is_organizer:
            return view_func(request,*args,**kwargs)
        else:
            messages.error(request, "Only registered organizers can create an event. Please login as an organizer.")
            return redirect('login')  
    return wrapper


#decorator for updating notifications
def update_notifications(view_func):
    def wrapper(request,*args,**kwargs):
        response = view_func(request,*args,**kwargs)        
        unread_notifiations = Notification.objects.filter(recepient=request.user.id).filter(read=False).count()
        request.session['notifications'] = unread_notifiations
        return response
    return wrapper
