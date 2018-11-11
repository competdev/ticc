#!/bin/bash

while [[ $# -gt 0 ]]
do
key="$1"
case $key in
    -d|--delete)
    python manage.py clear_database
    shift
    ;;
esac
done

bash run_fixtures.sh
python manage.py create_students
python manage.py create_tournament
python manage.py create_tournament
python manage.py create_tournament
python manage.py calculate_scores
