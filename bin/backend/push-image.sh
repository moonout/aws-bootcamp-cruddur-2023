#! /usr/bin/bash

docker tag backend-flask-prod:latest $ECR_BACKEND_FLASK_URL:latest
docker push $ECR_BACKEND_FLASK_URL:latest
