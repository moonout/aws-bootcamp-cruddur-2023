#!/usr/bin/bash

CYAN='\033[1;36m'
RED='\033[1;31m'
NO_COLOR='\033[0m'

if [[ "$1" == "prod" ]]; then
    printf "${RED}WARNING: going to prod${NO_COLOR}\n"
    URL=$CONNECTION_URL
else
    printf "${CYAN}MEH: that's local${NO_COLOR}\n"
    URL=$LOCAL_CONNECTION_URL
fi

psql $URL -c "select pid as process_id, \
       usename as user,  \
       datname as db, \
       client_addr, \
       application_name as app,\
       state \
from pg_stat_activity;"
