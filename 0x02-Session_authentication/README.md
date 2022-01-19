# Session authentication

This topic's aim was to understand how to authenticate a users using session authentication.

Also understanding the following concepts:

* What `authentication` means 
* What `session authentication` means 
* What `Cookies` are 
* How to send Cookies 
* How to parse Cookies

## Simple API

Simple HTTP API for playing with `User` model.


## Files

### `models/`

- `base.py`: base of all models of the API - handle serialization to file
- `user.py`: user model

### `api/v1`

- `app.py`: entry point of the API
- `views/index.py`: basic endpoints of the API: `/status` and `/stats`
- `views/users.py`: all users endpoints


## Setup

```
$ pip3 install -r requirements.txt
```


## Run

```
$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
```


## Routes

- `GET /api/v1/status`: returns the status of the API
- `GET /api/v1/stats`: returns some stats of the API
- `GET /api/v1/users`: returns the list of users
- `GET /api/v1/users/:id`: returns an user based on the ID
- `DELETE /api/v1/users/:id`: deletes an user based on the ID
- `POST /api/v1/users`: creates a new user (JSON parameters: `email`, `password`, `last_name` (optional) and `first_name` (optional))
- `PUT /api/v1/users/:id`: updates an user based on the ID (JSON parameters: `last_name` and `first_name`)


## Tasks

### Task 0

Add a new endpoint: `GET /users/me` to retrieve the authenticated `User` object.

Files:

[api/v1/app.py](./api/v1/app.py)

[api/v1/views/users.py](./api/v1/views/users.py)

### Task 1 

Create a class `SessionAuth` that inherits from `Auth`.

Update `api/v1/app.py` for using `SessionAuth` instance for the variable auth depending of the value of the environment variable `AUTH_TYPE`, If `AUTH_TYPE` is equal to `session_auth`

* import `SessionAuth` from `api.v1.auth.session_auth`
* create an instance of `SessionAuth` and assign it to the variable `auth`

Files: 

[api/v1/app.py](./api/v1/app.py)

[api/v1/auth/session_auth.py](./api/v1/auth/session_auth.py)

### Task 2 (Create a session)

Update `SessionAuth` class:

* Create a class attribute `user_id_by_session_id` initialized by an empty dictionary 
* Create an instance method `def create_session(self, user_id: str = None) -> str:` that creates a Session ID for a `user_id`

File: [api/v1/auth/session_auth.py](./api/v1/auth/session_auth.py)

### Task 3 (User ID for Session ID)

Update `SessionAuth` class:

Create an instance method `def user_id_for_session_id(self, session_id: str = None) -> str:` that returns a `User` ID based on a Session ID:

File: [api/v1/auth/session_auth.py](./api/v1/auth/session_auth.py)

### Task 4 (Session Cookie)

Update `api/v1/auth/auth.py` by adding the method `def session_cookie(self, request=None):` that returns a cookie value from a request:

File: [api/v1/auth/auth.py](./api/v1/auth/auth.py)


### Task 5 (Before request)

Update the `@app.before_request` method in `api/v1/app.py`:

* Add the URL path `/api/v1/auth_session/login/` in the list of excluded paths of the method `require_auth` - this route doesn’t exist yet but it should be accessible outside authentication
* If `auth.authorization_header(request)` and `auth.session_cookie(request) return `None`, `abort(401)`


Sample output:

Terminal 1:
```commandline
candiepih@ubuntu:~$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=session_auth SESSION_NAME=_my_session_id python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
```

Terminal 2:
```commandline
candiepih@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/status"
{
  "status": "OK"
}
candiepih@ubuntu:~$
candiepih@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/auth_session/login" # not found but not "blocked" by an authentication system
{
  "error": "Not found"
}
candiepih@ubuntu:~$
candiepih@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/users/me"
{
  "error": "Unauthorized"
}
candiepih@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/users/me" -H "Authorization: Basic Ym9iQGhidG4uaW86SDBsYmVydG9uU2Nob29sOTgh" # Won't work because the environment variable AUTH_TYPE is equal to "session_auth"
{
  "error": "Forbidden"
}
candiepih@ubuntu:~$
candiepih@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/users/me" --cookie "_my_session_id=5535d4d7-3d77-4d06-8281-495dc3acfe76" # Won't work because no user is linked to this Session ID
{
  "error": "Forbidden"
}
candiepih@ubuntu:~$
```

File: [api/v1/app.py](./api/v1/app.py)

### Task 6 (Use Session ID for identifying a User)

Update `SessionAuth` class:

Create an instance method `def current_user(self, request=None):` (overload) that returns a `User` instance based on a cookie value.

File: [api/v1/auth/session_auth.py](./api/v1/auth/session_auth.py)

### Task 7 (New view for Session Authentication)

Create a new Flask view that handles all routes for the Session authentication.

In the file `api/v1/views/session_auth.py`, create a route POST `/auth_session/login` (`= POST /api/v1/auth_session/login`):

* If `email` is missing or empty, return the JSON `{ "error": "email missing" }` with the status code `400`
* If `password` is missing or empty, return the JSON `{ "error": "password missing" }` with the status code `400`
* Retrieve the `User` instance based on the `email` - you must use the class method `search` of `User` (same as the one used for the `BasicAuth`)

    * If no `User` found, return the JSON `{ "error": "no user found for this email" }` with the status code `404`
    * If the `password` is not the one of the `User` found, return the JSON `{ "error": "wrong password" }` with the status code `401`
    * Otherwise, create a Session ID for the `User` ID

* In the file `api/v1/views/__init__.py`, add this new view at the end of the file.

Sample output:

Terminal 1:
```commandline
candiepih@ubuntu:~$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=session_auth SESSION_NAME=_my_session_id python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
```

Terminal 2:
```commandline
candiepih@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/auth_session/login" -XGET
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>405 Method Not Allowed</title>
<h1>Method Not Allowed</h1>
<p>The method is not allowed for the requested URL.</p>
candiepih@ubuntu:~$
candiepih@ubuntu:~$  curl "http://0.0.0.0:5000/api/v1/auth_session/login" -XPOST
{
  "error": "email missing"
}
candiepih@ubuntu:~$ 
candiepih@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/auth_session/login" -XPOST -d "email=guillaume@hbtn.io"
{
  "error": "password missing"
}
candiepih@ubuntu:~$ 
candiepih@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/auth_session/login" -XPOST -d "email=guillaume@hbtn.io" -d "password=test"
{
  "error": "no user found for this email"
}
candiepih@ubuntu:~$
candiepih@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/auth_session/login" -XPOST -d "email=bobsession@hbtn.io" -d "password=test"
{
  "error": "wrong password"
}
candiepih@ubuntu:~$
candiepih@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/auth_session/login" -XPOST -d "email=bobsession@hbtn.io" -d "password=fake pwd"
{
  "created_at": "2017-10-16 04:23:04", 
  "email": "bobsession@hbtn.io", 
  "first_name": null, 
  "id": "cf3ddee1-ff24-49e4-a40b-2540333fe992", 
  "last_name": null, 
  "updated_at": "2017-10-16 04:23:04"
}
candiepih@ubuntu:~$
candiepih@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/auth_session/login" -XPOST -d "email=bobsession@hbtn.io" -d "password=fake pwd" -vvv
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 0.0.0.0...
* TCP_NODELAY set
* Connected to 0.0.0.0 (127.0.0.1) port 5000 (#0)
> POST /api/v1/auth_session/login HTTP/1.1
> Host: 0.0.0.0:5000
> User-Agent: curl/7.54.0
> Accept: */*
> Content-Length: 42
> Content-Type: application/x-www-form-urlencoded
> 
* upload completely sent off: 42 out of 42 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Set-Cookie: _my_session_id=df05b4e1-d117-444c-a0cc-ba0d167889c4; Path=/
< Access-Control-Allow-Origin: *
< Content-Length: 210
< Server: Werkzeug/0.12.1 Python/3.4.3
< Date: Mon, 16 Oct 2017 04:57:08 GMT
< 
{
  "created_at": "2017-10-16 04:23:04", 
  "email": "bobsession@hbtn.io", 
  "first_name": null, 
  "id": "cf3ddee1-ff24-49e4-a40b-2540333fe992", 
  "last_name": null, 
  "updated_at": "2017-10-16 04:23:04"
}
* Closing connection 0
candiepih@ubuntu:~$ 
candiepih@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/users/me" --cookie "_my_session_id=df05b4e1-d117-444c-a0cc-ba0d167889c4"
{
  "created_at": "2017-10-16 04:23:04", 
  "email": "bobsession@hbtn.io", 
  "first_name": null, 
  "id": "cf3ddee1-ff24-49e4-a40b-2540333fe992", 
  "last_name": null, 
  "updated_at": "2017-10-16 04:23:04"
}
candiepih@ubuntu:~$
```

Files: 

[api/v1/views/session_auth.py](./api/v1/views/session_auth.py)

[api/v1/auth/__init__.py](./api/v1/auth/__init__.py)

### Task 8 (Logout)

Update the class SessionAuth by adding a new method `def destroy_session(self, request=None):` that deletes the user session / logout:

* If the `request` is equal to `None`, return `False`
* If the `request` doesn’t contain the Session ID cookie, return `False` - you must use `self.session_cookie(request)`
* If the Session ID of the request is not linked to any User ID, return `False` - you must use `self.user_id_for_session_id(...)`
* Otherwise, delete in `self.user_id_by_session_id` the Session ID (as key of this dictionary) and return `True`

Update the file `api/v1/views/session_auth.py`, by adding a new route `DELETE /api/v1/auth_session/logout`:

* You must use from `api.v1.app import auth`
* You must use `auth.destroy_session(request)` for deleting the Session ID contains in the request as cookie:
    * If `destroy_session` returns `False`, `abort(404)`
    * Otherwise, return an empty JSON dictionary with the status code 200

Files: 

[api/v1/auth/session_auth.py](./api/v1/auth/session_auth.py)

[api/v1/views/session_auth.py](./api/v1/views/session_auth.py)

### Task 9 (Expiration?)

Now you will add an expiration date to a Session ID.

Create a class `SessionExpAuth` that inherits from `SessionAuth` in the file `api/v1/auth/session_exp_auth.py`:

Overload `def __init__(self)`: method

* Assign an instance attribute `session_duration`

Overload `def create_session(self, user_id=None)`

* Create a Session ID by calling `super()` - `super()` will call the `create_session()` method of `SessionAuth`
* Return `None` if `super()` can’t create a Session ID 
* Use this Session ID as key of the dictionary `user_id_by_session_id` - the value for this key must be a dictionary (called “session dictionary”):
    * The key `user_id` must be set to the variable `user_id` 
    * The key `created_at` must be set to the current `datetime` - you must use `datetime.now()`
* Return the Session ID created

Overload `def user_id_for_session_id(self, session_id=None)`:

* Return the `user_id` key from the session dictionary if `self.session_duration` is equal or under 0 
* Return `None` if session dictionary doesn’t contain a key `created_at`
* Return `None` if the `created_at` + `session_duration` seconds are before the current datetime. `datetime - timedelta` 
* Otherwise, return `user_id` from the session dictionary

Update `api/v1/app.py` to instantiate auth with `SessionExpAuth` if the environment variable `AUTH_TYPE` is equal to `session_exp_auth`.

Sample output:

Terminal 1:
```commandline
candiepih@ubuntu:~$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=session_exp_auth SESSION_NAME=_my_session_id SESSION_DURATION=60 python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
```
Terminal 2:
```commandline
candiepih@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/auth_session/login" -XPOST -d "email=bobsession@hbtn.io" -d "password=fake pwd" -vvv
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 0.0.0.0...
* TCP_NODELAY set
* Connected to 0.0.0.0 (127.0.0.1) port 5000 (#0)
> POST /api/v1/auth_session/login HTTP/1.1
> Host: 0.0.0.0:5000
> User-Agent: curl/7.54.0
> Accept: */*
> Content-Length: 42
> Content-Type: application/x-www-form-urlencoded
> 
* upload completely sent off: 42 out of 42 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Set-Cookie: _my_session_id=eea5d963-8dd2-46f0-9e43-fd05029ae63f; Path=/
< Access-Control-Allow-Origin: *
< Content-Length: 210
< Server: Werkzeug/0.12.1 Python/3.4.3
< Date: Mon, 16 Oct 2017 04:57:08 GMT
< 
{
  "created_at": "2017-10-16 04:23:04", 
  "email": "bobsession@hbtn.io", 
  "first_name": null, 
  "id": "cf3ddee1-ff24-49e4-a40b-2540333fe992", 
  "last_name": null, 
  "updated_at": "2017-10-16 04:23:04"
}
* Closing connection 0
candiepih@ubuntu:~$
candiepih@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/users/me" --cookie "_my_session_id=eea5d963-8dd2-46f0-9e43-fd05029ae63f"
{
  "created_at": "2017-10-16 04:23:04", 
  "email": "bobsession@hbtn.io", 
  "first_name": null, 
  "id": "cf3ddee1-ff24-49e4-a40b-2540333fe992", 
  "last_name": null, 
  "updated_at": "2017-10-16 04:23:04"
}
candiepih@ubuntu:~$
candiepih@ubuntu:~$ sleep 10
candiepih@ubuntu:~$
candiepih@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/users/me" --cookie "_my_session_id=eea5d963-8dd2-46f0-9e43-fd05029ae63f"
{
  "created_at": "2017-10-16 04:23:04", 
  "email": "bobsession@hbtn.io", 
  "first_name": null, 
  "id": "cf3ddee1-ff24-49e4-a40b-2540333fe992", 
  "last_name": null, 
  "updated_at": "2017-10-16 04:23:04"
}
candiepih@ubuntu:~$ 
candiepih@ubuntu:~$ sleep 51 # 10 + 51 > 60
candiepih@ubuntu:~$ 
candiepih@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/users/me" --cookie "_my_session_id=eea5d963-8dd2-46f0-9e43-fd05029ae63f"
{
  "error": "Forbidden"
}
candiepih@ubuntu:~$
```

Files: 

[api/v1/auth/session_exp_auth.py](./api/v1/auth/session_exp_auth.py)

[api/v1/app.py](./api/v1/app.py)


### Task 10 (Sessions in database)

Since the beginning, all Session IDs are stored in memory. It means, if your application stops, all Session IDs are lost.

For avoid that, you will create a new authentication system, based on Session ID stored in database (for us, it will be in a file, like `User`).

Create a new model `UserSession` in `models/user_session.py` that inherits from `Base`:

* Implement the `def __init__(self, *args: list, **kwargs: dict):`
    * `user_id`: string 
    * `session_id`: string

Create a new authentication class `SessionDBAuth` in `api/v1/auth/session_db_auth.py` that inherits from `SessionExpAuth`:

* Overload `def create_session(self, user_id=None):` that creates and stores new instance of `UserSession` and returns the Session ID 
* Overload `def user_id_for_session_id(self, session_id=None):` that returns the User ID by requesting `UserSession` in the database based on `session_id` 
* Overload `def destroy_session(self, request=None):` that destroys the UserSession based on the Session ID from the request cookie

Update `api/v1/app.py` to instantiate auth with `SessionDBAuth` if the environment variable `AUTH_TYPE` is equal to `session_db_auth`

Files:

[api/v1/auth/session_db_auth.py](./api/v1/auth/session_db_auth.py)

[api/v1/app.py](./api/v1/app.py)

[models/user_session.py](./models/user_session.py)
