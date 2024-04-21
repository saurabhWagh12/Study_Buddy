from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('makerequest/',makeRequest,name='Making Request'),
    path('acceptrequest/<str:id>/',acceptRequest,name='Accept Request'),
    path('getbuddies/',getBuddies,name='Get All Buddies'),
    path('deleterequest/<str:id>',deleteRequest,name='Delete Request'),
    path('getallrequests/',getAllRequests,name='Get All the Requests of a User'),
    path('removebuddy/',removeBuddy,name='Remove Buddy'),

    path('api/register/',RegisterAPI.as_view(),name='Register API'),
    path('api/login/',LoginAPI.as_view(),name='Login API'),
    path('deleteuser/',deleteUser,name='Deleting User'),
    path('getuserdetails/',userDetails,name='Get User Details'),

]