##Trajectory recommendation model trained using trajectories observed in Melbourne

###List of files
 - `example_Melb.py` An example to illustrate the usage of the trained model (Python 3 script)
 - `inference_lv.so` Inference procedure (Linux)
 - `inference_lv_mac.so` Inference procedure (MacOS)
 - `model-Melb.pkl`  Trained model
 - `shared.pyc`      Python 3 bytecode used in trained model
 - `ssvm.pyc`        Python 3 bytecode used in trained model

###Usage
Copy all the above files to a directory (on Linux/MacOS), for example `recommender`, 
go to this directory and run the example:

```$ cd recommender```

```$ python example_Melb.py```

The output are the 10 trajectories recommended given the start POI and length of trajectory (specified in ```example_Melb.py```).

###NOTE
 - the required python version to load the trained model is 3.5.3, other versions of python will cause "bad magic number" error.
 - on MacOS, please rename `inference_lv_mac.so` to `inference_lv.so` before running the example.
 - Because of a compatability issue from a specific library, which we are using in the recommendation algorithm, it is not possible to compile Windows binary for `inference_lv.so`. Until we can resolve this problem, please use Linux or macOS systems instead.
