# Healthcare Backend API Documentation

## Overview
This is a Django REST Framework-based healthcare backend system that provides user authentication, patient management, doctor management, and patient-doctor mapping functionality.

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL
- pip

### Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables in `.env`:
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key-here-change-in-production
   
   DB_NAME=healthcare_db
   DB_USER=postgres
   DB_PASSWORD=your_password_here
   DB_HOST=localhost
   DB_PORT=5432
   
   SIMPLE_JWT_SIGNING_KEY=jwt-secret-key-change-in-production
   SIMPLE_JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
   SIMPLE_JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
   ```

4. Set up PostgreSQL database:
   - Create a database named `healthcare_db`
   - Update the database credentials in `.env`

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Base URL
```
http://localhost:8000/api/
```

### Authentication Endpoints

#### 1. Register User
- **URL:** `POST /api/auth/register/`
- **Description:** Register a new user
- **Request Body:**
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }
  ```
- **Response:**
  ```json
  {
    "message": "User registered successfully",
    "user": {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com"
    },
    "tokens": {
      "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
  }
  ```

#### 2. Login User
- **URL:** `POST /api/auth/login/`
- **Description:** Login user and get JWT tokens
- **Request Body:**
  ```json
  {
    "email": "john@example.com",
    "password": "securepassword123"
  }
  ```
- **Response:**
  ```json
  {
    "message": "Login successful",
    "user": {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com"
    },
    "tokens": {
      "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
  }
  ```

#### 3. Get User Profile
- **URL:** `GET /api/auth/profile/`
- **Description:** Get authenticated user's profile
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:**
  ```json
  {
    "user": {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "username": "john",
      "date_joined": "2025-10-15T10:00:00Z"
    }
  }
  ```

### Patient Management Endpoints

#### 4. Create Patient
- **URL:** `POST /api/patients/`
- **Description:** Create a new patient (authenticated users only)
- **Headers:** `Authorization: Bearer <access_token>`
- **Request Body:**
  ```json
  {
    "name": "Jane Smith",
    "email": "jane@example.com",
    "phone": "+1234567890",
    "address": "123 Main St, City, Country",
    "date_of_birth": "1990-01-01",
    "gender": "F",
    "medical_history": "No known allergies"
  }
  ```

#### 5. Get All Patients
- **URL:** `GET /api/patients/`
- **Description:** Get all patients created by authenticated user
- **Headers:** `Authorization: Bearer <access_token>`

#### 6. Get Patient Details
- **URL:** `GET /api/patients/{id}/`
- **Description:** Get details of a specific patient
- **Headers:** `Authorization: Bearer <access_token>`

#### 7. Update Patient
- **URL:** `PUT /api/patients/{id}/`
- **Description:** Update patient details
- **Headers:** `Authorization: Bearer <access_token>`

#### 8. Delete Patient
- **URL:** `DELETE /api/patients/{id}/`
- **Description:** Delete a patient record
- **Headers:** `Authorization: Bearer <access_token>`

### Doctor Management Endpoints

#### 9. Create Doctor
- **URL:** `POST /api/doctors/`
- **Description:** Create a new doctor (authenticated users only)
- **Headers:** `Authorization: Bearer <access_token>`
- **Request Body:**
  ```json
  {
    "name": "Dr. Smith",
    "email": "drsmith@example.com",
    "phone": "+1234567891",
    "specialization": "CARDIOLOGY",
    "years_of_experience": 10,
    "qualification": "MD, MBBS",
    "hospital_affiliation": "General Hospital",
    "consultation_fee": "150.00"
  }
  ```

#### 10. Get All Doctors
- **URL:** `GET /api/doctors/`
- **Description:** Get all doctors
- **Headers:** `Authorization: Bearer <access_token>`

#### 11. Get Doctor Details
- **URL:** `GET /api/doctors/{id}/`
- **Description:** Get details of a specific doctor
- **Headers:** `Authorization: Bearer <access_token>`

#### 12. Update Doctor
- **URL:** `PUT /api/doctors/{id}/`
- **Description:** Update doctor details (only by creator)
- **Headers:** `Authorization: Bearer <access_token>`

#### 13. Delete Doctor
- **URL:** `DELETE /api/doctors/{id}/`
- **Description:** Delete a doctor record (only by creator)
- **Headers:** `Authorization: Bearer <access_token>`

### Patient-Doctor Mapping Endpoints

#### 14. Assign Doctor to Patient
- **URL:** `POST /api/mappings/`
- **Description:** Assign a doctor to a patient
- **Headers:** `Authorization: Bearer <access_token>`
- **Request Body:**
  ```json
  {
    "patient": 1,
    "doctor": 1,
    "notes": "Regular checkup assignment"
  }
  ```

#### 15. Get All Mappings
- **URL:** `GET /api/mappings/list/`
- **Description:** Get all patient-doctor mappings for authenticated user
- **Headers:** `Authorization: Bearer <access_token>`

#### 16. Get Patient's Doctors
- **URL:** `GET /api/mappings/{patient_id}/`
- **Description:** Get all doctors assigned to a specific patient
- **Headers:** `Authorization: Bearer <access_token>`

#### 17. Remove Doctor from Patient
- **URL:** `DELETE /api/mappings/remove/{mapping_id}/`
- **Description:** Remove a doctor from a patient
- **Headers:** `Authorization: Bearer <access_token>`

## Data Models

### User
- `id`: Primary key
- `name`: Full name
- `email`: Unique email (used for login)
- `username`: Auto-generated from email
- `password`: Encrypted password

### Patient
- `id`: Primary key
- `name`: Patient name
- `email`: Unique email
- `phone`: Phone number
- `address`: Address
- `date_of_birth`: Date of birth
- `gender`: M/F/O
- `medical_history`: Optional medical history
- `created_by`: Foreign key to User
- `created_at`: Timestamp
- `updated_at`: Timestamp

### Doctor
- `id`: Primary key
- `name`: Doctor name
- `email`: Unique email
- `phone`: Phone number
- `specialization`: Medical specialization
- `years_of_experience`: Years of experience
- `qualification`: Medical qualifications
- `hospital_affiliation`: Hospital affiliation
- `consultation_fee`: Consultation fee
- `created_by`: Foreign key to User
- `created_at`: Timestamp
- `updated_at`: Timestamp

### PatientDoctorMapping
- `id`: Primary key
- `patient`: Foreign key to Patient
- `doctor`: Foreign key to Doctor
- `assigned_date`: Assignment timestamp
- `notes`: Optional notes
- `is_active`: Active status
- `created_by`: Foreign key to User

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request (validation errors)
- `401`: Unauthorized (authentication required)
- `403`: Forbidden (permission denied)
- `404`: Not Found
- `500`: Internal Server Error

Error responses follow this format:
```json
{
  "error": "Error message",
  "details": "Detailed error information"
}
```

## Testing with Postman

1. Import the collection or create requests manually
2. For authentication endpoints, use the returned JWT tokens
3. Add `Authorization: Bearer <token>` header for protected endpoints
4. Use appropriate HTTP methods (GET, POST, PUT, DELETE)
5. Include required request bodies for POST/PUT requests

## Security Features

- JWT authentication with access and refresh tokens
- Password validation
- User-specific data access (patients belong to creators)
- CORS configuration for frontend integration
- Input validation and sanitization
- Proper error handling without exposing sensitive information