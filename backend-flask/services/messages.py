from lib.db import query_one
from lib.ddb import Ddb


class Messages:
    @staticmethod
    def run(cognito_user_id, message_group_uuid):
        model = {"errors": None, "data": None}

        sql = """
            SELECT users.uuid::text
            FROM public.users
            WHERE users.cognito_user_id = %(cognito_user_id)s
            LIMIT 1
        """
        my_user_uuid = query_one(sql, {"cognito_user_id": cognito_user_id})

        data = Ddb().list_messages(my_user_uuid["uuid"], message_group_uuid)
        model["data"] = data
        return model
