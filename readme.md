# Assessment Scheduler App #

### Collaborators: ###
* TINK-A-TON

### Dependencies & Tools: ###
* pip3
* FullCalendar
* Full List of packages are in requirements.txt file.

### To install Dependencies: ###
pip install -r requirements.txt

### How To Run: ###
Run by executing
1. flask init 
2. flask asm
3. flask run

### CLI Commands
| Command               | Description                                                      |
|-----------------------|------------------------------------------------------------------|
| flask help            | Displays all available commands and descriptions.                |
| flask init            | Creates and initializes the database                             |
| flask test all        | Runs all tests (Unit and Integration)                            |
| flask test int        | Runs all Integration tests                                       |
| flask test unit       | Runs all Unit tests                                              |
| flask exam clashes    | Lists all clashes (based on given rule setting)                  |
| flask exam list       | Lists all existing exams                                         |
| flask exam schedule   | Schedules an exam                                                |
| flask course create   | Creates a new course                                             |
| flask course list     | Lists all existing courses                                       |
| flask staff clashes   | Shows clashes that a specified staff member is responsible for   |
| flask staff courses   | Shows courses that a specified staff member is responsible for   |
| flask staff exams     | Shows exams that a specified staff member is responsible for     |
| flask staff list      | Lists all existing staff members                                 |
| flask staff lookup    | Displays specified staff member                                  |
