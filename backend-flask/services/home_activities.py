from datetime import datetime, timedelta, timezone
from opentelemetry import trace
from lib.db import pool
from psycopg.rows import dict_row

tracer = trace.get_tracer("home.activities")


class HomeActivities:
    @staticmethod
    def run():
        with tracer.start_as_current_span("mock-data"):
            now = datetime.now(timezone.utc).astimezone()
            span = trace.get_current_span()
            span.set_attribute("app.now", now.isoformat())
            sql = """
                SELECT
                    activities.uuid,
                    users.display_name,
                    users.handle,
                    activities.message,
                    activities.replies_count,
                    activities.reposts_count,
                    activities.likes_count,
                    activities.reply_to_activity_uuid,
                    activities.expires_at,
                    activities.created_at
                FROM activities
                LEFT JOIN public.users ON users.uuid = activities.user_uuid
                ORDER BY activities.created_at DESC
            """
            with pool.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    print(results)

            span.set_attribute("app.result.len", len(results))
        return results
