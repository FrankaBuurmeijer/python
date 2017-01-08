#!/usr/bin/env python
"""
This program does the following.
"""
# Standard python library imports here
import csv
import numpy as np
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim as nom
from mpl_toolkits.basemap import Basemap as map
# 3rd party library imports here
# your own imports here

def main():
    document, diploma, niveau, plaats = funload_variables()
    data = funload_data(document)
    relevant_data = funrelevant_data(data,diploma,niveau,plaats)
    students_per_location = funstudents_per_location(relevant_data,plaats)
    geo_students = funlongitudes_latitudes(students_per_location)
    fundraw_map(geo_students,niveau,plaats)
    return

def funload_variables():
    document = raw_input("Geef het pad naar de datafile:")
    diploma = raw_input("Kies 'geen diploma' of 'diploma':")
    niveau = raw_input("Kies 'havo' of 'vwo':")
    plaats = raw_input("Geef de plaats in nederland:")
    return (document, diploma, niveau, plaats)

def funload_data(documentin):
    data = np.genfromtxt(documentin,delimiter=';',skip_header=True,dtype=None)
    data = np.squeeze(data)
    return data

def funrelevant_data(datain,diplomain,niveauin,plaatsin):
    print str(niveauin+plaatsin)
    relevant_data = []
    relevant_columns = [3,11,12]
    for i in range(len(datain)):
        if datain[i,5] == diplomain and datain[i,4] == niveauin and datain[i,3] == str.upper(plaatsin):
            relevant_data.append(datain[i,relevant_columns])
    relevant_data = np.squeeze(relevant_data)
    return relevant_data

def funstudents_per_location(relevant_datain,plaatsin):
    uniques = np.vstack(np.unique(relevant_datain[:,1]))
    locations = np.vstack(np.array([plaatsin]*len(uniques)))
    counter = np.zeros((len(uniques),1))
    students_per_location = np.hstack((locations,uniques,counter))

    for i in np.arange(0,len(relevant_datain)):
        for a in np.arange(0,len(students_per_location)):
            if relevant_datain[i,1] == students_per_location[a,1]:
                students_per_location[a,2] = np.float(students_per_location[a,2])+np.float(relevant_datain[i,2])
    return students_per_location

def funlongitudes_latitudes(students_per_locationin):
    print students_per_locationin[:,1], len(students_per_locationin)
    #for b in range
    geolocator = nom()
    geo_students = np.zeros((len(students_per_locationin),5))

    for i in range(len(students_per_locationin)):
        if students_per_locationin[i,1] != "elders buiten NED":
        	print students_per_locationin[i,1]
        	lat = geolocator.geocode(students_per_locationin[i,0])
        	geo_students[i,0] = lat.longitude
        	geo_students[i,1] = lat.latitude
        	let = geolocator.geocode(students_per_locationin[i,1])
        	geo_students[i,2] = let.longitude
        	geo_students[i,3] = let.latitude
        	geo_students[i,4] = students_per_locationin[i,2]
    print geo_students
    return geo_students

def fundraw_map(geo_studentsin, niveauin, plaatsin):
    m = map(projection='merc', llcrnrlat=51,urcrnrlat=54,llcrnrlon=3,urcrnrlon=8,lat_ts=0.1,resolution='f')
    m.drawmapboundary(fill_color='aqua')
    m.fillcontinents(color='coral', lake_color='aqua')
    m.drawcoastlines()
    m.drawcountries()
    m.drawrivers(color='coral')

    for i in range(len(geo_studentsin)):
        if geo_studentsin[i,4] != 0.:
        	xbegin, ybegin = m(geo_studentsin[i,0],geo_studentsin[i,1])
        	xend, yend = m(geo_studentsin[i,2],geo_studentsin[i,3])
        	width = np.log10(geo_studentsin[i,4])+1
        	plt.arrow(xbegin,ybegin,xend-xbegin,yend-ybegin,fc='k', ec='k', linewidth = width, head_width=10, head_length=10)
    
    plt.savefig(str(niveauin+plaatsin), format='png')
    #plt.close()
    return

if __name__ == '__main__':
    main()
