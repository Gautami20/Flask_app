# Flask User Management Application

This is a simple Flask application that demonstrates user login, logout, session management, and user deletion functionalities using Flask and SQLAlchemy.

## Features

- User login
- User logout
- Displaying all users
- Deleting users
- Flash messages for user feedback

## Requirements

- Python 3.x
- Flask
- Flask-SQLAlchemy

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/flask-user-management.git
    cd flask-user-management
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install Flask Flask-SQLAlchemy
    ```

4. Set up the database:

    ```bash
    python
    ```

    ```python
    from app import db
    db.create_all()
    exit()
    ```

5. Run the application:

    ```bash
    flask run
    ```
## Routes

- `/register` (GET, POST): register page for user.
- `/login` (GET, POST): Login page for user authentication.
- `/logout` (GET): Logout the current user.
- `/` (GET): Home page. Redirects to login if the user is not logged in.
- `/read` (GET): Page to display all users.
- `/delete` (POST): Endpoint to delete a user.
-`/update` (POST): Endpoint to update a user.
-`/delete_blog` (POST): Endpoint to delete a users blogs.
-`/update_blog` (POST): Endpoint to update a users blogs.
