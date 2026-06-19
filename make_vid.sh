#!/bin/bash

ffmpeg -framerate 30 -i $1/%08d.png -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p -vf scale=-2:1080 "osd_util_$(date +'%F_%H-%M-%S').mp4"
