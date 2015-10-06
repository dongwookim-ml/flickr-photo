#!/usr/bin/env python3
import sys
import random
import numpy as np
import pandas as pd
from datetime import datetime
from fastkml import kml, styles
from shapely.geometry import Point, LineString


def load_traj(ftable1, ftable2):
    """Load data"""
    traj_data  = pd.read_csv(ftable1, parse_dates=[3], skipinitialspace=True)
    traj_stats = pd.read_csv(ftable2, parse_dates=[3], skipinitialspace=True)
    return traj_data, traj_stats


def gen_kml(fname, traj_data, traj_stats, traj_id_list, traj_name_list=None):
    """Generate KML file"""
    assert(len(traj_id_list) > 0)
    if traj_name_list: 
        assert(len(traj_id_list) == len(traj_name_list))

    k = kml.KML()
    ns = '{http://www.opengis.net/kml/2.2}'
    stid = 'style1'
    # colors in KML: aabbggrr, aa=00 is fully transparent
    # developers.google.com/kml/documentation/kmlreference?hl=en#colorstyle
    st = styles.Style(id=stid, styles=[styles.LineStyle(color='2f0000ff', width=3)]) # transparent red
    doc = kml.Document(ns, '001', 'Trajectories', 'Trajectory visualization', styles=[st])
    k.append(doc)

    stats = traj_stats[traj_stats['Trajectory_ID'].isin(traj_id_list)]
    assert(stats.shape[0] == len(traj_id_list))

    pm_traj = []
    pm_photo = []

    for i in range(len(stats.index)):
        ri = stats.index[i]
        traj_id = stats.ix[ri]['Trajectory_ID']
        photos = traj_data[traj_data['Trajectory_ID'] == traj_id]
        lngs = [lng for lng in photos['Longitude'].tolist()]
        lats = [lat for lat in photos['Latitude'].tolist()]
        name = 'Trajectory_' + str(traj_id)
        if traj_name_list: name += '_' + traj_name_list[i]
        desc = 'User_ID: '              + str(stats.ix[ri]['User_ID']) + \
               '<br/>Start_Time: '      + str(stats.ix[ri]['Start_Time']) + \
               '<br/>Travel_Distance: ' + str(round(stats.ix[ri]['Travel_Distance(km)'], 2)) + ' km' + \
               '<br/>Total_Time: '      + str(round(stats.ix[ri]['Total_Time(min)'], 2)) + ' min' + \
               '<br/>Average_Speed: '   + str(round(stats.ix[ri]['Average_Speed(km/h)'], 2)) + ' km/h' + \
               '<br/>#Photos: '         + str(stats.ix[ri]['#Photo']) + \
               '<br/>Photos: '          + str(photos['Photo_ID'].tolist())
        pm = kml.Placemark(ns, str(traj_id), name, desc, styleUrl='#' + stid)
        pm.geometry = LineString([(lngs[j], lats[j]) for j in range(len(lngs))])
        pm_traj.append(pm)

        for rj in photos.index:
            name = 'Photo_' + str(photos.ix[rj]['Photo_ID'])
            desc = 'Trajectory_ID: '  + str(traj_id) + \
                   '<br/>Photo_ID: '  + str(photos.ix[rj]['Photo_ID']) + \
                   '<br/>User_ID: '   + str(photos.ix[rj]['User_ID']) + \
                   '<br/>Timestamp: ' + str(photos.ix[rj]['Timestamp']) + \
                   '<br/>Coordinates: (' + str(photos.ix[rj]['Longitude']) + ', ' + str(photos.ix[rj]['Latitude']) + ')' + \
                   '<br/>Accuracy: '  + str(photos.ix[rj]['Accuracy']) + \
                   '<br/>URL: '       + str(photos.ix[rj]['URL'])
            pm = kml.Placemark(ns, str(photos.ix[rj]['Photo_ID']), name, desc)
            pm.geometry = Point(photos.ix[rj]['Longitude'], photos.ix[rj]['Latitude'])
            pm_photo.append(pm)

    for pm in pm_traj:  doc.append(pm)
    for pm in pm_photo: doc.append(pm)

    kmlstr = k.to_string(prettyprint=True)
    with open(fname, 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(kmlstr)


def main(ftable1, ftable2):
    """Main Procedure"""
    # load data
    traj_data, traj_stats = load_traj(ftable1, ftable2)

    # remove trajctories with only one photos
    traj_stats = traj_stats[traj_stats['#Photo'] > 1]

    # remove trajctories with zero distance
    traj_stats = traj_stats[traj_stats['Travel_Distance(km)'] > 1e-4]

    # trajectory with the most number of photos 
    ri = traj_stats['#Photo'].idxmax()
    traj_id = traj_stats.ix[ri]['Trajectory_ID']
    fname = 'most_photos.kml'
    gen_kml(fname, traj_data, traj_stats, [traj_id], ['most_photos'])

    # trajectory took the longest time
    ri = traj_stats['Total_Time(min)'].idxmax()
    traj_id = traj_stats.ix[ri]['Trajectory_ID']
    fname = 'longest_time.kml'
    gen_kml(fname, traj_data, traj_stats, [traj_id], ['longest_time'])

    # trajectory took the longest distance
    ri = traj_stats['Travel_Distance(km)'].idxmax()
    traj_id = traj_stats.ix[ri]['Trajectory_ID']
    fname = 'longest_distance.kml'
    gen_kml(fname, traj_data, traj_stats, [traj_id], ['longest_distance'])

    # trajectory has the highest speed
    ri = traj_stats['Average_Speed(km/h)'].idxmax()
    traj_id = traj_stats.ix[ri]['Trajectory_ID']
    fname = 'highest_speed.kml'
    gen_kml(fname, traj_data, traj_stats, [traj_id], ['highest_speed'])

    # random 5 trajectories
    traj_id_list = traj_stats['Trajectory_ID'].sample(n=5).tolist() # requires pandas version >= 0.16.1
    fname = 'random5.kml'
    gen_kml(fname, traj_data, traj_stats, traj_id_list)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: ', sys.argv[0], 'TRAJECTORY_PHOTO_FILE  TRAJECTORY_STATS_FILE')
        print('e.g. : ', sys.argv[0], 'trajectory_photos.csv  trajectory_stats.csv')
        sys.exit(0)

    ftable1 = sys.argv[1]
    ftable2 = sys.argv[2]
    main(ftable1, ftable2)

