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
| flask help            | Displays all available commands and descriptions.                                                           |
| flask init            | Creates and initializes the database                                                                        |
| flask test all        | Runs all tests (Unit and Integration)                                                                       |
| flask test int        | Runs all Integration tests                                                                                  |
| flask test unit       | Runs all Unit tests                                                                                         |
| flask exam clashes    | [RULE_SETTING] #list clashes                                                                                |
| flask exam list       | [RULE_SETTING] #list existing exams                                                                         |
| flask exam schedule   | [COURSE_CODE] [DATE] [START_TIME] [END_TIME] [RULE_SETTING] #schedule an exam                               |
| flask course create   | [COURSE_CODE] [COURSE_TITLE] [LEVEL] [SEMESTER] #creates a course                                           |
| flask course list     | This command shows the list of all existing courses                                                         |
| flask staff clashes   | [ID] #shows clashes from specified staff member                                                             |
| flask staff courses   | [ID] #shows courses a staff member is responsible for                                                       |
| flask staff exams     | [ID] #shows exams from specified staff member                                                               |
| flask staff list      | This command shows the list of all existing courses                                                         |
| flask staff lookup    | [ID] #display specified staff member                                                                         |
