# Assessment Scheduler
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Postgresql](https://img.shields.io/badge/postgresql-4169e1?style=for-the-badge&logo=postgresql&logoColor=white)

A platform for staff to coordinate assessment scheduling, minimising student overload by limiting weekly assessment load. Built using MVC in Flask

## App Availability

You can view and test the web site at [Site Link](https://assessment-scheduler-0z5v.onrender.com). For login credentials, please refer to the documentation under the **Deliverable Links** section.

## Features

- User Authentication - Restricts access to authorized users only.  
- Exam Scheduling Options - Schedule exams easily via the "Add Exams" page.  
- Drag-and-Drop Scheduling - Quickly assign exams by dragging them to a desired time slot on the calendar.  
- Exam Clash Detection - Identifies scheduling conflicts using advanced clash detection rules.  
- Clash Resolution - Enables admins to resolve conflicts, ensuring exams proceed smoothly.  

## Installation Guide

<details>
<summary>
  <code>There are several ways you can run this application</code>
</summary>

1. **Clone the repository**:
    ```sh
    git clone https://github.com/Tink-A-Ton/assessment-scheduler.git
    cd assessment-scheduler
    ```

2. **(Optional) Create a virtual environment**:

- Using `venv`:
    ```sh
    python -m venv venv
    source venv/bin/activate    # On Windows use `venv\Scripts\activate`
    ```
- Using `conda`:
    ```sh
    conda create --name your-env-name python=3.x
    conda activate your-env-name
    ```

3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```
    
4. **Initialize and Run the application**
    ```sh
    flask init && flask run
    ```

5. **Precondition Environment Variables**

    ```js
    ENV=DEVELOPMENT
    SQLALCHEMY_DATABASE_URI=sqlite:///development.db
    SECRET_KEY=feliciaisanegg
    JWT_ACCESS_TOKEN_EXPIRES=7
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    TEMPLATES_AUTO_RELOAD=True
    SERVER_NAME=0.0.0.0
    PREFERRED_URL_SCHEME=https
    UPLOADED_PHOTOS_DEST=App/uploads
    JWT_ACCESS_COOKIE_NAME=access_token
    MAIL_DEFAULT_SENDER=assessment.scheduler.emails@gmail.com
    ```
To run the app, environment variables are required. While it uses PostgreSQL in production, SQLite can be used locally as specified in the sample `.env` file.


#### **Alernative**
- [Downloading repository as ZIP](https://github.com/Tink-A-Ton/assessment-scheduler/archive/refs/heads/main.zip)

</details>

## Model Diagram 

The diagram models an academic system denoting `User`, `Programme`, `Course`, `Semester`, and `Exam`, emphasizing course assignments, program structures, and a customizable clash detection system.

<img src="https://i.imgur.com/8jieMdD.png" alt="Model Diagram" height="500"/>

## Test & CLI Commands

| Command              | Description                                   | Usage                                |
|----------------------|-----------------------------------------------|--------------------------------------|
| `flask help`         | Displays available commands.                  | `flask help`                         |
| `flask init`         | Creates and initializes the database.         | `flask init`                         |
| `flask test all`     | Runs all tests sequentially.                  | `flask test all`                     |
| `flask test int`     | Runs all Integration tests.                   | `flask test int`                     |
| `flask test unit`    | Runs all Unit tests.                          | `flask test unit`                    |


### Feature CLI Commands

These are the commands available.

| Command                 | Description                                                      |
|-------------------------|------------------------------------------------------------------|
| `flask exam clashes`    | Lists all clashes (based on given rule setting)                  |
| `flask exam list`       | Lists all existing exams                                         |
| `flask exam schedule`   | Schedules an exam                                                |
| `flask course create`   | Creates a new course                                             |
| `flask course list`     | Lists all existing courses                                       |
| `flask staff clashes`   | Shows clashes that a specified staff member is responsible for   |
| `flask staff courses`   | Shows courses that a specified staff member is responsible for   |
| `flask staff exams`     | Shows exams that a specified staff member is responsible for     |
| `flask staff list`      | Lists all existing staff members                                 |
| `flask staff lookup`    | Displays specified staff member                                  |