# Django Dual Project Authentication System

This project demonstrates a dual-project Django setup with a centralized authentication system. It consists of two separate Django projects:

1. **Auth Project** (Port 8000): Handles user authentication and provides tokens
2. **App Project** (Port 8001): Main application that requires authentication

## Features

- User registration and login through the Auth Project
- Secure token-based communication between projects
- Protected views in the App Project that redirect to Auth Project for login
- Custom middleware for authentication validation
- Task management system in the main application

## Setup Instructions

### 1. Install Requirements

```bash
pip install -r requirements.txt
```

### 2. Run the Auth Project

```bash
chmod +x start_auth.sh
./start_auth.sh
```

This will:
- Make migrations for the authentication app
- Apply migrations
- Start the auth server on port 8000

### 3. Run the App Project (in a separate terminal)

```bash
chmod +x start_app.sh
./start_app.sh
```

This will:
- Make migrations for the main app
- Apply migrations
- Start the app server on port 8001

## How It Works

1. When a user tries to access a protected page in the App Project, they are redirected to the Auth Project login page.
2. After successful authentication, the Auth Project creates a secure token and redirects the user back to the App Project with this token.
3. The App Project validates the token with the Auth Project's API and allows access to protected pages if the token is valid.
4. The token is stored in the App Project's session for future requests.

## Project Structure

### Auth Project
- Handles user authentication (registration, login, logout)
- Manages auth tokens
- Provides API endpoint for token validation
- Redirects back to App Project after successful authentication

### App Project
- Contains the main application features
- Custom middleware to check authentication status
- Redirects to Auth Project when authentication is required
- Task management system for authenticated users

## Important URLs

- Auth Project: http://localhost:8000/
- Auth Login: http://localhost:8000/auth/login/
- Auth Register: http://localhost:8000/auth/register/
- App Project: http://localhost:8001/
- App Dashboard (protected): http://localhost:8001/dashboard/