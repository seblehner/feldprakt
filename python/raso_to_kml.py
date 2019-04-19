# -*- coding: utf-8 -*-
#
# Python Template
# @Author: SebiMac
# @Date:   2019-03-18 15:15:17 +0100
# @Last modified by:   SebiMac
# @Last modified time: 2019-04-17 12:16:16 +0200

"""
Downloads radio sounding data from the University of Wyoming: http://weather.uwyo.edu/upperair/sounding.html
Calculates horizontal translation and converts to lat/lon.
Writes new positions in a .kml file, for the use with Google Earth.

Input:  1) station name: wien, linz, graz (first letter as capital works as well)
        2) hour: 0, 12, if wien/muenchen/udine/zagreb, 03 if linz/graz/innsbruck, 06 if ljubljana
        3) date: date in the format "YYYYMMDD" (if omitted, current day with datetime.now() is used)

Output: 1) data from radio sounding will be saved as a textfile
            in '/raso_text/gearth_STATIONNAME_STATIONNUMBER_YYYYMMDD-HH.txt'
        2) google earth kml files will be saved in
            '/google_earth_kml/gearth_raso_STATIONNAME_STATIONNUMBER_YYYYMMDD-HH.kml'

Example calls:
from command line:  "python raso_to_kml.py STATIONNAME HOUR"
                    "python raso_to_kml.py STATIONNAME HOUR YYYYMMDD"

from a script:      from raso_to_kml import main
                    main(STATIONNAME, HOUR, YYYYMMDD)
###############################################################################
NOTE: A new download is only started, if the corresponding .txt file does NOT
exist. This is done to prevent too much queries, which would result in a temporal
ban from the university server.
###############################################################################
"""
from datetime import datetime
import errno
import numpy as np
import os
import sys
import urllib

def write_kml_file(name, data, stat_num, year, month, day, hour):
    """
    Create a directory for google earth kml files and write a file containing
    coordinates from the input variable "data".
    """
    print('Writing kml file ...')
    # create directory for google earth kml files, ignore if exists
    google_kml_dir = os.path.join('data', 'google_earth_kml')
    try:
        os.makedirs(google_kml_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # body text for kml file
    filename = "".join(['gearth_', name, '.kml'])
    file_path = os.path.join(google_kml_dir, filename)
    with open(file_path, 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" \n')
        f.write('xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n')
        f.write('<Document>\n')
        f.write("".join(['	<name>', stat_num, '_', year, month, day, hour, '_UTC.kml</name>\n']))
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

def main(station_name='wien', hour=12, date=None):
    """
    Includes downlod of the radio sounding data, save process into a txt file,
    calculation of the horizontal translation and conversion into lat/lon.
    """
    print('Executing raso_to_kml.py ...')
    # transform into correct type and format
    if not type(station_name) == str: station_name = str(station_name)
    if not type(hour) == int: hour = '{:02d}'.format(int(hour))

    # get wmo station number
    if station_name in ('wien', 'Wien'):
        stat_num = '11035'
    elif station_name in ('linz', 'Linz'):
        stat_num = '11010'
    elif station_name in ('graz', 'Graz'):
        stat_num = '11240'
    elif station_name in ('innsbruck', 'Innsbruck'):
        stat_num = '11120'
    elif station_name in ('muenchen', 'Muenchen'):
        stat_num = '10868'
    elif station_name in ('udine', 'Udine'):
        stat_num = '16045'
    elif station_name in ('zagreb', 'Zagreb'):
        stat_num = '14240'
    elif station_name in ('ljubljana', 'Ljubljana'):
        stat_num = '14015'

    # check if hour is eligible
    # NOTE: wien: 0, 12; linz, graz, innsbruck: 3
    if station_name in ('linz', 'Linz', 'graz', 'Graz', 'innsbruck', 'Innsbruck') and hour not in ('03'):
        raise ValueError('Hour input for the station %s has to be 03 (UTC)!!!' % (station_name))
    if station_name in ('wien', 'Wien') and hour not in ('00', '12'):
        raise ValueError('Hour input for the station %s has to be 00, or 12 (UTC)!!!' % (station_name))

    # if no date is given, use today
    if not date:
        year = '{:04d}'.format(datetime.now().year)
        month =  '{:02d}'.format(datetime.now().month)
        day =  '{:02d}'.format(datetime.now().day)
    if date:
        year = date[:4]
        month = date[4:6]
        day = date[6:8]

    # url for radiosounding data from the university of wyoming
    urlp1 = 'http://weather.uwyo.edu/cgi-bin/sounding?region=europe&TYPE=TEXT%3ALIST&YEAR='
    urlp2 = '&MONTH='
    urlp3 = '&FROM='
    urlp4 = '&TO='
    urlp5 = '&STNM='
    url_full = "".join([urlp1, year, urlp2, month, urlp3, day, hour, urlp4, day, hour, urlp5, stat_num])

    # create directory if it does not exist
    raso_dir = os.path.join('data', 'raso_text')
    try:
        os.makedirs(raso_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    new_file_name = "".join(["_".join(['raso', station_name, stat_num, "".join([year, month, day, '-', hour])]), '.txt'])
    new_file_path = os.path.join(raso_dir, new_file_name)

    # only download and create a new file if there exists none (needs to be deleted if redownload is wanted!!)
    if not os.path.isfile(new_file_path):
        print('Downloading raso data ...')
        # read data from url and save to txt file
        urldata = urllib.request.urlopen(url_full)
        dataraw = urldata.read().decode('utf-8')
        with open(new_file_path, 'w') as f:
            f.write(dataraw)

    data_list = []
    # read text file and extract needed data
    with open(new_file_path, 'r') as f:
        data =  f.readlines()

        # loop through lines from txt file
        for line in data:
            # get longitude and latitude from the station
            if line.strip().startswith('Station longitude'): stat_lon = line.split()[2]
            if line.strip().startswith('Station latitude'): stat_lat = line.split()[2]
            lines_split = line.split()
            try: # only include lines from the table data
                height = float(lines_split[1]) # in metres
                v_dir = float(lines_split[6]) # in degrees
                v_spd = float(lines_split[7]) # in knots

                # append to new list
                data_list.append([height, v_dir, v_spd])
            except: # skip lines without eligible numbers
                pass

    # create numpy array from list
    data_arr = np.array(data_list)
    if data_arr.size == 0:
        raise ValueError("""
                ERROR NOTIFICATION:
                Could not find available data in the textfile, check if
                the timestamp is eligible (i.e. not in the future) and/or
                if the data is available at http://weather.uwyo.edu/upperair/sounding.html!!!""")

    # knots to m/s
    data_arr[:,2] = data_arr[:,2]*0.5144

    # estimate time between each data point
    vert_velo = 5 # approximation of vertical velocity (needed because there is no such data available)
    # source for velocity: http://www.zamg.ac.at/medien/lnf_vortraege/wetterballon_leopold-bunzengruber.pdf
    dt = np.diff(data_arr[:,0])/vert_velo

    # define new arrays for new lon, lat positions
    lons = np.zeros(data_arr[:,0].shape)
    lats = np.zeros(data_arr[:,0].shape)

    # initial positon
    lons[0] = float(stat_lon)*np.pi/180
    lats[0] = float(stat_lat)*np.pi/180

    ## calculate new lons, lats
    print('Calculate trajectory ...')
    # transform degrees to radians and flip by pi
    translate_direction = data_arr[:,1]
    td_rad = translate_direction*np.pi/180 - np.pi

    # calculate velocity in x, y direction
    translate_velo = data_arr[:,2]
    ts_x = np.sin(td_rad)*translate_velo
    ts_y = np.cos(td_rad)*translate_velo

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

    # create numpy array with needed data
    data_mat = np.array([lons, lats, data_arr[:,0]])

    # write kml file
    name = "_".join([station_name, stat_num, "".join([year, month, day, '-', hour])])
    write_kml_file(name, data_mat, stat_num, year, month, day, hour)
    return None

if __name__ == '__main__':
    # args from command line
    station = sys.argv[1]
    hour = sys.argv[2]
    try:
        date = sys.argv[3]
        main(station_name=station, hour=hour, date=date)
    except:
        pass
    main(station_name=station, hour=hour)
