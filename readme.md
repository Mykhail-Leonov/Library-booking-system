# Bradford College Study Booth Booking System

This project is a web Booth Booking System developed for Bradford College Library.
It is developed to replace the outdated booking system with a new secure, responsive and human-centred system to allow the students to book the study booths.

## Description

The Study Booth booking System is built using a client–server architecture. It has developed frontend, that provides interface for users in browser, and backend that handles authentication, booking logic and database. Server side validation provides real time availability updates and prevents double bookings.
In the system, students must create or log into account in order to complete the booking, linking each booking to the student and providing secure authentication.
The system was created with focus on human-centered design and providing accessibility, usability and simplified booking process.


## System features
- Student registration using college student id, e-mail and name
- Secure login with password hashing
- Real-time dynamic booth availability without page reload
- Calendar-based booking up to 7 days in advance
- One booking per day
- View and cancel current bookings 
- Prevention of double bookings via server-side validation
- Server-side input validation for registration, login and bookings.
- Separate databases for users and bookings.
## Technologies Used

### Frontend
- HTML5 (Semantic structure for accessibility)
- CSS3 (Styling and responsive layout)
- JavaScript (Dynamic updates and frontend logic)
- Bootstrap 5 (Forms and responsiveness)

### Backend
- Python (Flask)
- SQLite database
- REST-style API endpoints

### Version Control
- Git & GitHub

## Getting Started
### Dependencies
Ensure that you have installed:
- Python 3.8+
- pip (Python package manager)

### Installing and Executing
1. Clone or download the project repository from https://github.com/Mykhail-Leonov/Library-booking-system

2.  Ensure the following files/folders exist:
    - app.py
    - userdatabase.py
    - bookingdatabase.py
    - static/ (HTML, CSS, JS, images)
3. Navigate to the project folder

4. In the terminal, set up virtual environment:
    - python -m venv venv //Creates a virtual environment within directory
    - venv\Scripts\activate //Activating ensures all pip installs go into your local venv, not your global system Python.

5. Install required dependencies:
    - pip install -r requirements.txt

6. Run the Flask application:
    - python app.py

7. In your browser open: 
    - http://127.0.0.1:5000 

## How the Solution Meets Client Requirements
- Secure authentication with hashed passwords
- SQL injection security via parameterised SQL queries
- Prevention of double bookings via server-side validation
- Server-side input validation for registration, login and bookings.
- Real-time availability updates
- Dynamic interface
- Clear availability feedback via colors
- Reliable data storage in SQLite
- Reduced number of booking steps
- Calendar-based booking
- Responsive design for mobile and desktop
- Keyboard navigation
- Support of screen readers via semantic HTML
- Consideration of Human-Centred Design principles

## Version History
- v0.1
  - Added static folder with main page and CSS styling
- v0.1.1
  - Update: Made the booking page full-width by default and added a button to toggle the guide panel on the left
- v0.1.2
  - Update: Moved the guide button from nav bar to the left side of main page. Added picture for logo
- v0.1.3
  - Update: Improved indentation for code clarity and consistency
- v0.2 
  - Created a registering page using Bootstrap with register form
- v0.2.1
  - Created a login page using Bootstrap with login form
- v0.3
  - Authentication backend
- v0.9
  - Complete booth booking
- v0.9.1
  - Added redirect to main page by clicking on logo. Improved keyboard navigation for booking
- v1.0
  - Added Profile page, where users can see their details and cancell bookings
- v1.0.1
  - Updated guide section with correct guide and terms and conditions
- v1.0.2
  - Added pictures of booths
- v1.1
  - Improved responsiveness and added requirements.txt and readme.md


## Acknowledgments
The template for readme.md was taken from DomPizzie (https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc)

