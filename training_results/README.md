This folder contains folders with training results. Folder names corespond to folder names in `/models`. Additionally number of parameters and lowest log-loss on validation is appended to folder names.

### Folder contents:
- `model` - hdf5 file with trained model (WARNING! This is end result, NOT the BEST result)
- `model_weights` - hdf5 file with weights from `model` file
- `model.json` - json description of architecture
- `model_notlearned` - model before first epoch
- `model_weights.$EPOCHNUM.$VAL_LOSS.hdf5` - hdf5 files with weights. To get the best weights you have to get one of this files with lowest VAL_LOSS.
- `on_epoch_end_acc.csv` - csv file with correct classification percent (50% threshold) in learn set after each epoch
- `on_epoch_end_loss.csv` - csv files with log-loss in learn set after each epoch
- `on_epoch_end_val_acc.csv` - csv with correct classification percent (50% threshold) in validation set after each epoch
- `on_epoch_end_val_loss.csv` - csv files with log-loss in validation set after each epoch

