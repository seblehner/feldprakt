# -*- coding: utf-8 -*-
#
# Python Template
# @Author: SebiMac
# @Date:   2019-04-05 23:19:06 +0200
# @Last modified by:   SebiMac
# @Last modified time: 2019-04-19 03:15:31 +0200
"""
Plotting routines for time series data from csv files.
"""
from datetime import datetime
import errno
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import os
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import sys

def main(plotroutine=None, csv_filename=None, var_dict=None, figurename=None, titlestr=None, flag=None, timebegin=None, timeend=None, timemarker=None, hour_interval=3, time_freq='D'):
    # define some methods
    register_matplotlib_converters()
    def set_visuals(ax, pl, spine_location):
        # set all kinds of visuals to correspond to the line color
        ax.yaxis.label.set_color(pl.get_color())
        ax.tick_params(axis='y', colors=pl.get_color())
        ax.spines[spine_location].set_color(pl.get_color())
        ax.spines[spine_location].set_linewidth(2)
        return None

    def set_time_axis(ax, time, withDate=True):
        # set labelling, lim and some visuals for the time/x-axis
        ax.set_xlabel('time UTC')
        hours = mdates.HourLocator(interval=1)
        if withDate:
            ax.set_xlim([time[0], time[-1]])
            ax.spines['top'].set_linewidth(2)
            ax.spines['bottom'].set_linewidth(2)
            h_fmt = mdates.DateFormatter('%d.%m.%y - %H:%M')
            fig.autofmt_xdate(rotation=45)
        else:
            dt2 = (time[1]-time[0])/2
            ax.set_xlim([time[0]-dt2, time[-1]+dt2])
            h_fmt = mdates.DateFormatter('%H')
        ax.xaxis.set_major_locator(hours)
        ax.xaxis.set_major_formatter(h_fmt)
        return None

    def set_time_axis_compare(ax, time, hour_interval=1):
        ax.set_xlabel('time UTC')
        hours = mdates.HourLocator(interval=hour_interval)
        ax.set_xlim([time[0], time[-1]])
        h_fmt = mdates.DateFormatter('%d.%m.%y - %H:%M')
        fig.autofmt_xdate(rotation=45)
        ax.xaxis.set_major_locator(hours)
        ax.xaxis.set_major_formatter(h_fmt)
        return None

    # create figure directory
    fig_dir = 'figures'
    try:
        os.makedirs(fig_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # timeseries from hobo csv file
    if plotroutine == 'hobo':
        # read into dataframe from csv file
        df = pd.read_csv(os.path.join('data', 'csv', csv_filename), index_col=0, sep=',')
        timestr = df['time']
        if len(timestr[0]) > 18:
            time = [datetime.strptime(tt, '%d.%m.%Y %H:%M:%S') for tt in timestr]
        else:
            time = [datetime.strptime(tt, '%d.%m.%y %H:%M:%S') for tt in timestr]

        # create figure
        fig, ax = plt.subplots(figsize=(12, 6))
        plt.subplots_adjust(left=0.20, right=0.8)
        axr1 = ax.twinx()

        # iterate through dictionary and plot specified parameters
        pls = [] # used for the legend
        for index, item in enumerate(var_dict.items()):
            if item[1]:
                if item[0] == 'wind_spd':
                    y = df['wind speed [m/s]']

                    # plotting
                    p1, = ax.plot(time, y, 'cyan', label='wind speed')
                    ax.set_ylabel('wind speed [m/s]')
                    set_visuals(ax, p1, 'left')
                    pls.append(p1)

                elif item[0] == 'wind_gusts':
                    y = df['wind gusts [m/s]']

                    # plotting
                    p2, = ax.plot(time, y, 'magenta', label='wind gusts')
                    ax.set_ylabel('wind speed [m/s]')
                    pls.append(p2)

                elif item[0] == 'wind_dir':
                    y = df['wind direction [deg]']

                    # plotting
                    p3, = axr1.plot(time, y, 'k*', label='wind direction')
                    axr1.set_ylabel('wind direction [°]')
                    axr1.set_ylim([0, 360])
                    axr1.set_yticks(np.arange(0,361,45))
                    axr1.set_yticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N'])
                    set_visuals(axr1, p3, 'right')
                    pls.append(p3)

                elif item[0] == 'temp':
                    y = df['temperature [deg C]']

                    # plotting
                    if axr1.lines:
                        axr2 = ax.twinx()
                        axr2.spines['right'].set_position(('axes', 1.1))
                        axr2.spines['right'].set_visible(True)

                        p4, = axr2.plot(time, y, 'r', label='temperature')
                        axr2.set_ylabel('temperature [°C]')
                        set_visuals(axr2, p4, 'right')
                    else:
                        p4, = axr1.plot(time, y, 'r', label='temperature')
                        axr1.set_ylabel('temperature [°C]')
                        set_visuals(axr1, p4, 'right')
                    pls.append(p4)

                elif item[0] == 'rel_hum':
                    y = df['relative humidity [%]']

                    # plotting
                    if axr1.lines:
                        try:
                            if axr2.lines:
                                axr3 = ax.twinx()
                                axr3.spines['right'].set_position(('axes', 1.2))
                                axr3.spines['right'].set_visible(True)

                                p5, = axr3.plot(time, y, 'g', label='relative humidity')
                                axr3.set_ylabel('relative humidity [%]')
                                axr3.set_ylim([35, 100])
                                set_visuals(axr3, p5, 'right')
                        except:
                            axr2 = ax.twinx()
                            axr2.spines['right'].set_position(('axes', 1.1))
                            axr2.spines['right'].set_visible(True)

                            p5, = axr2.plot(time, y, 'g', label='relative humidity')
                            axr2.set_ylabel('relative humidity [%]')
                            axr2.set_ylim([35, 100])
                            set_visuals(axr2, p5, 'right')
                    else:
                        p5, = axr1.plot(time, y, 'g', label='relative humidity')
                        axr1.set_ylabel('relative humidity [%]')
                        axr1.set_ylim([35, 100])
                        set_visuals(axr1, p5, 'right')
                    pls.append(p5)

                elif item[0] == 'pres':
                    y = df['pressure [hPa]']

                    # plotting
                    if ax.lines:
                        axl2 = ax.twinx()
                        axl2.yaxis.tick_left()
                        axl2.yaxis.set_label_position('left')

                        axl2.set_ylabel('air pressure [hPa]')
                        axl2.spines['left'].set_position(('axes', -0.1))
                        axl2.spines['left'].set_visible(True)

                        p6, = axl2.plot(time, y, 'b', label='pressure')
                        axl2.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
                        set_visuals(axl2, p6, 'left')
                    else:
                        p6, = ax.plot(time, y, 'b', label='pressure')
                        ax.set_ylabel('air pressure [hPa]')
                        ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
                        set_visuals(ax, p6, 'left')
                    pls.append(p6)

                elif item[0] == 'radiation':
                    y = df['radiation [W/m2]']

                    # plotting
                    if ax.lines:
                        try:
                            if axl2.lines:
                                axl3 = ax.twinx()
                                axl3.yaxis.tick_left()
                                axl3.yaxis.set_label_position('left')

                                axl3.set_ylabel('sun radiation [W/m2]')
                                axl3.spines['left'].set_position(('axes', -0.22))
                                axl3.spines['left'].set_visible(True)

                                p7, = axl3.plot(time, y, 'y', label='radiation')
                                set_visuals(axl3, p7, 'left')
                        except:
                            axl2.yaxis.tick_left()
                            axl2.yaxis.set_label_position('left')

                            axl2.set_ylabel('sun radiation [W/m2]')
                            axl2.spines['left'].set_position(('axes', -0.1))
                            axl2.spines['left'].set_visible(True)

                            p7, = axl2.plot(time, y, 'y', label='radiation')
                            set_visuals(axl2, p7, 'left')
                    else:
                        ax.set_ylabel('sun radiation [W/m2]')
                        p7, = ax.plot(time, y, 'y', label='radiation')
                        set_visuals(ax, p7, 'left')
                    pls.append(p7)

        # set title
        if not titlestr:
            plt.title("".join(['HOBO time series from ', time[0].strftime('%d.%m.%Y - %H:%M'), ' to ', time[-1].strftime('%d.%m.%Y - %H:%M')]))
        else:
            plt.title(titlestr)
        # set time/x-axis and legend
        set_time_axis(ax, time, withDate=False)
        labels = [pl.get_label() for pl in pls]
        fig.legend(pls, labels, loc='upper center', ncol=len(labels))
        ax.grid(True)

        # save figure
        print('Saving figure ...')
        plt.savefig(os.path.join(fig_dir, figurename))

    if plotroutine == 'hobo_multi':
        # height correction for stations: dp = -g * rho * dz
        station_heights = {'Campingplatz': 771,
                         'Lanzenkreuz': 791,
                         'Seetal': 842,
                         'Stübming': 824,
                         'UnterDerLanzen': 733}
        metrs = []
        for num, itm in enumerate(station_heights.items()):
            metrs.append(itm[1])
        avg_height = np.mean(metrs)

        # read into dataframe from csv file
        id = []
        dflist = []
        dplist = []
        for index, item in enumerate(csv_filename.items()):
            height_corr = station_heights[item[0]] - avg_height
            dp = -9.81*1.1*height_corr
            id.append(item[0])
            dflist.append(pd.read_csv(os.path.join('data', 'csv', item[1]), index_col=0, sep=','))
            dplist.append(dp)

        def get_time_vec(df):
            timestr = df['time']
            if len(timestr[0]) > 18:
                time = [datetime.strptime(tt, '%d.%m.%Y %H:%M:%S') for tt in timestr]
            else:
                time = [datetime.strptime(tt, '%d.%m.%y %H:%M:%S') for tt in timestr]
            return time

        # create figure
        # 1) wind gusts, wind speed, wind direction comparison
        for i, flags in enumerate(flag.items()):
            if flags[0] == 'wind_gusts':
                if flags[1]:
                    fig, (ax, ax2, ax3) = plt.subplots(nrows=3, sharex=True, figsize=(13, 8))
                    switch = 1
                else:
                    fig, (ax, ax2) = plt.subplots(nrows=2, sharex=True, figsize=(12, 7))
                    switch = 0

        pls = []
        colrs = ['b', 'g', 'r', 'orange', 'magenta', 'cyan']
        for ind, df in enumerate(dflist):
            colr = colrs[ind]
            lab = id[ind]
            time = get_time_vec(df)
            y = df['wind speed [m/s]']
            p, = ax.plot(time, y, color=colr, label=lab)
            ax.set_ylabel('wind speed [m/s]')
            pls.append(p)


            if switch == 1:
                y = df['wind gusts [m/s]']
                ax3.plot(time, y, '--', color=colr)
                ax3.set_ylabel('wind gusts [m/s]')
                ax3.grid(True)

            y = df['wind direction [deg]']
            ax2.plot(time, y, '*', color=colr)
            ax2.set_ylabel('wind direction [°]')
            ax2.set_ylim([0, 360])
            ax2.set_yticks(np.arange(0,361,45))
            ax2.set_yticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N'])

        # set title
        if not titlestr:
            ax.set_title("".join(['HOBO time series from ', time[0].strftime('%d.%m.%Y - %H:%M'), ' to ', time[-1].strftime('%d.%m.%Y - %H:%M')]))
        else:
            ax.set_title(titlestr)

        # set time/x-axis and legend
        set_time_axis_compare(ax, time)
        labels = [pl.get_label() for pl in pls]
        plt.xlabel('time [UTC]')
        fig.legend(pls, labels, loc='upper center', ncol=len(labels))

        ax.grid(True)
        ax2.grid(True)

        # save figure
        print('Saving figure ...')
        if switch == 1:
            savename = 'wind_speed_direction_gusts.png'
        else:
            savename = 'wind_speed_direction.png'
        plt.savefig(os.path.join(fig_dir, "".join([figurename, savename])))


        # create figure
        # 2) Temperature, RH, pressure
        for i, flags in enumerate(flag.items()):
            if flags[0] == 'pressure':
                if flags[1]:
                    fig, (ax, ax2, ax3) = plt.subplots(nrows=3, sharex=True, figsize=(13, 8))
                    switch = 1
                else:
                    fig, (ax, ax2) = plt.subplots(nrows=2, sharex=True, figsize=(12, 7))
                    switch = 0

        pls = []
        colrs = ['b', 'g', 'r', 'orange', 'magenta', 'cyan']
        for ind, df in enumerate(dflist):
            colr = colrs[ind]
            lab = id[ind]
            time = get_time_vec(df)
            y = df['temperature [deg C]']
            p, = ax.plot(time, y, color=colr, label=lab)
            ax.set_ylabel('temperature [°C]')
            pls.append(p)

            y = df['relative humidity [%]']
            ax2.plot(time, y, '--', color=colr)
            ax2.set_ylabel('relative humidity [%]')
            ax2.set_ylim([35, 100])

            if switch == 1:
                y = df['pressure [hPa]']
                dp = dplist[ind]
                # station height, density and gravitational acceleration need to be verified
                #ax3.plot(time, y-dp/100, '-.', color=colr)
                ax3.plot(time, y, '-.', color=colr)
                ax3.set_ylabel('pressure [hPa]')
                ax3.grid(True)

        # set title
        if not titlestr:
            ax.set_title("".join(['HOBO time series from ', time[0].strftime('%d.%m.%Y - %H:%M'), ' to ', time[-1].strftime('%d.%m.%Y - %H:%M')]))
        else:
            ax.set_title(titlestr)

        # set time/x-axis and legend
        set_time_axis_compare(ax, time)
        labels = [pl.get_label() for pl in pls]
        fig.legend(pls, labels, loc='upper center', ncol=len(labels))
        ax.grid(True)
        ax2.grid(True)
        plt.xlabel('time [UTC]')

        # save figure
        print('Saving figure ...')
        if switch == 1:
            savename = 'temp_rh_pressure.png'
        else:
            savename = 'temp_rh.png'
        plt.savefig(os.path.join(fig_dir, "".join([figurename, savename])))


    elif plotroutine == 'hobo_precip':
        # read into dataframe from csv file
        df = pd.read_csv(os.path.join('data', 'csv', csv_filename), index_col=0, sep=',')
        timestr = df['time']
        if len(timestr[0]) > 18:
            time = [datetime.strptime(tt, '%d.%m.%Y %H:%M:%S') for tt in timestr]
        else:
            time = [datetime.strptime(tt, '%d.%m.%y %H:%M:%S') for tt in timestr]

        # accumulated ticks
        precip_ticks = df['precip ticks [0.2mm]']
        precip_num = [np.float(str(ti).split(',')[0].replace(' ', '')) for ti in precip_ticks.values]

        # diff and transform in precipitation mm
        precip_amount = np.diff(precip_num)*0.2

        new_pd_ticks = pd.Series(data=precip_ticks, index=time)
        new_pd_series = pd.Series(data=precip_amount, index=time[:-1])
        precip_hourly = new_pd_series.resample('H', label='right', closed='right').sum()
        precip_3hourly = new_pd_series.resample('3H', label='right', closed='right').sum()

        # create figure
        width_hourly = np.min(np.diff(mdates.date2num(precip_hourly.index)))
        width_3hourly = np.min(np.diff(mdates.date2num(precip_3hourly.index)))
        #ax.bar(x_values, y_values, width=width, ec="k")

        fig, (ax, ax2, ax3) = plt.subplots(nrows=3, figsize=(12, 9))
        ax.grid(True)
        ax2.grid(True)
        ax3.grid(True)
        ax.plot(time, precip_num)
        ax.set_title('precipitation ticks')
        ax.set_ylabel('precipitation ticks [0.2 mm]')
        ax2.bar(precip_hourly.index, precip_hourly, width=-width_hourly*0.9, align='edge')
        ax2.set_title('hourly precipitation')
        ax2.set_ylabel('hourly precipitation [mm/h]')
        ax3.bar(precip_3hourly.index, precip_3hourly, width=-width_3hourly*0.9, align='edge')
        ax3.set_title('3-hourly precipitation')
        ax3.set_ylabel('3-hourly precipitation [mm/3h]')

        if timebegin is not None:
            time = pd.date_range(datetime.strptime(timebegin, '%Y%m%d%H'), end=datetime.strptime(timeend, '%Y%m%d%H'), freq=time_freq)


        #ax.set_xlim([time[0], time[1]])
        set_time_axis_compare(ax, time, hour_interval=hour_interval)
        set_time_axis_compare(ax2, time, hour_interval=1)
        set_time_axis_compare(ax3, time, hour_interval=3)

        plt.suptitle('observed precipitation', fontsize=20)
        # save figure
        print('Saving figure ...')
        plt.savefig(os.path.join(fig_dir, "".join([figurename, 'new.png'])))

    # synoptic observations
    elif plotroutine == 'syn':
        # read into dataframe from csv file
        df = pd.read_csv(os.path.join('data', 'csv', csv_filename), sep=',')

        ## get important data
        # time
        timestr = df['UTC'].values
        time = [datetime.strptime(tt, '%H:%M:%S') for tt in timestr]

        # assmann
        T_assmann = df['T_assmann'].values
        TF_assmann = df['Tf_assmann'].values
        TD_assmann = df['Td_assmann'].values
        RH_assmann = df['RH_assmann'].values

        # davis
        T_davis = df['T_davis'].values
        TD_davis = df['Td_davis'].values
        RH_davis = df['RH_davis'].values

        # dew-point mirror
        TD_mirror = df['Td_mirror'].values

        # kestrel
        T_kestrel = df['T_kestrel'].values
        TD_kestrel = df['Td_kestrel'].values
        RH_kestrel = df['RH_kestrel'].values
        p_kestrel = df['p_kestrel'].values

        # davis-station
        T_davisstation = df['T_davis-station'].values
        TD_davisstation = df['Td_davis-station'].values
        RH_davisstation = df['RH_davis-station'].values

        # humiport
        T_humiport = df['T_humiport'].values
        RH_humiport = df['RH_humiport'].values

        # vaisala
        p_vaisala = df['p_vaisala'].values

        visibility = df['visibility'].values
        clouds_high = df['clouds_high'].values
        clouds_medium = df['clouds_medium'].values
        clouds_low = df['clouds_low'].values
        cloudiness = df['cloudiness'].values
        cloud_base = df['cloud_base'].values
        cloudiness_low = df['cloudiness_low'].values

        # define colors
        Cassmann = 'r'
        Cdavis = 'b'
        Ckestrel = 'g'
        Cdavisstation = 'purple'
        Chumiport = 'orange'

        # define labels
        Lassmann = 'Assmann'
        Ldavis = 'Davis'
        Lkestrel = 'Kestrel'
        Ldavisstation = 'Davis-Station'
        Lhumiport = 'Humiport'

        # create figure
        fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True, figsize=(12, 8))
        plt.subplots_adjust(right=0.85)
        axr1 = ax1.twinx()
        axr11 = ax1.twinx()
        axr2 = ax2.twinx()

        # plot temperature, dew-point temperature and relative humidity
        def plot_t_td_rh(axleft, axright, time, t, td, rh, label, color):
            p = axleft.plot(time, t, '-', label=label, color=color, linewidth=2)
            axleft.plot(time, td, '--', label=label, color=color, linewidth=2)
            axright.plot(time, rh, ':', label=label, color=color, linewidth=2)
            return p

        # plots
        p1 = plot_t_td_rh(ax1, axr1, time, T_assmann, TD_assmann, RH_assmann, label=Lassmann, color=Cassmann)
        p2 = plot_t_td_rh(ax1, axr1, time, T_davis, TD_davis, RH_davis, label=Ldavis, color=Cdavis)
        p3 = plot_t_td_rh(ax1, axr1, time, T_kestrel, TD_kestrel, RH_kestrel, label=Lkestrel, color=Ckestrel)
        p4 = plot_t_td_rh(ax1, axr1, time, T_davisstation, TD_davisstation, RH_davisstation, label=Ldavisstation, color=Cdavisstation)
        p5 = plot_t_td_rh(ax1, axr1, time, T_humiport, np.zeros(len(time))*np.nan, RH_humiport, label=Lhumiport, color=Chumiport)
        axr1.set_ylim([35, 100]) # set lim for relative humidity

        # set spine position
        axr11.spines['right'].set_position(('axes', 1.1))
        axr11.spines['right'].set_visible(True)

        # plot pressure
        p6 = axr11.plot(time, p_vaisala, '-.', label='Vaisala - pressure', color='k', linewidth=2)
        axr11.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        axr11.set_ylabel('pressure [hPa]')

        # set title and legend
        ax1.set_title(titlestr)
        pls = p1+p2+p3+p4+p5+p6
        labels = [pl.get_label() for pl in pls]
        fig.legend(pls, labels, loc=[0.125, 0.483], ncol=len(labels), prop={'size': 8})
        ax1.grid(True)
        ax1.set_ylabel('temperature [°C]')
        axr1.set_ylabel('relative humidity [%]')

        # plot synoptic observations
        # height (y) and time (x) axis
        z = np.arange(0, 8001, 10)
        set_time_axis(ax2, time, withDate=False)
        timeticks = ax2.get_xticks()

        # difference between ticks on x-axis; used for positioning and horizontal scaling
        dx = (timeticks[1] - timeticks[0])/2

        # add a path patch for the cloud structure
        def create_cloud_patch(axis, x, dx, y, calpha, ctype, scaling_factor):
            x = x-dx/3.
            height_scaling = 150*0.3 + 150*0.7*scaling_factor/8. # used for scaling the patch vertically
            dx = dx*0.3 + dx*0.7*scaling_factor/8.
            Path = mpath.Path
            # points and type of line path
            path_data = [
                (Path.MOVETO, [x, y]),
                (Path.LINETO, [x-dx, y]),
                (Path.CURVE4, [x-dx*2, y+height_scaling*2]),
                (Path.CURVE4, [x-dx*2, y+height_scaling*10]),
                (Path.CURVE4, [x-dx/1.3, y+height_scaling*7]),
                (Path.LINETO, [x-dx/1.3, y+height_scaling*7]),
                (Path.CURVE4, [x-dx*1.5, y+height_scaling*12]),
                (Path.CURVE4, [x-dx*0.2, y+height_scaling*17]),
                (Path.CURVE4, [x, y+height_scaling*10]),
                (Path.LINETO, [x, y+height_scaling*10]),
                (Path.CURVE4, [x+dx*0.2, y+height_scaling*17]),
                (Path.CURVE4, [x+dx*1.5, y+height_scaling*12]),
                (Path.CURVE4, [x+dx/1.3, y+height_scaling*7]),
                (Path.LINETO, [x+dx/1.3, y+height_scaling*7]),
                (Path.CURVE4, [x+dx*2, y+height_scaling*10]),
                (Path.CURVE4, [x+dx*2, y+height_scaling*2]),
                (Path.CURVE4, [x+dx, y]),
                (Path.LINETO, [x, y]),
                (Path.CLOSEPOLY, [0, 0])]
            codes, verts = zip(*path_data)
            path = mpath.Path(verts, codes)
            patch = mpatches.PathPatch(path, FaceColor=[1*calpha, 1*calpha, 1*calpha])
            axis.add_patch(patch)

            # add text about the cloud type information (can be omitted)
            #ptred = axis.text(x+dx/3, y+1400, int(ctype), FontSize=15, Color='m')
            return None

        # plots text about the cloudiness
        def plot_cloudiness(axis, x, dx, y, cl, cl_low):
            if np.isnan(cl):
                cl_str = None
            else:
                cl_str = str(int(cl))+'/8'
            axis.text(x-dx/1.7, -z[-1]/4., cl_str, FontSize=15, Color='k')

            if np.isnan(cl_low):
                cl_low = None
            else:
                cl_low = str(int(cl_low))
            if y > 500:
                axis.text(x-dx/3, y-500, cl_low, FontSize=15, Color='c')
            else:
                axis.text(x-dx/3, y, cl_low, FontSize=15, Color='c')
            return None

        # plot cloudiness text
        for i in range(len(timeticks)):
            if not (np.isnan(cloud_base[i]) or cloud_base[i]>4000):
                plot_cloudiness(ax2, timeticks[i], dx, cloud_base[i], cloudiness[i], cloudiness_low[i])
            else:
                plot_cloudiness(ax2, timeticks[i], dx, -2000, cloudiness[i], np.nan)

        # create low clouds
        for i in range(len(clouds_low)):
            if not np.isnan(clouds_low[i]):
                create_cloud_patch(ax2, timeticks[i], dx, cloud_base[i], calpha=0.3, ctype=clouds_low[i], scaling_factor=cloudiness_low[i])

        # create medium clouds
        for i in range(len(clouds_medium)):
            if not np.isnan(clouds_medium[i]):
                if np.isnan(cloudiness_low[i]):
                    scaling_low = 0
                else:
                    scaling_low = cloudiness_low[i]
                create_cloud_patch(ax2, timeticks[i], dx, 4000, calpha=0.6, ctype=clouds_medium[i], scaling_factor=cloudiness[i]-scaling_low)

        # create high clouds
        for i in range(len(clouds_high)):
            if not np.isnan(clouds_high[i]):
                if np.isnan(cloudiness_low[i]):
                    scaling_low = 0
                else:
                    scaling_low = cloudiness_low[i]
                create_cloud_patch(ax2, timeticks[i], dx, 6000, calpha=0.85, ctype=clouds_high[i], scaling_factor=cloudiness[i]-scaling_low)

        # create descriptive text
        #ax2.text(timeticks[5], z[-1]*1.02, 'cloud type', FontSize=8, color='m', backgroundcolor=[0.9, 0.9, 0.9])
        ax2.text(timeticks[0]-dx/1.7, -z[-1]/6, 'cloudiness total', FontSize=10, color='k')
        ax2.text(timeticks[0]-dx*0.8, z[-1]*1.02, 'cloudiness low', FontSize=8, color='c', backgroundcolor=[0.9, 0.9, 0.9])
        ax2.text(timeticks[0]-dx*0.8, z[-1]*1.15, 'T: drawn through; Td: dashed; RH: dotted', FontSize=8, color='k')
        #ax2.text(timeticks[0]+dx*0.9, z[-1]*1.02, 'visibility', FontSize=8, color='y', backgroundcolor=[0.9, 0.9, 0.9])
        #ax2.add_patch(mpatches.Rectangle((timeticks[0]-dx, z[-1]*0.99), dx*13, 700, FaceColor=[0.9, 0.9, 0.9], EdgeColor='k'))

        # set lims, labels, time axis properties
        ax2.set_ylim([0, 8001])
        axr2.bar(timeticks+dx/3, visibility, width=0.005, fill=False, hatch='/', EdgeColor='y', linewidth=1.2)
        axr2.set_ylabel('horizontal visibility [km]', color='y')
        axr2.tick_params(axis='y', colors='y')
        ax2.set_ylabel('height above ground [m]')
        ax2.set_xlabel('time UTC')
        set_time_axis(ax2, time, withDate=False)

        # save figure
        print('Saving figure ...')
        plt.savefig(os.path.join(fig_dir, "".join([figurename, '.png'])))

        ## barplot height of cloud base
        # approximation: spread * 125
        cb_assmann = (T_assmann - TD_assmann) * 125
        cb_davis = (T_davis - TD_davis) * 125
        cb_kestrel = (T_kestrel - TD_kestrel) * 125
        cb_davisstation = (T_davisstation - TD_davisstation) * 125

        # plot bars
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.bar(timeticks-dx/6*4, cloud_base, width=dx/3, color='y', align='center', label='observation')
        ax.bar(timeticks-dx/6*2, cb_assmann, width=dx/3, color='r', align='center', label='assmann')
        ax.bar(timeticks, cb_davis, width=dx/3, color='b', align='center', label='davis')
        ax.bar(timeticks+dx/6*2, cb_kestrel, width=dx/3, color='g', align='center', label='kestrel')
        ax.bar(timeticks+dx/6*4, cb_davisstation, width=dx/3, color='purple', align='center', label='davis-station')
        set_time_axis(ax, time, withDate=False)
        plt.title('Cloud base height')
        ax.set_ylabel('height [m]')
        plt.legend(loc=2)

        # save figure
        print('Saving figure ...')
        plt.savefig(os.path.join(fig_dir, "".join([figurename, '_cloudbase.png'])))


    # synoptic forecast
    elif plotroutine == 'syn_forecast':
        df = pd.read_csv(os.path.join('data', 'csv', csv_filename), sep=',')
        timestr = df['UTC'].values
        try:
            time = [datetime.strptime(tt, '%Y-%m-%d %H:%M:%S') for tt in timestr]
        except:
            time = [datetime.strptime(tt[:-4], '%Y-%m-%d %H:%M:%S') for tt in timestr]
        T_fcst = df['T_forecast [°C]'].values
        Td_fcst = df['Td_forecast [°C]'].values
        vs_fcst = df['wind_speed_forecast [m/s]'].values
        vd_fcst = df['wind_direction_forecast [m/s]'].values

        fig, ax = plt.subplots(nrows=4, ncols=2, sharex='col', figsize=(12, 15))

        ax[0,0].plot(time, T_fcst, 'b')
        ax[0,0].set_ylabel('temperature [°C]')
        ax[0,0].set_title('temperature forecast')

        ax[1,0].plot(time, Td_fcst, 'b--')
        ax[1,0].set_ylabel('dew-point temperature [°C]')
        ax[1,0].set_title('dew-point temperature forecast')

        ax[2,0].plot(time, vs_fcst, 'b')
        ax[2,0].set_ylabel('wind speed [m/s]')
        ax[2,0].set_title('wind speed forecast')

        ax[3,0].plot(time, vd_fcst, 'b*')
        ax[3,0].set_ylabel('wind direction')
        ax[3,0].set_title('wind direction forecast')
        ax[3,0].set_ylim([0, 360])
        ax[3,0].set_yticks(np.arange(0,361,45))
        ax[3,0].set_yticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N'])

        plt.suptitle('forecast 19.05.2019 15 UTC (blue)\n validation (red)', fontsize=20)

        cl_fcst = df['cloudiness_forecast'].values
        clb_fcst = df['cloud_base_forecast [m]'].values
        ra_fcst = df['rain_amount_forecast [mm/h]'].values
        rp_fcst = df['rain_probability_forecast [%]'].values

        #fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4, sharex=True, figsize=(12, 15))

        ax[0,1].plot(time, cl_fcst, 'b')
        ax[0,1].set_ylabel('cloudiness')
        ax[0,1].set_title('cloudiness forecast')
        ax[0,1].set_ylim([-0.3, 8.3])

        ax[1,1].plot(time, clb_fcst, 'b')
        ax[1,1].set_ylabel('cloud base [m]')
        ax[1,1].set_title('cloud base forecast')

        ax[2,1].plot(time, ra_fcst, 'b')
        ax[2,1].set_ylabel('amount of rain [mm/h]')
        ax[2,1].set_title('rain amount forecast')

        ax[3,1].plot(time, rp_fcst, 'b')
        ax[3,1].set_ylabel('probability of rain')
        ax[3,1].set_title('rain probability forecast')
        ax[3,1].set_ylim([0, 100])

        for axit in ax.ravel():
            axit.grid(True)

        # validation
        T_vali = df['T_validation [°C]'].values
        Td_vali = df['Td_validation [°C]'].values
        vs_vali = df['wind_speed_validation [m/s]'].values
        vd_vali = df['wind_direction_validation [m/s]'].values
        cl_vali = df['cloudiness_validation'].values
        clb_vali = df['cloud_base_validation [m]'].values
        ra_vali = df['rain_amount_validation [mm/h]'].values
        rp_vali = df['rain_probability_validation'].values

        ax[0,0].plot(time, T_vali, 'r')
        ax[1,0].plot(time, Td_vali, 'r--')
        ax[2,0].plot(time, vs_vali, 'r')
        ax[3,0].plot(time, vd_vali, 'r*')
        ax[0,1].plot(time, cl_vali, 'r')
        ax[1,1].plot(time, clb_vali, 'r')
        ax[2,1].plot(time, ra_vali, 'r')
        ax[3,1].plot(time, rp_vali, 'r')

        if timebegin is not None:
            time = pd.date_range(datetime.strptime(timebegin, '%Y%m%d%H'), end=datetime.strptime(timeend, '%Y%m%d%H'), freq='H')

        if timemarker is not None:
            timemark = datetime.strptime(timemarker, '%Y%m%d%H')
            for axit in ax.reshape(-1):
                axit.axvline(x=timemark, color='k', linestyle='--')

        set_time_axis_compare(ax[3,0], time, hour_interval=3)
        set_time_axis_compare(ax[3,1], time, hour_interval=3)
        print('Saving figure ...')
        plt.savefig(os.path.join(fig_dir, "".join([figurename, '_new.png'])))
    return None

if __name__ == '__main__':
    plotroutine = sys.argv[1]
    csv_file = sys.argv[2]
    dict = sys.argv[3]
    name = sys.argv[4]
    main(plotroutine=plotroutine, csv_filename=csv_file, csv_file2=dict, figurename=name)
