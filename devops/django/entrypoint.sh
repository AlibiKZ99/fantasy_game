#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

postgres_is_not_ready() {
python << END
import psycopg2
import sys

try:
    psycopg2.connect(
        host="${POSTGRES_HOST}",
        port="${POSTGRES_PORT}",
        dbname="${POSTGRES_DB}",
        user="${POSTGRES_USER}",
        password="${POSTGRES_PASSWORD}"
    )
except psycopg2.OperationalError:
    sys.exit(-1)

sys.exit(0)
END
}

until postgres_is_not_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available'

NUM_WORKERS=${NUM_WORKERS:-5}
TIMEOUT=${TIMEOUT:-180}


python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate

gunicorn fantasy.wsgi:application \
        --reload \
        --workers $NUM_WORKERS \
        --timeout $TIMEOUT \
        --keep-alive 5 \
        --bind 0.0.0.0:8000 \
        --log-level=debug \
        --log-file=- \
        -k gevent
exec "$@"