# -*- coding: utf-8 -*-
#
# Python Template
# @Author: SebiMac
# @Date:   2019-03-21 12:51:44 +0100
# @Last modified by:   SebiMac
# @Last modified time: 2019-04-18 21:31:28 +0200

"""
Calculation and plot of a theodolite single cut profile.
"""

import numpy as np
import os
import errno
import pandas as pd
import sys
import matplotlib.pyplot as plt

def main(station_height=0, csv_file=None, titlestr='theodolite single cut'):
    dt = 10
    vert_velo = 2.4 # assumption based on the volume/filling of the baloon

    # read data into a dataframe and transform to np array
    df = pd.read_csv(os.path.join('data', 'csv', csv_file), delimiter=',', index_col=0)
    data_arr = np.array(df)

    # extract data
    elevation = data_arr[:,0]
    azimuth = data_arr[:,1]

    # calculate vectors
    z = np.arange(0, len(elevation))*dt*vert_velo
    x = z * np.sin(azimuth*np.pi/180.)/np.tan(elevation*np.pi/180.)
    y = z * np.cos(azimuth*np.pi/180.)/np.tan(elevation*np.pi/180.)
    r = np.column_stack((x, y))

    r_delta = np.diff(r, axis=0)
    v_spd = np.sqrt(r_delta[:,0]**2 + r_delta[:,1]**2)/dt
    v_dir = np.arctan2(r_delta[:,1], r_delta[:,0])*180/np.pi
    v_dir = (270-v_dir) % 360

    # plot
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(14, 6))
    plt.suptitle(titlestr)

    # horizontal translation
    x_cs = np.cumsum(r_delta[:,0])
    y_cs = np.cumsum(r_delta[:,1])

    ax1.plot(x_cs[0], y_cs[0], 'x', color='b', markersize=20)
    ax1.plot(x_cs[-1], y_cs[-1], 'x', color='r', markersize=20)
    ax1.plot(x_cs, y_cs, '--', color='k', linewidth=0.7, alpha=0.7)
    p = ax1.scatter(x_cs, y_cs, c=z[1:], cmap='rainbow')
    plt.colorbar(p, ax=ax1, label='height above ground [m]')

    # set visuals
    dy = np.nanmax(y_cs) - np.nanmin(y_cs)
    dx = np.nanmax(x_cs) - np.nanmin(x_cs)
    ds = dx - dy
    if ds > 0:
        ax1.set_xlim([np.nanmin(x_cs)-100, np.nanmax(x_cs)+100])
        ax1.set_ylim([np.nanmin(y_cs)-ds/2., np.nanmax(y_cs)+ds/2.])
    elif ds < 0:
        ax1.set_xlim([np.nanmin(x_cs)-np.abs(ds)/2., np.nanmax(x_cs)+np.abs(ds)/2.])
        ax1.set_ylim([np.nanmin(y_cs)-100., np.nanmax(y_cs)+100])
    # ax1.set_aspect(aspect=1) # can be used to reduce the whole box to the corret aspect ratio
    ax1.set_title('horizontal translation (blue cross = starting point)')
    ax1.set_xlabel('x [m]')
    ax1.set_ylabel('y [m]')
    ax1.grid(True)

    # vertical plot
    wv = ax2.plot(v_spd[1:], z[1:-1], label='wind velocity')
    ax22 = ax2.twiny()
    wd = ax22.plot(v_dir[1:], z[1:-1], 'r*', label='wind direction')
    ax22.set_xticks(np.arange(0,361,45))
    ax22.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N'])

    ax2.set_xlabel('wind velocity [m/s]')
    ax2.set_ylabel('height above ground [m]')
    ax22.set_xlabel('wind direction [°]')
    lns = wv+wd
    labs = [l.get_label() for l in lns]
    ax2.legend(lns, labs)
    ax2.grid(True)

    # create figure directory
    fig_dir = 'figures'
    try:
        os.makedirs(fig_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # save figure
    print('Saving figure ...')
    plt.savefig(os.path.join(fig_dir, "".join([csv_file.split('.')[0], '.png'])))
    return None


if __name__ == '__main__':
    h = sys.argv[2]
    data = sys.argv[2]

    main(station_height=h, csv_file=data)
