import sys

lines = iter(sys.stdin)
header = next(lines)
header = next(lines)

count = 0
epoch = 0
p1Sum = 0
p2Sum = 0

for line in lines:
    data = line.replace('\n', '').split(';')
    currentEpoch = int(data[0])
    p1 = float(data[1])
    p2 = float(data[2])

    if(epoch != currentEpoch and epoch != 0):
        p1Sum/=count
        p2Sum/=count  

        values = [str(epoch),str(p1Sum),str(p2Sum)] 
        c = ';'
        print(c.join(values)) 
        p1Sum = 0
        p2Sum = 0
        count = 0
    
        
    epoch = currentEpoch

    p1Sum += p1
    p2Sum += p2
    count += 1


if(p1Sum + p2Sum != 0):
    p1Sum/=count
    p2Sum/=count   
    values = [str(epoch),str(p1Sum),str(p2Sum)] 
    c = ';'
    print(c.join(values)) 





