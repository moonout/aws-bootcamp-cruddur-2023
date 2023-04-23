#! /usr/bin/bash

ABS_PATH=$(readlink -f "$0")
FRONTEND_PATH=$(dirname $ABS_PATH)
BIN_PATH=$(dirname $FRONTEND_PATH)
PROJECT_PATH=$(dirname $BIN_PATH)
FRONTEND_REACT_JS_PATH="$PROJECT_PATH/frontend-react-js"

docker build \
  --build-arg REACT_APP_BACKEND_URL="$BACKEND_URL" \
  --build-arg REACT_APP_AWS_PROJECT_REGION="$AWS_DEFAULT_REGION" \
  --build-arg REACT_APP_AWS_COGNITO_REGION="$AWS_DEFAULT_REGION" \
  --build-arg REACT_APP_AWS_USER_POOLS_ID="$AWS_COGNITO_USER_POOL_ID" \
  --build-arg REACT_APP_CLIENT_ID="${AWS_COGNITO_USER_POOL_CLIENT_ID}" \
  -f "$FRONTEND_REACT_JS_PATH/Dockerfile.prod" \
  -t frontend-react-js \
  "$FRONTEND_REACT_JS_PATH/."
  
  

