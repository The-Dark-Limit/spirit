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

wait_am() {
  start_ts=$(date +%s)
  while ! curl -s --max-time 5 --head --request GET $ACCOUNT_MANAGER_IP | grep "404" > /dev/null; do
    now_ts=$(date +%s)
    if [ $(( now_ts - start_ts )) -gt ${BASH_WAIT_AM_TIMEOUTE:-300} ]; then
        echo "Timeout wait AM"
        exit 1
    fi
    echo "I'm waiting AM (Host: $ACCOUNT_MANAGER_IP)"
    sleep 1
  done
}


sync() {
  echo -e "\n### Migrate DB ###\n"
  wait_db
  python manage.py migrate

  echo -e "\n### Sync permissions with AM ###\n"
  wait_am
  python manage.py sync_perms_with_am

  STS=${STS_ENABLED:-'true'}
  STS_APP=metadata_enhancers.reloader:sts_reloader
  if [ "$STS" == "true" ];
    then echo -e "\n### Sync with STS ###\n" && stsreloader -a $STS_APP sync;
  fi
}
