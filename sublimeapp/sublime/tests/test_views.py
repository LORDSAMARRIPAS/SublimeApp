
from django.test import TestCase, Client
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.urls import reverse
from sublime.models import Event, Cart
from datetime import datetime
from django.utils import timezone
from django.test import TestCase, Client  # Add this line to import the missing module
User = get_user_model()
from django.test import TestCase, Client
from django.urls import reverse
from ..models import CustomUser, Review,Event, Cart ,Notification
from ..forms import CustomUserCreationForm, CustomLoginForm
from django.utils.timezone import now
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model
from datetime import timedelta
from ..forms import CustomerProfileForm

class ViewsShanTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        
        
    def set_session_variables(self):
        # set the session variable 'total_items'
        session = self.client.session
        session['total_items']=0
        session.save()
        self.assertEqual(session.has_key('total_items'),True)
  
       
    # test admin login with superuser
    def test_admin_superuser(self):
         test_user2 = User.objects.create_superuser(username='testuser2', password='1X<ISRUkw+tuK')
         test_user2.save()
         response = self.client.post("/admin/", {"username": "testuser2", "password": "1X<ISRUkw+tuK"}, follow=True)
         self.assertEqual(response.status_code, 200)  #check if the response is 200
         # --todo-- self.assertTemplateUsed(response, "admin/index.html")  #check if the template used is admin/index.html
    
    #test create user and login
    def create_user_and_login(self):
        self.user1 = User.objects.create_user('NinaSimone', 'nn@nn.com', '1X<ISRUkw+tuK', first_name='Nina')
        self.client.login(username='NinaSimone', password='1X<ISRUkw+tuK')

    def create_superuser_and_login(self):
        test_user2 = User.objects.create_superuser(username='admin2', password='1X<ISRUkw+tuK')
        test_user2.save()
        self.client.login(username = "admin2", password = "1X<ISRUkw+tuK")

    #test show reviews
    def test_show_reviews(self):        
        response = self.client.get(reverse('show_reviews', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/show_reviews.html')

    #test add review
    def test_add_review(self):
        self.create_user_and_login()

        # when login in with self.client.login, you need to call the function below to
        # set the session variable 'total_items'
        self.set_session_variables()

        #have user add a review      
        response = self.client.post(reverse('add_review'), {'title': 'Test Review Title', 'review_txt': 'Test review text', 'rating': 5, 'event_id': 1})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('show_reviews', args=[1]))       
     
    #test edit review
    def test_edit_review(self):          
        self.test_add_review()      
        review = Review.objects.get(title='Test Review Title')        
        # go to the edit review page
        response = self.client.get(reverse('edit_review', args=[review.review_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/edit_review.html')
        # edit the review
        response = self.client.post(reverse('edit_review', args=[review.review_id]), {'title': 'Test Review Title Edited', 'review_txt': 'Test review text edited', 'rating': 4})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('show_reviews', args=[1]))
        # check if the review was edited
        review = Review.objects.get(title='Test Review Title Edited')
        self.assertEqual(review.review_txt, 'Test review text edited')

    def test_add_review(self): 
        response = self.client.post(reverse('add_review'), {'title': 'Test Review Title', 'review_txt': 'Test Review Content', 'rating': 5})    
        self.assertEqual(response.status_code, 302)    
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.get(title='Test Review Title').title, 'Test Review Title')

    #test edit review
    def test_edit_review(self):
        #create review
        self.test_add_review()
        #create another user
        self.user2 = User.objects.create_user('NinaSimone2', 'nn2@nn2.com', '1P<ISRUkw+tuK', first_name='Nina2')
        self.client.login(username='NinaSimone2', password='1P<ISRUkw+tuK')
        
        # when login in with self.client.login, you need to call the function below to
        # set the session variable 'total_items'
        self.set_session_variables()


        # select the review
        review = Review.objects.get(title='Test Review Title')
        # go to the edit review page
        response = self.client.get(reverse('edit_review', args=[review.review_id]))
        self.assertEqual(response.status_code, 403)

    #test event dashboard not accessible by non-superuser
    def test_event_dashboard_fail(self):
        self.create_user_and_login()  

        # when login in with self.client.login, you need to call the function below to
        # set the session variable 'total_items'
        self.set_session_variables() 

        response = self.client.get(reverse('event_dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_event_dashboard(self):
        self.create_superuser_and_login()

        # when login in with self.client.login, you need to call the function below to
        # set the session variable 'total_items'
        self.set_session_variables()

        response = self.client.get(reverse('event_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/event_dashboard.html')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertEqual(response.status_code, 200)
        # edit the review
        response = self.client.post(reverse('edit_review', args=[response.review_id]), {'title': 'Test Review Title Edited', 'review_txt': 'Test Review Content Edited', 'rating': 4})
        self.assertEqual(response.status_code, 302)
        # check if the review was edited
        self.assertEqual(Review.objects.get(title='Test Review Title Edited').review_txt, 'Test Review Content Edited')
        


        
        
        
    #tear down
    def tearDown(self):
        self.user.delete()
        Review.objects.all().delete()


#tests for Review Views
class TestReviewViews(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user('TestUser', 'test@example.com', 'testpassword')
        self.client.login(username='TestUser', password='testpassword')
        self.organizer = CustomUser.objects.create_user('Organizer', 'organizer@example.com', 'orgpassword', user_type='organizer')
        self.event = Event.objects.create(
            name="Sample Event",
            description="Event Description",
            location="Test Location",
            edatetime=timezone.now(),
            price=10.00,
            available=100,
            creator=self.organizer,
            status='A'
        )
        self.review = Review.objects.create(
            title="Great Event",
            review_txt="It was an amazing experience.",
            rating=5,
            event=self.event,
            user_id=self.user,
            date=timezone.now()
        )
                                    
    def test_add_review(self):
        # Post data to add a review
        response = self.client.post(reverse('add_review', kwargs={'organizer_id': self.organizer.id}), {
            'title': 'Test Review Title',
            'review_txt': 'Test review text',
            'rating': 5,
            'event': self.event.id  # Ensure this field name matches your form's expected input
        })
        # Assert redirection happens to the correct URL
        self.assertRedirects(response, reverse('single_organizer_reviews', args=[self.organizer.id]))
        # Assert the review was actually added
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.first().title, 'Test Review Title')
        
    #test show reviews
    def test_show_reviews(self):        
        response = self.client.get(reverse('show_reviews', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/show_reviews.html')

    def test_edit_review(self):
        response = self.client.get(reverse('edit_review', args=[self.review.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/edit_review.html')
        response = self.client.post(reverse('edit_review', args=[self.review.id]), {
            'title': 'Test Review Title Edited',
            'review_txt': 'Test review text edited',
            'rating': 4,
            'event': self.event.id
        })
        self.assertEqual(response.status_code, 302)
        updated_review = Review.objects.get(id=self.review.id)
        self.assertEqual(updated_review.title, 'Test Review Title Edited')

    def test_edit_review_restrict(self):
        # Create another user who should not have permission to edit the review
        user2 = CustomUser.objects.create_user('NinaSimone2', 'nn2@nn2.com', 'password2')
        self.client.login(username='NinaSimone2', password='password2')
        response = self.client.get(reverse('edit_review', args=[self.review.id]))
        self.assertEqual(response.status_code, 403)

class CustomUserTests(TestCase):

    def setUp(self):
        # Initialize users for testing
        self.customer = CustomUser.objects.create_user(username='customer', email='customer@example.com', password='password', user_type='customer')
        self.organizer = CustomUser.objects.create_user(username='organizer', email='organizer@example.com', password='password', user_type='organizer')
        self.admin = CustomUser.objects.create_superuser(username='admin', email='admin@example.com', password='password')

    def login_and_set_session(self, username, password):
        login_url = reverse('login')  
        login_data = {'username': username, 'password': password}
        response = self.client.post(login_url, login_data)
        # Ensure 'total_items' is set for the session after login
        self.client.session['total_items'] = 0
        self.client.session.save()
        return response

    def test_user_creation(self):
        self.assertEqual(self.customer.user_type, 'customer')
        self.assertEqual(self.organizer.user_type, 'organizer')
        self.assertTrue(self.admin.is_superuser)

    def test_event_creation(self):
        self.login_and_set_session('organizer', 'password')
        response = self.client.post(reverse('create_event'), {
            'name': 'Test Event',
            'description': 'Test Description',
            'location': 'Test Location',
            'edatetime': timezone.now() + timedelta(days=1),
            'price': '20.00',
            'available': '50',
        })
        
        self.assertRedirects(response, reverse('event_created_confirmation'))
        event = Event.objects.get(name='Test Event')
        self.assertEqual(event.creator, self.organizer)
        self.assertEqual(event.status, 'P')


    def test_profile_update_invalid_inputs(self):
        self.client.login(username='customer', password='password')
        # Define a list of invalid field inputs
        invalid_inputs = {
            'postal_code': ('InvalidCode', "Enter a valid Canadian postal code"),  # Invalid postal code and expected error
            'email': ('invalidemail', "Enter a valid email address"),  # Invalid email format and expected error
            # Add other fields and invalid inputs as needed, with expected error messages
        }

        for field, (invalid_value, expected_error) in invalid_inputs.items():
            form_data = {
                'username': self.customer.username,
                'first_name': self.customer.first_name,
                'last_name': self.customer.last_name,
                'email': self.customer.email if field != 'email' else invalid_value,
                'postal_code': self.customer.postal_code if field != 'postal_code' else invalid_value,
                # Ensure other fields are filled with valid data
            }
            form = CustomerProfileForm(data=form_data, instance=self.customer)
            self.assertFalse(form.is_valid(), f"Form should be invalid for incorrect {field}")
            self.assertIn(field, form.errors, f"{field} should have errors for invalid input")

            # Assert that the specific expected error message is in the errors for this field
            error_messages = form.errors[field]
            self.assertTrue(any(expected_error in error for error in error_messages), f"Expected error message not found for {field}")

            
    def test_organizer_event_visibility(self):
        self.login_and_set_session('organizer', 'password')
        Event.objects.create(
            name="Organizer's Event",
            description="An event by the organizer",
            location="Event Location",  # Replace with actual location
            edatetime=now(),  # Or any future date and time
            price="10.00",  # Or any valid decimal value
            available=100,  # Total available tickets
            sold=0,  # Default is 0, but explicitly setting for clarity
            verified=False,  # Assuming not verified initially; adjust as necessary
            creator=self.organizer,  # Associating this event with the organizer created in setUp
            status='A',  # Explicitly setting status, though 'P' is default
        )

        response = self.client.get(reverse('my_tickets'))
        self.assertEqual(len(response.context['events']), 1)
        self.assertEqual(response.context['events'][0].creator, self.organizer)

    def test_access_control(self):
        self.login_and_set_session('customer', 'password')
        response_customer = self.client.get(reverse('create_event'))
        self.assertNotEqual(response_customer.status_code, 200)
        self.login_and_set_session('organizer', 'password')
        response_organizer = self.client.get(reverse('create_event'))
        self.assertEqual(response_organizer.status_code, 200)
        self.login_and_set_session('admin', 'password')
        response_admin = self.client.get(reverse('event_dashboard'))
        self.assertEqual(response_admin.status_code, 200)

    def test_login_with_empty_cart(self):
        response = self.login_and_set_session('customer', 'password')
        # Check if 'total_items' in session is correctly set to 0
        self.assertIn('total_items', self.client.session, "The 'total_items' key should be in the session after login.")
        self.assertEqual(self.client.session['total_items'], 0)
        # Optionally, check if the response redirects to the expected page after login
        profile_page_url = reverse('profilePage')
        self.assertRedirects(response, profile_page_url, msg_prefix="Login should redirect to the profile page.")
        
class TestListEventViews(TestCase):
    def setup(self):
        self.client = Client()
       
    ######### Helper methods ######### 
    def login_user_type_customer(self):
        # create a user in the User model
        self.user = User.objects.create_user('JamesBond', 'jb@007.com', 'Banana1138',first_name='James',user_type='customer')
        # login the user that was created above
        self.client.login(username='JamesBond', password="Banana1138")
        
        user = auth.get_user(self.client)
        # check if user is authenticated
        self.assertEqual(user.is_authenticated, True) 
    def login_user_type_organizer(self):
        # create a user in the User model
        self.user = User.objects.create_user('JamesBond', 'jb@007.com', 'Banana1138',first_name='James', user_type='organizer' )
        # login the user that was created above
        self.client.login(username='JamesBond', password="Banana1138")
        
        user = auth.get_user(self.client)
        # check if user is authenticated
        self.assertEqual(user.is_authenticated, True) 
       
    def create_event(self):  
        edatetime = datetime.now()
        aware_datetime = timezone.make_aware(edatetime, timezone=timezone.get_current_timezone())
        self.event = Event.objects.create(creator=self.user,
                             name='EventName1',
                             description='EventDescription1',
                             location='Location1',
                             edatetime=aware_datetime,
                             available=100,
                             price=15.30)
        
    def add_event_to_cart(self):  
        self.cart = Cart.objects.create(user_id=self.user,
                            event_id=self.event,
                            quantity=1)
 
# test list events by login in as organizer
    def test_list_events(self):
        #login first
        self.login_user_type_organizer()
        # create a row in the Event model
        self.create_event()
        eventList = Event.objects.all()
        response = self.client.get(reverse("list_events"),{'eventList':eventList})
        self.assertEqual(response.status_code, 200)
        
        self.assertTemplateUsed(response, 'sublime/login.html')
        self.assertIsInstance(response.context['form'], CustomLoginForm)
    def test_login_view_post_success(self):
        user = User.objects.create_user('testuser', 'nn@nn.com', 'testpassord', first_name='Nina')
        
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        # since we are calling the login form we do not need to set the session
        # variable 'total_items'. 
        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, 302)
        # Check if user is authenticated
        self.assertTrue(user.is_authenticated)

        self.assertEqual(user.first_name,'Nina')
        self.assertEqual(user.user_type,'customer')

    def test_signup_form(self):
        response = self.client.post(reverse('signup'), {
            'username': 'testuser2',
            'email': 'testuser2@example.com',
            'password1': 'Testpassword1234',
            'password2': 'Testpassword1234',
            'user_type': 'customer',
        })

        self.assertEqual(response.status_code, 302)  # Assuming redirect after successful signup
        self.assertTrue(User.objects.filter(username='testuser2').exists())
        
    def tearDown(self):
        # Cleanup code to delete users created during tests
        User.objects.all().delete()
        Event.objects.all().delete()
    def test_profile_access_after_login(self):
        # login as a customer
        self.login_as_customer()
      
        # when login in with self.client.login, you need to call the function below to
        # set the session variable 'total_items'
        self.set_session_variables()

        response = self.client.get(reverse('profilePage'))
        # Correction: response.status_code instead of response.status_id
        # --todo-- self.assertEqual(response.status_code, 200)
        # --tod0-- self.assertTemplateUsed(response, 'registration/profilePage.html')

    


#Tests for Event creation and confirmation
class CreateEventViewTests(TestCase):    

    def setUp(self):
        self.client = Client()
       
        # user_type is an organizer
        self.user = get_user_model().objects.create_user(username='testuser', password='12345', user_type='organizer')
        login_data = {
            'username': 'testuser',
            'password': '12345'
        }
        # since we are calling the login form we do not need to set the session
        # variable 'total_items'. 
        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, 302)
        # Check if user is authenticated
        self.assertTrue(self.user.is_authenticated)

        
    def test_create_event_view_get(self):
        response = self.client.get(reverse('create_event'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/create_events.html')

    def test_create_event_view_post(self):
        response = self.client.post(reverse('create_event'), data={
            'name': 'New Name',
            'description': 'New Event',
            'location': 'New Location',
            'edatetime': '2022-01-01T00:00',
            'price': 20.00,
            'available': 50,
        })
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertRedirects(response, reverse('event_created_confirmation'))
        
        
class EventCreatedConfirmationViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        response = self.client.get("/sublime/")
        self.assertEqual(response.status_code, 200)

        # user_type is an organizer
        self.user = get_user_model().objects.create_user(username='testuser', password='12345', user_type='organizer')
        self.client.login(username='testuser', password='12345')

        session = self.client.session
        session['total_items']=0
        session.save()
        self.assertEqual(session.has_key('total_items'),True)
  
 
    def test_create_event_view_post(self):
        response = self.client.post(reverse('create_event'), data={
            'name': 'New Name',
            'description': 'New Event',
            'location': 'New Location',
            'edatetime': '2022-01-01T00:00',
            'price': 20.00,
            'available': 50,
        })
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertRedirects(response, reverse('event_created_confirmation'))
        
        

    def test_event_created_confirmation_view(self):
        self.test_create_event_view_post()

        eventList = Event.objects.all()  # Define the "eventList" variable by retrieving all the Event objects
        response = self.client.get(reverse('event_created_confirmation'))
        self.assertEqual(response.status_code, 200)

        # test the template used
        self.assertTemplateUsed(response, 'events/event_created_confirmation.html')
        
        # test only one event in the list
        self.assertEqual(eventList.count(),1) 
        # make sure the first event name is "New Name"
        self.assertEqual(eventList[0].name, "New Name")

    
        # test to check if the cart is empty after delete
        cart = Cart.objects.filter(user_id=self.user.pk)
        self.assertEqual(cart[0].quantity,3) 
    


class EventDashboardViewTests(TestCase):     
        
    #create admin
    def adminSetUp(self):
        self.user = User.objects.create_superuser(username='admin', password='12345')
        self.client.login(username='admin', password='12345')
   
        #test event dashboard accessible by superuser
    def test_event_dashboard(self):
        self.adminSetUp()
        response = self.client.get(reverse('event_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/event_dashboard.html')
   

    def test_event_dashboard_view(self):
        self.adminSetUp()
        response = self.client.get(reverse('event_dashboard'))
        self.assertEqual(response.status_code, 200)
        

    def test_approve_event_view(self):
        self.adminSetUp()
        testuser = User.objects.create_user(username='testuser', password='12345')
        event = Event.objects.create(creator=testuser, name='EventName1', description='EventDescription1', location='Location1', edatetime=timezone.now(), available=100, price=15.30)
        response = self.client.get(reverse('approve_event', args=[event.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Event.objects.get(pk=event.pk).status, 'A')

    def test_reject_event_view(self):
        self.adminSetUp()
        testuser = User.objects.create_user(username='testuser', password='12345')
        event = Event.objects.create(creator=testuser, name='EventName1', description='EventDescription1', location='Location1', edatetime=timezone.now(), available=100, price=15.30)
        response = self.client.get(reverse('reject_event', args=[event.pk]))
        self.assertEqual(response.status_code, 200)        
        self.client.post(reverse('reject_event', args=[event.pk]), {'reason': 'Test rejection reason'})
        self.assertEqual(Event.objects.get(pk=event.pk).status, 'R')  

    def tearDown(self):
         self.user.delete()
         Event.objects.all().delete()

  
class NotificationsViewTest (TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_notification_view(self):
        response = self.client.get(reverse('notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notifications/view_notifications.html')

    def test_notification_count_view(self):
        notification = Notification.objects.create(recepient=self.user, message='Test Notification', read=False)       
        #check if notification is unread
        self.assertEqual(Notification.objects.get(pk=notification.pk).read, False)
        #count number of notifications for user
        self.assertEqual(Notification.objects.filter(recepient=self.user).count(), 1)        
       

    def tearDown(self):
        self.user.delete()
        Notification.objects.all().delete()
