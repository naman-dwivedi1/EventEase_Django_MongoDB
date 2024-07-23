from django.urls import path
from .views import event,display_events,userevent,admin_approve_event,register_event

urlpatterns = [
    path('event/', event, name='event'),
    path('',display_events,name='display_events'),
    path('userevent/',userevent,name='userevent'),
    path('adminApproval/',admin_approve_event,name='admin_approve_event'),
    path('registerEvent/',register_event,name="register_event")
]