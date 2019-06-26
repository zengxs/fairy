#!/bin/bash
export DJANGO_SETTINGS_MODULE=fairy.settings_prod

case $1 in
    collectstatic)
        DJANGO_SETTINGS_MODULE=fairy.settings python manage.py collectstatic
        ;;
    migrate)
        python manage.py migrate
        ;;
    manage)
        args=( "$@" )
        python manage.py ${args[@]:1}
        ;;
    freeze)
        python freeze.py
        ;;
    ""|runserver)
        gunicorn -b 0.0.0.0:8000 -w $(nproc) fairy.wsgi:application
        ;;
    *)
        echo "error command"
        exit 1
esac
exit
