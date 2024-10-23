#!/bin/bash

set -o errexit
set -o nounset

. ./scripts/utils/graceful-exit.sh
. ./scripts/utils/prestart.sh
. ./scripts/utils/start-gunicorn.sh

trap 'graceful_exit 60' TERM INT HUP

sync

start_gunicorn
