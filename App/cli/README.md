# Command Line Interface

### Structure
- Each py file besides `__init__.py`, `cli.py` and `utils.py` each export an "AppGroup" which is a subcommand with all its commands.<br>
- For example `course.py` has its **assign** and **ls** commands which would be called by **flask course assign** and **flask course ls** respectively
- `__init__.py` exports a single function "create_cli_commands" which is how the CLI code gets initiated for usage
- `cli.py` imports the subcommands and holds the function definition of "create_cli_commands" and everything in context required for it to work
- `utils.py` has helper functions, like parameter validation functions and what not

### Sub Command List
- `test`: cli functionality given for running tests such as unit tests or integration tests, etc
- `exam`: brings the functionality of clash detection to utility functions surrounding exam scheduling and management
- `staff`: utility functions for the management of staff members
- `course`: simple utility to view courses and assign a course to an instructor