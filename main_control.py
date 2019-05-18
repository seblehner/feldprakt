# -*- coding: utf-8 -*-
#
# Python Template
# @Author: SebiMac
# @Date:   2019-03-21 12:54:43 +0100
# @Last modified by:   SebiMac
# @Last modified time: 2019-04-19 04:27:35 +0200
"""
Control script for the use of field exercise data tools.
Can be used to play around with the included test data or modified to use other data.
"""
from datetime import datetime
import sys

import python.pressure_reduction_msl as presreduc
import python.excel_to_csv as etcsv
import python.raso_to_kml as rasokml
import python.theo_to_kml as theokml
import python.theo_single_cut as thsin
import python.theo_double_cut as thdou
import python.plotting_routines as plotrout

# 0 = ignore; 1 = execute
workflow_dict = {'pressure_reduction':           0,
                 'excel_to_csv_theo_gearth':     0,
                 'excel_to_csv_theo_cut':        0,
                 'excel_to_csv_hobo':            0,
                 'excel_to_csv_syn':             0,
                 'theo_calc_single_cut':         0,
                 'theo_calc_double_cut':         0,
                 'raso_to_kml':                  0,
                 'theo_to_kml':                  0,
                 'timeseries_plot':              0,
                 'timeseries_syn_plot':          1}


""" pressure reduction to mean sea level """
if workflow_dict['pressure_reduction'] == 1:
    pressure = 1000.15
    temp = 15
    temp_dew = 10
    h = 200
    latitude = 48
    presreduc.main(p=pressure, T=temp, Td=temp_dew, station_height=h, lat=latitude)


""" Excel to CSV conversion """
# theodolite for google earth trajectory
if workflow_dict['excel_to_csv_theo_gearth'] == 1:
    excel_filename = 'theo_testfile_single.xlsx'
    etcsv.main(conversion_type='theo_gearth', excel_file=excel_filename)

# theodolite for single/double cut calculations
if workflow_dict['excel_to_csv_theo_cut'] == 1:
    excel_filename1 = 'theo_testfile_single3.xlsx'
    etcsv.main(conversion_type='theo_cut', excel_file=excel_filename1)
    # excel_filename1 = 'theo_testfile_double1.xlsx'
    # etcsv.main(conversion_type='theo_cut', excel_file=excel_filename1)
    # excel_filename2 = 'theo_testfile_double2.xlsx'
    # etcsv.main(conversion_type='theo_cut', excel_file=excel_filename2)

# hobo weather station (XLS file)
if workflow_dict['excel_to_csv_hobo'] == 1:
    excel_filename = 'hobo_testfile.xls'
    etcsv.main(conversion_type='hobo', excel_file=excel_filename)

# synoptic observations
if workflow_dict['excel_to_csv_syn'] == 1:
    excel_filename = 'syn_obs_template_20190518_2.xlsx'
    etcsv.main(conversion_type='syn', excel_file=excel_filename)


""" Theodolite cuts calculations """
# theodolite single cut
if workflow_dict['theo_calc_single_cut'] == 1:
    # input vars
    h = 785
    csv_file = 'theo_testfile_single3_cut_20190419-0142.csv'

    thsin.main(station_height=h, csv_file=csv_file)

# theodolite double cut
if workflow_dict['theo_calc_double_cut'] == 1:
    # input vars
    B = 111.7 # distance between the two theodolites
    phi = 97.54 # angle between the north and the thedolite connecting line
    csv_file1 = '.csv'
    csv_file2 = '.csv'

    thdou.main(B=B, phi=phi, csv_file1=csv_file1, csv_file2=csv_file2)


""" Radiosounding to kml file """
# download radiosounding data and create a kml file for google earth
if workflow_dict['raso_to_kml'] == 1:
    # datestr = datetime.now().strftime('%Y%m%d')
    # datestr = '20190202'
    # rasokml.main(station_name='wien', hour='00', date=datestr)
    # rasokml.main(station_name='linz', hour='03', date=datestr)
    # rasokml.main(station_name='innsbruck', hour='03', date=datestr)
    # rasokml.main(station_name='muenchen', hour='00', date=datestr)
    # rasokml.main(station_name='udine', hour='00', date=datestr)
    # rasokml.main(station_name='zagreb', hour='00', date=datestr)
    # rasokml.main(station_name='ljubljana', hour='06', date=datestr)
    # rasokml.main(station_name='graz', hour='03', date=datestr)
    # datestr = '20190203'
    # rasokml.main(station_name='graz', hour='03', date=datestr)
    # datestr = '20190207'
    # rasokml.main(station_name='graz', hour='03', date=datestr)
    # datestr = '20190209'
    # rasokml.main(station_name='graz', hour='03', date=datestr)
    datestr = '20190515'
    rasokml.main(station_name='wien', hour='12', date=datestr)

    # datestr = '20190501'
    # rasokml.main(station_name='wien', hour='12', date=datestr)


""" Theodolite csv to kml file """
# use the csv file for gearth
if workflow_dict['theo_to_kml'] == 1:
    h = 785
    lon = 12.30912
    lat = 47.44752
    name = 'theo_testfile_single_gearth_20190419-0142.csv'
    theokml.main(stat_height=h, stat_lon=lon, stat_lat=lat, csv_file=name)


""" Plotting routines """
# timeseries plot for various parameters
if workflow_dict['timeseries_plot'] == 1:
    # creates a single windowed timeseries plot for specified vars
    csv_filename = 'hobo_testfile_20190419-0142.csv'

    ## a few example calls
    # vars which shall be plotted => set to 1
    var_dict = {'wind_spd':     1,
                'wind_gusts':   1,
                'wind_dir':     0,
                'temp':         1,
                'rel_hum':      1,
                'pres':         0,
                'radiation':    0}

    figname = 'hobo_testplot_vspd_t_rh.png'
    plotrout.main(plotroutine='hobo', csv_filename=csv_filename, var_dict=var_dict, figurename=figname, titlestr='hobo wind, temp, rh')

    var_dict = {'wind_spd':     0,
                'wind_gusts':   0,
                'wind_dir':     1,
                'temp':         0,
                'rel_hum':      1,
                'pres':         1,
                'radiation':    0}

    figname = 'hobo_testplot_vdir_rh_p.png'
    plotrout.main(plotroutine='hobo', csv_filename=csv_filename, var_dict=var_dict, figurename=figname)

    var_dict = {'wind_spd':     0,
                'wind_gusts':   0,
                'wind_dir':     0,
                'temp':         1,
                'rel_hum':      1,
                'pres':         0,
                'radiation':    1}

    figname = 'hobo_testplot_t_rh_rad.png'
    plotrout.main(plotroutine='hobo', csv_filename=csv_filename, var_dict=var_dict, figurename=figname)

    var_dict = {'wind_spd':     1,
                'wind_gusts':   1,
                'wind_dir':     1,
                'temp':         1,
                'rel_hum':      1,
                'pres':         1,
                'radiation':    1}

    figname = 'hobo_testplot_all.png'
    plotrout.main(plotroutine='hobo', csv_filename=csv_filename, var_dict=var_dict, figurename=figname)


# timeseries plot for synoptic observations (such as cloudiness)
if workflow_dict['timeseries_syn_plot'] == 1:
    csv_filename = 'syn_obs_template_20190518_2_20190518-1637.csv'
    figname = 'syn_obs_20190518_15UTC'
    title = 'synoptic observations 18.05.2019'
    plotrout.main(plotroutine='syn', csv_filename=csv_filename, figurename=figname, titlestr=title)
