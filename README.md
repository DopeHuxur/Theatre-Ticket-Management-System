<h1 align="center" id="title">Theatre Ticket Management System</h1>

<p align="center"><img src="https://socialify.git.ci/DopeHuxur/Theatre-Ticket-Management-System/image?custom_language=MySQL&amp;font=Bitter&amp;language=1&amp;name=1&amp;owner=1&amp;pattern=Plus&amp;theme=Dark" alt="project-image"></p>

<p id="description">A web-based theatre ticket management system built with Flask and MySQL. This application provides a complete solution for managing movie listings ticket bookings and administrative functions through an intuitive web interface.</p>

<h2>🚀 Demo</h2>

[https://www.youtube.com/watch?v=dDRieVyl2WI](https://www.youtube.com/watch?v=dDRieVyl2WI)

  
  
<h2>🧐 Features</h2>

Here're some of the features of the project:

*   <b>User Management:</b>
      - User registration and authentication
      - Secure login/logout functionality
      - Email validation and confirmation
*   <b>Movie Management:</b>
      - Browse available movies with detailed information
      - Movie details page with comprehensive information
      - Admin panel for adding and deleting movies
      - Dynamic movie carousel display
*   <b>Ticket Booking:</b>
      - Secure payment processing with Stripe integration
      - Real-time seat availability
      - Booking confirmation system
*   <b>Administrative Features:</b>
      - Admin dashboard for movie management
      - Database operations for movie CRUD
      - User session management
*   <b>Security:</b>
      - Encrypted database credentials
      - Secure API key management
      - Form validation with CSRF protection

<h2>🛠️ Installation Steps:</h2>

<p>1. Clone the repository</p>

```
git clone https://github.com/DopeHuxur/Theatre-Ticket-Management-System.git
```

```
cd Theatre-Ticket-Management-System
```

<p>3. Create a virtual environment</p>

```
python -m venv venv
```

```
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

<p>5. Install dependencies</p>

```
pip install -r requirements.txt
```

<p>6. Set up environment variables</p>

```
Create a .env file in the root directory and add:
```

```
DATABASE_URL=your_mysql_database_url
```

```
SECRET_KEY=your_secret_key
```

```
STRIPE_API_KEY=your_stripe_api_key
```

```
MAIL_PASSWORD=your_email_password
```

<p>11. Initialize the database</p>

```
python database.py
```

<p>12. Run the application</p>

```
python main.py
```

  
  
<h2>💻 Built with</h2>

Technologies used in the project:

*   <b>Backend:</b> Python, Flask
*   <b>Database:</b> MySQL with SQLAlchemy ORM
*   <b>Frontend:</b> HTML, CSS, JavaScript
*   <b>Forms:</b> Flask-WTF, WTForms
*   <b>Payment:</b> Stripe API
*   <b>Session Management:</b> Flask-Session
*   <b>Deployment:</b> Replit
*   <b>Database Host:</b> PlanetScale
