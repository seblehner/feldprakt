## Overview

Short explanation for the use of different python scripts regarding field exercise data analysis.

# Feldpraktikum SoSe 2019 - Turnau

## Table of Contents

* [Dependencies and Setup](#Dependencies-and-Setup)
* [Structure](#Structure)
* [Pressure reduction to MSL](#Pressure-reduction-to-MSL)
* [Data conversions](#Data-conversions)
* [Theodolite cuts](#Theodolite-cuts)
* [Google Earth kml files](#Google-Earth-kml-files)
* [Plotting routines](#Plotting-routines)



### Dependencies and Setup
**Some modules require Python 3!** Dependencies can be found in the **environment.yml** file. Download the repository, move it to any path you wish for. You can either install all packages by hand, or you can use `
```sh
conda env create -f environment.yml
```
inside the
```sh
/field_exercise_data_tools/
```
folder for a one-step installation of all dependencies. When installed a new environment named **fedt** is created, remember to use
```sh
source activate fedt
```
before executing any files and you are ready to go.


### Structure

The general structure looks like:
```sh
/field_exercise_data_tools/main_control.py
```
Control script for all working steps. If the underlying methods are only used and not modified, no other file has to be executed. The file itself is explained via comments inside.

```sh
/field_exercise_data_tools/data/
```
Contains all different kinds of data, separated in subfolders. New data has to be sorted accordingly. Usually, new data consist of excel files only, hence move it to **/field_exercise_data_tools/data/excel/**.

```sh
/field_exercise_data_tools/python/
```
All python files which are used via the **main_control.py** file reside in this subfolder. Only modify them, if you want to change some functionality of the toolkit.

```sh
/field_exercise_data_tools/figures/
```
Python generated plots are saved in this directory.

## Python scripts

### Pressure reduction to MSL

```sh
pressure_reduction_msl.py
```
Reduces the pressure to the mean sea level. Needs station observed pressure, temperature, dew-point temperature as well as station height and station latitude. Can be run on the command line via:
```sh
python pressure_reduction_msl.py PRESSURE TEMPERATURE DEW-POINT_TEMPERATURE STATION_HEIGHT STATION_LATITUDE
```


### Data conversions
```sh
excel_to_csv.py
```
Used to convert and filter the data from excel files (measurment tool output) to csv files using the pandas module. Should always be the first step, because working with a clean pandas dataframes is a lot neater than with excel files, which do not look necessarily the same across different stations and can cause compatibility problems when used across multiple operating systems.

Is divided in different conversion types (one of these has to be the first argument of a call).
* 'theo_gearth': Extracts all relevant information to be able to calculate horizontal translations with the **pilot_to_kml.py** script afterwards.
* 'theo_cut': Extracts all relevant information needed for the calculation of single and double cuts.
* 'hobo': Extracts common meteorological parameters from the Hobo weather station excel file.
* 'syn': Converts the synoptic observation template excel into a csv file, for the corresponding plotting routines.

Can be run on the command line via:
```sh
python excel_to_csv.py CONVERSION_TYPE FILENAME
```


### Theodolite cuts

```sh
theo_single_cut.py
```
Single cut using data from one theodolite. To be able to calculate a vertical profile, the assumption of a constant vertical velocity (2.4 m/s) is made.
A figure with two plots is created, the first visualizes the horizontal translation with color coded height, and the second one a vertical profile of wind velocity and direction.


```sh
theo_double_cut.py
```
Double cut using data from two different theodolite observations of the same balloon. No assumption about the vertical velocity needs to be made, but the result is very sensitive to the accuracy of the measurements.
A figure with two plots is created, the first visualizes the horizontal translation with color coded height, and the second one a vertical profile of wind velocity and direction.

### Google Earth kml files
```sh
raso_to_kml.py
```
Downloads radio sounding data from the University of Wyoming server, calculates geographical location (longitude/latitude) for each data point available and writes the result into a kml file for the use with Google Earth (visualizing the trajectory).


```sh
theo_to_kml.py
```
Same as above, but for theodolite measurements. Note that the corresponding input file has to be prepared using the **excel_to_csv.py** script and the **'theo_gearth'** conversion type option.


### Plotting routines
```sh
plotting_routines.py
```
Different plotting settings can be targeted via the **plotroutine** variable. Available values are:
* 'hobo': Plots specified meteorological parameters as a time series plot.
* 'syn': Creates 2 figures. A time series plot containing thermodynamic at the top and dynamic parameter values of different measurement tools and synoptic observations such as cloudiness below and a bar plot encapsulating observed and approximated (spread formula) cloud base height.
