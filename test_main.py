from main import *

do_api("request_auth_token")
do_api("refresh_token")
do_api("list_user")
for _ in range(10):
    do_api("create_user")
do_api("get_user_detail_by_id")
do_api("list_user")
do_api("list_teams")
for _ in range(5):
    do_api("create_team")
do_api("add_member_to_team")
do_api("list_members_in_team")
do_api("list_teams")
do_api("delete_member_from_team")
do_api("list_members_in_team")
do_api("del_team_by_id")
do_api("list_teams")
