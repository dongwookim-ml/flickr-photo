#!/usr/bin/env python3
import unittest
import tempfile
import os
from datetime import datetime
from generate_tables import load_data, gen_trajectories, filter_trajectories, calc_dist


class GenTablesTestCase(unittest.TestCase):
    def setUp(self):
        datastr = """\
Photo_ID, User_ID, Timestamp, Longitude, Latitude, Accuracy, URL, Marker(photo=0 video=1)
4257224959,26303188@N00,2010-01-09 09:39:19.0,145.314132,-37.765855,16,http://www.flickr.com/photos/26303188@N00/4257224959/,0
4258044588,26303188@N00,2010-01-09 10:08:50.0,145.314042,-37.765869,16,http://www.flickr.com/photos/26303188@N00/4258044588/,0
4257973354,26303188@N00,2010-01-09 09:36:11.0,145.314132,-37.765855,16,http://www.flickr.com/photos/26303188@N00/4257973354/,0
4307776599,26303188@N00,2010-01-26 09:59:49.0,144.978418,-37.821446,14,http://www.flickr.com/photos/26303188@N00/4307776599/,0
4308514792,26303188@N00,2010-01-26 11:35:44.0,144.978418,-37.821446,14,http://www.flickr.com/photos/26303188@N00/4308514792/,0
4308515366,26303188@N00,2010-01-26 08:34:17.0,144.978418,-37.821446,14,http://www.flickr.com/photos/26303188@N00/4308515366/,0
5222294050,26303188@N00,2010-12-01 10:13:27.0,145.565843,-37.767118,13,http://www.flickr.com/photos/26303188@N00/5222294050/,0
8246699008,89521819@N07,2012-11-23 23:50:37.0,145.011763,-37.768543,14,http://www.flickr.com/photos/89521819@N07/8246699008/,0
8246697974,89521819@N07,2012-11-23 23:54:11.0,145.011763,-37.768543,14,http://www.flickr.com/photos/89521819@N07/8246697974/,0
5548843638,52361622@N02,2011-03-18 22:36:54.0,145.387573,-37.581589,7,http://www.flickr.com/photos/52361622@N02/5548843638/,0
5548265115,52361622@N02,2011-03-18 09:27:31.0,144.997619,-37.827316,15,http://www.flickr.com/photos/52361622@N02/5548265115/,0
5548848742,52361622@N02,2011-03-18 08:10:26.0,144.997619,-37.827316,15,http://www.flickr.com/photos/52361622@N02/5548848742/,0
5548839426,52361622@N02,2011-03-18 22:45:19.0,145.387573,-37.581589,7,http://www.flickr.com/photos/52361622@N02/5548839426/,0
"""
        self.result_gentraj = [[2, 0, 1], [5, 3, 4], [6], [11, 10], [9, 12], [7, 8]]
        self.result_filtraj = [[2, 0, 1], [5, 3, 4], [11, 10], [7, 8]]

        fi = tempfile.NamedTemporaryFile(mode='w', delete=False)
        fi.write(datastr)
        self.fin = fi.name
        fi.close()

        self.rawdata = load_data(self.fin)


    def tearDown(self):
        os.unlink(self.fin)

    
    def test_gen_trajectories(self):
        trajs = gen_trajectories(self.rawdata)
        self.assertEqual(trajs, self.result_gentraj)


    def test_filter_trajectories(self):
        lng_min = 144.597363
        lat_min = -38.072257
        lng_max = 145.360413
        lat_max = -37.591764
        trajs = gen_trajectories(self.rawdata)
        trajs = filter_trajectories(lng_min, lat_min, lng_max, lat_max, trajs, self.rawdata)
        self.assertEqual(trajs, self.result_filtraj)


    def test_calc_dist(self):
        coords = [(-37.85967, 144.73251), (-37.8615, 144.73306), (-38.14967, 144.32739)]
        index = [(0, 1), (0, 2), (1, 2)]
        dists = [0.193, 47.989, 47.861] # km, http://www.daftlogic.com/projects-google-maps-distance-calculator.htm
        for i in range(len(index)):
            with self.subTest():
                p1 = coords[index[i][0]]
                p2 = coords[index[i][1]]
                dist = calc_dist(p1[1], p1[0], p2[1], p2[0]) # km
                acc = 1 - abs(dist - dists[i]) / dists[i]
                #print('\n', dist, dists[i], acc)
                self.assertTrue(acc > 0.9)


if __name__ == '__main__':
    unittest.main(verbosity=2)

