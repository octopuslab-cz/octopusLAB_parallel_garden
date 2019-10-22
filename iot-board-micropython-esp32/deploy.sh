#!/bin/bash

export AMPY_PORT=/dev/ttyUSB0

ampy mkdir hydroponics 2> /dev/null

for file in $(ls hydroponics)
do
  echo "Uploading $file..."
  ampy put "hydroponics/$file" "hydroponics/$file"
done

echo "Uploading main"
ampy put main.py
