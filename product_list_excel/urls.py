from django.urls import path

from product_list_excel.views import product_in_excel


urlpatterns = [
    path('product_excel/', product_in_excel, name='product_in_excel'),
]
