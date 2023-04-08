import uuid
from datetime import datetime, timezone
from lib.db import query_all
from lib.ddb import Ddb


class CreateMessage:
    @staticmethod
    def run(message, cognito_user_id, user_receiver_handle, message_group_uuid):
        model = {"errors": None, "data": None}

        if not message_group_uuid:
            mode = "create"
            if not user_receiver_handle:
                model["errors"] = ["user_receiver_handle_blank"]
        elif not user_receiver_handle:
            mode = "update"
            if not message_group_uuid:
                model["errors"] = ["message_group_uuid_blank"]

        if not message:
            model["errors"] = ["message_blank"]
        elif len(message) > 1024:
            model["errors"] = ["message_exceed_max_chars"]

        if model["errors"]:
            model["data"] = {"message": message}
            return model
        sql = """
            SELECT
                users.uuid::text,
                users.display_name,
                users.handle,
                CASE users.cognito_user_id = %(cognito_user_id)s
                    WHEN TRUE THEN
                    'sender'
                    WHEN FALSE THEN
                    'recv'
                    ELSE
                        'other'
                END as kind
                FROM public.users
                WHERE
                    users.cognito_user_id = %(cognito_user_id)s
                    OR
                    users.handle = %(user_receiver_handle)s
        """
        users = query_all(sql, {"cognito_user_id": cognito_user_id, "user_receiver_handle": user_receiver_handle})
        my_user = next((item for item in users if item["kind"] == "sender"), None)

        if mode == "update":
            data = Ddb().create_message(
                message_group_uuid=message_group_uuid,
                message=message,
                my_user_uuid=my_user["uuid"],
                my_user_display_name=my_user["display_name"],
                my_user_handle=my_user["handle"],
            )
        elif mode == "create":
            other_user = next((item for item in users if item["kind"] == "recv"), None)

            data = Ddb().create_message_group(
                message=message,
                my_user_uuid=my_user["uuid"],
                my_user_display_name=my_user["display_name"],
                my_user_handle=my_user["handle"],
                other_user_uuid=other_user["uuid"],
                other_user_display_name=other_user["display_name"],
                other_user_handle=other_user["handle"],
            )
        # MomentoCounter.incr(f"msgs/{user_handle}")
        model["data"] = data
        return model
