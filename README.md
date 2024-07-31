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
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/dd6fcefe-f7ff-470a-bf18-336a43ad8e0f">
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/02553a32-9c1d-49e7-873a-b02f0badb30d">

### Changing user role in the Database
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/08093106-56da-4b47-9d2a-20fd58ef4692">

### Signin
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/d0354716-eb7d-4fec-a57e-1a94087427b9">

# CRUD
## ADMIN
### Create
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/4efd6c9e-102e-4a62-ba7d-a90a78a2edc5">
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/128dafa0-08fe-4917-b9bc-018a1534afff">

### Update
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/05bc162c-fd68-4ce6-b791-eb9830fe257d">
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/48a360f4-4509-4436-ae3f-1fb25894a339">

### Delete
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/8c6b8fb4-0bbd-4709-acba-1f40959a4249">
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/00a7b19a-8d5e-4451-9914-b4f24ae21f54">

## USER
### Create
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/b55e7c28-e3be-40bc-a319-8fbae89e6883">
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/7796f0c9-ee7d-4027-9436-42cc1a7a9501">
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/d973ca95-1ffd-490a-8396-3756b77d776c">

### Update
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/28f3e7cb-bf20-4cd6-b537-f5d24181ee74">
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/5d383363-eaee-42a6-9add-a857003f6748">
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/6aae7f56-a56c-4adb-bccb-b351ac47305a">

### Delete
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/0d229eb9-b677-48ef-b2ae-5077938b7670">
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/a5268b66-2ffa-4172-bb60-794fbd8b4cba">

# ADMIN APPROVALS
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/91675343-f4a7-425b-aeac-c365c24dfa7b">
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/565faf1b-4e84-410a-8ad7-73bc72962509">
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/ee3fc222-3736-4cc9-acf6-525deb3b9ae3">
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/28fb7bd6-785e-477c-a0f7-f7743827368d">













