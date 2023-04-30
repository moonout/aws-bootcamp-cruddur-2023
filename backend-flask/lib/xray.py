import os
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware


def init_xray(app):
    daemon_address = os.getenv("AWS_XRAY_URL", "127.0.0.1:2000")
    xray_recorder.configure(service="backend-flask", daemon_address=daemon_address)
    XRayMiddleware(app, xray_recorder)
