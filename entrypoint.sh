#!/usr/bin/env bash

set -e
RUN_MANAGE_PY='poetry run python myproject/manage.py'

#echo "Running migrations..."
#$RUN_MANAGE_PY migrate --no-input

echo 'Collecting static files...'
$RUN_MANAGE_PY collectstatic --no-input
exec "$@"