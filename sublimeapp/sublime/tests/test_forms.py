from django.test import TestCase
from ..forms import CustomUserCreationForm, CustomLoginForm, ReviewForm, EventForm
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from ..forms import CustomUserCreationForm, CustomLoginForm, OrganizerProfileForm, CustomerProfileForm, ReviewForm
from ..models import CustomUser
from django.core.files.uploadedfile import SimpleUploadedFile
from ..forms import AdminProfileForm
import uuid

class TestForms(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for login test
        cls.user = CustomUser.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword'
        )

    def test_custom_login_form_valid(self):
        form_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        form = CustomLoginForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)


    def test_custom_user_creation_form_invalid(self):
        form_data = {
            'username': '',  # Invalid as username is required
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        
    def test_user_creation_form_user_type_choices(self):
        form = CustomUserCreationForm()
        expected_choices = [choice for choice in CustomUser.USER_TYPE_CHOICES if choice[0] != 'admin']
        self.assertEqual(form.fields['user_type'].choices, expected_choices) 
        
    def test_organizer_profile_form_valid(self):
        form_data = {
            'username': 'testuser',
            'first_name': 'UpdatedTest',
            'last_name': 'UpdatedUser',
            'email': 'test@example.com',
            # 'profile_image': SimpleUploadedFile("test_img.jpg", b"file_content", content_type="image/jpeg") if required
        }
        form = OrganizerProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
    
    def test_customer_profile_form_valid(self):
        form_data = {
            'username': 'testuser',
            'first_name': 'UpdatedTest',
            'last_name': 'UpdatedUser',
            'email': 'test@example.com',
            # 'profile_image': SimpleUploadedFile("test_img.jpg", b"file_content", content_type="image/jpeg") if required
        }
        form = CustomerProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        
    def test_admin_profile_form_field_modifications(self):
        admin_user = CustomUser.objects.create_superuser(username='adminuser', email='admin@example.com', password='adminpassword')
        form = AdminProfileForm(instance=admin_user)
        self.assertNotIn('profile_image', form.fields)  # profile_image should be removed

class TestCustomerProfileForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user to be updated
        cls.user = CustomUser.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpassword',
            first_name='Test', last_name='User', user_type='customer'
        )

    def test_profile_form_save(self):
        # Prepare form data with updates
        form_data = {
            'username': 'testuser',  # Typically, username might not change
            'first_name': 'UpdatedFirst',
            'last_name': 'UpdatedLast',
            'email': 'updated@example.com',
            'postal_code': 'A1A 1A1',
            'phone_number': '1234567890',
            # Image field is currently not functional, thus omitted from this test
        }

        # Initialize the form with the existing instance and updated data
        form = CustomerProfileForm(data=form_data, instance=self.user)

        # Validate the form
        self.assertTrue(form.is_valid(), form.errors)

        # Save the form and fetch the updated user instance
        updated_user = form.save()
        updated_user.refresh_from_db()  # Refresh the instance to ensure it reflects updated data from the database

        # Assert changes were saved correctly
        self.assertEqual(updated_user.first_name, form_data['first_name'])
        self.assertEqual(updated_user.last_name, form_data['last_name'])
        self.assertEqual(updated_user.email, form_data['email'])
        self.assertEqual(updated_user.postal_code, form_data['postal_code'])
        self.assertEqual(updated_user.phone_number, form_data['phone_number'])

        # Additional field assertions as needed

class ReviewFormTest(TestCase):
    
    def test_valid_data(self):
        form = ReviewForm(data={
            'title': 'Test title',
            'review_txt': 'Test review text',
            'rating': 5
        })
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = ReviewForm(data={
            'title': 'T',
            'review_txt': 'Test review text',
            'rating': 5
        })
        self.assertFalse(form.is_valid())

        form = ReviewForm(data={
            'title': 'Test title',
            'review_txt': 'T',
            'rating': 5
        })
        self.assertFalse(form.is_valid())

        form = ReviewForm(data={
            'title': 'Test title',
            'review_txt': 'Test review text',
            'rating': 6
        })
        self.assertFalse(form.is_valid())

        form = ReviewForm(data={
            'title': 'Test title',
            'review_txt': 'Test review text',
            'rating': 0
        })
        self.assertFalse(form.is_valid())


    # Add more tests for invalid data, form customization, and form behavior

class ReviewFormTest(TestCase):
    
    def test_valid_data(self):
        form = ReviewForm(data={
            'title': 'Test title',
            'review_txt': 'Test review text',
            'rating': 5
        })
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = ReviewForm(data={
            'title': 'T',
            'review_txt': 'Test review text',
            'rating': 5
        })
        self.assertFalse(form.is_valid())

        form = ReviewForm(data={
            'title': 'Test title',
            'review_txt': 'T',
            'rating': 5
        })
        self.assertFalse(form.is_valid())


        form = ReviewForm(data={
            'title': 'Test title',
            'review_txt': 'Test review text',
            'rating': 6
        })
        self.assertFalse(form.is_valid())

        
        form = ReviewForm(data={
            'title': 'Test title',
            'review_txt': 'Test review text',
            'rating': 0
        })
        self.assertFalse(form.is_valid())
        
        
#Testing Event form for Event creation
class EventFormTests(TestCase):

    def test_event_form_valid_data(self):
        form = EventForm(data={
            'name': 'Test Name',
            'description': 'Test Event',
            'location': 'Test Location',
            'edatetime': '2022-01-01T00:00',
            'price': 10.00,
            'available': 100,
        })
        self.assertTrue(form.is_valid())

    def test_event_form_invalid_data(self):
        form = EventForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)  



    # Add more tests for form customization, and form behavior