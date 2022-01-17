# User authentication service

This project's objective was to provide understanding on the following concepts:

* How to declare API routes in a Flask app 
* How to get and set cookies 
* How to retrieve request form data 
* How to return various HTTP status codes

## Files

The following task files were used for this project as per task instructions:

### Task 0 (User model)
Create a SQLAlchemy model named User for a database table named users (by using the mapping declaration of SQLAlchemy)
with the following attributes.

* `id`, the integer primary key 
* `email`, a non-nullable string 
* `hashed_password`, a non-nullable string 
* `session_id`, a nullable string 
* `reset_token`, a nullable string

File: [user.py](./user.py)

### Task 1 (create user)

method: `add_user`

which has two required string arguments: `email` and `hashed_password`, and returns a `User` object. The method should save the user to the database. No validations are required at this stage.

File: [db.py](./db.py)

### Task 2 (Find user)

method: `DB.find_user_by`

This method takes in arbitrary keyword arguments and returns the first row found in the `users` table as filtered by the method’s input arguments. No validation of input arguments required at this point.

File: [db.py](./db.py)

### Task 3 (update user)

method: `DB.update_user`

Takes as argument a required `user_id` integer and arbitrary keyword arguments, and returns `None`.

The method will use `find_user_by` to locate the user to update, then will update the user’s attributes as passed in the method’s arguments then commit changes to the database.

If an argument that does not correspond to a user attribute is passed, raise a `ValueError`.

File: [db.py](./db.py)

### Task 4 (Hash password)

method: _`hash_password`

Takes in a `password` string arguments and returns bytes.

The returned bytes is a salted hash of the input password, hashed with `bcrypt.hashpw`.

File: [auth.py](./auth.py)

### Task 5 (Register user)

method: `Auth.register_user` in the `Auth` class

Takes mandatory `email` and `password` string arguments and return a `User` object.

If a user already exist with the passed email, raise a `ValueError` with the message `User <user's email> already exists`.

If not, hash the password with `_hash_password`, save the user to the database using `self._db` and return the `User` object.

File: [auth.py](./auth.py)

### Task 6 (Basic Flask app)

Create a Flask app that has a single `GET` route (`"/"`) and use `flask.jsonify` to return a JSON payload of the form:
```json
{"message": "Bienvenue"}
```

File: [app.py](./app.py)

### Task 7 (Register user)

Implement the end-point to register a user. Define a users function that implements the `POST /users` route.

Import the `Auth` object and instantiate it at the root of the module as such:

The end-point should expect two form data fields: `"email"` and `"password"`. If the user does not exist, the end-point 
should register it and respond with the following JSON payload:

```json
{"email": "<registered email>", "message": "user created"}
```

If the user is already registered, catch the exception and return a JSON payload of the form

```json
{"message": "email already registered"}
```
and return a 400 status code.

File: [app.py](./app.py)

### Task 8 (Credentials validation)

method: `Auth.valid_login`

It should expect `email` and `password` required arguments and return a boolean.

Sample:

```bash
candiepih@ubuntu:~$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

auth.register_user(email, password)

print(auth.valid_login(email, password))

print(auth.valid_login(email, "WrongPwd"))

print(auth.valid_login("unknown@email", password))

candiepih@ubuntu:~$ python3 main.py
True
False
False
candiepih@ubuntu:~$ 
```

File: [auth.py](./auth.py)

### Task 9 (Generate UUIDs)

method: _`generate_uuid` in the `auth` module

The function returns a string representation of a new UUID.

### Task 10 (Get session ID)

method: `Auth.create_session`

Takes an `email` string argument and returns the session ID as a string.

The method should find the user corresponding to the email, generate a new UUID and store it in the database as the user’s `session_id`, then return the session ID.

File: [auth.py](./auth.py)

### Task 11 (Log in)

method: `login` to respond to the `POST /sessions` route.

The request is expected to contain form data with `"email"` and a `"password"` fields.

If the login information is incorrect, use `flask.abort` to respond with a 401 HTTP status.

Otherwise, create a new session for the user, store it the session ID as a cookie with key `"session_id"` on the response and return a JSON payload of the form:

```json
{"email": "<user email>", "message": "logged in"}
```

Sample:

```bash
candiepih@ubuntu:~$ curl -XPOST localhost:5000/users -d 'email=bob@bob.com' -d 'password=mySuperPwd'
{"email":"bob@bob.com","message":"user created"}
candiepih@ubuntu:~$ 
candiepih@ubuntu:~$  curl -XPOST localhost:5000/sessions -d 'email=bob@bob.com' -d 'password=mySuperPwd' -v
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /sessions HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.58.0
> Accept: */*
> Content-Length: 37
> Content-Type: application/x-www-form-urlencoded
> 
* upload completely sent off: 37 out of 37 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 46
< Set-Cookie: session_id=163fe508-19a2-48ed-a7c8-d9c6e56fabd1; Path=/
< Server: Werkzeug/1.0.1 Python/3.7.3
< Date: Wed, 19 Aug 2020 00:12:34 GMT
< 
{"email":"bob@bob.com","message":"logged in"}
* Closing connection 0
candiepih@ubuntu:~$ 
candiepih@ubuntu:~$ curl -XPOST localhost:5000/sessions -d 'email=bob@bob.com' -d 'password=BlaBla' -v
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /sessions HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.58.0
> Accept: */*
> Content-Length: 34
> Content-Type: application/x-www-form-urlencoded
> 
* upload completely sent off: 34 out of 34 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 401 UNAUTHORIZED
< Content-Type: text/html; charset=utf-8
< Content-Length: 338
< Server: Werkzeug/1.0.1 Python/3.7.3
< Date: Wed, 19 Aug 2020 00:12:45 GMT
< 
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>401 Unauthorized</title>
<h1>Unauthorized</h1>
<p>The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required.</p>
* Closing connection 0
candiepih@ubuntu:~$ 
```

File: [app.py](./app.py)

### Task 12 (Find user by session ID)

method: `Auth.get_user_from_session_id`

It takes a single `session_id` string argument and returns the corresponding `User` or `None`.

If the session ID is `None` or no user is found, return `None`. Otherwise return the corresponding user.

File: [auth.py](./auth.py)

### Task 13 (Destroy session)

method: `Auth.destroy_session`

Takes a single `user_id` integer argument and returns `None`.

The method updates the corresponding user’s session ID to `None`.

File: [auth.py](./auth.py)

### Task 14 (Log out)

method: `logout` function to respond to the `DELETE /sessions` route.

The request is expected to contain the session ID as a cookie with key `"session_id"`.

Find the user with the requested session ID. If the user exists destroy the session and redirect the user to `GET /`. If the user does not exist, respond with a 403 HTTP status.

File: [auth.py](./auth.py)

### Task 15 (User profile)

In this task, you will implement a `profile` function to respond to the `GET /profile` route.

The request is expected to contain a `session_id` cookie. Use it to find the user. If the user exist, respond with a 200 HTTP status and the following JSON payload:

```json
{"email": "<user email>"}
```

File: [app.py](./app.py)

### Task 16 (Generate reset password token)

method: `Auth.get_reset_password_token`

It take an email string argument and returns a string.

Find the user corresponding to the `email`. If the user does not exist, raise a `ValueError` exception. If it exists, generate a UUID and update the user’s `reset_token` database field. Return the token.

File: [auth.py](./auth.py)

### Task 17 (Get reset password token)

method: `get_reset_password_token` to respond to the `POST /reset_password` route.

The request is expected to contain form data with the `"email"` field.

If the email is not registered, respond with a 403 status code. Otherwise, generate a token and respond with a 200 HTTP status and the following JSON payload:

```json
{"email": "<user email>", "reset_token": "<reset token>"}
```

File: [app.py](./app.py)

### Task 18 (Update password)

method: `Auth.update_password`

It takes `reset_token` string argument and a `password` string argument and returns `None`.

Use the `reset_token` to find the corresponding user. If it does not exist, raise a `ValueError` exception.

Otherwise, hash the password and update the user’s `hashed_password` field with the new hashed password and the `reset_token` field to `None`.

File: [auth.py](./auth.py)

### Task 19 (Update password end-point)

method: `update_password`  to respond to the `PUT /reset_password` route.

The request is expected to contain form data with fields `"email"`, `"reset_token"` and `"new_password"`.

Update the password. If the token is invalid, catch the exception and respond with a 403 HTTP code.

If the token is valid, respond with a 200 HTTP code and the following JSON payload:

```json
{"email": "<user email>", "message": "Password updated"}
```

### Task 20 (End-to-end integration test)

Start your app. Open a new terminal window.

Create a new module called `main.py`. 

Create one function for each of the following tasks. Use the `requests` module to query your web server for the corresponding end-point.

Use `assert` to validate the response’s expected status code and payload (if any) for each task.

* `register_user(email: str, password: str) -> None`
* `log_in_wrong_password(email: str, password: str) -> None`
* `log_in(email: str, password: str) -> str`
* `profile_unlogged() -> None`
* `profile_logged(session_id: str) -> None`
* `log_out(session_id: str) -> None`
* `reset_password_token(email: str) -> str`
* `update_password(email: str, reset_token: str, new_password: str) -> None`

Running `python main.py`. If everything is correct, you should see no output.
