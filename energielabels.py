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
    type_woning, begin_postcode, eind_postcode = load_variables()
    data = import_data()
    relevant_data = select_relevant_data(data, type_woning)
    unieke_postcodes, unieke_energielabels = find_the_uniques(relevant_data,data)
    number_of_energielabels_per_postcode = count_number_of_labels_per_postcode(unieke_postcodes, unieke_energielabels, relevant_data)
    save_number_energielabels_postcode(number_of_energielabels_per_postcode)
    index = select_the_most_common_energielabel(unieke_postcodes, number_of_energielabels_per_postcode)
    color = apply_color_to_postcode(unieke_postcodes, index)
    postcodeandcolorlabel = create_postcode_and_colorlabel(unieke_postcodes, color)
    location, kleur = calculate_locations_of_postcodes(begin_postcode, eind_postcode, postcodeandcolorlabel)
    #save_locations(location, type_woning)
    draw_map(location,kleur, type_woning, begin_postcode,eind_postcode)
    return

def load_variables():
    type_woning = raw_input("Van welk type woningen wil je de energielabels zien? Je kunt kiezen uit: Flatwoning (overig), Galerijwoning, Maisonnette, Portiekwoning, Rijwoning tussen, Twee-onder-een-kap / rijwoning hoek, Vrijstaande woning, Woongebouw met niet-zelfstandige woo: ")
    begin_postcode = raw_input("Bij welke postcode wil je beginnen? Voer alleen het getal van de postcode in: ")
    eind_postcode = raw_input("Bij welke postcode wil je eindigen? Voer alleen het getal van de postcode in: ")
    return type_woning, begin_postcode, eind_postcode

def import_data():
    columns = [0,15,24]
    data = np.genfromtxt('selectie gemeentes Amsterdam 4-1-2012.csv',delimiter=';',skip_header=True,dtype=None,usecols=columns)
    return data

def select_relevant_data(data,type_woning):
    relevant_data = []
    for i in range(len(data)):
        if data[i,2] == type_woning:
            relevant_data.append(data[i,:])
    relevant_data = np.squeeze(relevant_data)
    return relevant_data

def find_the_uniques(relevant_data,data):
    unieke_postcodes = np.unique(relevant_data[:,0])
    unieke_energielabels = np.unique(data[:,1])
    return unieke_postcodes, unieke_energielabels

def count_number_of_labels_per_postcode(unieke_postcodes, unieke_energielabels, relevant_data):
    number_of_energielabels_per_postcode = np.zeros((len(unieke_postcodes), len(unieke_energielabels)))
    geolocator = nom()
    for a in range(len(relevant_data)):
        for i in range(len(unieke_postcodes)):
            if relevant_data[a,0] == unieke_postcodes[i]:
                if relevant_data[a,1] == 'A':
                    number_of_energielabels_per_postcode[i,0] += 1
                elif relevant_data[a,1] == 'A+':
                    number_of_energielabels_per_postcode[i,1] += 1
                elif relevant_data[a,1] == 'A++':
                    number_of_energielabels_per_postcode[i,2] += 1
                elif relevant_data[a,1] == 'B':
                    number_of_energielabels_per_postcode[i,3] += 1
                elif relevant_data[a,1] == 'C':
                    number_of_energielabels_per_postcode[i,4] += 1
                elif relevant_data[a,1] == 'D':
                    number_of_energielabels_per_postcode[i,5] += 1
                elif relevant_data[a,1] == 'E':
                    number_of_energielabels_per_postcode[i,6] += 1
                elif relevant_data[a,1] == 'F':
                    number_of_energielabels_per_postcode[i,7] += 1
                elif relevant_data[a,1] == 'G':
                    number_of_energielabels_per_postcode[i,8] += 1
    return number_of_energielabels_per_postcode

def save_number_energielabels_postcode(number_of_energielabels_per_postcode):
    np.savetxt("energielabelsperpostcode.csv", number_of_energielabels_per_postcode)
    return

def select_the_most_common_energielabel(unieke_postcodes, number_of_energielabels_per_postcode):
    max = np.zeros((len(unieke_postcodes)))
    index = np.zeros((len(unieke_postcodes)))
    length = np.zeros((len(unieke_postcodes)))
    for i in range(len(unieke_postcodes)):
        max[i] = np.amax(number_of_energielabels_per_postcode[i])
        length[i] = len(str(np.squeeze(np.where(number_of_energielabels_per_postcode[i] == max[i]))))
        if length[i] > 1:
            index[i] = 9
        else:
            index[i] = np.squeeze(np.where(number_of_energielabels_per_postcode[i] == max[i]))
    return index

def apply_color_to_postcode(unieke_postcodes, index):
    color = np.empty(len(unieke_postcodes), dtype='a10')
    for i in range(len(unieke_postcodes)):
        if index[i] == 0.:
            color[i] = '#00FF00'
        elif index[i] == 1.:
            color[i] = '#44FF00'
        elif index[i] == 2.:
            color[i] = '#88FF00'
        elif index[i] == 3.:
            color[i] = '#CCFF00'
        elif index[i] == 4.:
            color[i] = '#FFFF00'
        elif index[i] == 5.:
            color[i] = '#FFCC00'
        elif index[i] == 6.:
            color[i] = '#FF8800'
        elif index[i] == 7.:
            color[i] = '#FF4400'
        elif index[i] == 8.:
            color[i] = '#FF0000'
        elif index[i] == 9.:
            color[i] = '#000000'
    return color

def create_postcode_and_colorlabel(unieke_postcodes, color):
    postcodeandcolorlabel = np.vstack((unieke_postcodes,color))
    postcodeandcolorlabel = np.transpose(postcodeandcolorlabel)
    return postcodeandcolorlabel

def calculate_locations_of_postcodes(begin_postcode, eind_postcode, postcodeandcolorlabel):
    location = np.zeros((len(postcodeandcolorlabel),2))
    kleur =np.empty([len(postcodeandcolorlabel),1], dtype=np.dtype('a7'))
    geolocator = nom()
    for i in range(len(postcodeandcolorlabel)):
        if int(postcodeandcolorlabel[i,0][:4]) >= int(begin_postcode) and int(postcodeandcolorlabel[i,0][:4]) < int(eind_postcode):
            #print postcodeandcolorlabel[i,0]
            kleur[i] = postcodeandcolorlabel[i,1]
            lat = geolocator.geocode(postcodeandcolorlabel[i,0])
            location[i,0] = lat.longitude
            location[i,1] = lat.latitude

    return location, kleur

def save_locations(location, type_woning):
    np.savetxt("location.csv", location)
    return

def draw_map(location, kleur, type_woning, begin_postcode,eind_postcode):
    m = map(projection='merc', llcrnrlat=52.2,urcrnrlat=52.6,llcrnrlon=4.6,urcrnrlon=5.4,lat_ts=0.1,resolution='f')
    m.drawmapboundary(fill_color='aqua')
    m.fillcontinents(color='coral', lake_color='aqua', zorder = 0)
    m.drawcountries(zorder=1)
    m.drawcoastlines(zorder=2)
    m.drawrivers(color='coral',zorder=3)

    for i in range(len(location)):
        if location[i,0] != 0.:
            x,y = m(location[i,0],location[i,1])
            print kleur[i]
            k = kleur[i]
            plt.scatter(x,y,color=k, zorder=10)

    plt.savefig(str(type_woning+begin_postcode+eind_postcode), format='png')
    plt.show()
    return

if __name__ == '__main__':
    main()
