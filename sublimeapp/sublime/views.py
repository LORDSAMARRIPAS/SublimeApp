from datetime import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, Review, EventRejection, Cart, Transaction, TransactionItem, Registered, Notification, CustomUser
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from sublime.forms import CustomUserCreationForm, CustomerProfileForm, EventForm, OrganizerProfileForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import CustomLoginForm, ReviewForm, EventRejectionForm, AdminProfileForm
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from .filters import EventFilter
from django.core.exceptions import PermissionDenied
from .emailVerify import send_verification_email
from django.db.models import Count
from django.db.models import Subquery
from django.db.models import OuterRef
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from sublime.decorators import admin_only, organizer_only, update_notifications
from django.dispatch import receiver
from sublime.signals import event_updated

from .payment import create_payment_link


# Create your views here.
def home(request):
    # current logged in user 
    current_user = request.user
    # need to define the session variable here or else gets an error
    # get the shopping cart list, total price and total items
    shoppingcart_list = Cart.objects.filter(user_id=current_user.id)
    total_price = sum(item.event_id.price * item.quantity for item in shoppingcart_list)
    total_items = sum(item.quantity for item in shoppingcart_list)
    request.session['total_items'] = total_items
    
    return render(request, 'home.html')

# This view is accessible to everyone without requiring login
def list_events(request):
    
    # Start with approved events for everyone
    event_queryset = Event.objects.filter(status='A', edatetime__gte=timezone.now())

    # If the user is authenticated and an organizer, include their own events regardless of approval
    if request.user.is_authenticated and hasattr(request.user, 'is_organizer') and request.user.is_organizer:
        event_queryset |= Event.objects.filter(creator=request.user)
    
    # Apply additional filtering based on filter form
    myFilter = EventFilter(request.GET, queryset=event_queryset)
    event_queryset = myFilter.qs
    
    context = {'eventList': event_queryset,
               'myFilter': myFilter,
               }
    return render(request, "registration/list_events.html", context)


def authView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_verification_code()  # Set the verification code
            
            # Try to send verification email
            try:
                send_verification_email(user.email, user.email_verification_code)
                messages.success(request, 'Your account has been created! Please check your email to verify.')
                return redirect('email_verify_code', user_id=user.id)  # Redirect to email verification page
            except Exception as e:
                user.delete()  # Optionally delete the user if email sending fails
                messages.error(request, f'There was an error creating your account: {e}')
                return redirect('signup')
        else:
            # If form is not valid, display form with errors
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# View for verifying the email verification code
def verify_code(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    
    if request.method == "POST":
        verification_code = request.POST.get('verification_code')
        success, message = user.verify_email(verification_code)
        
        if success:
            messages.success(request, message)
            return redirect('login')  # Redirect to login after successful verification
        else:
            messages.error(request, message)
    
    return render(request, 'registration/EmailVerifyCode.html', {'user_id': user_id})

@update_notifications
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Add a success message on login
            messages.success(request, f'Welcome back, {user.username}!')
             # add a routine to update the number of items in the cart here.
            shoppingcart_list = Cart.objects.filter(user_id=request.user.id)
            total_items = sum(item.quantity for item in shoppingcart_list)
            #unread_notifiations = Notification.objects.filter(recepient=request.user.id).filter(read=False).count()
            request.session['total_items'] = total_items
            #request.session['notifications'] = unread_notifiations
            return redirect('profilePage')  # Assuming 'profilePage' is the correct path to the profile page
        else:
            # Add an error message if login is invalid
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    else:
        form = CustomLoginForm()  # If using a custom login form
        return render(request, "registration/login.html", {'form': form})


@login_required(login_url='login')
def profile(request):
    form_class = CustomerProfileForm
    if request.user.is_organizer:
        form_class = OrganizerProfileForm
    elif request.user.is_superuser:
        form_class = AdminProfileForm
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            if 'email' in form.changed_data:
                request.user.set_verification_code()  # Generate new verification code
                send_verification_email(request.user.email, request.user.email_verification_code)
                messages.info(request, 'Please verify your new email address. A verification email has been sent.')
                # Redirect to a dedicated page for email verification after update
                return redirect('email_verification_needed', user_id=request.user.id)
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profilePage')
    else:
        form = form_class(instance=request.user)
    context = {'form': form}
    return render(request, 'registration/profilePage.html', context)

@login_required(login_url='login')
def email_verification_needed(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Make sure the user can only access their own verification page
    if request.user != user:
        return redirect('some_error_page')  # Redirect to an error page or home

    if request.method == "POST":
        verification_code = request.POST.get('verification_code')
        success, message = user.verify_email(verification_code)
        
        if success:
            messages.success(request, message)
            return redirect('profilePage')  # Redirect to the profile page after successful verification
        else:
            messages.error(request, message)
            # Stay on the verification page and show the error

    context = {'user_id': user_id}
    return render(request, 'registration/updateEmail.html', context)

    
@login_required(login_url='login')
def my_tickets(request):
    # Determine if the user is a customer or an organizer
    user_type = 'customer' if request.user.is_customer else 'organizer'

    # Based on the user type, retrieve the appropriate events
    if user_type == 'customer':
        # Fetch events the customer has registered for
        # This is a placeholder - update with actual query after merge
        registered_events = []  # EventRegistration.objects.filter(user=request.user)
    else:
        # Fetch events created by the organizer
        created_events = Event.objects.filter(creator=request.user)

    # Adjust context based on user type
    context = {
        'events': registered_events if user_type == 'customer' else created_events,
        'user_type': user_type
    }

    return render(request, 'registration/Myevents.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')

@login_required
def profile_image_change(request):
    if request.method == 'POST':
        # Select the correct form class based on the user type
        form_class = OrganizerProfileForm if request.user.is_organizer else CustomerProfileForm
        # Instantiate the form with the POST and FILES data and bind it to the current user instance
        form = form_class(request.POST, request.FILES, instance=request.user)
        
        if form.is_valid():
            # If the form is valid, save it and set a success message
            form.save()
            messages.success(request, "Profile image updated successfully.")
        else:
            # If the form is not valid, print the errors to the console and set an error message
            print(form.errors)
            messages.error(request, "Error updating your profile image. Please check the form.")
        
        # After processing the form, redirect to the profile page
        return redirect('profilePage')
    else:
        # If the request is not POST, redirect to the profile page with an error message
        messages.error(request, "Invalid request.")
        return redirect('profilePage')

@login_required(login_url='home')
def add_review(request, organizer_id):
    # Ensure the user is a customer
    if not request.user.is_customer:
        return HttpResponseForbidden("You do not have permission to review.")

    # Filter events for the given organizer that are approved
    organizer_events = Event.objects.filter(creator_id=organizer_id, status='A').values_list('id', flat=True)

    # Check if the user has already left a review for this organizer's events
    if Review.objects.filter(user_id=request.user, event_id__in=organizer_events).exists():
        messages.warning(request, "You have already reviewed an event by this organizer.")
        return redirect('single_organizer_reviews', organizer_id=organizer_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, organizer_id=organizer_id)
        if form.is_valid():
            review = form.save(commit=False)
            review.user_id = request.user
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('single_organizer_reviews', organizer_id=organizer_id)
    else:
        # Form is instantiated here with the organizer_id to ensure the correct queryset
        form = ReviewForm(organizer_id=organizer_id)
        form.fields['event'].queryset = Event.objects.filter(creator_id=organizer_id, status='A')

    return render(request, 'reviews/add_review.html', {'form': form, 'organizer_id': organizer_id})

def show_reviews(request, event_id):   
    #show reviews for event_id
    reviewList = Review.objects.filter(event_id=event_id).select_related('user_id')        
    return render(request, "reviews/show_reviews.html",{"reviews":reviewList, 'event_id':event_id})
    

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    # Check if the current user is the one who created the review
    if request.user != review.user_id:
        messages.error(request, "You do not have permission to edit this review.")
        return redirect('organizers_list')  # Redirect them to a suitable view

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review, organizer_id=review.event.creator_id if review.event else None)
        if form.is_valid():
            form.save()
            messages.success(request, "Review updated successfully.")
            return redirect('single_organizer_reviews', organizer_id=review.event.creator_id if review.event else None)
    else:
        # Initialize the form with the review instance and limit event choices
        form = ReviewForm(instance=review, organizer_id=review.event.creator_id if review.event else None)

    return render(request, 'reviews/edit_review.html', {'form': form, 'review_id': review_id})

from django.db.models import IntegerField  # Import IntegerField

def organizers_list(request):
    organizer_events = Event.objects.filter(creator_id=OuterRef('pk'))
    reviews_subquery = Review.objects.filter(
        event_id__in=Subquery(organizer_events.values('id'))
    ).values('event_id').annotate(cnt=Count('pk')).values('cnt')
    organizers = CustomUser.objects.filter(user_type='organizer').annotate(
        reviews_count=Subquery(reviews_subquery, output_field=IntegerField()))
    return render(request, 'reviews/OrgReviews_show.html', {'organizers': organizers})

def single_organizer_reviews(request, organizer_id):
    organizer = get_object_or_404(CustomUser, pk=organizer_id)
    # Retrieve only events that are approved.
    events = Event.objects.filter(creator=organizer, status='A').order_by('-edatetime')
    # Now we're getting the IDs of these events to filter reviews.
    event_ids = events.values_list('id', flat=True)
    # Filter reviews where the event_id is in the list of approved events' IDs.
    reviews = Review.objects.filter(event_id__in=event_ids).select_related('user_id')
    add_review_url = reverse('add_review', kwargs={'organizer_id': organizer_id})
    context = {
        'organizer': organizer,
        'reviews': reviews,
        'add_review_url': add_review_url,
    }
    return render(request, 'reviews/SingleOrgReviews.html', context)


@organizer_only
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            return redirect('event_created_confirmation')
    else:
        form = EventForm()
    return render(request, 'events/create_events.html', {'form': form})

@organizer_only
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)   
    form = EventForm(instance = event)   
    if request.method == "POST":                  
        form = EventForm(request.POST, instance=event)      
        if form.is_valid():
            if form.has_changed():
                event = form.save(commit=False)
                event.status = 'P'
                event.save()
            return redirect('my_tickets')            
       
    context = {'form': form, 'event': event}  
    return render(request, 'events/edit_event.html', context)

 
# Created_event confirmation!
@login_required(login_url='home')
def event_created_confirmation(request):
    return render(request, 'events/event_created_confirmation.html')


# Admin event dashboard
@admin_only
def event_dashboard(request, status = 'pending'):        
    event_queryset = Event.objects.all().prefetch_related('eventrejection_set') 
    eventList = event_queryset
    return render(request, "admin/event_dashboard.html", {"eventList": eventList, "status": status })


# Admin event approval
@admin_only
def approve_event(request, event_id):    
    event = get_object_or_404(Event, pk=event_id)
    event.status = 'A'    
    #event.verified = True
    event.save()
    #event_updated.send(sender=event, event_id = event.id, name = event.name, creator = event.creator)
    event.notify()
    return redirect('event_dashboard')

# Admin event rejection
@admin_only
def reject_event(request, event_id):       
    form = EventRejectionForm()
    if request.method == 'POST':   
        form = EventRejectionForm(request.POST)
        if form.is_valid():               
            #Add rejection reason to the database
            reason = form.cleaned_data['reason']   
            event = get_object_or_404(Event, pk=event_id)
            event.status = 'R'
            event.save()    
            event_rejection = EventRejection(event_id = event, reason=reason)
            event_rejection.save()  
            event.notify()                 
            return redirect('event_dashboard')
    context = {'form' : form, 'event_id': event_id}    
    return render(request, 'admin/reject_event.html', context)

@admin_only
def edit_rejection(request, rejection_id):      
    rejection = get_object_or_404(EventRejection, pk=rejection_id)   
    form = EventRejectionForm(instance = rejection)   
    if request.method == "POST":                 
        form = EventRejectionForm(request.POST, instance=rejection)      
        if form.is_valid():               
            form.save()          
            return redirect('event_dashboard') 
    context = {'form': form, 'rejection': rejection}  
    return render(request, 'admin/reject_event_edit.html', context)



# Display the list of events in a shopping cart for the current user
@login_required(login_url='login')
def shopping_cart(request):
    
    # current logged in user 
    current_user = request.user
    
    # get the shopping cart list, total price and total items
    shoppingcart_list = Cart.objects.filter(user_id=current_user.id)
    total_price = sum(item.event_id.price * item.quantity for item in shoppingcart_list)
    total_items = sum(item.quantity for item in shoppingcart_list)
    request.session['total_items'] = total_items
    return render(request, "sublime/cart/shopping_cart.html/",{"cartList":shoppingcart_list, "total_price":total_price,"total_items":total_items})

@login_required(login_url='login')
def add_to_shopping_cart(request, event_id):
    # Post request from list_event
    if request.method == 'POST':        
        # Check if event exists in Event table
        # event = Event.objects.filter(pk=eid).first()
        event = get_object_or_404(Event,pk=event_id)
        current_user = request.user
        
        if event:
            # Check the shopping cart if the event already exists. if so then increment
            # the quantity by 1.
            #cart = Cart.objects.filter(event_id=event.pk, user_id=current_user.pk).first()
            cart, created = Cart.objects.get_or_create(event_id=event, user_id=current_user)
            # if cart already contains the same event, then quantity gets incremented by 1
            # else quantity is 1.
            cart.quantity += 1
            cart.save()    
        else: 
            print("***** add_to_shopping_cart Error, can't find event id to add to Cart")   
    # call method shopping_cart in views.py   
    return redirect('shopping_cart')

@login_required(login_url='login')
def delete_from_shopping_cart(request, cart_id):
    # Post request from cart.html
    if request.method == 'POST':
        # delete the selected event from the cart.   
        Cart.objects.filter(id=cart_id).delete()
            
    # call method shopping_cart in views.py   
    return redirect('shopping_cart')

@login_required(login_url='login')
def update_shopping_cart(request, cart_id):
    # Post request from shopping_cart.html
    if request.method == 'POST':
        # get the quantity from the form
        quantity = request.POST["quantity"] # the new quantity from the form
        
        cart = get_object_or_404(Cart, pk=cart_id)
        if cart:
            # found an item in cart for the event, lets update the quantity.
            cart.quantity = quantity
            # save to the database
            cart.save()
            
            messages.success(request, 'Shopping Cart Updated!')
        else: 
            print("***** update_shopping_cart Error, can't find item in Cart")
            
     # call method shopping_cart in views.py   
    return redirect('shopping_cart')

# Display the payment page for the user
@login_required(login_url='home')
def payment(request):
    total_price = sum(item.event_id.price * item.quantity for item in Cart.objects.filter(user_id=request.user.id))
    price_in_cents = int(total_price * 100)

    payment_link = create_payment_link(price_in_cents)

    if payment_link:
        return redirect(payment_link)
    else:
        return render(request, "sublime/cart/payment.html", {"error": "Unable to create payment link."})

# Verify the payment 
# add the items from the shopping cart to the Transaction and TransactionItem models.
# update the quantity sold in the Event module
# empty the shopping cart
# send a confirmation email
# display a transaction success email
# retun the user back to the home page
@login_required(login_url='home')
def complete_payment(request):
    # current logged in user 
    current_user = request.user

    # verify payment
    # --TODO--

    # add the items from the shopping cart to the Transaction and TransactionItem models.
    # update the quantity sold in the Event module
    # empty the shopping cart
    
    # must be a better way to get the total price, but for now it works
    total_price = 0
    cart = Cart.objects.filter(user_id=current_user.id)
    for each_item in cart:
        total_price= total_price + (each_item.quantity * each_item.event_id.price)
    # create a new Transaction model    
    new_transaction = Transaction(user=current_user, total_price=total_price)
    new_transaction.save()
    for each_item in cart:
        # update the amount sold in the Event module
        each_item.event_id.sold = each_item.event_id.sold + each_item.quantity
        each_item.event_id.save()  
        # create the TransactionItem model
        new_transaction_item = TransactionItem(quantity=each_item.quantity,
                                               price=each_item.event_id.price,
                                               event=each_item.event_id,
                                               user=current_user)
        new_transaction_item.save()
        new_transaction.items.add(new_transaction_item)

        #register user for Event notifications
        registered = Registered(user=current_user, event=each_item.event_id)
        registered.save()


    # empty the shopping cart
    Cart.objects.filter(user_id=current_user.id).delete()

    # set the session variable total_items to 0
    request.session['total_items'] = 0
    
    # html message
    # msg_html = render_to_string('templates/email.html', {'some_params': some_params})
    # get the user email address
    user_email = current_user.email
    
    # send a confirmation email to the user 
    subject="Your tickes are available"
    message=("Thank you for using Sublime System.\nhere is your ticket" +
    "\nThe total price of your order is $"+ str(total_price))
    # send_mail(subject, message, DEFAULT_FROM_EMAIL,[current_user.email])

    # display a success message 
    messages.success(request, "Thank you for using Ticket Booking system. Payment was successful. Your ticket has been emailed to your email: " + user_email +".")
    
    


    # return back to the home page  
    return render(request, "home.html")

@login_required(login_url='home')
def list_transactions(request):
    # Post request from shopping_cart.html
    
    # current logged in user 
    current_user = request.user

    # get all Transactions of the current user
    transactionList = Transaction.objects.filter(user=current_user.id).order_by('-date')
    # return back to the home page  
    return render(request, "sublime/cart/list_transactions.html",{"transactionList":transactionList})


#view notifications for the user
@update_notifications
@login_required(login_url='home')
def view_notifications(request):
    # current logged in user 
    current_user = request.user
    # get all notifications of the current user
    notificationList = Notification.objects.filter(recepient=current_user.id)
    notificationList.update(read=True)
    request.session['notifications'] = 0
    # return back to the home page  
    return render(request, "notifications/view_notifications.html", {"notifications":notificationList})

