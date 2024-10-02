import numpy as np
import math
import sys
import matplotlib.pyplot as plt
import matplotlib.colors as plt_c
# The following allows the script to work over SSH.  Check it still works when not SSH tunnelling.
plt.switch_backend('agg')
import os
import copy
import statistics as st
import scipy.interpolate as si

# Import user-defined modules .
sys.path.insert(1,'/home/home01/scdrw/scripts/python/processing/run/tools')          # ARC
import readingNek as rn
import general as gn

# Print whole arrays instead of truncating.
np.set_printoptions(threshold=sys.maxsize)


def find_rise_height( filename, order, start_file, jump, final_timestep, numelz, s_val ):

    plot_onImages = 1
    fineness = 1
    plot_frequency = 10

    if (plot_onImages == 1):
        print('Producing an image for verification every ',plot_frequency,' step(s).  Will increase simulation time.')
        print(' ')

    top_data = []
    top_time = []

    order = order - 1

    final_file = int(final_timestep/jump)
    range_vals = [x-(jump-1) for x in np.array(range(1,final_file+1))*jump]

    save_name = './processing/rise_height/images/'
    num_checks = save_name.count('/')
    save_dir_list = save_name.split('/')
    save_dir = '.'
    for i in range(1,num_checks):
        save_dir = ''.join([save_dir,'/',save_dir_list[i]])
        dir_exist = os.path.isdir(save_dir)
        if (dir_exist):
            print("The folder '" + save_dir + "' exists.")
            dir_exist = []
        else:
            os.mkdir(''.join(save_dir))
            print("Creating the folder '" + save_dir + "'.")

    f = open('/home/home01/scdrw/scripts/python/processing/colour_map/full_colour_map.txt','r')
    cm_str = f.read(); cm_str = cm_str[:-1]
    cm_str = [x.split(',') for x in cm_str.split('\n')]
    cm = [[float(v)/256.0 for v in r ] for r in cm_str]
    f.close()

    cm = plt_c.ListedColormap(np.flipud(cm))

    # Reading in mesh data.
    data,time,istep,header,elmap,u_i,v_i,w_i,t_i,s_i = rn.readnek(''.join([filename,'0.f00001']))

    Z = data[:,:,2]

    if (plot_onImages == 1):

        X = data[:,:,0]
        Y = data[:,:,1]
   
        # Looking only at specific vertical slice.
        y_slice = 0.0
        Y = np.array(Y)

        nel,gll = np.shape(Y)
        order = int(round(gll**(1/3),0))
        npoints = nel*gll

        coords1 = []
        coords2 = []
        test = 0.001

        ell = 0
        odd = 0
        for el in range(0,nel):
            ell_check = 1
            for od in range(0,gll):
                tester = abs(Y[el,od] - y_slice)
                if ( tester < test ):
                    mapp = ell + odd
                    coords1.append(el)
                    coords2.append(od)
                    if (ell_check > 0):
                        ell += 1
                        ell_check = 0
                    else:
                        odd += 1

        minx, maxx = round(min(X[coords1,coords2]),0), round(max(X[coords1,coords2]),0)
        minz, maxz = min(Z[coords1,coords2]), max(Z[coords1,coords2])


    file_counter = 0
    print_counter = 0

    # Opening files for writing.
    f = open('./processing/rise_height/riseheight_data.file','w')
    g = open('./processing/rise_height/riseheight_time.file','w')

    start_threshold = (start_file - 1)*jump

    for k in range_vals:

        file_counter += 1

        if ( k > start_threshold ):

            file_num = int((k-1)/jump + 1)

            # Outputs counter to terminal.
            files_remaining = int(final_file - k/jump + 1)
            sys.stdout.write("\r")
            sys.stdout.write("Working on file: ({:3d}/{:3d})...                 ".format(file_num,int(range_vals[-1]/jump)))
            sys.stdout.flush()

            # Reads data files.
            data,time,istep,header,elmap,u_i,v_i,w_i,t_i,s_i = rn.readnek(''.join([filename, \
                '0.f',repr(k).zfill(5)]))

            S = data[:,:,w_i]

            [S_x, S_y] = S.shape

            newZ = []

            for x in range(S_x):
                for y in range(S_y):
                    if (S[x,y] > s_val):
                        newZ.append(round(Z[x,y],2))

            maxPlumeHeight = max(newZ)
            top_data.append(maxPlumeHeight)
            top_time.append(time)

            # Writing to file.
            f.write(str(maxPlumeHeight))
            f.write("\n")
            g.write(str(time))
            g.write("\n")

            if ( (file_counter-1) % plot_frequency == 0 ):

                sys.stdout.write("\r")
                sys.stdout.write("Working on file: ({:3d}/{:3d})...(making image)".format(file_num,int(range_vals[-1]/jump)))
                sys.stdout.flush()

                if (plot_onImages == 1):
                    print_counter += 1

                    Xplane = np.array(X[coords1,coords2])
                    Zplane = np.array(Z[coords1,coords2])
                    Splane = np.array(S[coords1,coords2])

                    # Interpolate to uniform grid for plotting.
                    zpoints = numelz*order
                    npoints = len(Xplane)
                    xpoints = npoints/zpoints
                    xel = xpoints/order

                    xi = np.linspace(minx,maxx,fineness*xpoints)
                    zi = np.linspace(minz,maxz,fineness*zpoints)
                    xi,zi = np.meshgrid(xi,zi)
                    xzplane = np.zeros((npoints,2))
                    xzplane[:,0] = Xplane
                    xzplane[:,1] = Zplane

                    Si = si.griddata(xzplane,Splane,(xi,zi),method='cubic')

                    plt.figure(figsize=(4,10))
                    plt.pcolor(xi,zi,Si,cmap=cm)
                    plt.plot(np.linspace(-1,1,2),maxPlumeHeight*np.ones((2,1)),color='black')
                    plt.savefig(os.path.join(''.join([save_dir,'/rise_height',repr(print_counter).zfill(5),'.png'])),bbox_inches='tight')
                    plt.close('all') 


    # Closing files.
    f.close()
    g.close()

#    f = open('top_data.file','w')
#    for x in top_data:
#        f.write(str(x))
#        f.write("\n")
#    f.close()
#
#    f = open('top_time.file','w')
#    for x in top_time:
#        f.write(str(x))
#        f.write("\n")
#    f.close()

#    for t in range(len((top_time))):
#        if (top_time[t] > start_avg_at_time):
#            start = t
#            print(start)
#            break
#
#    top_mean = st.mean(top_data[start:-1])
#
#    f = open('./processing/rise_height/riseheight_mean.file','w')
#    f.write(str(top_mean))
#    f.close()
#
# Plotting height vs. time
#    fig = plt.figure(figsize=(12,6))
#
#    domain_height = 15
#
#    plt.plot(top_time,top_data)
#    plt.plot([top_time[0],top_time[-1]],[top_mean,top_mean])
#    plt.plot([top_time[start],top_time[start]],[0,domain_height])
#
#    axes = plt.gca()
#    axes.set_xlim([0,max(top_time)])
#    axes.set_ylim([0,domain_height])
#    plt.xlabel('time',fontsize=12)
#    plt.ylabel('height',fontsize=12)
#
#    plt.savefig(os.path.join(''.join([save_dir,'/top_vs_time.png'])),bbox_inches='tight')
#    plt.close('all')

    return


def find_instability_height( filename, order, start_file, jump, final_timestep, numelz, s_val ):

    plot_onImages = 1
    fineness = 1
    plot_frequency = 10

    if (plot_onImages == 1):
        print('Producing an image for verification every ',plot_frequency,' step(s).  Will increase simulation time.')
        print(' ')

    top_data = []
    top_time = []

    order = order - 1

    final_file = int(final_timestep/jump)
    range_vals = [x-(jump-1) for x in np.array(range(1,final_file+1))*jump]

    save_name = './processing/instability_height/images/'
    num_checks = save_name.count('/')
    save_dir_list = save_name.split('/')
    save_dir = '.'
    for i in range(1,num_checks):
        save_dir = ''.join([save_dir,'/',save_dir_list[i]])
        dir_exist = os.path.isdir(save_dir)
        if (dir_exist):
            print("The folder '" + save_dir + "' exists.")
            dir_exist = []
        else:
            os.mkdir(''.join(save_dir))
            print("Creating the folder '" + save_dir + "'.")

    f = open('/home/home01/scdrw/scripts/python/processing/colour_map/full_colour_map.txt','r')
    cm_str = f.read(); cm_str = cm_str[:-1]
    cm_str = [x.split(',') for x in cm_str.split('\n')]
    cm = [[float(v)/256.0 for v in r ] for r in cm_str]
    f.close()

    cm = plt_c.ListedColormap(np.flipud(cm))

    # Reading in mesh data.
    data,time,istep,header,elmap,u_i,v_i,w_i,t_i,s_i = rn.readnek(''.join([filename,'0.f00001']))

    Z = data[:,:,2]

    if (plot_onImages == 1):

        X = data[:,:,0]
        Y = data[:,:,1]
   
        # Looking only at specific vertical slice.
        y_slice = 0.0
        Y = np.array(Y)

        nel,gll = np.shape(Y)
        order = int(round(gll**(1/3),0))
        npoints = nel*gll

        coords1 = []
        coords2 = []
        test = 0.001

        ell = 0
        odd = 0
        for el in range(0,nel):
            ell_check = 1
            for od in range(0,gll):
                tester = abs(Y[el,od] - y_slice)
                if ( tester < test ):
                    mapp = ell + odd
                    coords1.append(el)
                    coords2.append(od)
                    if (ell_check > 0):
                        ell += 1
                        ell_check = 0
                    else:
                        odd += 1

        minx, maxx = round(min(X[coords1,coords2]),0), round(max(X[coords1,coords2]),0)
        minz, maxz = min(Z[coords1,coords2]), max(Z[coords1,coords2])


    file_counter = 0
    print_counter = 0

    # Opening files for writing.
    f = open('./processing/instability_height/instability_height.file','w')
    g = open('./processing/instability_height/instability_time.file','w')

    start_threshold = (start_file - 1)*jump

    for k in range_vals:

        file_counter += 1

        if ( k > start_threshold ):

            file_num = int((k-1)/jump + 1)

            # Outputs counter to terminal.
            files_remaining = int(final_file - k/jump + 1)
            sys.stdout.write("\r")
            sys.stdout.write("Working on file: ({:3d}/{:3d})...                 ".format(file_num,int(range_vals[-1]/jump)))
            sys.stdout.flush()

            # Reads data files.
            data,time,istep,header,elmap,u_i,v_i,w_i,t_i,s_i = rn.readnek(''.join([filename, \
                '0.f',repr(k).zfill(5)]))

            S = data[:,:,w_i]

            [S_x, S_y] = S.shape

            newZ = []

            for x in range(S_x):
                for y in range(S_y):
                    if (S[x,y] < s_val):
                        newZ = round(Z[x,y],2)

            top_data.append(newZ)
            top_time.append(time)

            # Writing to file.
            f.write(str(newZ))
            f.write("\n")
            g.write(str(time))
            g.write("\n")

            if ( (file_counter-1) % plot_frequency == 0 ):

                sys.stdout.write("\r")
                sys.stdout.write("Working on file: ({:3d}/{:3d})...(making image)".format(file_num,int(range_vals[-1]/jump)))
                sys.stdout.flush()

                if (plot_onImages == 1):
                    print_counter += 1

                    Xplane = np.array(X[coords1,coords2])
                    Zplane = np.array(Z[coords1,coords2])
                    Splane = np.array(S[coords1,coords2])

                    # Interpolate to uniform grid for plotting.
                    zpoints = numelz*order
                    npoints = len(Xplane)
                    xpoints = npoints/zpoints
                    xel = xpoints/order

                    xi = np.linspace(minx,maxx,fineness*xpoints)
                    zi = np.linspace(minz,maxz,fineness*zpoints)
                    xi,zi = np.meshgrid(xi,zi)
                    xzplane = np.zeros((npoints,2))
                    xzplane[:,0] = Xplane
                    xzplane[:,1] = Zplane

                    Si = si.griddata(xzplane,Splane,(xi,zi),method='cubic')

                    plt.figure(figsize=(4,10))
                    plt.pcolor(xi,zi,Si,cmap=cm)
                    plt.plot(np.linspace(-1,1,2),newZ*np.ones((2,1)),color='black')
                    plt.savefig(os.path.join(''.join([save_dir,'/instability_height',repr(print_counter).zfill(5),'.png'])),bbox_inches='tight')
                    plt.close('all') 


    # Closing files.
    f.close()
    g.close()

    return
