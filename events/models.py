from db_connection import db
from datetime import datetime

event_collection=db['events']
approval_collection=db['approvals']
pending_events_collection=db['pending_events']

class Event:
    def __init__(self, title, description, venue, date, time, organizer, attendees=None, approved=False):
        self.title = title
        self.description = description
        self.venue = venue
        if isinstance(date, str):
            self.date = date
        else:
            self.date = date.strftime('%Y-%m-%d')
        if isinstance(time, str):
            self.time = time
        else:
            self.time = time.strftime('%H:%M:%S')
        self.organizer = organizer
        self.attendees = attendees if attendees is not None else []
        self.approved=approved
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "venue": self.venue,
            "date": self.date,
            "time": self.time,
            "organizer": self.organizer,
            "attendees": self.attendees,
            "approved": self.approved,
            "created_at": self.created_at,
        }
        
class EventApproval:
    def __init__(self, event_id, user_id, action, approved=None):
        self.event_id = event_id
        self.user_id = user_id
        self.action = action
        self.approved = approved
        self.requested_at = datetime.utcnow()

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "user_id": self.user_id,
            "action": self.action,
            "approved": self.approved,
            "requested_at": self.requested_at
        }