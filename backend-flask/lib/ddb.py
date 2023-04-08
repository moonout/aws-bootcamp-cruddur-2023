import boto3
from datetime import datetime, timezone
import uuid
import os
import botocore.exceptions


class Ddb:
    def __init__(self):
        endpoint_url = os.getenv("AWS_ENDPOINT_URL")

        if endpoint_url:
            attrs = {"endpoint_url": endpoint_url}
        else:
            attrs = {}
        self.ddb_client = boto3.client("dynamodb", **attrs)
        self.table_name = "cruddur-messages"

    def list_message_groups(self, my_user_uuid):
        year = str(datetime.now().year)
        query_params = {
            "TableName": self.table_name,
            "KeyConditionExpression": "pk = :pk AND begins_with(sk,:year)",
            # "KeyConditionExpression": "pk = :pk",
            "ScanIndexForward": False,
            "Limit": 20,
            "ExpressionAttributeValues": {
                ":pk": {"S": f"GRP#{my_user_uuid}"},
                ":year": {"S": year},
            },
        }
        # query the table
        response = self.ddb_client.query(**query_params)
        items = response["Items"]

        results = []
        for item in items:
            last_sent_at = item["sk"]["S"]
            results.append(
                {
                    "uuid": item["message_group_uuid"]["S"],
                    "display_name": item["user_display_name"]["S"],
                    "handle": item["user_handle"]["S"],
                    "message": item["message"]["S"],
                    "created_at": last_sent_at,
                }
            )
        return results

    def list_messages(self, my_user_uuid, message_group_uuid):
        year = str(datetime.now().year)
        query_params = {
            "TableName": self.table_name,
            "KeyConditionExpression": "pk = :pk AND begins_with(sk,:year)",
            "ScanIndexForward": False,
            "Limit": 20,
            "ExpressionAttributeValues": {
                ":pk": {"S": f"MSG#{message_group_uuid}"},
                ":year": {"S": year},
            },
        }

        response = self.ddb_client.query(**query_params)
        items = response["Items"]
        items.reverse()
        results = []
        for item in items:
            created_at = item["sk"]["S"]
            results.append(
                {
                    "uuid": item["message_uuid"]["S"],
                    "display_name": item["user_display_name"]["S"],
                    "handle": item["user_handle"]["S"],
                    "message": item["message"]["S"],
                    "created_at": created_at,
                }
            )
        return results

    def create_message(self, message_group_uuid, message, my_user_uuid, my_user_display_name, my_user_handle):
        now = datetime.now(timezone.utc).astimezone().isoformat()

        message_uuid = str(uuid.uuid4())

        record = {
            "pk": {"S": f"MSG#{message_group_uuid}"},
            "sk": {"S": now},
            "message": {"S": message},
            "message_uuid": {"S": message_uuid},
            "user_uuid": {"S": my_user_uuid},
            "user_display_name": {"S": my_user_display_name},
            "user_handle": {"S": my_user_handle},
        }
        # insert the record into the table

        response = self.ddb_client.put_item(TableName=self.table_name, Item=record)
        # print the response
        print(response)
        return {
            "message_group_uuid": message_group_uuid,
            "uuid": my_user_uuid,
            "display_name": my_user_display_name,
            "handle": my_user_handle,
            "message": message,
            "created_at": now,
        }

    def create_user_message_group(
        self, message_group_uuid, user_uuid, other_user_uuid, other_display_name, other_handle, message, now
    ):
        last_message_at = now

        message_group = {
            "pk": {"S": f"GRP#{user_uuid}"},
            "sk": {"S": last_message_at},
            "message_group_uuid": {"S": message_group_uuid},
            "message": {"S": message},
            "user_uuid": {"S": other_user_uuid},
            "user_display_name": {"S": other_display_name},
            "user_handle": {"S": other_handle},
        }
        return message_group

    def create_message_group(
        self,
        message,
        my_user_uuid,
        my_user_display_name,
        my_user_handle,
        other_user_uuid,
        other_user_display_name,
        other_user_handle,
    ):
        print("== create_message_group.1")

        # message_group_uuid = str(uuid.uuid4())
        message_uuid = str(uuid.uuid4())
        now = datetime.now(timezone.utc).astimezone().isoformat()
        message_group_uuid = str(uuid.uuid4())

        my_message_group = self.create_user_message_group(
            message_group_uuid, my_user_uuid, other_user_uuid, other_user_display_name, other_user_handle, message, now
        )
        # last_message_at = now
        #
        print("== create_message_group.2")

        # my_message_group = {
        #     "pk": {"S": f"GRP#{my_user_uuid}"},
        #     "sk": {"S": last_message_at},
        #     "message_group_uuid": {"S": message_group_uuid},
        #     "message": {"S": message},
        #     "user_uuid": {"S": other_user_uuid},
        #     "user_display_name": {"S": other_user_display_name},
        #     "user_handle": {"S": other_user_handle},
        # }

        print("== create_message_group.3")
        # other_message_group = {
        #     "pk": {"S": f"GRP#{other_user_uuid}"},
        #     "sk": {"S": last_message_at},
        #     "message_group_uuid": {"S": message_group_uuid},
        #     "message": {"S": message},
        #     "user_uuid": {"S": my_user_uuid},
        #     "user_display_name": {"S": my_user_display_name},
        #     "user_handle": {"S": my_user_handle},
        # }
        other_message_group = self.create_user_message_group(
            message_group_uuid, other_user_uuid, my_user_uuid, my_user_display_name, my_user_handle, message, now
        )

        print("== create_message_group.4")
        created_at = now
        message_item = {
            "pk": {"S": f"MSG#{message_group_uuid}"},
            "sk": {"S": created_at},
            "message": {"S": message},
            "message_uuid": {"S": message_uuid},
            "user_uuid": {"S": my_user_uuid},
            "user_display_name": {"S": my_user_display_name},
            "user_handle": {"S": my_user_handle},
        }
        print(my_message_group)
        print(other_message_group)
        print(message_item)
        items = {
            self.table_name: [
                {"PutRequest": {"Item": my_message_group}},
                {"PutRequest": {"Item": other_message_group}},
                {"PutRequest": {"Item": message_item}},
            ]
        }

        try:
            print("== create_message_group.try")
            # Begin the transaction
            response = self.ddb_client.batch_write_item(RequestItems=items)
            # return {"message_group_uuid": message_group_uuid}
            return {
                "message_group_uuid": message_group_uuid,
                "uuid": my_user_uuid,
                "display_name": my_user_display_name,
                "handle": my_user_handle,
                "message": message,
                "created_at": now,
            }

        except botocore.exceptions.ClientError as e:
            print("== create_message_group.error")
            print(e)
