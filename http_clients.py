import http_requests
from logger_config import loguru_looger as logger

base_endpoint = "api/v1"


def request_auth_token(username: str, password: str):
    """
    curl 'http://127.0.0.1:5000/auth/oauth2/token?grant_type=password&client_id=documentation&username=root&password=q'
    """
    endpoint = "auth/oauth2/token"
    paras = {
        "grant_type": "password",
        "client_id": "documentation",
        "username": username,
        "password": password,
    }
    client = http_requests.SimpleFlaskClientWithHeaders()
    code, resp = client.get(endpoint, params=paras)
    try:
        if code == 401:
            logger.warning(
                f"Unauthorized account {username}/{password}. Check and try again."
            )
            return None
        elif code == 200:
            logger.info(f"Get token of {username}")
            logger.info(f"Username:{username};Token_type:{resp['token_type']};")
            logger.info(
                f"Access:{resp['access_token']};Refresh:{resp['refresh_token']}"
            )
            logger.info(f"Scope:{resp['scope']}")
            return resp
        else:
            # Unhandled exception or error
            logger.warning(f"Unhandled exception: Code {code}")
            return None
    except Exception as e:
        logger.exception(f"捕获到未处理的异常：{e}")


def refresh_token(username: str, refresh_token: str):
    endpoint = "auth/oauth2/token"
    paras = {
        "grant_type": "refresh_token",
        "client_id": "documentation",
        "refresh_token": refresh_token,
    }
    client = http_requests.SimpleFlaskClientWithHeaders()
    code, resp = client.get(endpoint, params=paras)
    try:
        if code == 200:
            logger.info(f"Get refreshed token for {username}")
            logger.info(
                f"Access:{resp['access_token']};Refresh:{resp['refresh_token']}"
            )
            logger.info(f"Scope:{resp['scope']}")
            return resp
        else:
            # Unhandled exception or error
            logger.warning(f"Unhandled exception: Code {code}")
            return None
    except Exception as e:
        logger.exception(f"捕获到未处理的异常：{e}")


def list_user(access_token, username):
    """
    [{
        "last_name": "",
        "middle_name": "",
        "first_name": "",
        "id": 1,
        "username": "root"
    },...]"""
    endpoint = f"{base_endpoint}/users/"
    token = f"Bearer {access_token}"
    header = {"Authorization": token}
    logger.info(f"[{endpoint}] User {username} tries to list users")
    client = http_requests.SimpleFlaskClientWithHeaders()
    code, resp = client.get(endpoint, headers=header)
    try:
        if code == 200:
            logger.info(
                f"Get users list:{[(user['id'],user['username']) for user in resp]}"
            )
            return resp
        else:
            # Unhandled exception or error
            logger.warning(f"Unhandled error: Code {code}")
    except Exception as e:
        logger.exception(f"捕获到未处理的异常：{e}")


def create_user(access_token, form_dict: dict):
    """
    NOTE: due to recaptcha_key is needed to create user except admin, only admin can send this request to bypass the recaptcha
    NOTE: e-mail must be vaild
    Use dict to input signup forms
    Dictform shoule include:
    username first_name middle_name last_name email password
    """
    endpoint = f"{base_endpoint}/users/"
    token = f"Bearer {access_token}"
    header = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": token,
    }
    try:
        logger.info(
            f"Trying to create user by {form_dict['username']}:{form_dict['password']} with email {form_dict['email']}"
        )
        client = http_requests.SimpleFlaskClientWithHeaders()
        code, resp = client.post(endpoint, headers=header, data=form_dict)
        if code == 200:
            logger.info(f"User {resp['username']} created")
            # TODO activate the user
            # TODO get_user_detail_by_id
            return resp
        else:
            # Unhandled exception or error
            logger.warning(f"Unhandled error: Code {code}")
    except Exception as e:
        logger.exception(f"Unhandled exception:{e}")


def get_user_detail_by_id(access_token, id: int) -> bool:
    """
    NOTE:Only admin can do
    """
    endpoint = f"{base_endpoint}/users/{str(id)}"
    token = f"Bearer {access_token}"
    header = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": token,
    }
    logger.info(f"Trying to query user {id}")
    try:
        client = http_requests.SimpleFlaskClientWithHeaders()
        code, resp = client.get(endpoint, headers=header)
        if code == 200:
            logger.info(f"Get user {id}'s detail: {resp['username']}")
            return True
        elif code == 404:
            logger.warning(f"User {id} not found")
            return False
        else:
            # Unhandled exception or error
            logger.warning(f"Unhandled error: Code {code}")
            return False
    except Exception as e:
        logger.exception(f"Unhandled exception:{e}")


def patch_user_by_id():
    """
    Not implemented yet
    """
    pass


def list_teams(access_token, username):
    """
        [
        {
            "id": 1,
            "title": "team1"
        }
    ]
    """
    endpoint = f"{base_endpoint}/teams/"
    token = f"Bearer {access_token}"
    header = {"Authorization": token}
    logger.info(f"[{endpoint}] User {username} tries to list teams")
    client = http_requests.SimpleFlaskClientWithHeaders()
    code, resp = client.get(endpoint, headers=header)
    try:
        if code == 200:
            logger.info(
                f"Get teams list:{[(team['id'],team['title']) for team in resp]}"
            )
            return resp
        else:
            # Unhandled exception or error
            logger.warning(f"Unhandled error: Code {code}")
            return None
    except Exception as e:
        logger.exception(f"捕获到未处理的异常：{e}")


def get_team_detail_by_id(access_token, id: int) -> bool:
    """
    NOTE:Only admin can do
    """
    endpoint = f"{base_endpoint}/teams/{str(id)}"
    token = f"Bearer {access_token}"
    header = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": token,
    }
    logger.info(f"Trying to query team {id}")
    try:
        client = http_requests.SimpleFlaskClientWithHeaders()
        code, resp = client.get(endpoint, headers=header)
        if code == 200:
            logger.info(f"Get team {id}'s detail: {resp['title']}")
            return True
        elif code == 404:
            logger.warning(f"Team {id} not found")
            return False
        else:
            # Unhandled exception or error
            logger.warning(f"Unhandled error: Code {code}")
            return False
    except Exception as e:
        logger.exception(f"Unhandled exception:{e}")


def patch_team_by_id():
    """
    Not implemented yet
    NOTE Only admin can do
    TODO Impment it when multi-user required
    """

    pass


def del_team_by_id(access_token, id: int) -> bool:
    """
    NOTE: Only admin can do
    """
    endpoint = f"{base_endpoint}/teams/{str(id)}"
    token = f"Bearer {access_token}"
    header = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": token,
    }
    logger.info(f"Trying to delete team {id}")
    try:
        client = http_requests.SimpleFlaskClientWithHeaders()
        code, resp = client.delete(endpoint, headers=header)
        if code == 204 or code == 200:
            logger.info(f"Team {id} deleted, return nothing")
            return True
        elif code == 404:
            logger.warning(f"Team {id} not found")
            return False
        else:
            # Unhandled exception or error
            logger.warning(f"Unhandled error: Code {code}")
            return False
    except Exception as e:
        logger.exception(f"Unhandled exception:{e}")


def list_members_in_team(access_token, id: int):
    """
    NOTE: Only admin can do
    NOTE: Members no more than 100.
    """
    endpoint = f"{base_endpoint}/teams/{str(id)}/members/"
    token = f"Bearer {access_token}"
    header = {"Authorization": token}
    logger.info(f"Trying to list all members in the team {id}")
    data = {"limit": 100}
    try:
        client = http_requests.SimpleFlaskClientWithHeaders()
        code, resp = client.get(endpoint, headers=header, params=data)
        if code == 200:
            logger.info(
                f"Team {id} has the following members:{[(user['user']['id'],user['user']['username']) for user in resp]}"
            )
            return True
        elif code == 404:
            logger.warning(f"Team {id} not found")
            return False
        else:
            # Unhandled exception or error
            logger.warning(f"Unhandled error: Code {code}")
            return False
    except Exception as e:
        logger.exception(f"Unhandled exception:{e}")


def add_member_to_team(
    access_token, team_id: int, user_id: int, is_leader: bool
) -> bool:
    """
    NOTE: Only admin can do
    """
    endpoint = f"{base_endpoint}/teams/{str(team_id)}/members/"
    token = f"Bearer {access_token}"
    header = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": token,
    }

    data = {"user_id": user_id, "is_leader": is_leader}
    logger.info(f"Trying to add user {user_id} to team {team_id}")
    try:
        client = http_requests.SimpleFlaskClientWithHeaders()
        code, resp = client.post(endpoint, headers=header, data=data)
        if code == 200:
            logger.info(f"User {user_id} has been added to team {team_id}")
            return True
        elif code == 404:
            logger.warning(f"Team {team_id} or user {user_id} not found")
            return False
        else:
            # Unhandled exception or error
            logger.warning(f"Unhandled error: Code {code}")
            return False
    except Exception as e:
        logger.exception(f"Unhandled exception:{e}")


def delete_member_from_team(access_token, team_id: int, user_id: int):
    """
    NOTE: Only admin can do
    """
    endpoint = f"{base_endpoint}/teams/{str(team_id)}/members/{str(user_id)}"
    token = f"Bearer {access_token}"
    header = {"Authorization": token}

    logger.info(f"Trying to remove user {user_id} from team {team_id}")
    try:
        client = http_requests.SimpleFlaskClientWithHeaders()
        code, resp = client.delete(endpoint, headers=header)
        if code == 204 or code == 200:
            logger.info(f"User {user_id} has been removed to team {team_id}")
            return True
        elif code == 404:
            logger.warning(f"Team {team_id} or user {user_id} not found")
            return False
        else:
            # Unhandled exception or error
            logger.warning(f"Unhandled error: Code {code}")
            return False
    except Exception as e:
        logger.exception(f"Unhandled exception:{e}")


def create_team(access_token, username, teamname):
    """
    Any activate user is OK
    """
    endpoint = f"{base_endpoint}/teams/"
    token = f"Bearer {access_token}"
    header = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": token,
    }
    logger.info(f"User {username} tries to create a team")
    try:
        client = http_requests.SimpleFlaskClientWithHeaders()
        code, resp = client.post(endpoint, headers=header, data={"title": teamname})
        if code == 200:
            logger.info(f"Team {resp['title']} created")
            return resp
        else:
            # Unhandled exception or error
            logger.warning(f"Unhandled error: Code {code}")
    except Exception as e:
        logger.exception(f"Unhandled exception:{e}")
