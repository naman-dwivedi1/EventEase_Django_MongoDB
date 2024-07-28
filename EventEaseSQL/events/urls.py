from django.urls import path
from .views import display_events,event,userevent,admin_approve_event,register_event,unregister_event,event_attendees,user_events

urlpatterns = [
    path('event/', event, name='event'),
    path('',display_events,name='display_events'),
    path('userevent/',userevent,name='userevent'),
    path('adminApproval/',admin_approve_event,name='admin_approve_event'),
    path('registerEvent/',register_event,name="register_event"),
    path('unregisterEvent/',unregister_event,name="unregister_event"),
    path('eventAttendees/',event_attendees,name="event_attendees"),
    path('userEvents/',user_events,name="user_events"),
]