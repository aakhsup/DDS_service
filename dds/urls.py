from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('types/', views.types_list, name='types_list'),
    path('categories/', views.categories_list, name='categories_list'),
    path('transactions/', views.transactions_list, name='transactions_list'),
    path('transactions/new/', views.transaction_create, name='transaction_create'),
]
