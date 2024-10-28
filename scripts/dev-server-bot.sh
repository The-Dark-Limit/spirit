#!/bin/bash

set -o errexit
set -o nounset

. ./scripts/utils/graceful-exit.sh
. ./scripts/utils/prestart.sh

trap 'graceful_exit 60' TERM INT HUP

python main.py
