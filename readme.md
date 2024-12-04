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
| Command         | Description                                                                                                 |
|-----------------|-------------------------------------------------------------------------------------------------------------|
| course          | Commands that relate to the management of courses                                                           |
| exam            | Commands that relate to the management of examinations with all commands having a customisable rule setting |
| help            | Displays all available commands and descriptions.                                                           |
| init            | Creates and initializes the database                                                                        |
| staff           | Commands that relate to the management of staff members                                                     |
| test            | Testing commands                                                                                            |
| test all        | Runs all tests (Unit and Integration)                                                                       |
| test int        | Runs all Integration tests                                                                                  |
| test unit       | Runs all Unit tests                                                                                         |
| exam clashes    | [RULE_SETTING] #list clashes                                                                                |
| exam list       | [RULE_SETTING] #list existing exams                                                                         |
| exam schedule   | [COURSE_CODE] [DATE] [START_TIME] [END_TIME] [RULE_SETTING] #schedule an exam                               |
| course create   | [COURSE_CODE] [COURSE_TITLE] [LEVEL] [SEMESTER] #creates a course                                           |
| course list     | This command shows the list of all existing courses                                                         |
| staff clashes   | [ID] #shows clashes from specified staff member                                                             |
| staff courses   | [ID] #shows courses a staff member is responsible for                                                       |
| staff exams     | [ID] #shows exams from specified staff member                                                               |
| staff list      | This command shows the list of all existing courses                                                         |
| staff lookup    | [ID] #display specified staff member                                                                         |
