# Personal data

Topics aim was to understand the following concepts:

* What Is PII, non-PII, and Personal Data?
* Implementing logging in python
* [bcrypt package](https://github.com/pyca/bcrypt/)
* Logging to Files, Setting Levels, and Formatting
* Examples of Personally Identifiable Information (PII)
* How to implement a log filter that will obfuscate PII fields 
* How to encrypt a password and check the validity of an input password 
* How to authenticate to a database using environment variables

## Files

The tasks for this project were completed using the following files:

### [filtered_logger.py](./filtered_logger.py)

**Task 0**:

Function called `filter_datum` that returns the log message obfuscated:

Arguments:

* `fields`: a list of strings representing all fields to obfuscate 
* `redaction`: a string representing by what the field will be obfuscated 
* `message`: a string representing the log line 
* `separator`: a string representing by which character is separating all fields in the log line (`message`)

**Task 1**:

Update the class `RedactingFormatter` to accept a list of `strings` fields constructor argument.

Implement the `format` method to filter values in incoming log records using `filter_datum`. Values for fields in `fields` should be filtered.

DO NOT extrapolate `FORMAT` manually. The `format` method implementation should be less than 5 lines long.

**Task 2**:

Implement a `get_logger` function that takes no arguments and returns a `logging.Logger` object.
The logger should be named `"user_data"` and only log up to `logging.INFO` level. It should not propagate messages to other loggers. It should have a `StreamHandler` with `RedactingFormatter` as formatter.

**Task 3**:

Implement a `get_db` function that returns a connector to the database (`mysql.connector.connection.MySQLConnection` object).

Requirements:

* Use the os module to obtain credentials from the environment 
* Use the module mysql-connector-python to connect to the MySQL database

**Task 4**:

Implement a `main` function that takes no arguments and returns nothing.
The function will obtain a database connection using `get_db` and retrieve all rows in the `users` table and display each row under a filtered format like this:

```
[HOLBERTON] user_data INFO 2019-11-19 18:37:59,596: name=***; email=***; phone=***; ssn=***; password=***; ip=e848:e856:4e0b:a056:54ad:1e98:8110:ce1b; last_login=2019-11-14T06:16:24; user_agent=Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; KTXN);
```
Filtered fields:

name, email, phone, ssn, password


### [encrypt_password.py](./encrypt_password.py)

**Task 5**:

Implement a `hash_password` function that expects one string argument name `password` and returns a salted, hashed password, which is a byte string.

Use the `bcrypt` package to perform the hashing (with `hashpw`).

**Task 6**:

Implement an `is_valid` function that expects 2 arguments and returns a boolean.
Use `bcrypt` to validate that the provided password matches the hashed password.

