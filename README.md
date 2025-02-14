# Hospital Backend System Test
## Overview
This is a backend system for a hospital that handles user signups, patient–doctor assignments, doctor note submissions, and dynamic scheduling of actionable steps based on live LLM processing. The system ensures data security through encryption and leverages Celery and Redis for background task processing.


## ER Diagram of Database Design
![alt text](graph.png)

## Key Features

1. **User Management** : Signup, authentication, and role-based access control (Patients and Doctors).

2. **Doctor-Patient Assignment**: Patients select a doctor; doctors view their assigned patients.

3. **Doctor Notes & LLM Integration**: Doctors submit encrypted notes, and an LLM extracts actionable steps.

4. **Doctor-Patient Assignment** Dynamic Scheduling: Automated reminders based on the treatment plan, dynamically adjusting for missed check-ins.

5. **Background Task Processing**: Uses Celery and Redis for handling scheduled tasks.

## Tech Stack

1. **Backend Framework**: Django & Django Rest Framework (DRF)

2. **Authentication**: Django SimpleJWT

3. **Task Queue**:Celery with Redis as the message broker

4. **Database**:PostgreSQL

5. **Encryption**:AES encryption for patient notes

6. **LLM Processing**: Google Gemini Flash

## Installation

### Prerequisites

Ensure you have the following installed:

Python 3.10

Redis