#!/bin/bash

ENV_PATH=/home/pi/Documents/venv
APP=app.py
CMD="python ../$APP"
NAPP=`ps -ef | grep "$CMD" | grep -v "grep" | wc -l`

if [[ $NAPP == 0 ]]; then
	source $ENV_PATH/bin/activate
	$CMD
else
	echo 'surveillance application already started!'
fi
