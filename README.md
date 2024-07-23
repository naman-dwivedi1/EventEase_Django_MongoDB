# Event Management System

The Event Management System is a Django-based web application that utilizes MongoDB for database management. This application supports two types of users: USER and ADMIN, each with distinct roles and permissions.

## Features

### ADMIN Capabilities:
- **List Events:** View all events categorized as upcoming or past.
- **Create Events:** Directly add new events to the system.
- **Read Events:** View detailed information about each event.
- **Update Events:** Modify details of existing events.
- **Delete Events:** Remove events from the system.
- **Approve Requests:** Review and approve or reject event requests made by USERs (create, update, delete).

### USER Capabilities:
- **Request Event Creation:** Submit a request to create new events (subject to ADMIN approval).
- **Request Event Updates:** Submit a request to update their created events (subject to ADMIN approval).
- **Request Event Deletion:** Submit a request to delete their created events (subject to ADMIN approval).
- **Register for Events:** Sign up for upcoming events.
- **View Events:** Access details of past and upcoming events.

### Home Page:
- **Event Listings:** Displays all events, divided into upcoming and past categories.
- **Event Details:** Provides detailed information for each event.
- **User Authentication:** Users must register and log in to create events or register for events.

## Installation

### Prerequisites:
- Python 3.x
- Django
- MongoDB
- `pymongo` library
- `pyjwt` library

### Steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/event-management-system.git
   cd event-management-system
   ```
2. **Create a Virtual Environment:**
   ```
   python -m venv venv
   source venv/bin/activate
   ```
3. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```
