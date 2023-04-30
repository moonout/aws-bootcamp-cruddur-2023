from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import os


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
from services.users_short import *

from lib.token import TokenVerification

from lib.xray import init_xray

# from opentelemetry import trace
# from opentelemetry.instrumentation.flask import FlaskInstrumentor
# from opentelemetry.instrumentation.requests import RequestsInstrumentor
# from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor, ConsoleSpanExporter


from lib.rollbar import init_rollbar

# # Initialize tracing and an exporter that can send data to Honeycomb
# provider = TracerProvider()

# processor = BatchSpanProcessor(OTLPSpanExporter())
# provider.add_span_processor(processor)

# # simple_processor = SimpleSpanProcessor(ConsoleSpanExporter())
# # provider.add_span_processor(simple_processor)

# trace.set_tracer_provider(provider)
# tracer = trace.get_tracer(__name__)

# Initialize automatic instrumentation with Flask
app = Flask(__name__)
# FlaskInstrumentor().instrument_app(app)
# RequestsInstrumentor().instrument()


frontend_url = os.getenv("FRONTEND_URL")
backend_url = os.getenv("BACKEND_URL")
origins = [frontend_url, backend_url]

cors = CORS(
    app,
    resources={r"/api/*": {"origins": origins}},
    headers=["Content-Type", "Authorization"],
    expose_headers="Authorization",
    # expose_headers="location,link",
    # allow_headers="content-type,if-modified-since",
    methods="OPTIONS,GET,HEAD,POST",
)


# X-RAY ----------
init_xray(app)

token_verifier = TokenVerification(app)

# Rollbar ----------
init_rollbar(app)


@app.route("/api/health-check")
def health_check():
    return {"success": True}, 200


@app.route("/api/message_groups", methods=["GET"])
def data_message_groups():
    claims = token_verifier.verify()
    if not claims:
        return {"errors": "Not logged in", "data": None}, 401

    model = MessageGroups().run(cognito_user_id=claims["sub"])
    if model["errors"] is not None:
        return model["errors"], 422
    return model["data"], 200


@app.route("/api/messages/<string:message_group_uuid>", methods=["GET"])
def data_messages(message_group_uuid):
    claims = token_verifier.verify()
    if not claims:
        return {"errors": "Not logged in", "data": None}, 401

    model = Messages().run(cognito_user_id=claims["sub"], message_group_uuid=message_group_uuid)
    if model["errors"] is not None:
        return model["errors"], 422
    return model["data"], 200


@app.route("/api/messages", methods=["POST", "OPTIONS"])
@cross_origin()
def data_create_message():
    claims = token_verifier.verify()
    if not claims:
        return {"errors": "Not logged in", "data": None}, 401
    message = request.json.get("message")
    user_receiver_handle = request.json.get("handle")
    message_group_uuid = request.json.get("message_group_uuid")

    model = CreateMessage().run(
        message=message,
        cognito_user_id=claims["sub"],
        user_receiver_handle=user_receiver_handle,
        message_group_uuid=message_group_uuid,
    )

    if model["errors"] is not None:
        return model["errors"], 422
    return model["data"], 200


@app.route("/api/activities/home", methods=["GET"])
def data_home():
    claims = token_verifier.verify()
    if claims:
        app.logger.debug("verified token")
        data = HomeActivities().run(cognito_user_id=claims["sub"])
    else:
        app.logger.debug("unverified token")
        data = HomeActivities().run()
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
    return model["data"], 200


@app.route("/api/activities/search", methods=["GET"])
def data_search():
    term = request.args.get("term")
    model = SearchActivities.run(term)
    if model["errors"] is not None:
        return model["errors"], 422
    return model["data"], 200


@app.route("/api/activities", methods=["POST", "OPTIONS"])
@cross_origin()
def data_activities():
    user_handle = "moon"
    message = request.json["message"]
    ttl = request.json["ttl"]
    model = CreateActivity().run(message, user_handle, ttl)
    if model["errors"]:
        return model["errors"], 422

    return model["data"], 200


@app.route("/api/activities/<string:activity_uuid>", methods=["GET"])
def data_show_activity(activity_uuid):
    data = ShowActivity.run(activity_uuid=activity_uuid)
    return data, 200


@app.route("/api/activities/<string:activity_uuid>/reply", methods=["POST", "OPTIONS"])
@cross_origin()
def data_activities_reply(activity_uuid):
    user_handle = "moon"
    message = request.json["message"]
    model = CreateReply.run(message, user_handle, activity_uuid)
    if model["errors"] is not None:
        return model["errors"], 422
    return model["data"], 200


@app.route("/api/users/@<string:handle>/short", methods=["GET"])
def data_users_short(handle):
    data = UsersShort().run(handle)
    if not data:
        return f"User {handle} not found", 404
    return data, 200


if __name__ == "__main__":
    app.run()
