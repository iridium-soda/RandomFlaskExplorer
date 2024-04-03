"""
call id:
"""

from logger_config import loguru_looger as logger
import random
from http_clients import *
import os
import string

op_list = [
    "request_auth_token",
    "refresh_token",
    "list_user",
    "create_user",
    "get_user_detail_by_id",
    "list_teams",
    "get_team_detail_by_id",
    "del_team_by_id",
    "list_members_in_team",
    "add_member_to_team",
    "delete_member_from_team",
    "create_team",
]
users_list = [
    {"id": 1, "username": "root", "password": "q", "admin": True},
    {"id": 3, "username": "user", "password": "w", "admin": False},
]
teams_list = (
    []
)  # Should be {id,title,members:[{"id": 1, "username": "root", "password": "q", "admin": True}]}
acc_token, ref_token = None, None
current_user_id = 1  # TODO To be implemented when adding multi-users support
current_user_name = "root"  # TODO To be implemented when adding multi-users support
# [(1, 'root'), (2, 'documentation'), (3, 'user'), (4, 'internal')]
# 提权好像是用PATCH
# NOTE All commands are executed by admin


def do_api(op_name):
    global acc_token, ref_token
    if op_name == "request_auth_token":
        user = query_user_in_list(current_user_id)
        password = user["password"]
        resp = request_auth_token(current_user_name, password)
        acc_token, ref_token = resp["access_token"], resp["refresh_token"]
    elif op_name == "refresh_token":
        resp = refresh_token(current_user_name, ref_token)
        acc_token, ref_token = resp["access_token"], resp["refresh_token"]
    elif op_name == "list_user":
        list_user(acc_token, current_user_name)
    elif op_name == "create_user":
        if len(users_list) >= 20:
            logger.info(f"Too many users(over 20), skip the signup operation.")
            return
        password = gen_string()
        resp = create_user(
            access_token=acc_token,
            form_dict={
                "username": gen_string(),
                "email": gen_email(),
                "password": password,
                "first_name": gen_string(special_char=False),
                "middle_name": gen_string(special_char=False),
                "last_name": gen_string(special_char=False),
            },
        )
        if resp:
            user_info = {
                "id": resp["id"],
                "username": resp["username"],
                "password": password,
                "admin": False,
            }
            users_list.append(user_info)
        else:
            logger.warning(f"Creating user failed")

    elif op_name == "get_user_detail_by_id":
        user = random.choice(users_list)
        resp = get_user_detail_by_id(access_token=acc_token, id=user["id"])
    elif op_name == "list_teams":
        list_teams(acc_token, current_user_name)
    elif op_name == "get_team_detail_by_id":
        if len(teams_list) == 0:
            logger.info(f"No team listed, skip listing teams")
            return
        team = random.choice(teams_list)
        get_team_detail_by_id(acc_token, team["id"])
    elif op_name == "del_team_by_id":
        if len(teams_list) == 0:
            logger.info(f"No team listed, skip deleting teams")
            return
        team_index = random.randint(0, len(teams_list) - 1)
        team = teams_list[team_index]
        if del_team_by_id(acc_token, team["id"]):
            # Update teamlist
            _ = teams_list.pop[team_index]
        else:
            logger.warning(f"Remove team {team['title']} failed")

    elif op_name == "list_members_in_team":
        if len(teams_list) == 0:
            logger.info(f"No team listed, skip listing members in team")
            return
        team = random.choice(teams_list)
        list_members_in_team(acc_token, team["id"])
    elif op_name == "add_member_to_team":
        if len(teams_list) == 0:
            logger.info(f"No team listed, skip adding members in team")
            return
        team_index = random.randint(0, len(teams_list) - 1)
        team = teams_list[team_index]
        unexist_users = [user for user in users_list if user not in team["members"]]
        if len(unexist_users) == 0:
            logger.info(
                f"No user out of this team:{team['title']}, skip adding members in team"
            )
            return
        user = random.choice(unexist_users)
        if add_member_to_team(
            acc_token, team["id"], user["id"], random.choice([True, False])
        ):
            # Update team member list
            teams_list[team_index]["members"].append(user)
        else:
            logger.warning(
                f"Join user {user['username']} to team {team['title']} failed"
            )
    elif op_name == "delete_member_from_team":
        if len(teams_list) == 0:
            logger.info(f"No team listed, skip deleting members in team")
            return
        team_index = random.randint(0, len(teams_list) - 1)
        team = teams_list[team_index]
        # NOTE: Assumption: all team's leader is root. Assumption failed after adding multi-user support
        if len(team["members"]) <= 1:
            logger.info(
                f"No user can be removed from this team:{team['title']}, skip deleting members in team"
            )
        user = random.choice([user for user in team["members"] if user["id"] != 1])
        if delete_member_from_team(acc_token, team["id"], user["id"]):
            # Update teamlist
            teams_list[team_index]["members"] = [
                u
                for u in teams_list[team_index]["members"]
                if u.get("id") != user["id"]
            ]
        else:
            logger.warning(
                f"Remove user {user['username']} from team {team['title']} failed"
            )
    elif op_name == "create_team":
        teamname = gen_string(special_char=False)
        resp = create_team(acc_token, current_user_name, teamname)
        if resp:
            # update teaminfo
            team = {
                "id": resp["id"],
                "title": resp["title"],
                "members": [
                    query_user_in_list(member["user"]["id"])
                    for member in resp["members"]
                ],
            }
        else:
            logger.warning(f"Failed to create team {teamname}")
    else:
        logger.error(f"Unhandled API name {op_name}")


def query_user_in_list(id: int) -> dict:
    for user in users_list:
        if user["id"] == id:
            return user
    return None


def print_userlist():
    print(users_list)


def print_teamlist():
    print(teams_list)


def gen_string(length=10, special_char=True) -> str:
    if special_char:
        # Combine letters and digits to form the pool of characters
        characters = string.ascii_letters + string.digits + "@#$%!&%*-+"
    else:
        characters = string.ascii_letters + string.digits
    # Use random.choices to pick characters at random, then join them into a string
    random_string = "".join(random.choices(characters, k=length))
    return random_string


def gen_email(domain=None, tld=None) -> str:
    # Define the length of the random username part
    username_length = random.randint(5, 10)

    # Generate a random username using letters and digits
    username = "".join(
        random.choices(string.ascii_letters + string.digits, k=username_length)
    )

    # Default domain and TLD if not provided
    if domain is None:
        domain = random.choice(["gmail", "outlook", "foxmail", "pcacmail"])
    if tld is None:
        tld = random.choice(["com", "net", "org", "io"])

    # Construct the email
    email = f"{username}@{domain}.{tld}"
    return email


if __name__ == "__main__":
    # Initialize token
    logger.info("Ready to start random walk")
    resp = request_auth_token(current_user_name, "q")
    acc_token, ref_token = resp["access_token"], resp["refresh_token"]
    while True:  # Main loop
        # Random time interval
        os.sleep(random.randint(3, 10))
        chosen_function = random.choice(op_list)
        do_api(chosen_function, acc_token, ref_token, current_user_name, "q")
