#!/bin/bash

ffmpeg -i $1 -filter "minterpolate='fps=120:mi_mode=blend:scd=none'" interp_$1
