#! /bin/sh

flask db upgrade
gunicorn -b 0.0.0.0:5000 --reload "ls-auth-api:create_app()"
