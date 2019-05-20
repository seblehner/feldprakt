# -*- coding: utf-8 -*-
#
# Python Template
# @Author: SebiMac
# @Date:   2019-03-20 15:51:21 +0100
# @Last modified by:   SebiMac
# @Last modified time: 2019-04-06 15:55:46 +0200

"""
Converts excel files to csv files seperated with a ','.
Supports the following specified types:
(a) conversion_type: 'theo_gearth' Theodolite .xlsx files for the use in trajectory calculations for google earth
(b) conversion_type: 'theo_cut' Theodolite .xlsx files for the use in single/double cut calculations
(c) conversion_type: 'hobo' Hobo .xls files for the use in data analysis and plotting routines
(d) conversion_type: 'syn' .xls files containing synoptic observations according to a given template
"""

import errno
from datetime import datetime
import numpy as np
import os
import pandas as pd
import sys


def main(conversion_type='theo_gearth', excel_file='theo_testfile_single.xlsx'):
    """
    Converts specified excel file for given conversion_type into a .csv file,
    which only contains relevant information for further analysis (dependant on
    the specified conversion_type).
    """
    def save_as_csv(df, filename):
        # create directory if it does not exist
        csv_dir = os.path.join('data', 'csv')
        try:
            os.makedirs(csv_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        df.to_csv(os.path.join(csv_dir, filename), sep=',')
        return None

    print('Executing excel_to_csv.py ...')
    # used for naming new files
    datestr = datetime.now().strftime('%Y%m%d-%H%M')
    if conversion_type == 'theo_gearth':
        # read excel file with pandas
        print('Read excel file ...')
        df = pd.read_excel(os.path.join('data', 'excel', excel_file),
                           skiprows=4, sheet_name='Data')

        # get important data
        v_dir = df['WD(deg) for graph'].values # mathematical degree
        v_spd = df['WS(m/s) for graph'].values
        height = df['Height(m) for graph'].values

        # create new pandas dataframe
        df_new = pd.DataFrame(np.column_stack([height, v_dir, v_spd]),
                              columns=['height above ground [m]', 'wind direction [deg]',
                              'wind speed [m/s]'])

        # save dateframe as csv file
        print('Saving data to csv file ...')
        csv_filename = "".join([excel_file.split('.')[0], '_', 'gearth', '_', datestr, '.csv'])
        save_as_csv(df_new, csv_filename)

    elif conversion_type == 'theo_cut':
        # read excel file with pandas
        print('Read excel file ...')
        df = pd.read_excel(os.path.join('data', 'excel', excel_file),
                           usecols=[3, 4], sheet_name='Data')

        # get important data
        elevation = df['Unnamed: 3'].values[4:]
        azimuth = df['Unnamed: 4'].values[4:]

        # create new pandas dataframe
        df_new = pd.DataFrame(np.column_stack([elevation, azimuth]),
                              columns=['elevation [deg]', 'azimuth [deg]'])

        # save dateframe as csv file
        print('Saving data to csv file ...')
        csv_filename = "".join([excel_file.split('.')[0], '_', 'cut', '_', datestr, '.csv'])
        save_as_csv(df_new, csv_filename)

    elif conversion_type == 'hobo':
        # read excel file with pandas
        print('Read excel file ...')
        df = pd.read_excel(os.path.join('data', 'excel', excel_file), skiprows=1)

        # fix column header from hobo file output (remove serial num)
        for i, x in enumerate(df.columns):
            newstr = x.split(' ')
            df.columns.values[i] = " ".join(newstr[:2]).strip(',')

        # get important data
        # include time meta for old and new versions
        if isinstance(df['Datum Zeit'].values[0], str):
            time_vec = df['Datum Zeit'].values
        elif isinstance(df['Datum Zeit'].values[0], np.datetime64):
            time = pd.to_datetime(df['Datum Zeit'].values)
            new_time_vec = []
            for i in range(len(time)):
                new_time = time[i].strftime('%d.%m.%Y %H:%M:%S')
                new_time_vec.append(new_time)
            time_vec = np.array(new_time_vec)

        # print(np.array(new_time_vec))
        # check if data from excel file uses a , or . as decimal
        if isinstance(df['Windgeschwindigkeit, m/s'].values[0], float):
            v_spd = [v for v in df['Windgeschwindigkeit, m/s'].values] # m/s
            v_spd_boeen = [vb for vb in df['Böengeschwindigkeit, m/s'].values] # m/s
            v_dir = [vd for vd in df['Windrichtung, ø'].values] # deg
            T = [t for t in df['Temp., °C'].values] # deg C
            RH = [rh for rh in df['RH, %'].values] # %
            p = [pp for pp in df['Druck, mbar'].values] # hPa
            sun_rad = [l for l in df['Sonnenstrahlung, W/m²'].values] # W/m2
        else:
            v_spd = [float(v.replace(',', '.')) for v in df['Windgeschwindigkeit, m/s'].values] # m/s
            v_spd_boeen = [float(vb.replace(',', '.')) for vb in df['Böengeschwindigkeit, m/s'].values] # m/s
            v_dir = [float(vd.replace(',', '.')) for vd in df['Windrichtung, ø'].values] # deg
            T = [float(t.replace(',', '.')) for t in df['Temp., °C'].values] # deg C
            RH = [float(rh.replace(',', '.')) for rh in df['RH, %'].values] # %
            p = [float(pp.replace(',', '.')) for pp in df['Druck, mbar'].values] # hPa
            sun_rad = [float(l.replace(',', '.')) for l in df['Sonnenstrahlung, W/m²'].values] # W/m2

        # create new pandas dataframe
        df_new = pd.DataFrame(np.column_stack([time_vec, v_spd, v_spd_boeen, v_dir, T, RH, p, sun_rad]),
                              columns=['time', 'wind speed [m/s]', 'wind gusts [m/s]', 'wind direction [deg]',
                              'temperature [deg C]', 'relative humidity [%]', 'pressure [hPa]', 'radiation [W/m2]'])

        # save dateframe as csv file
        print('Saving data to csv file ...')
        csv_filename = "".join([excel_file.split('.')[0], '_', datestr, '.csv'])
        save_as_csv(df_new, csv_filename)

    elif conversion_type == 'hobo_precip':
        # read excel file with pandas
        print('Read excel file ...')
        df = pd.read_excel(os.path.join('data', 'excel', excel_file), skiprows=1)

        # fix column header from hobo file output (remove serial num)
        for i, x in enumerate(df.columns):
            newstr = x.split(' ')
            df.columns.values[i] = " ".join(newstr[:2]).strip(',')

        # get important data
        # include time meta for old and new versions
        if isinstance(df['Datum Zeit'].values[0], str):
            time_vec = df['Datum Zeit'].values
        elif isinstance(df['Datum Zeit'].values[0], np.datetime64):
            time = pd.to_datetime(df['Datum Zeit'].values)
            new_time_vec = []
            for i in range(len(time)):
                new_time = time[i].strftime('%d.%m.%Y %H:%M:%S')
                new_time_vec.append(new_time)
            time_vec = np.array(new_time_vec)

        precip_ticks = df['Event, units'].values

        # create new pandas dataframe
        df_new = pd.DataFrame(np.column_stack([time_vec, precip_ticks]),
                              columns=['time', 'precip ticks [0.2mm]'])


        # save dateframe as csv file
        print('Saving data to csv file ...')
        csv_filename = "".join([excel_file.split('.')[0], '_', datestr, '.csv'])
        save_as_csv(df_new, csv_filename)

    elif conversion_type == 'syn':
        # read excel file with pandas
        print('Read excel file ...')
        df = pd.read_excel(os.path.join('data', 'excel', excel_file))

        # save dateframe as csv file
        print('Saving data to csv file ...')
        csv_filename = "".join([excel_file.split('.')[0], '_', datestr, '.csv'])
        save_as_csv(df, csv_filename)
    return None

if __name__ == '__main__':
    conversion_type = sys.argv[1]
    excel_file = sys.argv[2]
    main(conversion_type=conversion_type, excel_file=excel_file)
