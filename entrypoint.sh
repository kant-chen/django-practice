#!/bin/bash
# set -ex
# for debugging env variables echo $(env)
#POSTGRES_DB=$(echo ${DATABASE_URL} | rev | cut -d '/' -f 1 | rev)
#echo $("echo $POSTGRES_DB")

_print_status() {
    # Show   red x if last command failed
    # Show green o if last command succeeded
    case $? in
        0) printf '\342\234\224\n' ;;
        *) printf '\342\234\227\n' ;;
    esac
    history -a
    true
}


function wait_for_db {
    until psql -h "$POSTGRES_HOST" -U "postgres" -c '\q'; do
        >&2 echo "Postgres is unavailable - sleeping"
        sleep 1
    done
    >&2 echo "Postgres is up - executing command"
}

function createdb {
    wait_for_db
    if psql -h ${POSTGRES_HOST} -U postgres -lqt | cut -d \| -f 1 | grep -qw ${POSTGRES_DB}; then
        echo "Database exists. Not creating"
        echo "Check if user is existed..."
        if  psql -l -U ${POSTGRES_USER} -h ${POSTGRES_HOST} >> /dev/null; then
          echo "User exists"
        else
          echo "Creating role..."
          psql -h ${POSTGRES_HOST} -U postgres -c "CREATE ROLE ${POSTGRES_USER} LOGIN PASSWORD '${POSTGRES_PASWORD}'; ALTER USER ${POSTGRES_USER} CREATEDB;"
          psql -h ${POSTGRES_HOST} -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_USER};"
        fi
    else
       echo "Creating database"
       psql -h ${POSTGRES_HOST} -U postgres -c "CREATE DATABASE ${POSTGRES_DB}"
       echo "Creating role..."
       psql -h ${POSTGRES_HOST} -U postgres -tc "SELECT 1 FROM pg_user WHERE usename = '${POSTGRES_USER}'" | grep -q 1 || psql -h "${POSTGRES_HOST}" -U postgres -c "CREATE ROLE ${POSTGRES_USER} LOGIN PASSWORD '${POSTGRES_PASWORD}'; ALTER USER ${POSTGRES_USER} CREATEDB;"
       psql -h ${POSTGRES_HOST} -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_USER};"
    fi
}


function migrate {
    echo $("pwd")
    python manage.py migrate
}


function assets {
    python manage.py collectstatic --noinput
}

function startdjango {
    python manage.py runserver 0.0.0.0:8000
}

function start_django_with_https {
  stunnel4 stunnel/stunnel.config &
  HTTPS=1 python manage.py runserver 0.0.0.0:8001 &
}


function init {
    echo -n "Checking database"
    createdb
    _print_status
    echo -n "Migrating"
    migrate
    _print_status
    echo -n "Starting django"
    startdjango
    _print_status
    start_django_with_https
    _print_status
}

function test {
    createdb
    migrate
    # all runnable tests are imported in central location under amazingtalker.tests
    python manage.py test amazingtalker.tests
}

eval $@
