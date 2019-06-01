# -*- coding: utf-8 -*-
#
# Python Template
# @Author: SebiMac
# @Date:   2019-03-20 12:36:56 +0100
# @Last modified by:   SebiMac
# @Last modified time: 2019-05-31 23:35:47 +0200

import numpy as np
import sys

def main(p, T, Td, station_height, lat):
    """
    Returns reduced pressure based on pressure, temperature, dew-point temperature,
    station height above sea level and station latitude using the barometric height formula.

    Input variables:
            Pressure                p in hPa
            Temperature             T in deg Celsius
            Dew-Point Temperature   Td in deg Celsius
            Height of station       station_height in metres
            Latitude                lat in deg (decimal)
    """
    print('Executing pressure_reduction_msl.py ...')
    # convert input vars to floats
    p = float(p)
    T = float(T)
    Td = float(Td)
    station_height = float(station_height)
    lat_rad = float(lat)*np.pi/180 # conversion to radian

    # mean values correspond to average between sea level and station height,
    # which is used to reduce the pressure via the barometric formula
    # g_corrected_station = 9.80616 * (1 - 0.0026373*np.cos(2*lat_rad) + 0.0000059*np.cos(2*lat_rad)**2) * (1 - 2*station_height/6371e3) # not needed
    g_corrected_mean = 9.80616 * (1 - 0.0026373*np.cos(2*lat_rad) + 0.0000059*np.cos(2*lat_rad)**2) * (1 - station_height/6371e3)

    # magnus formula
    e = 6.11*np.exp(17.08*Td/(234.175 + Td))
    q = 0.622*e/(p - 0.378*e)*1000
    Tv_h = (1 + 0.609*q/1000) * (T+273.15) - 273.15
    Tv_mean = Tv_h + 1./2*station_height*0.65/100
    p_red = p * (np.exp(g_corrected_mean*station_height / (287 * (Tv_mean+273.15))))
    print(f'Reduced pressure for station: h = {station_height}m, lat = {lat}° is: p_red = {p_red} hPa')
    return p_red

if __name__ == '__main__':
    # args from command line
    p_obs = sys.argv[1]
    t_obs = sys.argv[2]
    td_obs = sys.argv[3]
    station_height = sys.argv[4]
    latitude = sys.argv[5]

    main(p=p_obs, T=t_obs, Td=td_obs, station_height=station_height, lat=latitude)
