#!/bin/bash

FILES=website/fixtures/*
for f in $FILES
do
  python manage.py loaddata $f --app website
done
