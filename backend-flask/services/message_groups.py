from lib.ddb import Ddb
from lib.db import query_one


class MessageGroups:
    @staticmethod
    def run(cognito_user_id):
        model = {"errors": None, "data": None}

        sql = """
            SELECT users.uuid::text
            FROM public.users
            WHERE users.cognito_user_id = %(cognito_user_id)s
            LIMIT 1
        """
        my_user_uuid = query_one(sql, {"cognito_user_id": cognito_user_id})
        data = Ddb().list_message_groups(my_user_uuid["uuid"])
        model["data"] = data
        return model
