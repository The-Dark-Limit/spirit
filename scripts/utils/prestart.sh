#!/bin/bash

wait_db() {
  start_ts=$(date +%s)
  while ! /usr/bin/pg_isready -h $DB_HOST -p ${DB_PORT:-5432} >/dev/null 2>/dev/null; do
    now_ts=$(date +%s)
    if [ $(( now_ts - start_ts )) -gt ${BASH_WAIT_DB_TIMEOUTE:-300} ]; then
        echo "Timeout wait DB"
        exit 1
    fi
    echo "I'm waiting DB (Host: $DB_HOST, port: ${DB_PORT:-5432})"
    sleep 1
  done
}
