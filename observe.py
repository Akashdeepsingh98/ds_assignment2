import matplotlib.pyplot as plt 
from numpy import genfromtxt

constMem1Thread = genfromtxt('constantfile.csv',delimiter=',')
print(constMem1Thread)
plt.plot(constMem1Thread[:,0], constMem1Thread[:,1])
plt.xlabel('Memory Size(in MB)')
plt.ylabel('Time (in seconds)')
plt.show()