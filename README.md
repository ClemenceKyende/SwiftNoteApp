# SwiftNote

SwiftNote is a powerful and user-friendly task and note management web application designed to help individuals and teams organize their work efficiently. Built using Django, Bootstrap, and other modern technologies, SwiftNote provides features such as task management, reminders, notifications, and seamless note linking.

---

## Features

- **Task Management**
  - Create, update, and delete tasks.
  - Set task priorities (Low, Medium, High) and statuses (Pending, In Progress, Completed).
  - Link tasks to relevant notes for context.

- **Note Management**
  - Create, view, edit, and delete notes.
  - Organize notes by linking them to tasks.

- **Reminders and Notifications**
  - Set reminders for tasks.
  - Receive email and in-app notifications for upcoming tasks and reminders.

- **User Authentication**
  - Secure user login and registration.
  - Password reset functionality.

- **Responsive Design**
  - Optimized for both desktop and mobile devices.
  - Clean and modern UI using Bootstrap 5.

---

## Technologies Used

### Backend
- **Django**: A high-level Python web framework.
- **Celery**: For asynchronous task processing.
- **Redis**: Used as a message broker for Celery.

### Frontend
- **HTML5**, **CSS3**, **JavaScript**
- **Bootstrap 5**: For responsive design and modern UI components.

### Database
- **SQLite (development)**: Easily migratable to PostgreSQL or MySQL for production.

---

## Installation

Follow these steps to set up SwiftNote locally:

### Prerequisites
- Python 3.11 or above
- Redis server (for Celery)
- A virtual environment tool (e.g., `venv`)

### Steps

### Clone the Repository
   ```bash
   git clone https://github.com/ClemenceKyende/SwiftNoteApp.git
   cd SwiftNoteApp


### Set Up Virtual Environment
python -m venv env
source env/bin/activate  # On Windows, use env\Scripts\activate

### Install Dependencies
pip install -r requirements.txt

### Set Up Database
python manage.py makemigrations
python manage.py migrate
Configure Environment Variables
Create a .env file in the project directory with the following content:

### Make sure Redis is installed and running:
redis-server
Start Celery

### Open a new terminal and run:
celery -A SwiftNote worker --loglevel=info
celery -A SwiftNote beat --loglevel=info

### Run the Development Server
python manage.py runserver
Access the App
Open http://127.0.0.1:8000/ in your web browser.

### Usage
Manage Tasks: Create and organize your tasks with priorities and statuses.
Take Notes: Keep detailed notes and link them to relevant tasks.
Stay Notified: Use reminders and notifications to stay on top of your schedule.
Personalize: Access your data securely with user authentication.

### Contributing
We welcome contributions to improve SwiftNote. Follow these steps to contribute:
Fork the repository.
Create a new branch:
git checkout -b feature/your-feature-name
Make your changes and commit:
git commit -m "Add your message here"
Push to the branch:
git push origin feature/your-feature-name
Open a pull request on GitHub.

### License
This project is licensed under the MIT License. See the LICENSE file for details.

### Author
Clemence Kyende

### Acknowledgments
Special thanks to the eMobilis team and mentors for their guidance.
Django, Celery, and Redis communities for their amazing tools and resources.

### Future Enhancements
Add advanced analytics for tasks and notes.
Implement collaboration features for teams.
Incorporate AI-based suggestions for task and time management.
Enjoy using SwiftNote to organize your life efficiently! 😊