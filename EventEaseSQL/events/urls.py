from django.urls import path
from .views import display_events,event,userevent,admin_approve_event,register_event,unregister_event,event_attendees,user_events,fetch_by_venue,fetch_by_title,fetch_by_date

urlpatterns = [
    path('event/', event, name='event'),
    path('',display_events,name='display_events'),
    path('userevent/',userevent,name='userevent'),
    path('adminApproval/',admin_approve_event,name='admin_approve_event'),
    path('registerEvent/',register_event,name="register_event"),
    path('unregisterEvent/',unregister_event,name="unregister_event"),
    path('eventAttendees/',event_attendees,name="event_attendees"),
    path('userEvents/',user_events,name="user_events"),
    path('fetchByVenue/',fetch_by_venue,name="fetch_by_venue"),
    path('fetchByTitle/',fetch_by_title,name="fetch_by_title"),
    path('fetchByDate/',fetch_by_date,name="fetch_by_date"),
]