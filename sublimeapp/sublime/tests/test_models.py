from django.test import TestCase
from ..models import CustomUser, Event, Cart, Transaction, TransactionItem
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime
CustomUser = get_user_model()
import pytest

class CustomUserModelTest(TestCase):

    def test_user_type_organizer(self):
        organizer_user = CustomUser.objects.create_user(username='organizer', user_type='organizer')
        self.assertTrue(organizer_user.is_organizer)
        self.assertFalse(organizer_user.is_customer)

    def test_user_type_customer(self):
        customer_user = CustomUser.objects.create_user(username='customer', user_type='customer')
        self.assertTrue(customer_user.is_customer)
        self.assertFalse(customer_user.is_organizer)
        
    def test_superuser_type_admin(self):
        admin_user = CustomUser.objects.create_superuser(username='adminuser', email='admin@example.com', password='password')
        self.assertTrue(admin_user.is_admin)
        self.assertEqual(admin_user.user_type, 'admin')
        
    def test_email_verification_logic(self):
        user = CustomUser.objects.create_user(username='testuser', user_type='customer')
        user.set_verification_code()  # Set a code
        # Test with correct code within expiry
        valid, message = user.verify_email(user.email_verification_code)
        self.assertTrue(valid)
        self.assertEqual(message, "Email verified successfully")
        # Test expired code (you might need to mock `timezone.now()` to simulate expiry)
        # Test incorrect code


pytestmark = pytest.mark.django_db
class TestReviewModel:
    def test_str_return(self, review_factory):
        review = review_factory()
        assert review.__str__() == review.title
        

#Test For Eventmodel
class EventModelTests(TestCase):

    def test_event_creation(self):
        user = get_user_model().objects.create_user(username='testuser', password='12345')
        event = Event.objects.create(
            creator=user,
            name='Test Name',
            description='Test Event',
            location='Test Location',
            edatetime=timezone.now(),
            price=10.00,
            available=100,
            status='pending'
        )
        self.assertEqual(event.creator, user)
        self.assertTrue(event.is_available())
        
#Test For CartModel
class CartModelTests(TestCase):

    def test_event_creation(self):
        user = get_user_model().objects.create_user(username='testuser', password='12345')
        event = Event.objects.create(
            creator=user,
            name='Test Name',
            description='Test Event',
            location='Test Location',
            edatetime=timezone.now(),
            price=10.00,
            available=100,
            status='pending'
        )
        cart = Cart.objects.create(
            quantity=1,
            user_id=user,
            event_id=event
        )
        self.assertEqual(cart.user_id, user)
        self.assertEqual(cart.event_id,event)
        self.assertTrue(cart.get_total_item_price)
        self.assertTrue(cart.quantity_available)
        
#Test For TransactionModel
class TransactionModelTests(TestCase):

    def test_event_creation(self):
        user = get_user_model().objects.create_user(username='testuser', password='12345')
        event = Event.objects.create(
            creator=user,
            name='Test Name',
            description='Test Event',
            location='Test Location',
            edatetime=timezone.now(),
            price=10.00,
            available=100,
            status='pending'
        )
        transaction_item = TransactionItem.objects.create(
            quantity=1,
            price=10,
            user=user,
            event=event
        )
        transaction = Transaction.objects.create(
            date=datetime.now,
            total_price=10,
            user=user,
            completed=False,
        )

        transaction.items.add(transaction_item)
        self.assertEqual(transaction.user, user)
        qs = transaction.items.get_queryset()
        self.assertEqual(qs[0],transaction_item)
        
        