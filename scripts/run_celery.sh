#!/bin/bash

cd home-app
su -m app -c "celery -A tasks worker --loglevel INFO"
