import os
import time

start = time.time()
solved = 0
almost = 0
for i in range(1, 61):
    start1 = time.time()
    print(i)
    os.system("python Seminar1.py "+str(i)+".txt")
    end1 = time.time()
    print(end1-start1)
    if (end1-start1) < 20:
        print("solved!")
        solved += 1
    elif (end1-start1) < 30:
        print("Under 30")
        almost += 1
    else:
        pass

end = time.time()
print("Final time:")
print(end - start)
print("Final score: "+str(solved)+"/60 " +str(almost)+" almost")
