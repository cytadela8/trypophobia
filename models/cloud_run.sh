#!/usr/bin/env bash

neptune data upload ../common/common.py;
neptune send --config ../common/neptune-cloud.yaml --input tryponet_set-test --input common.py --environment keras-2.0-gpu-py3 --worker gcp-gpu-large main.py;

