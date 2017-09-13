In order to to be train a new model create in a new folder a python script main.py which begins with:

import sys
sys.path.insert(0, "/input/")
import common
from keras.models import Sequential
from keras.layers import *

Then after the keras model was defined add:

common.experiment(model)

To run the experiment in the cloud adjust cloud_run.sh to select the desired environment
