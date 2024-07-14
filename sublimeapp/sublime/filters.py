import django_filters
from django import forms
from django_filters.widgets import RangeWidget
from .models import Event

class EventFilter(django_filters.FilterSet):
    CHOICES = (
        ('date_ascending', 'Date Acending'),
        ('date_descending', 'DateDescending'),
        ('price_ascending', 'Price Ascending'),
        ('price_descending', 'Price Descending')
    )

    description = django_filters.CharFilter(
        lookup_expr='icontains',
        label='',
        widget=forms.TextInput(attrs={'size':20, 'placeholder':'Search Description'})
    )
    location = django_filters.CharFilter(
        lookup_expr='icontains',
        label='',
        widget=forms.TextInput(attrs={'size':20, 'placeholder':'Search Location'})
    )
    price = django_filters.RangeFilter(
        label='Price',
        widget=RangeWidget(attrs={'size':5})
    )
    ordering = django_filters.ChoiceFilter(label='Order by date:',
                                           choices=CHOICES,
                                           method='filter_by_order')
    class Meta:
        model = Event
        fields = ['description',
                  'location',
                  ]
        
    def filter_by_order(self, queryset, name, value):
        if value == 'date_acending':
            expression = 'edatetime'
        elif value == 'date_descending':
            expression = '-edatetime'
        elif value == 'price_ascending':
            expression = 'price'
        else:
            expression = '-price'
        return queryset.order_by(expression)
    