#!/bin/bash
FILENAME=$(date +"%Y-%m-%d")

python manage.py dblist 2>> $FILENAME.dat

echo "===========================================================" >> $FILENAME.dat
echo "Done!"