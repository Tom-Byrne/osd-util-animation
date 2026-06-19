# Animate the OSD utilisation of a Ceph cluster

![demo](./demo.gif)

## Collect raw data

you could use a simple cron to collecting the data:

```
# cat /etc/cron.d/ceph-osd-df.cron
*/10 * * * * root ( date --iso-8601=seconds --utc; ceph osd df -fjson > /root/df-dumps/df_$(date +'\%Y-\%m-\%d_\%H-\%M').json) >> /var/log/ceph-osd-df.log 2>&1
```

### Generate images

`histo_with_size.py` loops over the json files and produces the histogram images using matplotlib

All configuration (input directory, output format) is done via tweaking the script. You can tweak the glob used to change the time scale e.g. `df_*_00_00` to have one frame an hour.

### Make the video

`make_vid.sh` takes a directory of images and turn them into a video. The files must be sequentially numbered, which is handled by the python script.

`interp_vid.sh` does some basic interpolation to smooth the movement, useful for longer term animations
