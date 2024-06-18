from datetime import datetime 
import os 

time=datetime.now()
print(f"test success \n the time is {time} " )

port=os.getenv("mirion_port")
print(f' port : {port}')

try:
    i=input("this is an interactive shell\n")
except ValueError:
    print("value is not accepted")

with open('../src/data_acquisitions/data/writing_test.txt','w+') as f:
    f.write(i)




