#!/bin/bash

docker run -i -p 5672:5672 rabbitmq &
celery -A progress worker -l info &
celery -A progress beat -l info &
./manage.py runserver
