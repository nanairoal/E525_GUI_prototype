#!/bin/bash

if [ $# -ne 6 ] ; then
  echo "hoge"
  exit 1
fi

echo "check parameter"
echo $1
echo $2
echo $3
echo $4
echo $5
echo $6
