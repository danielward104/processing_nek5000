import os
import glob

dirs = next(os.walk('.'))[1]
dirs.sort()

for i in dirs:
    if (len(i) == 7):
        if (os.path.isfile(''.join(['./',i,'/azimuthal_averages/azs2d.fld01']))):
            with open(''.join(['./',i,'/azimuthal_averages/azs2d.fld01']),"rb") as f:
                first_line = f.readline()
                time1 = first_line[0:100].decode().split()[4]

            final = len(glob.glob1(''.join([i,"/azimuthal_averages/"]),"azs2d.fld*"))
            if (os.path.isfile(''.join(['./',i,'/azimuthal_averages/azs2d.fld00']))):
                final = final - 1
            with open(''.join(['./',i,'/azimuthal_averages/azs2d.fld',str(final)]),"rb") as f:
                first_line = f.readline()
                time2 = first_line[0:100].decode().split()[4]


            time1 = round(float(time1),1)
            time2 = round(float(time2),1)
            diff = round(time2 - time1,1)

            print(i,time1,time2,diff)
        else:
            print(i,'empty')
