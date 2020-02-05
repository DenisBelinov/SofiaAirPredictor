import sys
import datetime
import calendar 

lines = iter(sys.stdin)
header = next(lines)
print(header)
for line in lines:
    words = line.split(';')
    
    time = words[5]
    time = time.replace('-', ':')
    time = time.replace('T', ':')
    h = time.split(':')
    h= [int(i) for i in h]

    aprilFirst=datetime.datetime(*h)
    epoch = calendar.timegm(aprilFirst.timetuple())
    epoch = epoch - (epoch % 3600)
    words[5] = str(epoch)
    c = ';'
    line = c.join(words)

    print(line),