from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('userSignup/', views.userSignup, name='userSignup'),
    path('userLogin/', views.userLogin, name='userLogin'),
    path('userlogout/', views.userlogout, name='userlogout'),
    path('userdashboard/', views.userdashboard, name='userdashboard'),
    path('service/', views.services, name='services'),
    path('bookPandit/',views.bookPandit, name='bookPandit'),
    path('popularPuja/', views.popularPuja, name='popularPuja'),
    path('destinationWedding/', views.destinationWedding, name='destinationWedding'),
    path('contactPage/', views.contactPage, name='contactPage'),
    path('searchData/', views.searchData, name='searchData'),
    path('checkoutPage/', views.checkoutPage, name='checkoutPage'),
    path('historyPage/', views.historyPage, name='historyPage'),
    
    #pandit function paths
    path('panditSignup/', views.panditSignup, name='panditSignup'),
    path('panditLogin/', views.panditLogin, name='panditLogin'),
    path('panditlogout/', views.panditlogout, name='panditlogout'),
    path('panditdashboard/', views.panditdashboard, name='panditdashboard'),
    path('panditProfile/', views.panditProfile, name='panditProfile'),
    path('panditHome/', views.panditHome, name='panditHome'),
    path('servicePage/', views.servicePage, name='servicePage'),
    path('servicePage/addService/', views.addService, name='addService'),
    path('servicePage/updateService<str:pk>/', views.updateService, name='updateService'),
    path('events/', views.events, name='events'),
    path('notification/', views.notification, name='notification'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),
    path('help/', views.help, name='help'),
    path('Panditsetting/', views.Panditsetting, name='Panditsetting'),
    path('review/', views.review, name='review'),

]