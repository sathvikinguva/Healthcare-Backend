# Healthcare Backend API

A comprehensive Django REST Framework-based backend system for healthcare applications with JWT authentication, patient management, doctor management, and patient-doctor mapping functionality.

## Features

- **User Authentication**: JWT-based authentication with access and refresh tokens
- **Patient Management**: Full CRUD operations for patient records
- **Doctor Management**: Complete doctor profile management
- **Patient-Doctor Mapping**: Assign and manage doctor-patient relationships
- **Secure API**: Role-based access control and data validation
- **Admin Interface**: Django admin for easy data management
- **PostgreSQL Integration**: Robust database backend
- **Comprehensive Documentation**: API documentation and Postman collection

## Requirements

- Python 3.8+
- PostgreSQL 12+
- pip (Python package installer)

## Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd healthcare_backend
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup
1. Install PostgreSQL and create a database:
   ```sql
   CREATE DATABASE healthcare_db;
   CREATE USER healthcare_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE healthcare_db TO healthcare_user;
   ```

2. Update the `.env` file with your database credentials:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key-here-change-in-production
   
   DB_NAME=healthcare_db
   DB_USER=healthcare_user
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   
   SIMPLE_JWT_SIGNING_KEY=jwt-secret-key-change-in-production
   SIMPLE_JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
   SIMPLE_JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
   ```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 6. Start Development Server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Authentication Endpoints
- `POST /auth/register/` - Register new user
- `POST /auth/login/` - User login
- `GET /auth/profile/` - Get user profile

### Patient Endpoints
- `GET /patients/` - List all patients (user's patients only)
- `POST /patients/` - Create new patient
- `GET /patients/{id}/` - Get patient details
- `PUT /patients/{id}/` - Update patient
- `DELETE /patients/{id}/` - Delete patient

### Doctor Endpoints
- `GET /doctors/` - List all doctors
- `POST /doctors/` - Create new doctor
- `GET /doctors/{id}/` - Get doctor details
- `PUT /doctors/{id}/` - Update doctor (creator only)
- `DELETE /doctors/{id}/` - Delete doctor (creator only)

### Patient-Doctor Mapping Endpoints
- `POST /mappings/` - Assign doctor to patient
- `GET /mappings/list/` - List all mappings (user's mappings)
- `GET /mappings/{patient_id}/` - Get patient's doctors
- `DELETE /mappings/remove/{mapping_id}/` - Remove doctor assignment

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

## Example Usage

### 1. Register a User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

### 3. Create a Patient
```bash
curl -X POST http://localhost:8000/api/patients/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "phone": "+1234567890",
    "address": "123 Main St, City, Country",
    "date_of_birth": "1990-01-01",
    "gender": "F",
    "medical_history": "No known allergies"
  }'
```

## Testing with Postman

1. Import the provided Postman collection: `healthcare_backend_postman_collection.json`
2. Set the `base_url` variable to `http://localhost:8000/api`
3. Register/Login to get an access token
4. Set the `access_token` variable with the received token
5. Test all endpoints using the pre-configured requests

## Data Models

### User
- Custom user model with email-based authentication
- Fields: name, email, username (auto-generated)

### Patient
- Complete patient information management
- Fields: name, email, phone, address, date_of_birth, gender, medical_history
- Linked to the user who created the record

### Doctor
- Comprehensive doctor profile management
- Fields: name, email, phone, specialization, years_of_experience, qualification, hospital_affiliation, consultation_fee
- Linked to the user who created the record

### PatientDoctorMapping
- Manages patient-doctor relationships
- Fields: patient, doctor, assigned_date, notes, is_active
- Unique constraint on patient-doctor combination

## Security Features

- JWT authentication with access and refresh tokens
- Password validation and encryption
- User-specific data access control
- Input validation and sanitization
- CORS configuration for frontend integration
- Proper error handling without sensitive data exposure

## Development

### Project Structure
```
healthcare_backend/
├── authentication/          # User authentication app
├── healthcare/             # Healthcare management app
├── healthcare_backend/     # Main project settings
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables
├── API_Documentation.md   # Detailed API docs
├── healthcare_backend_postman_collection.json  # Postman collection
└── README.md             # This file
```

### Running Tests
```bash
python manage.py test
```

### Making Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Update `SECRET_KEY` and `SIMPLE_JWT_SIGNING_KEY` with secure values
3. Configure proper PostgreSQL settings
4. Set up proper CORS origins
5. Use a production WSGI server (e.g., Gunicorn)
6. Configure SSL/HTTPS
7. Set up proper logging and monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

**Happy Coding! 🚀**
=======
# Healthcare-Backend
>>>>>>> 2293a39e975cd086b87e4edb409fa8a54bcfcc9a
