# -*- coding: utf-8 -*-
#
# Python Template
# @Author: SebiMac
# @Date:   2019-03-18 15:15:17 +0100
# @Last modified by:   SebiMac
# @Last modified time: 2019-04-19 01:50:08 +0200

"""
Calculates horizontal translation and converts to lat/lon.
Writes new positions in a .kml file, for the use with Google Earth.

Input:  1) csv file generated via excel_to_csv method for conversion_type: theo_gearth
            from theodolite measurements.

Output: 1) google earth kml files will be saved in
            '/google_earth_kml/geart_theo_ID_YYYYMMDD-HH.kml'

Example calls:
from command line:  "python theo_to_kml.py STATION_HEIGHT STATION_LON STATION_LAT CSV_FILENAME"
                    "python theo_to_kml.py STATION_HEIGHT STATION_LON STATION_LAT CSV_FILENAME"

from a script:      from theo_to_kml import main
                    main(STATION_HEIGHT, STATION_LON, STATION_LAT, CSV_FILENAME)
"""
from datetime import datetime
import errno
import numpy as np
import os
import pandas as pd
import sys

def write_kml_file(name, data):
    """
    Create a directory for google earth kml files and write a file containing
    coordinates from the input variable "data".
    """
    print('Writing kml file ...')
    # create directory for google earth kml files in child dir, ignore if exists
    google_kml_dir = os.path.join('data', 'google_earth_kml')
    try:
        os.makedirs(google_kml_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # body text for kml file
    filename = "".join([name, '.kml'])
    file_path = os.path.join(google_kml_dir, filename)
    with open(file_path, 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" \n')
        f.write('xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n')
        f.write('<Document>\n')
        f.write("".join(['	<name>', name, '.kml</name>\n']))
        f.write('	<StyleMap id="m_ylw-pushpin">\n')
        f.write('		<Pair>\n')
        f.write('			<key>normal</key>\n')
        f.write('			<styleUrl>#s_ylw-pushpin</styleUrl>\n')
        f.write('		</Pair>\n')
        f.write('		<Pair>\n')
        f.write('			<key>highlight</key>\n')
        f.write('			<styleUrl>#s_ylw-pushpin_hl</styleUrl>\n')
        f.write('		</Pair>\n')
        f.write('	</StyleMap>\n')
        f.write('	<Style id="s_ylw-pushpin">\n')
        f.write('		<IconStyle>\n')
        f.write('			<scale>1.1</scale>\n')
        f.write('			<Icon>\n')
        f.write('				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>\n')
        f.write('			</Icon>\n')
        f.write('			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>\n')
        f.write('		</IconStyle>\n')
        f.write('	</Style>\n')
        f.write('	<Style id="s_ylw-pushpin_hl">\n')
        f.write('		<IconStyle>\n')
        f.write('			<scale>1.3</scale>\n')
        f.write('			<Icon>\n')
        f.write('				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>\n')
        f.write('			</Icon>\n')
        f.write('			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>\n')
        f.write('		</IconStyle>\n')
        f.write('	</Style>\n')
        f.write('	<Placemark>\n')
        f.write('		<name>Pfad ohne Namen</name>\n')
        f.write('		<styleUrl>#m_ylw-pushpin</styleUrl>\n')
        f.write('		<LineString>\n')
        f.write('			<extrude>1</extrude>\n')
        f.write('			<tessellate>1</tessellate>\n')
        f.write('			<altitudeMode>absolute</altitudeMode>\n')
        f.write('			<coordinates>\n')
        for i in range(len(data[0,:])):
            lon_str = str(data[0,i])
            lat_str = str(data[1,i])
            z_str = str(data[2,i])
            data_str = ",".join([lon_str, lat_str, z_str])
            f.write("".join([data_str, '\n']))
        f.write('			</coordinates>\n')
        f.write('		</LineString>\n')
        f.write('	</Placemark>\n')
        f.write('</Document>\n')
        f.write('</kml>\n')
    return None

def main(stat_height=None, stat_lon=None, stat_lat=None, csv_file=None):
    """
    Calculate horizontal translation from a theodolite measurement given as csv file,
    convert to lat/lon vals.
    """
    print('Executing theo_to_kml.py ...')
    # read cds file into dataframe
    csv_path = os.path.join('data', 'csv', csv_file)
    df = pd.read_csv(csv_path, delimiter=',', index_col=0)

    # get name
    namestr = csv_file.split('.')[0]

    # convert pandas dataframe to numpy array
    data_arr = np.array(df)
    if data_arr.size == 0:
        raise ValueError('Could not find available data, check csvfile!')

    # estimate time between each data point
    vert_velo = 2.4 # estimate of vertical velocity (needed because there is no such data available)
    dt = np.diff(data_arr[:,0])/vert_velo

    # define new arrays for new lon, lat positions
    lons = np.zeros(data_arr[:,0].shape)
    lats = np.zeros(data_arr[:,0].shape)

    # initial positon
    lons[0] = float(stat_lon)*np.pi/180
    lats[0] = float(stat_lat)*np.pi/180

    ## calculate new lons, lats
    print('Calculate trajectory ...')
    # transform degrees to radians and flip by pi (because wind vector degree show from where the wind is coming)
    translate_direction = data_arr[:,1]
    td_rad = translate_direction*np.pi/180 - np.pi
    # transform geographical to meteo degrees
    td_rad = (450 - td_rad) % 360

    # calculate velocity in x, y direction
    translate_velo = data_arr[:,2]
    ts_x = np.cos(td_rad)*translate_velo
    ts_y = np.sin(td_rad)*translate_velo

    # calculate translation in each direction
    translation_x = ts_x[:-1]*dt
    translation_y = ts_y[:-1]*dt

    earth_radius = 6371e3 # in m
    earth_u = 2*earth_radius*np.pi

    # source: http://www.geomidpoint.com/destination/calculation.html
    # distance covered in radians
    ds = np.sqrt(translation_x**2 + translation_y**2)/earth_radius
    for i in range(len(ds)):
        lats[i+1] = np.arcsin(np.sin(lats[i])*np.cos(ds[i]) + np.cos(lats[i])*np.sin(ds[i])*np.cos(td_rad[i]))
        lons[i+1] = lons[i] + np.arctan2(np.sin(td_rad[i])*np.sin(ds[i])*np.cos(lats[i]), np.cos(ds[i]) - np.sin(lats[i])*np.sin(lats[i+1]))

    # convert back to degree
    lons = lons*180/np.pi
    lats = lats*180/np.pi

    # add station height to data
    height = data_arr[:,0] + stat_height
    data_mat = np.array([lons, lats, height])

    # write kml file
    write_kml_file(namestr, data_mat)
    return None

if __name__ == '__main__':
    # args from command line
    h = sys.argv[1]
    lon = sys.argv[2]
    lat = sys.argv[3]
    csv_file = sys.argv[4]
    main(stat_height=h, stat_lon=lon, stat_lat=lat, csv_file=csv_file)
