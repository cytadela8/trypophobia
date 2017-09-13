#!/usr/bin/env bash

neptune run --input ../../tryponet_set-test --input     common.py --environment keras-2.0-cpu-py3 --worker gcp-small main.py;

