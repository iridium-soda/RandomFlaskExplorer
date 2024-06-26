from http_clients import *

resp = request_auth_token(username="root", password="q")
print(resp)

acc_token, ref_token = resp["access_token"], resp["refresh_token"]
print(f"Acc token:{acc_token},Ref_token:{ref_token}")

resp = refresh_token(username="root", refresh_token=ref_token)
print(resp)

acc_token, ref_token = resp["access_token"], resp["refresh_token"]
print(f"Acc token:{acc_token},Ref_token:{ref_token}")

list_user(acc_token, "root")
resp = create_user(
    access_token=acc_token,
    form_dict={
        "username": "pac",
        "email": "acc@gmail.com",
        "password": "asus",
        "first_name": "",
        "middle_name": "",
        "last_name": "",
    },
)
username, userid, userpwd = resp["username"], resp["id"], "asus"
resp = get_user_detail_by_id(access_token=acc_token, id=userid)
print(resp)

list_user(acc_token, "root")

list_teams(access_token=acc_token, username="root")
resp = create_team(acc_token, "root", teamname="testTeam123")
print(resp)
team_title, team_id = resp["title"], resp["id"]
add_member_to_team(acc_token, team_id, userid, False)
list_members_in_team(acc_token, team_id)
list_teams(access_token=acc_token, username="root")
delete_member_from_team(acc_token, team_id, userid)
list_members_in_team(acc_token, team_id)
del_team_by_id(acc_token, team_id)
list_teams(access_token=acc_token, username="root")
