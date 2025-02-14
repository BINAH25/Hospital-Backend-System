# **BACKEND API DOCUMENTATION**
<!-- TOC -->
- [USERS](#users)
  - [LOGIN](#login)
    - [Request Information](#request-information)
    - [Header](#header)
    - [JSON Body](#json-body)
    - [Error Responses](#error-responses)
    - [Successful Response Example](#successful-response-example)
  - [REGISTRATION](#registration)
    - [Request Information](#request-information)
    - [Header](#header)
    - [JSON Body](#json-body)
    - [Error Responses](#error-responses)
    - [Successful Response Example](#successful-response-example)
  - [GET ALL DOCTORS  ](#get-all-doctors)
    - [Request Information](#request-information)
    - [Header](#header)
    - [Error Responses](#error-responses)
    - [Successful Response Example](#successful-response-example)
  - [ASSIGN PATIENT TO DOCTOR](#assign-patient-to-doctor)
    - [Request Information](#request-information)
    - [Header](#header)
    - [JSON Body](#json-body)
    - [Error Responses](#error-responses)
    - [Successful Response Example](#successful-response-example)
  - [ GET ALL  PATIENTS OF DOCTOR](#get-all-patients-of-doctor)
    - [Request Information](#request-information)
    - [Header](#header)
    - [Error Responses](#error-responses)
    - [Successful Response Example](#successful-response-example)
  - [SUBMITING AND PROCESSING ACTIONABLE STEPS](#submiting-and-processing-actionable-steps)
    - [Request Information](#request-information)
    - [Header](#header)
    - [JSON Body](#json-body)
    - [Error Responses](#error-responses)
  - [ RETRIEVING ACTIONABLE STEPS](#retrieving-actionable-steps)
    - [Request Information](#request-information)
    - [Header](#header)
    - [Error Responses](#error-responses)
    - [Successful Response Example](#successful-response-example)
  - [ RETRIEVING REMINDERS](#retrieving-reminders)
    - [Request Information](#request-information)
    - [Header](#header)
    - [Error Responses](#error-responses)
    - [Successful Response Example](#successful-response-example)

RETRIEVING ACTIONABLE STEPS

# Users
## LOGIN

### Request Information

| Method | URL                    |
| ------ | -----------------------|
| POST   | http://127.0.0.1:8000/ |

### Header

| Type         | Property Name    |
| ------------ | ---------------- |
| Allow        | POST, OPTION     |
| Content-Type | Application/Json |
| Vary         | Accept           |

### JSON Body

| Property Name | type   | required | Description                  |
| ------------- | ------ | -------- | ---------------------------- |
| email         | String | true     | The email  of user           |
| password      | String | true     | The password of user         |

### Error Responses

| Code | Message                             |
| ---- | ----------------------------------- |
| 400  | "Invalid Credential"                |
| 400  | "this field is required "           |
| 404  | "User Not Found"                    |

### Successful Response Example

```
{
  "user": {
    "email": "vistee192@gmail.com",
    "name": "Patient Admas",
    "user_type": "Patient"
  },
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTYxNTE3MSwiaWF0IjoxNzM5NTI4NzcxLCJqdGkiOiJlNzZiYjBmZGUxM2U0YTYxYTdjYmU4ZDRmZmVjYWM1MyIsInVzZXJfaWQiOjN9.G8CN3-lMGnGgv1qOcD3uYYgaMyESErnZkDZ37KtozWk",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM5NjE1MTcxLCJpYXQiOjE3Mzk1Mjg3NzEsImp0aSI6ImQ1NjQ2Njg2ZjY3MjQ4NjI4YWE2ZjZmOGJhMzk3ZWUyIiwidXNlcl9pZCI6M30.T8aUboYdCm2bZp9uA48guX9ZacUAiNgxpkOvTI6c3eU"
}
```



## REGISTRATION

### Request Information

| Method | URL                             |  
| ------ | --------------------------------|
| POST   | http://127.0.0.1:8000/register/ |

### Header

| Type         | Property Name    |
| ------------ | ---------------- |
| Allow        | POST, OPTION     |
| Content-Type | Application/Json |
| Vary         | Accept           |

### JSON Body

| Property Name | type   | required | Description                  |
| ------------- | ------ | -------- | ---------------------------- |
| email         | String | true     | The email  of user           |
| password      | String | true     | The password of user         |
| name          | String | true     | The name of user             |
| user_type     | String | true     | Either Doctor or Patient     |

### Error Responses

| Code | Message                                 |
| ---- | ----------------------------------------|
| 400  | "Invalid email address format"          |
| 400  | "User with this Email already Exist "   |
| 404  | "required missing field"                |

### Successful Response Example

```
{
  "user": {
    "email": "binah@gmail.com",
    "name": "Blessing Seyram",
    "user_type": "Patient"
  },
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTYxNTc5NCwiaWF0IjoxNzM5NTI5Mzk0LCJqdGkiOiIxMTc1ZDE1NWE3OGY0NWFiOTU4OGVlNTFmMmI2NzA0MCIsInVzZXJfaWQiOjV9.89Hqs1wwWNVUGE4LN_T8CyHaN3ZvaIRhCe7R5tGRx5I",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM5NjE1Nzk0LCJpYXQiOjE3Mzk1MjkzOTQsImp0aSI6IjZiODE1NDYxZGE4NjQyNzk4MjhiMGI1ZWNlMWMwMzFiIiwidXNlcl9pZCI6NX0.2LDaCeGlZrLtJZ8JBd6bEcWkB-OwIURBXNkUAYgwmV8"
}
```



## GET ALL DOCTORS 
### Request Information

| Method | URL                                    |
| ------ | ---------------------------------------|
| GET    | http://127.0.0.1:8000/get/all/doctors/ |

### Header

| Type         | Property Name        |
| ------------ | ---------------------|
| Allow        | GET, OPTION         |
| Content-Type | Application/Json     |
| Vary         | Accept               |
| token        | Authentication Token |


### Error Responses

| Code | Message                                            |
| ---- | ---------------------------------------------------|
| 401  | "Authentication credentials were not provided"     |

### Successful Response Example

```
{
  "status": "success",
  "success_message": [
    {
      "email": "louisbinah@gmail.com",
      "name": "Louis Binah",
      "user_type": "Doctor"
    },
    {
      "email": "louis@gmail.com",
      "name": "Louis Seyram",
      "user_type": "Doctor"
    }
  ]
}
```

## ASSIGN PATIENT TO DOCTOR

### Request Information

| Method | URL                                  |
| ------ | -------------------------------------|
| POST   | http://127.0.0.1:8000/assign/doctor/ |

### Header

| Type         | Property Name        |
| ------------ | ---------------------|
| Allow        | POST, OPTION         |
| Content-Type | Application/Json     |
| Vary         | Accept               |
| token        | Authentication Token |


### JSON Body

| Property Name | type   | required | Description                  |
| ------------- | ------ | -------- | ---------------------------- |
| doctor_email  | String | true     | email address of the doctor  |

### Error Responses

| Code | Message                                            |
| ---- | ---------------------------------------------------|
| 401  | "Authentication credentials were not provided"     |
| 403  | "You are not a Patient"                            |
| 404  | "Doctor Not Found"                                 |
| 400  | " missing require field "                          |

### Successful Response Example

```
{
  "id": 3,
  "patient": {
    "email": "binah@gmail.com",
    "name": "Blessing Seyram",
    "user_type": "Patient"
  },
  "doctor": {
    "email": "louis@gmail.com",
    "name": "Louis Seyram",
    "user_type": "Doctor"
  },
  "created_at": "2025-02-14T10:57:00.372739Z"
}
```

## GET ALL  PATIENTS OF DOCTOR
### Request Information

| Method | URL                                    |
| ------ | ---------------------------------------|
| GET    | http://127.0.0.1:8000/doctor-patients/ |

### Header

| Type         | Property Name        |
| ------------ | ---------------------|
| Allow        | GET, OPTION         |
| Content-Type | Application/Json     |
| Vary         | Accept               |
| token        | Authentication Token |


### Error Responses

| Code | Message                                            |
| ---- | ---------------------------------------------------|
| 401  | "Authentication credentials were not provided"     |
| 403  | "You are not a Doctor"                             |

### Successful Response Example

```
{
  "status": "success",
  "success_message": [
    {
      "id": 2,
      "patient": {
        "email": "blessing@gmail.com",
        "name": "Blessing Seyram",
        "user_type": "Patient"
      },
      "created_at": "2025-02-13T17:10:34.961402Z"
    },
    {
      "id": 3,
      "patient": {
        "email": "binah@gmail.com",
        "name": "Blessing Seyram",
        "user_type": "Patient"
      },
      "created_at": "2025-02-14T10:57:00.372739Z"
    }
  ]
}
```

## SUBMITING AND PROCESSING ACTIONABLE STEPS

### Request Information

| Method | URL                                 |
| ------ | ------------------------------------|
| POST   | http://127.0.0.1:8000/doctor-notes/ |

### Header

| Type         | Property Name        |
| ------------ | ---------------------|
| Allow        | POST, OPTION         |
| Content-Type | Application/Json     |
| Vary         | Accept               |
| token        | Authentication Token |


### JSON Body

| Property Name | type   | required | Description                  |
| ------------- | ------ | -------- | ---------------------------- |
| patient_email | String | true     | email address of the patient |
| note          | String | true     | doctor's note                |

### Error Responses

| Code | Message                                            |
| ---- | ---------------------------------------------------|
| 401  | "Authentication credentials were not provided"     |
| 403  | "Only doctors can submit notes"                            |
| 404  | "Patient Not Found"                                 |
| 400  | " missing require field "                          |

### Successful Response Example

```
{
  "id": 40,
  "doctor": {
    "email": "louisbinah@gmail.com",
    "name": "Louis Binah",
    "user_type": "Doctor"
  },
  "patient": {
    "email": "vistee192@gmail.com",
    "name": "Patient Admas",
    "user_type": "Patient"
  },
  "note": "b'gAAAAABnryevjdOU_EUYAQE2D0QL_u4Q57QhUYlFLMKEpDwZrpUJhf_VkSPYYducFuFfc6oAULgqYvg0tLQ8yEi_Q84fnJVP4tXsNhjpSPN-09WZGv-9iQdxxQY0Cyr_xaNKyr8zm8Cu'",
  "created_at": "2025-02-14T11:23:27.206983Z"
}
```


## RETRIEVING ACTIONABLE STEPS
### Request Information

| Method | URL                                             |
| ------ | ------------------------------------------------|
| GET    | http://127.0.0.1:8000/get-pationt-action-steps/ |

### Header

| Type         | Property Name        |
| ------------ | ---------------------|
| Allow        | GET, OPTION         |
| Content-Type | Application/Json     |
| Vary         | Accept               |
| token        | Authentication Token |


### Error Responses

| Code | Message                                            |
| ---- | ---------------------------------------------------|
| 401  | "Authentication credentials were not provided"     |
| 403  | "Only patients can access this"                             |

### Successful Response Example

```
[
  {
    "id": "cf8e9c5b-78c1-4b84-b36b-0974669ac9ea",
    "note": 40,
    "step_type": "Plan",
    "description": "Take Amoxicillin 500mg twice a day",
    "scheduled_date": "2025-02-14T00:00:00Z",
    "completed": false,
    "duration": "5",
    "frequency": "twice daily"
  }
]
```


## RETRIEVING REMINDERS
### Request Information

| Method | URL                                          |
| ------ | ---------------------------------------------|
| GET    | http://127.0.0.1:8000/get-pationt-reminders/ |

### Header

| Type         | Property Name        |
| ------------ | ---------------------|
| Allow        | GET, OPTION         |
| Content-Type | Application/Json     |
| Vary         | Accept               |
| token        | Authentication Token |


### Error Responses

| Code | Message                                            |
| ---- | ---------------------------------------------------|
| 401  | "Authentication credentials were not provided"     |
| 403  | "Only patients can access this"                             |

### Successful Response Example

```
[
  {
    "id": 90,
    "patient": {
      "email": "vistee192@gmail.com",
      "name": "Patient Admas",
      "user_type": "Patient"
    },
    "actionable_step": {
      "id": "cf8e9c5b-78c1-4b84-b36b-0974669ac9ea",
      "note": 40,
      "step_type": "Plan",
      "description": "Take Amoxicillin 500mg twice a day",
      "scheduled_date": "2025-02-14T00:00:00Z",
      "completed": false,
      "duration": "5",
      "frequency": "twice daily"
    },
    "scheduled_time": "2025-02-15T11:23:29.027053Z",
    "sent": false
  },
  {
    "id": 91,
    "patient": {
      "email": "vistee192@gmail.com",
      "name": "Patient Admas",
      "user_type": "Patient"
    },
    "actionable_step": {
      "id": "cf8e9c5b-78c1-4b84-b36b-0974669ac9ea",
      "note": 40,
      "step_type": "Plan",
      "description": "Take Amoxicillin 500mg twice a day",
      "scheduled_date": "2025-02-14T00:00:00Z",
      "completed": false,
      "duration": "5",
      "frequency": "twice daily"
    },
    "scheduled_time": "2025-02-16T11:23:29.027053Z",
    "sent": false
  },
  {
    "id": 92,
    "patient": {
      "email": "vistee192@gmail.com",
      "name": "Patient Admas",
      "user_type": "Patient"
    },
    "actionable_step": {
      "id": "cf8e9c5b-78c1-4b84-b36b-0974669ac9ea",
      "note": 40,
      "step_type": "Plan",
      "description": "Take Amoxicillin 500mg twice a day",
      "scheduled_date": "2025-02-14T00:00:00Z",
      "completed": false,
      "duration": "5",
      "frequency": "twice daily"
    },
    "scheduled_time": "2025-02-17T11:23:29.027053Z",
    "sent": false
  },
  {
    "id": 93,
    "patient": {
      "email": "vistee192@gmail.com",
      "name": "Patient Admas",
      "user_type": "Patient"
    },
    "actionable_step": {
      "id": "cf8e9c5b-78c1-4b84-b36b-0974669ac9ea",
      "note": 40,
      "step_type": "Plan",
      "description": "Take Amoxicillin 500mg twice a day",
      "scheduled_date": "2025-02-14T00:00:00Z",
      "completed": false,
      "duration": "5",
      "frequency": "twice daily"
    },
    "scheduled_time": "2025-02-18T11:23:29.027053Z",
    "sent": false
  },
  {
    "id": 94,
    "patient": {
      "email": "vistee192@gmail.com",
      "name": "Patient Admas",
      "user_type": "Patient"
    },
    "actionable_step": {
      "id": "cf8e9c5b-78c1-4b84-b36b-0974669ac9ea",
      "note": 40,
      "step_type": "Plan",
      "description": "Take Amoxicillin 500mg twice a day",
      "scheduled_date": "2025-02-14T00:00:00Z",
      "completed": false,
      "duration": "5",
      "frequency": "twice daily"
    },
    "scheduled_time": "2025-02-19T11:23:29.027053Z",
    "sent": false
  }
]
```


