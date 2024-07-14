from django.test import SimpleTestCase
from django.urls import reverse, resolve
from sublime import views

class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, views.home)

    def test_signup_url_resolves(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func, views.authView)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, views.login_view)

    def test_profile_page_url_resolves(self):
        url = reverse('profilePage')
        self.assertEqual(resolve(url).func, views.profile)

    def test_profile_image_change_url_resolves(self):
        url = reverse('profile_image_change')
        self.assertEqual(resolve(url).func, views.profile_image_change)

    def test_list_events_url_resolves(self):
        url = reverse('list_events')
        self.assertEqual(resolve(url).func, views.list_events)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, views.logout_user)
    
        
    # def test_create_event_url_resolves(self):
    #     url = reverse('create_event')
    #     self.assertEqual(resolve(url).func, views.create_event)

    # def test_event_created_confirmation_url_resolves(self):
    #     url = reverse('event_created_confirmation')
    #     self.assertEqual(resolve(url).func, views.event_created_confirmation)

    def test_payment(self):
        url = reverse('payment')
        self.assertEqual(resolve(url).func, views.payment)

    def test_complete_payment(self):
        url = reverse('complete_payment')
        self.assertEqual(resolve(url).func, views.complete_payment)

    def test_list_transactions(self):
        url = reverse('list_transactions')
        self.assertEqual(resolve(url).func, views.list_transactions)
    
    def test_list_events(self):
        url = reverse('list_events')
        self.assertEqual(resolve(url).func, views.list_events)
   
    def test_delete_from_shopping_cart(self):
        url = reverse('delete_from_shopping_cart',kwargs={'cart_id':1})
        self.assertEqual(resolve(url).func, views.delete_from_shopping_cart)
    
    def test_update_shopping_cart(self):
        url = reverse('update_shopping_cart',kwargs={'cart_id':1})
        self.assertEqual(resolve(url).func, views.update_shopping_cart)
    
    def add_to_shopping_cart(self):
        url = reverse('add_to_shopping_cart',kwargs={'event_id':1})
        self.assertEqual(resolve(url).func, views.add_to_shopping_cart)
    
    def test_event_dashboard_url_resolves(self):
        url = reverse('event_dashboard')
        self.assertEqual(resolve(url).func, views.event_dashboard)

    def test_notification_url_resolves(self):
        url = reverse('notifications')
        self.assertEqual(resolve(url).func, views.view_notifications)

# More tests can be added for additional URLs
