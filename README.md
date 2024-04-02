# Random test
## Description
This application comes with a built-in functionality that allows you to generate random activity data, simulating real-world usage patterns for testing and demonstration purposes.

Repo is based on https://github.com/iridium-soda/flask-restplus-server-example
## Usage:
1. First steup the target container by simply pulling an image:
    ```shell
    docker run -it --rm --publish 5000:5000 frolvlad/flask-restplus-server-example
    ```
2. Run this script and do data gathering.
    ```shell
    python main.py
    ```
## Activites

Use the following to grant token to access the container:
```
curl 'http://127.0.0.1:5000/auth/oauth2/token?grant_type=password&client_id=documentation&username=root&password=q'
```
```json
{
    "token_type": "Bearer",
    "access_token": "oqvUpO4aKg5KgYK2EUY2HPsbOlAyEZ",
    "refresh_token": "3UTjLPlnomJPx5FvgsC2wS7GfVNrfH",
    "expires_in": 3600,
    "scope": "auth:read auth:write users:read users:write teams:read teams:write"
}
```

Refresh once expired:
```shell
curl --header 'Authorization: Bearer oqvUpO4aKg5KgYK2EUY2HPsbOlAyEZ' 'http://127.0.0.1:5000/api/v1/users/me'
```
```json
{
    "id": 1,
    "username": "root",
    "email": "root@localhost",
    "first_name": "",
    "middle_name": "",
    "last_name": "",
    "is_active": true,
    "is_regular_user": true,
    "is_admin": true,
    "created": "2016-10-20T14:00:35.912576+00:00",
    "updated": "2016-10-20T14:00:35.912602+00:00"
}
```

Then put token into header:
```shell
curl --header 'Authorization: Bearer oqvUpO4aKg5KgYK2EUY2HPsbOlAyEZ' 'http://127.0.0.1:5000/api/v1/users/me'
```
```json
{
    "id": 1,
    "username": "root",
    "email": "root@localhost",
    "first_name": "",
    "middle_name": "",
    "last_name": "",
    "is_active": true,
    "is_regular_user": true,
    "is_admin": true,
    "created": "2016-10-20T14:00:35.912576+00:00",
    "updated": "2016-10-20T14:00:35.912602+00:00"
}
```

The following activities can be used to traverse:
![](https://raw.githubusercontent.com/frol/flask-restplus-server-example/master/docs/static/Flask_RESTplus_Example_API.png)

## Design
- Tend to create user when number of user is lower than `THREHOLD`
- When number of users reach a threhold, stop creating users
- Need to be activated after signing up 

## Example

To create a user:
```shell
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -H "Authorization: Bearer sraetNjxofQcEOo2FGBNtNbe0ORAuH" \
     -d "username=upd&email=roupdot@gmail.com&password=asu&first_name=&middle_name=&last_name="
```
```json
{
    "last_name": "",
    "is_active": false,
    "middle_name": "",
    "updated": "2024-04-02T09:23:29.154503+00:00",
    "email": "roupdot@gmail.com",
    "is_admin": false,
    "first_name": "",
    "id": 5,
    "created": "2024-04-02T09:23:29.154487+00:00",
    "username": "upd",
    "is_regular_user": false
}
```

Query user by id:
```
curl --header 'Authorization: Bearer pWsIkHvfmLbU42jMl4xwyjJAASNMRN' 'http://127.0.0.1:5000/api/v1/users/3'
```
```json
{
    "last_name": "",
    "is_active": true,
    "middle_name": "",
    "updated": "2024-04-02T02:16:58.276672+00:00",
    "email": "user@localhost",
    "is_admin": false,
    "first_name": "",
    "id": 3,
    "created": "2024-04-02T02:16:58.276660+00:00",
    "username": "user",
    "is_regular_user": true
}
```

To create a team:
```shell
curl -X POST "http://127.0.0.1:5000/api/v1/teams/"\
    -H "Content-Type: application/x-www-form-urlencoded"\
    -H "Authorization: Bearer pWsIkHvfmLbU42jMl4xwyjJAASNMRN"\
    -d "title=team1"
```
```json
{
    "updated": "2024-04-02T12:30:49.046892+00:00",
    "title": "team1",
    "members": [
        {
            "is_leader": true,
            "user": {
                "last_name": "",
                "middle_name": "",
                "first_name": "",
                "id": 1,
                "username": "root"
            }
        }
    ],
    "id": 1,
    "created": "2024-04-02T12:30:49.046875+00:00"
}
```

To list all members in a team:
```shell
curl --header 'Authorization: Bearer pWsIkHvfmLbU42jMl4xwyjJAASNMRN' 'http://127.0.0.1:5000/api/v1/teams/1/members/'
```
```json
[
    {
        "is_leader": true,
        "user": {
            "last_name": "",
            "middle_name": "",
            "first_name": "",
            "id": 1,
            "username": "root"
        },
        "team": {
            "id": 1,
            "title": "team1"
        }
    }
]
```