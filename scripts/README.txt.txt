 cat $FILENAME | python datetimeToEpoch.py | cut -d ';' -f 6,7,10 |  python merge.py  > $DESTINATION

WHERE
FILENAME is your data.
DESTINATION is the fu***** destination.

