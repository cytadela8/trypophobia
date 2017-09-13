In order to to be train a new model create in a new folder a python script main.py which begins with:

import sys
sys.path.insert(0, "/input/") #for cloud
sys.path.insert(0, "../common/") #for local
import common

Then import and define a keras model and run the experiment as:

common.experiment(your_keras_model)

To run the experiment in the cloud adjust cloud_run.sh to select the desired environment and then from the model's folder run:

../cloud_run.sh

To run the experiment locally adjust the data locations in common/neptune-local.yaml and from the inside of the model's folder run:

../local_run.sh
