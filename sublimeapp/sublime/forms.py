from datetime import timezone
from django import forms
from django.forms import ModelForm, Textarea, TextInput, Select
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Review, EventRejection
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Event
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

from django.core.validators import RegexValidator

postal_code_regex = RegexValidator(
    regex=r'^[A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d$',
    message="Enter a valid Canadian postal code (e.g., 'K1A 0B1')."
)

# Forms for regular users and organizers
class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'user_type')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # Adjust the user_type field's choices to exclude 'admin'
        user_type_choices = list(self.fields['user_type'].choices)
        self.fields['user_type'].choices = [
            choice for choice in user_type_choices if choice[0] != 'admin'
        ]

class CustomerProfileForm(UserChangeForm):
    postal_code = forms.CharField(
        required=False, 
        validators=[postal_code_regex],
        widget=forms.TextInput(attrs={'placeholder': 'Postal Code'})
    )
    phone_number = forms.CharField(required=False)
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'profile_image', 'postal_code', 'phone_number')

class OrganizerProfileForm(UserChangeForm):
    postal_code = forms.CharField(
        required=False, 
        validators=[postal_code_regex],
        widget=forms.TextInput(attrs={'placeholder': 'Postal Code'})
    )
    phone_number = forms.CharField(required=False)
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'profile_image', 'postal_code', 'phone_number')

class AdminProfileForm(UserChangeForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide profile_image field for admin
        self.fields.pop('profile_image', None)
        # Ensure the password field is rendered correctly
        self.fields['password'].widget = forms.PasswordInput()
        # Only allow superusers to edit the 'is_superuser' field
        if not kwargs.get('initial', {}).get('is_superuser', False):
            self.fields.pop('is_superuser', None)
            
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

#Review form

class ReviewForm(ModelForm):
    # Add empty_label to include the "N/A" option and set required to False
    event = forms.ModelChoiceField(
        queryset=Event.objects.none(),
        required=False,
        empty_label="N/A",
        widget=Select(attrs={'class': 'form-control'}),
        label="Event"
    )

    class Meta:
        model = Review
        fields = ['event', 'title', 'review_txt', 'rating']
        help_texts = {
            'title': None,
            'review_txt': None,
            'rating': None,
        }
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Title Here'}),
            'review_txt': Textarea(attrs={'class': 'form-control', 'placeholder': 'Write Review Here'}),
            'rating': Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        organizer_id = kwargs.pop('organizer_id', None)
        super(ReviewForm, self).__init__(*args, **kwargs)
        if organizer_id:
            # Assuming 'A' stands for 'Approved'
            self.fields['event'].queryset = Event.objects.filter(creator__id=organizer_id, status='A')
        # Optionally, remove the empty label if you don't want '----' in the dropdown
        self.fields['event'].empty_label = None

    def clean_review_txt(self):
        data = self.cleaned_data['review_txt']
        if len(data) < 2:
            raise ValidationError("Review is too short")
        if len(data) > 1000:
            raise ValidationError("Review is too long")
        return data

    def clean_title(self):
        data = self.cleaned_data['title']
        if len(data) < 2:
            raise ValidationError("Your title is too short")
        if len(data) > 100:
            raise ValidationError("Your title is too long")
        return data
#Event Form crucial for creation of the event!
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name','description', 'location', 'edatetime', 'price', 'available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'edatetime': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'available': forms.NumberInput(attrs={'class': 'form-control'}),            
        }

      
        
       

    # Event Rejection Form 
class EventRejectionForm(ModelForm):
    class Meta:
        model = EventRejection 
        fields = ['reason']
        help_texts = {
            'reason': None,
        }    
        widgets = {
            'reason': Textarea(attrs={'class': 'form-control', 'placeholder':'Enter reason for rejecting event here'}),
        }

    def clean_reason(self):
        data = self.cleaned_data['reason']
        if len(data) < 2:
            raise ValidationError(_("Reason provided is too short. Add more helpful details for the organizer."))
        return data