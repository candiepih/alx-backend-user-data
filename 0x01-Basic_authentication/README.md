# Basic authentication

This topic's aim was to learn what the authentication process means and implement a `Basic Authentication` on a simple API.

Also understanding the following concepts:

* What authentication means 
* What `Base64` is 
* How to `encode` a string in `Base64`
* What Basic authentication means 
* How to send the `Authorization header`

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

### 1. Error handler: Unauthorized

Edit api/v1/app.py:

Add a new error handler for this status code, the response must be:

* a JSON: `{"error": "Unauthorized"}`
* status code `401` 
* you must use `jsonify` from Flask

For testing this new error handler, add a new endpoint in `api/v1/views/index.py`:

* Route: `GET /api/v1/unauthorized`
* This endpoint must raise a 401 error by using `abort`

Files:

[api/v1/app.py](./api/v1/app.py)

[api/v1/views/index.py](./api/v1/views/index.py)

### 2. Error handler: Forbidden

Edit api/v1/app.py:

Add a new error handler for this status code, the response must be:

* a JSON: `{"error": "Forbidden"}`
* status code `403`
* you must use `jsonify` from Flask

For testing this new error handler, add a new endpoint in `api/v1/views/index.py`:

* Route: `GET /api/v1/forbidden`
* This endpoint must raise a `403` error by using `abort`

Files: 

[api/v1/app.py](./api/v1/app.py)

[api/v1/views/index.py](./api/v1/views/index.py)

### 3. Auth class

Create class to manage the API authentication.

* in the file `api/v1/auth/auth.py`
* class name `Auth`
* public method `def require_auth(self, path: str, excluded_paths: List[str]) -> bool:` that returns `False` - path and excluded_paths will be used later, now, you don’t need to take care of them 
* public method `def authorization_header(self, request=None) -> str:` that returns `None` - request will be the Flask request object 
* public method `def current_user(self, request=None) -> TypeVar('User'):` that returns `None` - request will be the Flask request object

This class is the template for all authentication system you will implement.

File: [api/v1/auth/auth.py](./api/v1/auth/auth.py)

### 4. Define which routes don't need authentication

Update the method `def require_auth(self, path: str, excluded_paths: List[str]) -> bool:` in `Auth` that returns `True` if the `path` is not in the list of `strings excluded_paths`:

File: [api/v1/auth/auth.py](./api/v1/auth/auth.py)

### 5. Request validation!

Update the method def authorization_header(self, request=None) -> str: in `api/v1/auth/auth.py`:

* Create a variable `auth` initialized to `None` after the `CORS` definition 
* Based on the environment variable `AUTH_TYPE`, load and assign the right instance of authentication to `auth`
* Otherwise, return the value of the header request `Authorization`

Update the file `api/v1/app.py`:

* Create a variable `auth` initialized to `None` after the `CORS` definition 
* Based on the environment variable `AUTH_TYPE`, load and assign the right instance of authentication to `auth`
    * if `auth`
        * import `Auth` from `api.v1.auth.auth`
        * create an instance of `Auth` and assign it to the variable `auth`

Now the biggest piece is the filtering of each request. For that you will use the Flask method `before_request`

Add a method in `api/v1/app.py` to handler `before_request`

* if `auth` is `None`, do nothing 
* if `request.path` is not part of this list `['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']`, do nothing - you must use the method require_auth from the auth instance 
* if `auth.authorization_header(request)` returns `None`, raise the error `401` - you must use `abort` 
* if `auth.current_user(request)` returns `None`, raise the error `403` - you must use `abort`

Samples:

Terminal 1:
```commandline
candiepih@ubuntu:~$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=auth python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
```

Terminal 2
```commandline
candiepih@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/status"
{
  "status": "OK"
}
candiepih@ubuntu:~$ 
candiepih@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/status/"
{
  "status": "OK"
}
candiepih@ubuntu:~$ 
candiepih@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/users"
{
  "error": "Unauthorized"
}
candiepih@ubuntu:~$
candiepih@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/users" -H "Authorization: Test"
{
  "error": "Forbidden"
}
candiepih@ubuntu:~$
```

Files: 

[api/v1/app.py](./api/v1/app.py)

[api/v1/auth/auth.py](./api/v1/auth/auth.py)


### 6. Basic auth

Create a class `BasicAuth` that inherits from `Auth`. For the moment this class will be empty.

Update `api/v1/app.py` for using `BasicAuth` class instead of Auth depending of the value of the environment variable `AUTH_TYPE`, If `AUTH_TYPE` is equal to `basic_auth`:

* import `BasicAuth` from `api.v1.auth.basic_auth`
* create an instance of `BasicAuth` and assign it to the variable `auth`

Files: 

[api/v1/app.py](./api/v1/app.py)

[api/v1/auth/basic_auth.py](./api/v1/auth/basic_auth.py)


### 7. Basic - Base64 part

Add the method `def extract_base64_authorization_header(self, authorization_header: str) -> str:` in the class `BasicAuth` that returns the Base64 part of the `Authorization` header for a Basic Authentication

File: [api/v1/auth/basic_auth.py](./api/v1/auth/basic_auth.py)

### 8. Basic - Base64 decode

Add the method `def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:` in the class `BasicAuth` that returns the decoded value of a Base64 string `base64_authorization_header`:

File: [api/v1/auth/basic_auth.py](./api/v1/auth/basic_auth.py)

### 9. Basic - User credentials

Add the method `def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str)` in the class `BasicAuth` that returns the user `email` and `password` from the `Base64 decoded` value.

File: [api/v1/auth/basic_auth.py](./api/v1/auth/basic_auth.py)

### 10. Basic - User object

Add the method `def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):` in the class `BasicAuth` that returns the `User` instance based on his email and password.

File: [api/v1/auth/basic_auth.py](./api/v1/auth/basic_auth.py)

### 11. Basic - Overload current_user - and BOOM!

Now, you have all pieces for having a complete Basic authentication.

Add the `method def current_user(self, request=None) -> TypeVar('User')` in the class `BasicAuth` that overloads `Auth` and retrieves the `User` instance for a request:

File: [api/v1/auth/basic_auth.py](./api/v1/auth/basic_auth.py)

### 12. Basic - Allow password with ":"

Improve the method `def extract_user_credentials(self, decoded_base64_authorization_header)` to allow password with `:`.

File: [api/v1/auth/basic_auth.py](./api/v1/auth/basic_auth.py)

### 13. Require auth with stars

Improve `def require_auth(self, path, excluded_paths)` by allowing `*` at the end of `excluded paths`.

Example for `excluded_paths = ["/api/v1/stat*"]`:

* `/api/v1/users` will return `True`
* `/api/v1/status` will return `False`
* `/api/v1/stats` will return `False`

File: [api/v1/auth/auth.py](./api/v1/auth/auth.py)

