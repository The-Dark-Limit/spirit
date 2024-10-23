#!/bin/bash

set -o errexit
set -o nounset

. ./scripts/utils/graceful-exit.sh
. ./scripts/utils/prestart.sh

trap 'graceful_exit 60' TERM INT HUP

export LOG_LEVEL=${LOG_LEVEL:-INFO}
export CELERY_APP=metadata_enhancers
export CELERY_WORKER_CONCURRENCY=${CELERY_WORKER_CONCURRENCY:-8}

wait_db

exec celery worker -B --max-tasks-per-child=10
