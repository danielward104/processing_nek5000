import numpy as np
import os

def read_mesh( data, fineness, numelz, set_zoom, zoom_vals ):

    X = data[:,:,0]
    Y = data[:,:,1]
    Z = data[:,:,2]

    file_counter = 0

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

    if ( set_zoom ):
        coords11,coords22 = [],[]
        minx, maxx = zoom_vals[0],zoom_vals[1]
        minz, maxz = zoom_vals[2],zoom_vals[3]
        for i in range(0,len(coords1)):
            xi = X[coords1[i],coords2[i]]
            zi = Z[coords1[i],coords2[i]]
            if (xi <= maxx and xi >= minx and zi <= maxz and zi >= minz ):
                coords11.append(coords1[i])
                coords22.append(coords2[i])

        coords1,coords2 = coords11,coords22

    else:
        coords11,coords22 = [],[]
        for i in range(0,len(coords1)):
            xi = X[coords1[i],coords2[i]]
            zi = Z[coords1[i],coords2[i]]
            if ( zi >= 0 ):
                coords11.append(coords1[i])
                coords22.append(coords2[i])

        coords1,coords2 = coords11,coords22

    minx, maxx = min(X[coords1,coords2]), max(X[coords1,coords2])
    minz, maxz = min(Z[coords1,coords2]), max(Z[coords1,coords2])

    minmax = [minx,maxx,minz,maxz]

    print(' ')
    print('Limits of domain (x,z):',str(minx),' ',str(maxx),' ',str(minz),' ',str(maxz))
    print(' ')

    Xplane = np.array(X[coords1,coords2])
    Zplane = np.array(Z[coords1,coords2])

    # Interpolate to uniform grid for plotting.
    zpoints = numelz*order
    npoints = len(Xplane)
    xpoints = npoints/zpoints
    xel = xpoints/order

    xi = np.linspace(minx,maxx,fineness*xpoints)
    zi = np.linspace(minz,maxz,fineness*zpoints)
    xlen,zlen = len(xi),len(zi)

    xi,zi = np.meshgrid(xi,zi)
    xzplane = np.zeros((npoints,2))
    xzplane[:,0] = Xplane
    xzplane[:,1] = Zplane

    return Xplane,Zplane,xzplane,coords1,coords2,xi,zi,xlen,zlen,minmax,nel,gll


def create_folders( fields, nfields, save_dir_stub, set_zoom ):

    print(' '); print('Creating/checking for directories...')
    for i in range(0,nfields):
        name = fields[i].folder
        if (set_zoom): name = name + "_zoom"
        save_name = ''.join([save_dir_stub,name,'/',name])
        num_checks = save_name.count('/')
        save_dir_list = save_name.split('/')
        save_dir = '.'
        for i in range(1,num_checks):
            save_dir = ''.join([save_dir,'/',save_dir_list[i]])
            dir_exist = os.path.isdir(save_dir)
            if (dir_exist):
                dir_exist = []
                print("The folder '" + save_dir + "' exists.")
            else:
                os.mkdir(''.join(save_dir))
                print("Creating the folder '" + save_dir + "'.")

    return


