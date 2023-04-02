#!/usr/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

CYAN='\033[1;36m'
RED='\033[1;31m'
BLUE='\033[1;34m'
NO_COLOR='\033[0m'

printf "${BLUE}Load schema...${NO_COLOR}\n"


if [[ "$1" == "prod" ]]; then
    printf "${RED}WARNING: going to prod${NO_COLOR}\n"
    URL=$CONNECTION_URL
else
    printf "${CYAN}MEH: that's local${NO_COLOR}\n"
    URL=$LOCAL_CONNECTION_URL
fi

psql $URL/$DB_NAME < $SCRIPT_DIR/../../db/schema.sql

echo -e "Done\n"
