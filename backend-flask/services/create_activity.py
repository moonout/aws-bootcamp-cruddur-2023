import uuid
from datetime import datetime, timedelta, timezone
from lib.db import query_one
import psycopg
import traceback


class CreateActivity:
    ttl_to_time = {
        "30-days": timedelta(days=30),
        "7-days": timedelta(days=7),
        "3-days": timedelta(days=3),
        "1-day": timedelta(days=1),
        "12-hours": timedelta(hours=12),
        "3-hours": timedelta(hours=3),
        "1-hour": timedelta(hours=1),
    }

    def run(self, message, user_handle, ttl):
        model = {"errors": None, "data": None}

        ttl_offset = self.ttl_to_time.get(ttl)
        model["errors"] = self.is_invalid(message, user_handle, ttl_offset)
        if model["errors"]:
            return model

        data, errors = self.create_activity(message, user_handle, ttl_offset)
        if errors:
            model["data"] = {"handle": user_handle, "message": message}
            model["errors"] = errors
            return model
        model["data"] = data
        return model

    def is_invalid(self, message, user_handle, ttl_offset):
        if ttl_offset is None:
            return "ttl_blank"

        if user_handle == None or len(user_handle) < 1:
            return "user_handle_blank"

        if message == None or len(message) < 1:
            return "message_blank"
        elif len(message) > 280:
            return "message_exceed_max_chars"

        return None

    def create_activity(self, message, user_handle, ttl_offset):
        sql = """
            INSERT INTO activities (user_uuid, message, expires_at)
            VALUES (
                (SELECT uuid from public.users WHERE users.handle = %(handle)s LIMIT 1),
                %(message)s,
                %(expires_at)s
            )
            RETURNING uuid
        """
        now = datetime.now()
        expires_at = now + ttl_offset
        try:
            result = query_one(sql, {"handle": user_handle, "message": message, "expires_at": expires_at.isoformat()})
            return {
                "uuid": result["uuid"],
                # "display_name": "Andrew Brown",
                "handle": user_handle,
                "message": message,
                "created_at": now.isoformat(),
                "expires_at": expires_at.isoformat(),
            }, None
        except (Exception, psycopg.DatabaseError) as error:
            print(error)
            traceback.print_exc()
            return {}, "failed to add activity"
