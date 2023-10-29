
# README.md for LLM_analyzer-master

## Overview

The `LLM_analyzer-master` is a Flask-based web application that offers user authentication and provides insights into Reddit data. It structures its routes using Flask Blueprints and employs Flask-Login for user session management.

## Features

1. **User Management**: Supports user login and logout functionalities. Users' passwords are securely hashed using `werkzeug.security`.
2. **Reddit Data Analysis**: Fetches and displays Reddit posts from a database. Detailed views for individual Reddit posts are also available.
3. **Error Handling**: Handles internal server errors and logs them for further analysis.

## Modules

- `app.py`: Sets up the main Flask application, configures Flask-Login, and registers blueprints.
- `auth.py`: Contains routes related to authentication, including login and logout.
- `main.py`: Houses the main application routes, including those related to Reddit data display.
- `user.py`: Manages user-related operations and database interactions for user data.

## Dependencies

- Flask
- Flask-Login
- SQLAlchemy
- dotenv
- werkzeug.security (for password hashing)

## Setup

1. Clone the repository.
2. Install required dependencies using pip.
3. Set up environment variables, especially `DATABASE_URL` for database connectivity.
4. Run `main.py` to start the application.

## Future Work

- Integrate more data sources beyond Reddit.
- Enhance user management features like registration and password recovery.
- Improve UI/UX for better user engagement.
