import cognitojwt
import os
from flask import request
from typing import Dict


class TokenVerification:
    header = "Authorization"

    def __init__(self, app):
        self.app = app
        self.REGION = os.getenv("AWS_DEFAULT_REGION")
        self.AWS_COGNITO_USER_POOL_ID = os.getenv("AWS_COGNITO_USER_POOL_ID")
        self.AWS_COGNITO_USER_POOL_CLIENT_ID = os.getenv("AWS_COGNITO_USER_POOL_CLIENT_ID")

    def _extract_token_from_header(self):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None
        _, token = auth_header.split(" ")
        return token

    def verify(self) -> Dict:
        token = self._extract_token_from_header()
        if not token or token == "null":
            self.app.logger.error("No TOKEN")
            return None
        try:
            verified_claims = cognitojwt.decode(
                token, self.REGION, self.AWS_COGNITO_USER_POOL_ID, self.AWS_COGNITO_USER_POOL_CLIENT_ID, testmode=False
            )
        except cognitojwt.exceptions.CognitoJWTException:
            self.app.logger.debug("TOKEN expired")
            return None
        self.app.logger.debug("TOKEN confirmed")
        return verified_claims
