#!/usr/bin/env python3
import sys
import math
import os.path
from datetime import datetime


def load_data(fname):
    """Load data records"""
    # * Photo/video identifier 
    # * User NSID
    # * Date taken
    # * Longitude
    # * Latitude
    # * Accuracy
    # * Photo/video page URL
    # * Photos/video marker (0 = photo, 1 = video)

    data = []
    firstline = True
    with open(fname, 'r') as f:
        for line in f:
            if firstline:
                firstline = False
                continue
            t = line.strip().split(',')
            pid = t[0].strip()
            uid = t[1].strip()
            time = datetime.strptime(t[2].strip(), '%Y-%m-%d %H:%M:%S.%f')  # 2011-05-09 19:19:58.0
            lng = float(t[3].strip())
            lat = float(t[4].strip())
            acc = int(t[5].strip())
            url = t[6].strip()
            marker = int(t[7].strip())
            data.append((pid, uid, time, lng, lat, acc, url, marker))
    return data


def gen_trajectories(data, time_gap=8):
    """Generate trajectories"""
    assert(time_gap > 0)
    udict = dict()
    
    # group photos by user ID
    for i in range(len(data)):
        uid = data[i][1]
        if uid not in udict: udict[uid] = []
        udict[uid].append(i)

    # construct travel history (i.e. sort photos by time) for each user
    for uid, dlist in udict.items():
        dlist.sort(key=lambda idx: data[idx][2])

    # construct trajectories by splitting user's travel history
    TGAP = time_gap * 60 * 60  # 8 hours by default
    trajs = []
    for uid in sorted(udict.keys()): # sort by user ID
        dlist = udict[uid]
        if len(dlist) < 1: continue
        if len(dlist) == 1: 
            trajs.append(dlist)
            continue
        trajs.append([dlist[0]])
        for j in range(1, len(dlist)):
            p1 = dlist[j-1]
            p2 = dlist[j]
            t1 = data[p1][2]
            t2 = data[p2][2]
            assert(t1 <= t2)
            if (t2 - t1).total_seconds() < TGAP:
                trajs[-1].append(p2)
            else:
                trajs.append([p2])
    return trajs


def filter_trajectories(lng_min, lat_min, lng_max, lat_max, trajlist, data, min_photos_per_traj=1):
    """Drop Trajectories which are completely out of the bounding box:
       [(lng_min, lat_min), (lng_max, lat_max)]
    """
    assert(lng_min < lng_max)
    assert(lat_min < lat_max)
    assert(min_photos_per_traj >= 1)

    indexes = []
    for i in range(len(trajlist)):
        traj = trajlist[i]
        if len(traj) < min_photos_per_traj: continue
        anyin = False
        for p in traj:
            assert(p in range(len(data)))
            lng = data[p][3]
            lat = data[p][4]
            if lng_min < lng < lng_max and lat_min < lat < lat_max:
                anyin = True
                break
        if anyin: 
            indexes.append(i)
    return [trajlist[x] for x in indexes]


def calc_dist(longitude1, latitude1, longitude2, latitude2):
    """Calculate the distance (unit: km) between two places on earth"""
    # convert degrees to radians
    lng1 = math.radians(longitude1)
    lat1 = math.radians(latitude1)
    lng2 = math.radians(longitude2)
    lat2 = math.radians(latitude2)
    radius = 6371.009 # mean earth radius is 6371.009km, en.wikipedia.org/wiki/Earth_radius#Mean_radius

    # The haversine formula, en.wikipedia.org/wiki/Great-circle_distance
    dlng = math.fabs(lng1 - lng2)
    dlat = math.fabs(lat1 - lat2)
    dist =  2 * radius * math.asin( math.sqrt( 
                (math.sin(0.5*dlat))**2 + math.cos(lat1) * math.cos(lat2) * (math.sin(0.5*dlng))**2 ))
    return dist


def dump_trajectories(fout1, fout2, trajlist, data):
    """Save Trajectories"""
    # data table 1
    with open(fout1, 'w') as f1:
        f1.write('Trajectory_ID, Photo_ID, User_ID, Timestamp, Longitude, Latitude, Accuracy, Marker(photo=0 video=1), URL\n')
        for i, dlist in enumerate(trajlist):
            assert(len(dlist) > 0)
            tid = str(i)
            for p in dlist:
                assert(p in range(len(data)))
                pid = str(data[p][0])
                uid = str(data[p][1])
                time = str(data[p][2])
                lng = str(data[p][3])
                lat = str(data[p][4])
                acc = str(data[p][5])
                url = str(data[p][6])
                marker = str(data[p][7])
                f1.write(tid + ',' + pid + ',' + uid + ',' + \
                         time + ',' + lng + ',' + lat + ',' + \
                         acc + ',' + marker + ',' + url + '\n')

    # data table 2
    with open(fout2, 'w') as f2:
        f2.write('Trajectory_ID, User_ID, #Photo, Start_Time, Travel_Distance(km), Total_Time(min), Average_Speed(km/h)\n')
        for i, dlist in enumerate(trajlist):
            assert(len(dlist) > 0)
            tid = str(i)
            p1 = dlist[0]
            p2 = dlist[-1]
            uid = str(data[p1][1])
            num = str(len(dlist))
            dist = 0
            if len(dlist) > 1:
                for j in range(len(dlist)-1):
                    dist += calc_dist(data[dlist[j]][3], data[dlist[j]][4], data[dlist[j+1]][3], data[dlist[j+1]][4])  # km
            t1 = data[p1][2]
            t2 = data[p2][2]
            assert(t1 <= t2)
            seconds = (t2 - t1).total_seconds()
            ttime = seconds / 60  # minutes
            speed = None
            if seconds == 0: 
                speed = 0
            else:
                speed = dist * 60 * 60 / seconds  # km/h
            f2.write(tid + ',' + uid + ',' + num + ',' + str(t1) + ',' + \
                     str(dist) + ',' + str(ttime) + ',' + str(speed) + '\n')


def main(fin, fout1, fout2, longitude_min, latitude_min, longitude_max, latitude_max, min_photos_per_traj=1, time_gap=8):
    """Main Procedure"""
    assert(longitude_min < longitude_max)
    assert(latitude_min < latitude_max)
    assert(min_photos_per_traj >= 1)
    assert(time_gap > 0)
    data = load_data(fin)
    trajs = gen_trajectories(data, time_gap)
    trajs = filter_trajectories(longitude_min, latitude_min, longitude_max, latitude_max, trajs, data, min_photos_per_traj)
    dump_trajectories(fout1, fout2, trajs, data)


if __name__ == '__main__':
    if len(sys.argv) != 2 and len(sys.argv) != 8:
        print('Usage:', sys.argv[0], 'BIGBOX_DATA_FILE')
        print('Usage:', sys.argv[0], \
              'BIGBOX_DATA_FILE  MIN_LONGITUDE  MIN_LATITUDE  MAX_LONGITUDE  MAX_LATITUDE  MIN_PHOTOS_PER_TRAJECTORY  TIME_GAP(hour)')
        sys.exit(0)

    fin = sys.argv[1]
    path, filename = os.path.split(fin)
    fout1 = os.path.join(path, './trajectory_photos.csv')
    fout2 = os.path.join(path, './trajectory_stats.csv')

    if len(sys.argv) == 2:
        lng_min = 144.597363
        lat_min = -38.072257
        lng_max = 145.360413
        lat_max = -37.591764
        main(fin, fout1, fout2, lng_min, lat_min, lng_max, lat_max)
    else:
        lng_min = float(sys.argv[2])
        lat_min = float(sys.argv[3])
        lng_max = float(sys.argv[4])
        lat_max = float(sys.argv[5])
        min_photos_per_traj = int(sys.argv[6])
        time_gap = float(sys.argv[7])
        main(fin, fout1, fout2, lng_min, lat_min, lng_max, lat_max, min_photos_per_traj, time_gap)

