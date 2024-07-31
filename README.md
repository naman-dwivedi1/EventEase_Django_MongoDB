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

### Anyone can do
- **View Events:** View all the events which are completed in the past and which will be organized in future as the list.
- **View Events details:** Access details of past and upcoming events.
- **Search Event by venue:** Search all the events by venue (regex searching custom queries)
- **Search Event by title:** Search all the events by title (regex searching custom queries)
- **Search Event by date:** Search all the events by date

### Home Page:
- **Event Listings:** Displays all events, divided into upcoming and past categories.
- **Event Details:** Provides detailed information for each event.
- **User Authentication:** Users must register and log in to create events or register for events.

## Installation

### Prerequisites:
- Python 3.x
- Django
- MySql
- `pymysql` library for interacting with mysql database
- `pyjwt` library for token authorization

### Steps:

1. **Clone the Repository:**
   ```bash
   git clone --branch Event_Ease_SQL https://github.com/naman-dwivedi1/EventEase_Django_MongoDB.git
   cd Event_Ease_SQL
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

# Screenshots:
## Authentication
### Signup
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/4f70cbad-99b1-4e6b-8a37-976612af96bd">
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/01ca6d61-af0a-4cf8-8d94-ede354985aa4">

### Changing user role in the Database
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/9d85017b-5345-4bb9-9ed4-3262ccb078a4">

### Signin
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/d26f56ca-a904-4dfb-bee3-419f049fd5dd">

# CRUD
## ADMIN
### Create
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/0a2b6969-cc5b-4c1c-9100-45ddcd7774df">
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/b40c04d8-f05f-4a01-afbe-89aa6a47b0bd">

### Update
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/ad1e51ce-043c-4a03-b300-27282391266a">
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/742000b2-8de3-4f75-aefc-1f59d6c85c38">

### Delete
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/168a3834-8d69-459d-9c29-47f3c6281272">
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/9b1c3878-458a-4482-a59c-2831bd6220c8">

## USER
### Create
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/295553a8-045a-4549-b91c-f78dbe7c3b21">
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/dd1b076a-f56f-4818-b46f-a700444d6b18">
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/1c75c1b1-73a4-4eeb-9aeb-8f51c870ed71">

### Update
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/4fdfacb4-39d4-406f-a068-877c7dff93d6">
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/ed85344a-d192-4122-9331-3e1757bc4dfa">
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/2330702d-b48a-4c8e-9a2d-a77f63853d51">

### Delete
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/a25fe52d-071a-4f44-bbb8-e6b3b5444596">
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/77cfc1fa-4eaa-4d6b-805e-4e9db5ee35ee">

# ADMIN APPROVALS
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/3cff66a9-851c-40c8-8151-b4531e56352d">
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/317466b3-6830-4191-890b-2c99fb79289b">
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/fc2f974d-e4ed-4f51-88e8-80831b7f72a3">
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/1688766d-594a-48c3-a75c-2e37d3186562">

# Getting all events
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/da288f41-4161-4e2c-8789-7c457aaaf59d">

# Get event details
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/f4f70e3b-0ed6-45a2-9fb3-161e307381d3">

# Getting events through venue (regex searching)
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/ad04f454-8330-4eb7-9ff8-18a2a652d221">

# Getting events by their title (regex searching)
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/3138c241-4ff9-4eec-afb7-2a2483694fc3">

# Getting events by the date
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/bdef15d5-fb5d-43cb-85ed-7b19b81271da">





