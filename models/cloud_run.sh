#!/usr/bin/env bash

neptune data upload ../common/common.py;
neptune send --config ../common/neptune-cloud.yaml --input tryponet_set --input common.py --environment keras-2.0-cpu-py3 --worker gcp-small main.py;

