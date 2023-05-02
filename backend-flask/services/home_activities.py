from datetime import datetime, timezone
from opentelemetry import trace
from lib.db import query_all

tracer = trace.get_tracer("home.activities")


class HomeActivities:
    @staticmethod
    def run(cognito_user_id=None):
        with tracer.start_as_current_span("mock-data"):
            now = datetime.now()
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
                WHERE public.users.cognito_user_id = %(cognito_user_id)s
                ORDER BY activities.created_at DESC
            """
            results = query_all(sql, {"cognito_user_id": cognito_user_id})
            span.set_attribute("app.result.len", len(results))
            return results
