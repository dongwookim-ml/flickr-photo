#!/usr/bin/env python3
import unittest
import tempfile
import os
import re
from traj_visualise import load_traj, gen_kml


class TrajVisualiseTestCase(unittest.TestCase):
    def setUp(self):
        t2data = """\
Trajectory_ID, User_ID, #Photo, Start_Time, Travel_Distance(km), Total_Time(min), Average_Speed(km/h)
26519,99804259@N00,3,2013-12-28 19:31:54,0.44294172719428504,84.01666666666667,0.3163241852607471
"""
        t1data = """\
Trajectory_ID, Photo_ID, User_ID, Timestamp, Longitude, Latitude, Accuracy, Marker(photo=0 video=1), URL
26519,11617521194,99804259@N00,2013-12-28 19:31:54,144.962463,-37.810136,16,0,http://www.flickr.com/photos/99804259@N00/11617521194/
26519,11617542904,99804259@N00,2013-12-28 19:48:28,144.96588,-37.812213,16,0,http://www.flickr.com/photos/99804259@N00/11617542904/
26519,11617370033,99804259@N00,2013-12-28 20:55:55,144.966658,-37.812346,16,0,http://www.flickr.com/photos/99804259@N00/11617370033/
"""
        self.kmlstr = """\
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document id="001">
<name>Trajectories</name>
<description>Trajectory visualization</description>
<visibility>1</visibility>
<Style id="style1">
<LineStyle>
<color>2f0000ff</color>
<width>3</width>
</LineStyle>
</Style>
<Placemark id="26519">
<name>Trajectory_26519</name>
<description>User_ID: 99804259@N00&lt;br/&gt;Start_Time: 2013-12-28 19:31:54&lt;br/&gt;Travel_Distance: 0.44 km&lt;br/&gt;Total_Time: 84.02 min&lt;br/&gt;Average_Speed: 0.32 km/h&lt;br/&gt;#Photos: 3&lt;br/&gt;Photos: [11617521194, 11617542904, 11617370033]</description>
<visibility>1</visibility>
<styleUrl>#style1</styleUrl>
<LineString>
<coordinates>144.962463,-37.810136 144.965880,-37.812213 144.966658,-37.812346</coordinates>
</LineString>
</Placemark>
<Placemark id="11617521194">
<name>Photo_11617521194</name>
<description>Trajectory_ID: 26519&lt;br/&gt;Photo_ID: 11617521194&lt;br/&gt;User_ID: 99804259@N00&lt;br/&gt;Timestamp: 2013-12-28 19:31:54&lt;br/&gt;Coordinates: (144.962463, -37.810136)&lt;br/&gt;Accuracy: 16&lt;br/&gt;URL: http://www.flickr.com/photos/99804259@N00/11617521194/</description>
<visibility>1</visibility>
<Point>
<coordinates>144.962463,-37.810136</coordinates>
</Point>
</Placemark>
<Placemark id="11617542904">
<name>Photo_11617542904</name>
<description>Trajectory_ID: 26519&lt;br/&gt;Photo_ID: 11617542904&lt;br/&gt;User_ID: 99804259@N00&lt;br/&gt;Timestamp: 2013-12-28 19:48:28&lt;br/&gt;Coordinates: (144.96588, -37.812213)&lt;br/&gt;Accuracy: 16&lt;br/&gt;URL: http://www.flickr.com/photos/99804259@N00/11617542904/</description>
<visibility>1</visibility>
<Point>
<coordinates>144.965880,-37.812213</coordinates>
</Point>
</Placemark>
<Placemark id="11617370033">
<name>Photo_11617370033</name>
<description>Trajectory_ID: 26519&lt;br/&gt;Photo_ID: 11617370033&lt;br/&gt;User_ID: 99804259@N00&lt;br/&gt;Timestamp: 2013-12-28 20:55:55&lt;br/&gt;Coordinates: (144.966658, -37.812346)&lt;br/&gt;Accuracy: 16&lt;br/&gt;URL: http://www.flickr.com/photos/99804259@N00/11617370033/</description>
<visibility>1</visibility>
<Point>
<coordinates>144.966658,-37.812346</coordinates>
</Point>
</Placemark>
</Document>
</kml>
"""
        ft1 = tempfile.NamedTemporaryFile(mode='w', delete=False)
        ft2 = tempfile.NamedTemporaryFile(mode='w', delete=False)
        fo  = tempfile.NamedTemporaryFile(delete=False)
        ft1.write(t1data)
        ft2.write(t2data)
        self.ftable1 = ft1.name
        self.ftable2 = ft2.name
        self.fout = fo.name
        ft1.close()
        ft2.close()
        fo.close()
        

    def tearDown(self):
        os.unlink(self.ftable1)
        os.unlink(self.ftable2)
        os.unlink(self.fout)


    def test_gen_kml(self):
        traj_id = 26519
        traj_data, traj_stats = load_traj(self.ftable1, self.ftable2)
        gen_kml(self.fout, traj_data, traj_stats, [traj_id])
        with open(self.fout, 'r') as f:
            kmlstr1 = f.read()
            kmlstr1 = re.sub('\n\s+', '\n', kmlstr1)
            self.assertEqual(kmlstr1, self.kmlstr)


if __name__ == '__main__':
    unittest.main(verbosity=2)

