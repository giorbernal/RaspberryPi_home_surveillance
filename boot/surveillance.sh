#!/bin/bash

ENV_PATH=/home/pi/Documents/venv
APP=app.py
CMD="python ../$APP"
NAPP=`ps -ef | grep "$CMD" | grep -v "grep" | wc -l`
LOGFILE=app.log

function resetLogFile {
	if [[ -f $LOGFILE ]]; then
		TS=$(date +"%s")
		mv $LOGFILE $LOGFILE.$TS
	fi
}

if [[ $NAPP == 0 ]]; then
	resetLogFile
	source $ENV_PATH/bin/activate
	$CMD
else
	echo 'surveillance application already started!'
fi
