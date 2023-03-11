from datetime import datetime, timedelta, timezone
from opentelemetry import trace

tracer = trace.get_tracer("home.activities")


class HomeActivities:
    def run():
        # # Start a segment
        # segment = xray_recorder.begin_segment("segment_name_new")
        # # segment = xray_recorder.current_segment()
        # # Start a subsegment
        # subsegment = xray_recorder.begin_subsegment("subsegment_name_new")

        # # Add metadata or annotation here if necessary
        # segment.put_metadata("key", dict, "namespace")
        # subsegment.put_annotation("key", "value123")
        # segment.put_annotation("key", "aaaaaaaaaaaaa")
        # xray_recorder.end_subsegment()

        # # # Close the segment
        # xray_recorder.end_segment()

        # document = xray_recorder.current_segment()
        # document.put_metadata("my key", "my value")
        # document.put_annotation("key", "aaaaa!")

        # print("===================1")
        # # Start a segment
        # segment = xray_recorder.begin_segment("segment_name")
        # print("===================2")
        # # Start a subsegment
        # subsegment = xray_recorder.begin_subsegment("subsegment_name")
        # print("===================3")

        # # Add metadata or annotation here if necessary
        # print("===================4")
        # segment.put_metadata("key", dict, "namespace")
        # print("===================5")
        # subsegment.put_annotation("key", "value")
        # print("===================6")

        # xray_recorder.end_subsegment()
        # print("===================7")

        # # # Close the segment
        # xray_recorder.end_segment()

        with tracer.start_as_current_span("mock-data"):
            now = datetime.now(timezone.utc).astimezone()
            span = trace.get_current_span()
            span.set_attribute("app.now", now.isoformat())

            results = [
                {
                    "uuid": "68f126b0-1ceb-4a33-88be-d90fa7109eee",
                    "handle": "Andrew Brown",
                    "message": "Cloud is fun!",
                    "created_at": (now - timedelta(days=2)).isoformat(),
                    "expires_at": (now + timedelta(days=5)).isoformat(),
                    "likes_count": 5,
                    "replies_count": 1,
                    "reposts_count": 0,
                    "replies": [
                        {
                            "uuid": "26e12864-1c26-5c3a-9658-97a10f8fea67",
                            "reply_to_activity_uuid": "68f126b0-1ceb-4a33-88be-d90fa7109eee",
                            "handle": "Worf",
                            "message": "This post has no honor!",
                            "likes_count": 0,
                            "replies_count": 0,
                            "reposts_count": 0,
                            "created_at": (now - timedelta(days=2)).isoformat(),
                        }
                    ],
                },
                {
                    "uuid": "66e12864-8c26-4c3a-9658-95a10f8fea67",
                    "handle": "Worf",
                    "message": "I am out of prune juice",
                    "created_at": (now - timedelta(days=7)).isoformat(),
                    "expires_at": (now + timedelta(days=9)).isoformat(),
                    "likes": 0,
                    "replies": [],
                },
                {
                    "uuid": "248959df-3079-4947-b847-9e0892d1bab4",
                    "handle": "Garek",
                    "message": "My dear doctor, I am just simple tailor",
                    "created_at": (now - timedelta(hours=1)).isoformat(),
                    "expires_at": (now + timedelta(hours=12)).isoformat(),
                    "likes": 0,
                    "replies": [],
                },
            ]
            span.set_attribute("app.result.len", len(results))
        return results
