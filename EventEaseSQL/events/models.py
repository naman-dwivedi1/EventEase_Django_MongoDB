from django.db import models
from authentication.models import User

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    venue = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    organizer = models.IntegerField()
    attendees = models.ManyToManyField(User, related_name='events_attending')

    # def __str__(self):
    #     return self.title

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'venue': self.venue,
            'date': self.date,
            'time': self.time,
            'organizer': self.organizer,
        }

class EventApproval(models.Model):
    event_id = models.IntegerField()
    user_id = models.IntegerField()
    action = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(null=True, blank=True,default=None)

class PendingEvents(models.Model):
    id = models.AutoField(primary_key=True)
    event_id=models.IntegerField(default=0)
    title = models.CharField(max_length=255)
    description = models.TextField()
    venue = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    organizer = models.IntegerField()
    # attendees = models.ManyToManyField(User, related_name='events', blank=True)

    # def __str__(self):
    #     return self.title

    # def to_dict(self):
    #     return {
    #         'id': self.id,
    #         'event_id':self.event_id,
    #         'title': self.title,
    #         'description': self.description,
    #         'venue': self.venue,
    #         'date': self.date,
    #         'time': self.time.strftime('%H:%M:%S'),
    #         'organizer': self.organizer,
    #         # 'attendees': [attendee.username for attendee in self.attendees.all()]
    #     }