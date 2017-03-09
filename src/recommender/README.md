##Trajectory recommendation model trained using trajectories observed in Melbourne

###List of files
 - `example_Melb.py` An example to illustrate the usage of the trained model (Python 3 script)
 - `inference_lv.so` Inference procedure
 - `model-Melb.pkl`  Trained model
 - `shared.pyc`      Python 3 bytecode used in trained model
 - `ssvm.pyc`        Python 3 bytecode used in trained model

###Usage
Copy all the above files to a directory (on Linux), for example `recommender`, 
go to this directory and run the example:

```$ cd recommender```

```$ python example_Melb.py```

The output are the 10 trajectories recommended given the start POI and length of trajectory (specified in ```example_Melb.py```).
