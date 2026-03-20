# Authentication System (JWT) - College Submission

A complete JWT-based authentication system built with Django, HTML, CSS, and JavaScript.

## Features

- ✅ User Registration with validation
- ✅ Secure Login with JWT tokens
- ✅ Password hashing using Django's built-in system
- ✅ Protected routes with JWT authentication
- ✅ User profile management
- ✅ Secure token storage in localStorage
- ✅ Automatic token verification
- ✅ Session management
- ✅ CORS support for API access

## Tech Stack

**Backend:**
- Python 3.x
- Django 4.2
- Django REST Framework
- PyJWT (JSON Web Tokens)

**Frontend:**
- HTML5
- CSS3
- Vanilla JavaScript (ES6+)

## Project Structure

```
Authentication-system(JWT)/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── auth_project/            # Main Django project
│   ├── settings.py         # Django settings
│   ├── urls.py             # URL routing
│   └── wsgi.py             # WSGI application
├── auth_app/               # Authentication app
│   ├── models.py           # Database models
│   ├── views.py            # API endpoints
│   ├── authentication.py    # JWT authentication class
│   ├── urls.py             # App URLs
│   └── admin.py            # Admin configuration
└── static/                 # Frontend files
    ├── index.html          # Home page
    ├── register.html       # Registration page
    ├── login.html          # Login page
    ├── profile.html        # User profile page (protected)
    ├── css/
    │   └── style.css       # Global styles
    └── js/
        └── auth.js         # Authentication utilities
```

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone/Download Project
```bash
cd Authentication-system(JWT)
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Create Database
```bash
python manage.py migrate
```

### Step 5: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 6: Run Development Server
```bash
python manage.py runserver
```

The application will be available at: **http://localhost:8000**

## API Endpoints

### 1. Register User
**POST** `/api/register`

Request:
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securePassword123"
}
```

Response:
```json
{
    "success": true,
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com"
    }
}
```

### 2. Login User
**POST** `/api/login`

Request:
```json
{
    "username": "john_doe",
    "password": "securePassword123"
}
```

Response:
```json
{
    "success": true,
    "message": "Login successful",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com"
    }
}
```

### 3. Get User Profile (Protected)
**GET** `/api/profile`

Headers:
```
Authorization: Bearer <token>
```

Response:
```json
{
    "success": true,
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe"
    },
    "profile": {
        "bio": "Software developer",
        "phone_number": "+1234567890",
        "created_at": "2024-03-20T10:30:00Z",
        "updated_at": "2024-03-20T10:30:00Z"
    }
}
```

### 4. Update User Profile (Protected)
**PUT/POST** `/api/update-profile`

Headers:
```
Authorization: Bearer <token>
Content-Type: application/json
```

Request:
```json
{
    "bio": "Updated bio",
    "phone_number": "+1987654321"
}
```

Response:
```json
{
    "success": true,
    "message": "Profile updated successfully",
    "profile": {
        "bio": "Updated bio",
        "phone_number": "+1987654321"
    }
}
```

### 5. Logout User (Protected)
**POST** `/api/logout`

Headers:
```
Authorization: Bearer <token>
```

Response:
```json
{
    "success": true,
    "message": "Logged out successfully"
}
```

## Pages & Features

### Home Page (`index.html`)
- Navigation bar with auth status
- Welcome message for authenticated users
- Feature list showcasing system capabilities
- Quick access to login/register or profile

### Register Page (`register.html`)
- Username validation (min 3 chars)
- Email validation
- Password validation (min 6 chars)
- Password confirmation
- Real-time error messages
- Success message with auto-redirect to login

### Login Page (`login.html`)
- Username/email login
- Password field
- Error handling
- Auto-navigation to profile on success
- Token stored in localStorage

### Profile Page (`profile.html`) - Protected
- Requires valid JWT token
- Displays user information
- Shows profile bio and phone number
- Edit form to update profile
- Member since date
- Real-time profile updates

## Security Features

1. **Password Hashing**: Uses Django's built-in PBKDF2 password hashing
2. **JWT Tokens**: Secure token-based authentication
3. **Token Expiration**: Tokens expire after 24 hours (configurable)
4. **Protected Routes**: Profile page requires valid authentication
5. **CORS Security**: Configured CORS headers
6. **HTTPOnly Storage**: Tokens stored in localStorage (consider httpOnly cookies for production)

## Configuration

You can customize the following settings in `auth_project/settings.py`:

```python
JWT_SECRET = 'your-jwt-secret-key-change-in-production'
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24
```

## Testing the Application

1. Visit **http://localhost:8000** (Home page)
2. Click "Register" and create a new account
3. Login with your credentials
4. View your profile page
5. Edit your bio and phone number
6. Logout and verify the authentication flow

## Common Issues & Troubleshooting

### Issue: "Page not found" error
- Make sure you've run `python manage.py runserver`
- Check if you're accessing `http://localhost:8000`

### Issue: Database errors
- Run `python manage.py migrate` again
- Check if `db.sqlite3` exists in the project root

### Issue: CORS errors
- Ensure `localhost` is in `CORS_ALLOWED_ORIGINS` in settings.py

### Issue: Token expired
- Re-login to get a new token
- Check JWT_EXPIRATION_HOURS setting

## Production Deployment Notes

Before deploying to production:

1. Change `DEBUG = False` in settings.py
2. Update `SECRET_KEY` and `JWT_SECRET` with strong random values
3. Set proper `ALLOWED_HOSTS`
4. Use environment variables for sensitive data
5. Use HTTPS only
6. Consider using httpOnly cookies instead of localStorage for tokens
7. Implement rate limiting on authentication endpoints
8. Add proper logging and monitoring

## Files Overview

### Backend Files

- **auth_project/settings.py**: Django configuration, database setup, JWT settings
- **auth_project/urls.py**: Main URL routing
- **auth_app/models.py**: UserProfile model extending Django's User model
- **auth_app/views.py**: All API endpoints (register, login, profile, logout, update)
- **auth_app/authentication.py**: JWT token generation and verification
- **auth_app/urls.py**: App-level URL routing

### Frontend Files

- **index.html**: Home page with navigation and status display
- **register.html**: Registration form with validation
- **login.html**: Login form with authentication
- **profile.html**: Protected user profile page
- **css/style.css**: All styling for the application
- **js/auth.js**: Utility functions for authentication and API calls

## License

This project is created for educational purposes.

## Support

For issues or questions, please check the API documentation and ensure:
- All dependencies are installed from requirements.txt
- Database migrations have been run
- Development server is running on correct port
- Bearer token is properly formatted in headers
