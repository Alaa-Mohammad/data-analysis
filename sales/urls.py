from django.urls import path,re_path
from sales.views import (
    home_view,
    SaleListView,
    SaleDetailView,
    to_csv
) 

app_name = 'sales'

urlpatterns = [
    path('', home_view, name='home'),
    path('sales/', SaleListView.as_view(), name='list'),
    path('sales/<pk>/', SaleDetailView.as_view(), name='detail'),
    path('to_csv/',to_csv,name='to_csv')
]