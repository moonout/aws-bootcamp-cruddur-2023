from datetime import datetime, timedelta, timezone
from aws_xray_sdk.core import xray_recorder


class UserActivities:
    def run(user_handle):
        # segment = xray_recorder.begin_segment("segment_name")
        # # Start a subsegment
        # subsegment = xray_recorder.begin_subsegment("subsegment_name")

        # # Add metadata or annotation here if necessary
        # segment.put_metadata("key", dict, "namespace")
        # subsegment.put_annotation("key", "value")
        # xray_recorder.end_subsegment()

        model = {"errors": None, "data": None}

        now = datetime.now(timezone.utc).astimezone()

        if user_handle == None or len(user_handle) < 1:
            model["errors"] = ["blank_user_handle"]
        else:
            now = datetime.now()
            results = [
                {
                    "uuid": "248959df-3079-4947-b847-9e0892d1bab4",
                    "handle": "Andrew Brown",
                    "message": "Cloud is fun!",
                    "created_at": (now - timedelta(days=1)).isoformat(),
                    "expires_at": (now + timedelta(days=31)).isoformat(),
                }
            ]
            model["data"] = results

        subsegment = xray_recorder.begin_subsegment("mock-data")
        # xray ---
        data = {"now": now.isoformat(), "results-size": len(model["data"])}
        subsegment.put_annotation("data", data)
        subsegment.put_metadata("meta-data", data)

        document = xray_recorder.current_segment()
        document.put_annotation("annot", "some annot")

        xray_recorder.end_subsegment()

        return model
