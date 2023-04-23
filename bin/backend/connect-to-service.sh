#!/usr/bin/bash

if [ -z "$1" ]; then
    echo "No TASK_ID argument supplied"
    exit 1
fi

TASK_ID=$1
CONTAINER_NAME="backend-flask"


aws ecs execute-command  \
  --region $AWS_DEFAULT_REGION \
  --cluster cruddur \
  --task "$TASK_ID" \
  --container "$CONTAINER_NAME" \
  --command "/bin/bash" \
  --interactive
