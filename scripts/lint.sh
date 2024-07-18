#!/bin/bash

err=0
trap 'err=1' ERR

#mypy .
ruff check .
ruff format --diff .

exit $err
