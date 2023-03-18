from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import os
from typing import Dict

# these imports are ugly as fuck
from services.home_activities import *
from services.user_activities import *
from services.create_activity import *
from services.create_reply import *
from services.search_activities import *
from services.message_groups import *
from services.messages import *
from services.create_message import *
from services.show_activity import *
from services.notifications_activities import *

from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor, ConsoleSpanExporter

import cognitojwt

# Initialize tracing and an exporter that can send data to Honeycomb
provider = TracerProvider()

processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)

# simple_processor = SimpleSpanProcessor(ConsoleSpanExporter())
# provider.add_span_processor(simple_processor)

trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

# Initialize automatic instrumentation with Flask
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()


frontend = os.getenv("FRONTEND_URL")
backend = os.getenv("BACKEND_URL")
origins = [frontend, backend]

cors = CORS(
    app,
    resources={r"/api/*": {"origins": origins}},
    headers=["Content-Type", "Authorization"],
    expose_headers="Authorization",
    # expose_headers="location,link",
    # allow_headers="content-type,if-modified-since",
    methods="OPTIONS,GET,HEAD,POST",
)

# Rollbar
rollbar_access_token = os.getenv("ROLLBAR_ACCESS_TOKEN")


class TokenVerification:
    header = "Authorization"

    def __init__(self, app):
        self.app = app
        self.REGION = os.getenv("AWS_COGNITO_REGION")
        self.USER_POOL_ID = os.getenv("AWS_USER_POOLS_ID")
        self.APP_CLIENT_ID = os.getenv("APP_CLIENT_ID")

    def _extract_token_from_header(self):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None
        _, token = auth_header.split(" ")
        return token

    def verify(self) -> Dict:
        token = self._extract_token_from_header()
        if not token or token == "null":
            return
        app.logger.debug("TOKEN")
        app.logger.debug(token)
        try:
            verified_claims = cognitojwt.decode(
                token, self.REGION, self.USER_POOL_ID, self.APP_CLIENT_ID, testmode=False
            )
        except cognitojwt.exceptions.CognitoJWTException:
            app.logger.debug("TOKEN expired")
            return {}
        app.logger.debug("Verified Claims")
        app.logger.debug(verified_claims)


token_verifier = TokenVerification(app)


@app.route("/api/message_groups", methods=["GET"])
def data_message_groups():
    user_handle = "andrewbrown"
    model = MessageGroups.run(user_handle=user_handle)
    if model["errors"] is not None:
        return model["errors"], 422
    else:
        return model["data"], 200


@app.route("/api/messages/@<string:handle>", methods=["GET"])
def data_messages(handle):
    user_sender_handle = "andrewbrown"
    user_receiver_handle = request.args.get("user_reciever_handle")

    model = Messages.run(user_sender_handle=user_sender_handle, user_receiver_handle=user_receiver_handle)
    if model["errors"] is not None:
        return model["errors"], 422
    else:
        return model["data"], 200
    return


@app.route("/api/messages", methods=["POST", "OPTIONS"])
@cross_origin()
def data_create_message():
    user_sender_handle = "andrewbrown"
    user_receiver_handle = request.json["user_receiver_handle"]
    message = request.json["message"]

    model = CreateMessage.run(
        message=message, user_sender_handle=user_sender_handle, user_receiver_handle=user_receiver_handle
    )
    if model["errors"] is not None:
        return model["errors"], 422
    else:
        return model["data"], 200
    return


@app.route("/api/activities/home", methods=["GET"])
def data_home():
    claims = token_verifier.verify()
    if claims:
        app.logger.debug("verified token")
    else:
        app.logger.debug("unverified token")
    data = HomeActivities.run()
    return data, 200


@app.route("/api/activities/notifications", methods=["GET"])
def data_notifications():
    data = NotificationsActivities.run()
    return data, 200


@app.route("/api/activities/@<string:handle>", methods=["GET"])
def data_handle(handle):
    model = UserActivities.run(handle)
    if model["errors"] is not None:
        return model["errors"], 422
    else:
        return model["data"], 200


@app.route("/api/activities/search", methods=["GET"])
def data_search():
    term = request.args.get("term")
    model = SearchActivities.run(term)
    if model["errors"] is not None:
        return model["errors"], 422
    else:
        return model["data"], 200
    return


@app.route("/api/activities", methods=["POST", "OPTIONS"])
@cross_origin()
def data_activities():
    user_handle = "andrewbrown"
    message = request.json["message"]
    ttl = request.json["ttl"]
    model = CreateActivity.run(message, user_handle, ttl)
    if model["errors"] is not None:
        return model["errors"], 422
    else:
        return model["data"], 200
    return


@app.route("/api/activities/<string:activity_uuid>", methods=["GET"])
def data_show_activity(activity_uuid):
    data = ShowActivity.run(activity_uuid=activity_uuid)
    return data, 200


@app.route("/api/activities/<string:activity_uuid>/reply", methods=["POST", "OPTIONS"])
@cross_origin()
def data_activities_reply(activity_uuid):
    user_handle = "andrewbrown"
    message = request.json["message"]
    model = CreateReply.run(message, user_handle, activity_uuid)
    if model["errors"] is not None:
        return model["errors"], 422
    else:
        return model["data"], 200
    return


if __name__ == "__main__":
    app.run(debug=True)
