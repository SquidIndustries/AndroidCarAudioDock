#!/bin/bash

if [ "$2" != "2d02" ]; then #if idProduct is for AOA2 do nothing
  /usr/local/bin/androiddocked.sh $1 $2&
fi

exit 0
