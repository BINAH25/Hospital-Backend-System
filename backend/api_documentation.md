# **BACKEND API DOCUMENTATION**
<!-- TOC -->
- [Accounts](#accounts)
  - [LOGIN](#login)
    - [Request Information](#request-information)
    - [Header](#header)
    - [JSON Body](#json-body)
    - [Error Responses](#error-responses)
    - [Successful Response Example](#successful-response-example)
  - [ADD INSTITUTION ](#add-institution)
    - [Request Information](#request-information)
    - [Header](#header)
    - [JSON Body](#json-body)
    - [Error Responses](#error-responses)
    - [Successful Response Example](#successful-response-example)
  - [GET ALL INSTITUTIONS ](#get-all-institutions)
    - [Request Information](#request-information)
    - [Header](#header)
    - [Error Responses](#error-responses)
    - [Successful Response Example](#successful-response-example)
  - [ADD USER](#add-user)
    - [Request Information](#request-information)
    - [Header](#header)
    - [JSON Body](#json-body)
    - [Error Responses](#error-responses)
    - [Successful Response Example](#successful-response-example)


# Accounts
## LOGIN

### Request Information

| Method | URL                                                |
| ------ | ---------------------------------------------------|
| POST   | https://dcit418.pythonanywhere.com/api/auth/login/ |

### Header

| Type         | Property Name    |
| ------------ | ---------------- |
| Allow        | POST, OPTION     |
| Content-Type | Application/Json |
| Vary         | Accept           |

### JSON Body

| Property Name | type   | required | Description                  |
| ------------- | ------ | -------- | ---------------------------- |
| username      | String | true     | The username  of user        |
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
    "email": "lbinah@st.ug.edu.gh",
    "username": "admin",
    "is_superuser": true,
    "is_staff": true,
    "created_by": null,
    "institution": null
  },
  "permission": [
    "add_blacklistedtoken",
    "add_contenttype",
    "add_group",
    "add_institution",
    "add_institution",
    "add_logentry",
    "add_outstandingtoken",
    "add_permission",
    "add_session",
    "add_user",
    "add_user",
    "change_blacklistedtoken",
    "change_contenttype",
    "change_group",
    "change_institution",
    "change_logentry",
    "change_outstandingtoken",
    "change_permission",
    "change_session",
    "change_user",
    "delete_blacklistedtoken",
    "delete_contenttype",
    "delete_group",
    "delete_institution",
    "delete_institution",
    "delete_logentry",
    "delete_outstandingtoken",
    "delete_permission",
    "delete_session",
    "delete_user",
    "delete_user",
    "edit_institution",
    "edit_user",
    "view_blacklistedtoken",
    "view_contenttype",
    "view_group",
    "view_institution",
    "view_institution",
    "view_logentry",
    "view_outstandingtoken",
    "view_permission",
    "view_session",
    "view_user",
    "view_user"
  ],
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNzA2NzY2MywiaWF0IjoxNzE2OTgxMjYzLCJqdGkiOiI1MjU2ZDdkOGYyZmQ0NGRlYTZjNjNiODQxZjBhNmZkMSIsInVzZXJfaWQiOjF9.0sU31UMSUNp31KEnqrytVCuaa4kBA_oFoNpxOamxc5k",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE3MDY3NjYzLCJpYXQiOjE3MTY5ODEyNjMsImp0aSI6IjQwMjBhODg1OTFiZDQwNjVhODAyMGI4NGIwMDZkYzM1IiwidXNlcl9pZCI6MX0.wJY2IlNaE-aGs_fjX9g23v_hcZU16zUU3KFt05btkS4"
}
```
## ADD INSTITUTION 

### Request Information

| Method | URL                                             |
| ------ | ------------------------------------------------|
| POST   | https://dcit418.pythonanywhere.com/api/add/institution/      |

### Header

| Type         | Property Name        |
| ------------ | ---------------------|
| Allow        | POST, OPTION         |
| Content-Type | Application/Json     |
| Vary         | Accept               |
| token        | Authentication Token |

### JSON Body

| Property Name     | type   | required | Description                         |
| -------------     | ------ | -------- | ----------------------------------- |
| usernane          | String | true     | username of the institution         |
| email             | String | true     | email of the institution            |
| institution_name  | String | true     | name of the institution             |
| location          | String | true     | location of the institution         |
| phone             | String | true     | number of the institution           |
| institution_type  | String | true     | type of the institution             |

### Error Responses

| Code | Message                                            |
| ---- | ---------------------------------------------------|
| 401  | "Authentication credentials were not provided"     |
| 403  | "You do not have permission to perform this action"|
| 400  | "some field were not provided"                     |
| 400  | "institution with this usernane already exists"    |
| 400  | "institution with this email already exists"       |

### Successful Response Example

```
{
  "status": "success",
  "detail": "Institution added Successfully"
}
```

## GET ALL INSTITUTIONS 

### Request Information

| Method | URL                                             |
| ------ | ------------------------------------------------|
| GET    | https://dcit418.pythonanywhere.com/api/get/all/institutions/ |

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
| 403  | "You do not have permission to perform this action"|

### Successful Response Example

```
{
  "status": "success",
  "detail": [
    {
      "id": 3,
      "usernane": "UCC",
      "email": "ucc@st.ug.edu.gh",
      "institution_name": "University of Cape Coast",
      "location": "Cape Coast",
      "phone": "0246031105",
      "institution_type": "Tertiary",
      "created_at": "2024-05-29T13:02:02.366169Z",
      "updated_at": "2024-05-29T13:02:02.366206Z"
    },
    {
      "id": 2,
      "usernane": "UG",
      "email": "louisbinah@st.ug.edu.gh",
      "institution_name": "University of Ghana",
      "location": "Legon",
      "phone": "0246031105",
      "institution_type": "Tertiary",
      "created_at": "2024-05-29T08:26:39.359445Z",
      "updated_at": "2024-05-29T08:26:39.359489Z"
    }
  ]
}
```

## ADD USER

### Request Information

| Method | URL                                      |
| ------ | -----------------------------------------|
| POST   | https://dcit418.pythonanywhere.com/api/auth/register/ |

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
| institution   | String | true     | select the institution       |
| password      | String | true     | password of institution      |

### Error Responses

| Code | Message                                            |
| ---- | ---------------------------------------------------|
| 401  | "Authentication credentials were not provided"     |
| 403  | "You do not have permission to perform this action"|
| 404  | "institution Not Found"                            |
| 400  | "this field is required "                          |

### Successful Response Example

```
{
  "status": "success",
  "detail": "User added Successfully"
}
```
