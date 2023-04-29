#! /usr/bin/bash

ABS_PATH=$(readlink -f "$0")
TEMPL_PATH=$(dirname $ABS_PATH)
BIN_PATH=$(dirname $TEMPL_PATH)
PROJECT_PATH=$(dirname $BIN_PATH)


envsubst < "$PROJECT_PATH/env_templates/frontend-react-js.env.template"  > "$PROJECT_PATH/frontend-react-js.env"
