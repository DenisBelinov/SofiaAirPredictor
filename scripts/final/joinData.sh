#!/bin/bash

#parameters: 
# 1. weather data file
# 2. sensors data file

echo "epoch,temperature,windSpeed,pressure,humidity,precipIntensity,visibility,p1,p2"
#prepare weather
cat ${1} | grep '^1' | sed 's/,/ /g' | sort -n > wtemp.csv
# prepare sensors
cat ${2} | grep '^1' | sed 's/;/ /g' | sort -n > stemp.csv
join -j 1 -o 1.1,1.2,1.3,1.4,1.5,1.6,1.7,2.2,2.3 wtemp.csv stemp.csv

rm wtemp.csv stemp.csv
