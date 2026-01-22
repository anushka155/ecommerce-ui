from django.urls import path
from .views import *

urlpatterns = [
    path('',index, name='homepage' ),
    path('product/<slug:slug>/', detail, name = "product-detail"),
    path('order/<slug:slug>/', order, name="order"),
    path('success/<str:uid>', success, name="payment-success"),
    path('failure/<str:uid>', failure, name="failure"),
]