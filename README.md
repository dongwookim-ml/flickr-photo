###Flickr-Photo
Descrptions of photos/movies taken near Melbourne area from YFCC100M dataset and trajectories extracted from the descriptions.

--------------------

* ```data``` Data files
  * ```Melbourne-bbox.kml```     The two (big/small) bounding boxes of Melbourne
  * ```Melbourne-bigbox.csv```   Data inside the big bounding box, output of ```src/filtering_bigbox.py```
  * ```Melb-table1.csv```        Trajectories, output of ```src/generate_tables.py```
  * ```Melb-table2.csv```        Some metrics of trajectories, output of ```src/generate_tables.py```

* ```src``` Source files
  * ```filtering_bigbox.py```  Python3 scripts to filter out photos outside the big bounding box from YFCC100M dataset
  * ```generate_tables.py```  Python3 scripts to generate trajectories (i.e. the two tables) with respect to the small bounding box
  * ```traj_visualise.py```   Python3 scripts to generate (a number of) KML files to visualise trajectories
