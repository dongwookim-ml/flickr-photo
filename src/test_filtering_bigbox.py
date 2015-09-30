#!/usr/bin/env python3
import unittest
import tempfile
import os
from filtering_bigbox import filtering

class FilterBigBoxTestCase(unittest.TestCase):
    def setUp(self):
        datastr = """\
7088065	30302697@N00	jhf	2005-03-01 12:39:28.0	1111467388	SONY+CLIE	Gnome	This+gnome+just+appeared+three+stories+up+at+school+one+day.	2005,bushschool,gnome,prank,washington		-122.288368	47.622562	15	http://www.flickr.com/photos/30302697@N00/7088065/	http://farm1.staticflickr.com/8/7088065_65c9d45e09.jpg	Attribution-NonCommercial License	http://creativecommons.org/licenses/by-nc/2.0/	8	1	65c9d45e09	65c9d45e09	jpg	0
343224206	17143211@N00	MDG26	2006-12-31 23:00:32.0	1167783247	Canon+PowerShot+SD450	Team+Muppet+Show				-73.458709	41.394066	11	http://www.flickr.com/photos/17143211@N00/343224206/	http://farm1.staticflickr.com/141/343224206_0f11b3c88a.jpg	Attribution License	http://creativecommons.org/licenses/by/2.0/	141	1	0f11b3c88a	0f11b3c88a	jpg	0
6325727670	61048402@N08	Indigo+Skies+Photography	2011-11-07 07:20:22.0	1320751886	NIKON+D90	Sunlight+through+the+morning+fog	This+scene+greeted+me+on+the+way+to+work+yesterday+morning.%0A%0AI+hope+the+1+hour+of+using+the+content-aware+fill+was+worth+it+to+get+rid+of+the+power+lines%21%0A%0APhotomatrix+used+to+consolidate+5+exposures+and+then+converted+to+B%26W.+The+image+was+then+cropped+and+processed+in+Alien+Skin+Exposure.%0A%0AEnjoy%21	australia,b%26w,beautiful,black+and+white,clouds,farm,flickr,fog,hills,morning,paddock,panoramic,photography,pyalong,ray+christy,sky,sun,sunlight,trees,victoria		144.87957	-37.155665	11	http://www.flickr.com/photos/61048402@N08/6325727670/	http://farm7.staticflickr.com/6097/6325727670_5192fe3be9.jpg	Attribution-NonCommercial-NoDerivs License	http://creativecommons.org/licenses/by-nc-nd/2.0/	6097	7	5192fe3be9	8ed1387833	jpg	0
"""
        self.resultstr = """\
6325727670,61048402@N08,2011-11-07 07:20:22.0,144.87957,-37.155665,11,http://www.flickr.com/photos/61048402@N08/6325727670/,0
"""

        fi = tempfile.NamedTemporaryFile(mode='w', delete=False)
        fo = tempfile.NamedTemporaryFile(delete=False)
        fi.write(datastr)
        self.fin = fi.name
        self.fout = fo.name
        fi.close()
        fo.close()
        

    def tearDown(self):
        os.unlink(self.fin)
        os.unlink(self.fout)


    def test_filtering(self):
        lng_min = 141.9
        lat_min = -39.3 
        lng_max = 147.1
        lat_max = -35.8
        filtering(lng_min, lat_min, lng_max, lat_max, self.fin, self.fout)
        with open(self.fout, 'r') as f:
            self.assertEqual(f.read(), self.resultstr, 'unexpected results after filtering')


if __name__ == '__main__':
    unittest.main(verbosity=2)
