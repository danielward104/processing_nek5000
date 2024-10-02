import os
import glob

dirs = next(os.walk('.'))[1]
dirs.sort()

print('Location,Initial,Final,Range,Step')

for i in dirs:
    if (len(i) == 7):
        if (os.path.isfile(''.join(['./',i,'/plume0.f00001']))): 
            with open(''.join(['./',i,'/plume0.f00001']),"rb") as f:
                first_line = f.readline()
                time1 = first_line[0:100].decode().split()[7]

            with open(''.join(['./',i,'/plume0.f00002']),"rb") as f:
                first_line = f.readline()
                time_step = first_line[0:100].decode().split()[7]  

            final = len(glob.glob1(i,"plume0.f*"))
            fname = ''.join(['./',i,'/plume0.f',repr(final).zfill(5)])
            if ( os.path.isfile(fname) ):
                with open(fname,"rb") as f:
                    first_line = f.readline()
                    time2 = first_line[0:100].decode().split()[7]

                time_step = round(float(time_step) - float(time1),2)

                time1 = round(float(time1),1)
                time2 = round(float(time2),1)
                diff = round(time2 - time1,1)

                print(i,time1,time2,diff,time_step)
            else:
                print(i,time1,'unknown')
        else:
            print(i,'empty')
