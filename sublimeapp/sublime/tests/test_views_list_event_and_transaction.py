from django.test import TestCase, Client
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.urls import reverse
from sublime.models import Event, Cart, Transaction, TransactionItem
from datetime import datetime, timedelta
from django.utils import timezone
User = get_user_model()
from django.test import TestCase, Client
from django.urls import reverse
from ..models import CustomUser, Review
from ..forms import CustomUserCreationForm, CustomLoginForm


#write a test to check login for django admin


#Tests
class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

# Leia's Test for View Events and Transactions
class TestListEventViews(TestCase):
    def setup(self):
        self.client = Client()
       
    ######### Helper methods ######### 
    def set_session_variables(self):
        # set the session variable 'total_items'
        session = self.client.session
        session['total_items']=0
        session.save()
        self.assertEqual(session.has_key('total_items'),True)


    def login_user_type_customer(self):
        # create a user in the User model
        self.user = User.objects.create_user('MoneyPenny', 'mp@007.com', 'Banana1138',first_name='Money',user_type='customer')
        # login the user that was created above
        self.client.login(username='MoneyPenny', password="Banana1138")
        
        self.set_session_variables()
        
        user = auth.get_user(self.client)
        # check if user is authenticated
        self.assertEqual(user.is_authenticated, True) 

    def login_user_type_organizer(self):
        # create a user in the User model
        self.user = User.objects.create_user('JamesBond', 'jb@007.com', 'Banana1138',first_name='James', user_type='organizer' )
        # login the user that was created above
        self.client.login(username='JamesBond', password="Banana1138")
        
        self.set_session_variables()

        user = auth.get_user(self.client)
        # check if user is authenticated
        self.assertEqual(user.is_authenticated, True) 
       

    def create_event(self):  
        edatetime = datetime.now()
        #aware_datetime = timezone.make_aware(edatetime, timezone=timezone.get_current_timezone())
        fdate = datetime.now() + timedelta(days=1)
        aware_datetime = timezone.make_aware(fdate)
        self.event = Event.objects.create(creator=self.user,
                             name='EventName1',
                             description='EventDescription1',
                             location='Location1',
                             edatetime=aware_datetime,
                             available=100,
                             price=15.30)

    def create_event_approved(self):  
        edatetime = datetime.now()
        #aware_datetime = timezone.make_aware(edatetime, timezone=timezone.get_current_timezone())
        fdate = datetime.now() + timedelta(days=1)
        aware_datetime = timezone.make_aware(fdate)
        self.event = Event.objects.create(creator=self.user,
                             name='EventName2',
                             description='EventDescription2',
                             location='Location2',
                             edatetime=aware_datetime,
                             available=100,
                             price=15.30,
                             status='A')   
          
    def add_event_to_cart(self):  
        self.cart = Cart.objects.create(user_id=self.user,
                            event_id=self.event,
                            quantity=1)

 
    # test list events by login in as organizer and create an event
    def test_list_events(self):
        #login first
        self.login_user_type_organizer()

        self.set_session_variables()
        # create a row in the Event model
        self.create_event()

        eventList = Event.objects.all()
        response = self.client.get(reverse("list_events"),{'eventList':eventList})
        self.assertEqual(response.status_code, 200)
        
        self.assertTemplateUsed(response, 'registration/list_events.html')

        # test the queryset to see if the event name is correct
        qs = Event.objects.all()
        self.assertEqual(qs[0].name, 'EventName1')

    # Login as organizer, create an event, add event to the cart  
    def test_add_event_to_cart(self):
        #login first
        self.login_user_type_organizer()
        self.set_session_variables()
       
        # create a row in the Event model
        self.create_event()

        eventList = Event.objects.all()
        response = self.client.post(reverse("add_to_shopping_cart", kwargs={'event_id':eventList[0].pk}))
        # Redirect to shopping_cart so status code is 302
        self.assertEqual(response.status_code, 302)

        # Check the Cart table to see if there is a row for the event
        qs = Cart.objects.filter(user_id= self.user).all()
        # one item in the cart
        self.assertEqual(qs.count(),1)
        # name of event is EventName1
        self.assertEqual(qs[0].event_id.name, 'EventName1')

    # Login as organizer, create an event, add event to the cart twice
    def test_add_same_event_twice_to_cart(self):
        #login first
        self.login_user_type_organizer()
        self.set_session_variables()
       
        # create a row in the Event model
        self.create_event()

        eventList = Event.objects.all()
        response = self.client.post(reverse("add_to_shopping_cart", kwargs={'event_id':eventList[0].pk}))
        # Redirect to shopping_cart so status code is 302
        self.assertEqual(response.status_code, 302)

        # Check the Cart table to see if there is a row for the event
        qs = Cart.objects.filter(user_id= self.user).all()
        # one item in the cart
        self.assertEqual(qs.count(),1)
        # name of event is EventName1
        self.assertEqual(qs[0].event_id.name, 'EventName1')

        response = self.client.post(reverse("add_to_shopping_cart", kwargs={'event_id':eventList[0].pk}))
        # Redirect to shopping_cart so status code is 302
        self.assertEqual(response.status_code, 302)

        # Check the Cart table to see if there is a row for the event
        qs = Cart.objects.filter(user_id= self.user).all()
        # one item in the cart, because we added same event to cart
        self.assertEqual(qs.count(),1)
        # name of event is EventName1
        self.assertEqual(qs[0].event_id.name, 'EventName1')
        # check if the quantity is 2
        self.assertEqual(qs[0].quantity, 2)

    # Login as organizer, create an event, add event to cart
    # delete event from cart
    def test_delete_item_from_cart(self):
        #login first
        self.login_user_type_organizer()
        self.set_session_variables()
       
        # create a row in the Event model
        self.create_event()

        eventList = Event.objects.all()
        response = self.client.post(reverse("add_to_shopping_cart", kwargs={'event_id':eventList[0].pk}))
        # Redirect to shopping_cart so status code is 302
        self.assertEqual(response.status_code, 302)

        # Check the Cart table to see if there is a row for the event
        qs = Cart.objects.filter(user_id= self.user).all()
        # one item in the cart
        self.assertEqual(qs.count(),1)
        # name of event is EventName1
        self.assertEqual(qs[0].event_id.name, 'EventName1')

        # There is one item in the cart, lets delete this item
        response = self.client.post(reverse("delete_from_shopping_cart", kwargs={'cart_id':qs[0].pk}))
        # Redirect to shopping_cart so status code is 302
        self.assertEqual(response.status_code, 302)

        # Check the Cart table empty
        qs = Cart.objects.filter(user_id= self.user).all()
        # There should be 0 items in the cart
        self.assertEqual(qs.count(), 0)
        
    # Login as organizer, create an event, add event to cart
    # update event quantity in cart
    def test_update_item_quantity_in_cart(self):
        #login first
        self.login_user_type_organizer()
        self.set_session_variables()
       
        # create a row in the Event model
        self.create_event()

        eventList = Event.objects.all()
        response = self.client.post(reverse("add_to_shopping_cart", 
                                            kwargs={'event_id':eventList[0].pk}),
                                            )
        # Redirect to shopping_cart so status code is 302
        self.assertEqual(response.status_code, 302)

        # Check the Cart table to see if there is a row for the event
        qs = Cart.objects.filter(user_id= self.user).all()
        # one item in the cart
        self.assertEqual(qs.count(),1)
        # name of event is EventName1
        self.assertEqual(qs[0].event_id.name, 'EventName1')

        # There is one item in the cart, lets delete this item
        response = self.client.post(reverse("update_shopping_cart", 
                                            kwargs={'cart_id':qs[0].pk}),
                                            {'quantity':5})
        # Redirect to shopping_cart so status code is 302
        self.assertEqual(response.status_code, 302)

        # Check the Cart table empty
        qs = Cart.objects.filter(user_id= self.user).all()
        # The item should have the quantity of 5
        self.assertEqual(qs[0].quantity, 5)
        

    # Login as organizer, create an event, add event to cart,
    # complete the transaction payment
    def test_complete_payment(self):
        #login first
        self.login_user_type_organizer()
        self.set_session_variables()
       
        # create a row in the Event model
        self.create_event()

        eventList = Event.objects.all()
        response = self.client.post(reverse("add_to_shopping_cart", 
                                            kwargs={'event_id':eventList[0].pk}),
                                            )
        # Redirect to shopping_cart so status code is 302
        self.assertEqual(response.status_code, 302)

        # Check the Cart table to see if there is a row for the event
        qs = Cart.objects.filter(user_id= self.user).all()
        # one item in the cart
        self.assertEqual(qs.count(),1)
        # name of event is EventName1
        self.assertEqual(qs[0].event_id.name, 'EventName1')

        # There is one item in the cart, lets delete this item
        response = self.client.post(reverse("complete_payment"))
        # Render to home so status code is 200
        self.assertEqual(response.status_code, 200)

        # Check the Cart table empty after transaction is completed
        qs = Cart.objects.filter(user_id= self.user).all()
        # There should be 0 items in the cart
        self.assertEqual(qs.count(), 0)

        # See if transaction has been created
        qs = Transaction.objects.filter(user = self.user).all()
        # There should be one row int the Transaction table
        self.assertEqual(qs.count(), 1)

        # See if the TrasactionItem table has been created
        self.assertEqual(qs[0].items.count(), 1)
        # get the TransactionItem from the Transaction table
        qs_item = qs[0].items.get_queryset()
         # The event purchased should be EventName1
        self.assertEqual(qs_item[0].event.name, 'EventName1')
 
        
    # test list events by login in a organizer and create an event
    # that is pending, then logout.  Login as customer and check if
    # eventList is empty
    def test_list_event_pending_as_customer(self):
        #login first
        self.login_user_type_organizer()

        self.set_session_variables()
        # create a row in the Event model
        self.create_event()

        # logout organizer
        response = self.client.get(reverse("logout"))
        # Redirect to home after logout. Expect code 302
        self.assertEqual(response.status_code, 302)

        # login as customer
        self.login_user_type_customer()

        eventList = Event.objects.all()

        response = self.client.get(reverse("list_events"))
        self.assertEqual(response.status_code, 200)
        
        self.assertTemplateUsed(response, 'registration/list_events.html')

        # check if eventList is empty
        self.assertEqual(response.context['eventList'].count(), 0)

       
    # test list events by login in a organizer and create an event
    # that is approved, then logout.  Login as customer and check if
    # eventList has count of 1
    def test_list_event_approved_as_customer(self):
        #login first
        self.login_user_type_organizer()

        self.set_session_variables()
        # create a row in the Event model
        self.create_event_approved()

        # logout organizer
        response = self.client.get(reverse("logout"))
        # Redirect to home after logout. Expect code 302
        self.assertEqual(response.status_code, 302)

        # login as customer
        self.login_user_type_customer()

        eventList = Event.objects.all()

        response = self.client.get(reverse("list_events"))
        self.assertEqual(response.status_code, 200)
        
        self.assertTemplateUsed(response, 'registration/list_events.html')

        # check if eventList is empty
        self.assertEqual(response.context['eventList'].count(), 1)

    # test list events by login in a organizer and create an event
    # that is approved, then logout.  Login as customer and check if
    # eventList has count of 1
    def test_list_event_approved_as_customer(self):
        #login first
        self.login_user_type_organizer()

        self.set_session_variables()
        # create a row in the Event model
        self.create_event_approved()

        # logout organizer
        response = self.client.get(reverse("logout"))
        # Redirect to home after logout. Expect code 302
        self.assertEqual(response.status_code, 302)

        # login as customer
        self.login_user_type_customer()

        eventList = Event.objects.all()

        response = self.client.get(reverse("list_events"))
        self.assertEqual(response.status_code, 200)
        
        self.assertTemplateUsed(response, 'registration/list_events.html')

        # check if eventList is empty
        self.assertEqual(response.context['eventList'].count(), 1)

    