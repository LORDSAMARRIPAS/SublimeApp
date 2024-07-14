from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.urls import include, path, re_path
from . import views  # Make sure to import your views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('accounts/', include('django.contrib.auth.urls')),  # Django's built-in auth URLs
]

# Appending additional paths
urlpatterns += [
    path('signup/', views.authView, name='signup'),  # Signup page
    path('verify-email/<int:user_id>/', views.verify_code, name='email_verify_code'),
]

urlpatterns += [
    path('login/', views.login_view, name='login'),  # Login page
    path('profilePage/', views.profile, name='profilePage'),  # Profile page
    path('profilePage/image_change/', views.profile_image_change, name='profile_image_change'),
    path('my_tickets/', views.my_tickets, name='my_tickets'),
    path('profile/email_verification_needed/<int:user_id>/', views.email_verification_needed, name='email_verification_needed'),
    
]
urlpatterns += [path('list_events', views.list_events, name="list_events"),
                 path('logout_user', views.logout_user, name="logout"),
                 path('shopping_cart', views.shopping_cart, name="shopping_cart"),
                 path('add_to_shopping_cart/<int:event_id>', views.add_to_shopping_cart, name="add_to_shopping_cart"),
                 path('delete_from_shopping_cart/<int:cart_id>', views.delete_from_shopping_cart, name="delete_from_shopping_cart"),
                 path('update_shopping_cart/<int:cart_id>', views.update_shopping_cart, name="update_shopping_cart"),
                 path('payment', views.payment, name="payment"),
                 path('complete_payment', views.complete_payment, name="complete_payment"),
                 path('list_transactions', views.list_transactions, name="list_transactions"),

]

#Appending review related urls
#urlpatterns += [ path('add_review', views.add_review, name="add_review")]
#urlpatterns += [ path('show_reviews/<int:event_id>', views.show_reviews, name="show_reviews")] 
#urlpatterns += [ path('edit_review/<int:review_id>', views.edit_review, name='edit_review')]

from . import views  # Import the views module

urlpatterns += [
    path('organizers/<int:organizer_id>/add_review/', views.add_review, name='add_review'),
    path('show_reviews/<int:event_id>/', views.show_reviews, name='show_reviews'),
    path('edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('organizers/', views.organizers_list, name='organizers_list'),
    path('organizers/<int:organizer_id>/reviews/', views.single_organizer_reviews, name='single_organizer_reviews'),
]
#Creating events related URLs
urlpatterns += [path('create_events/', views.create_event, name='create_event')]
urlpatterns += [path('event-created-confirmation/', views.event_created_confirmation, name='event_created_confirmation')]  
urlpatterns += [path('edit_event/<int:event_id>', views.edit_event, name='edit_event')]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [re_path(r'admin/event_dashboard/(?P<status>\w+)?', views.event_dashboard, name="event_dashboard")]
urlpatterns += [path('admin/approve_event/<int:event_id>', views.approve_event, name='approve_event')]
urlpatterns += [path('admin/reject_event/<int:event_id>', views.reject_event, name='reject_event')]
urlpatterns += [path('admin/edit_rejection/<int:rejection_id>', views.edit_rejection, name='edit_rejection')]   

#notification related urls
urlpatterns += [path('notifications/', views.view_notifications, name='notifications')]
