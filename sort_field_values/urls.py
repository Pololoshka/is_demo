from django.urls import path

from sort_field_values.views import sort_field_values, form_sort_field_values

urlpatterns = [
    path('field/', sort_field_values, name='sort_field_values'),
    path('field_selection/', form_sort_field_values),
]
