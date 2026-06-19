#!/usr/bin/env python3

import statistics
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import glob, os, os.path
import time
import json
import sys

matplotlib.use('Agg')
plt.rcParams["patch.force_edgecolor"] = True
#bpl.default_style()
#Turns interactive plotting off use plt.ion() to turn back on
plt.ioff()

plt.style.use('ggplot')
#plt.bar(x,y, edgecolor="k")
#clb = plt.colorbar()
#clb.set_label('Counts', labelpad=-34, y=1.05, rotation=0, size=16)

#plt.rcParams['font.family'] = 'sans-serif'
#plt.rcParams['font.sans-serif'] = 'Calibri'

file_glob = "df_*.json"

fileList = []
fileList.extend(sorted(glob.glob('./df-dumps/' + file_glob)))

print(len(fileList))
#sys.exit(0)

output_dir=time.strftime("%Y-%m-%d_%H-%M-%S")
outputPath = "./images/" + output_dir
if not os.path.exists(outputPath):
    os.makedirs(outputPath)


#fileList = glob.glob('df_2018-06-28_12-30.json')

print("Histograms to plot: " + str(len(fileList)))
filename=0 # ffmpeg wants sequentially numbered images
arrPrev=[]
summaryPrev={}
maxY=70
for jsonDump in fileList: 
    print(jsonDump)
    savePath = outputPath+"/"+str(filename).zfill(8)+".png"
    print(savePath)

    try:
        # open and parse df dump
        with open(jsonDump) as jsonDumpFile:
            data = json.load(jsonDumpFile)
        # gen list of OSD utils
        utilArr = []
        for osd in data['nodes']:
            if osd['utilization'] != 0: # supress destroyed OSDs 
                utilArr.append(osd['utilization'])

        summary = data['summary']
    except Exception as e:
        print("error encountered, using previous values: " + str(e))
        utilArr = arrPrev
        summary = summaryPrev

    # catch empty dumps and replace with previous 
    if sum(utilArr) == 0:
        print("empty util values (mgr oddness), using previous values")
        utilArr = arrPrev
        summary = summaryPrev

    if utilArr == arrPrev:
        print('duplicate, skipping!')
        continue

    #if ( data.size == 0 ):
    #    print("input file is empty")
    #    if ( dataPrev.size != 0 ):
    #        print("using previous dataset")
    #        data = dataPrev 
    #    else: 
    #        print("previous dataset nonexistent, skipping")
    #        continue
        #continue

    #fig, ax = plt.subplots(1, 2)
    ax = plt.hist(utilArr, bins = 100, range = [0, 100], zorder=2)
    ax = plt.gca()
    # keep y-axis scaling in one direction (up)
    #if ax.get_ylim()[1] > maxY:
    #    maxY = plt.gca().get_ylim()[1]

    maxY=1450
    plt.ylim((0,maxY))
    plt.xlim((0,100))

    dumpName=jsonDump.split("/")[-1:][0]
    date=time.strptime(dumpName, "df_%Y-%m-%d_%H-%M.json")
    #plt.title(time.strftime("%d %b %Y %H:%M", date), loc='left',fontdict={'fontsize': 12})
    plt.title(time.strftime("%d %b %Y", date), loc='left',fontdict={'fontsize': 12})

    plt.xlabel('OSD util (%)', fontsize=11)
    plt.ylabel('count',fontsize=11)
    plt.gcf().text(0.75, 0.9, "%d OSDs" % len(utilArr), fontsize=12)
    #plt.gcf().text(0.4, 0.9, "{:.1f}/{:.1f}PB".format(summary['total_kb_used']/1000000000000, summary['total_kb']/1000000000000) , fontsize=12)

    # Mean line
    #utilMean = statistics.mean(utilArr) 
    #plt.axvline(utilMean, color='k', linestyle='dashed', linewidth=1, zorder=5)
    #plt.text(utilMean + utilMean/20,
    #     maxY - maxY/20,
    #     'Mean: {:.2f}'.format(utilMean))

    #utilStdDev = statistics.stdev(utilArr)
    #plt.axvline(utilMean - utilStdDev, color='k', linestyle='dashed', linewidth=0.6, zorder=5)
    #plt.axvline(utilMean - utilStdDev*2, color='k', linestyle='dashed', linewidth=0.6, zorder=5)
    #plt.axvline(utilMean - utilStdDev*3, color='k', linestyle='dashed', linewidth=0.6, zorder=5)
    #plt.axvline(utilMean + utilStdDev, color='k', linestyle='dashed', linewidth=0.6, zorder=5)
    #plt.axvline(utilMean + utilStdDev*2, color='k', linestyle='dashed', linewidth=0.6, zorder=5)
    #plt.axvline(utilMean + utilStdDev*3, color='k', linestyle='dashed', linewidth=0.6, zorder=5)
    #plt.text(1, maxY - maxY/10, 'Mean: {:.2f}\nStdev: {:.2f}'.format(utilMean, utilStdDev))



    plt.grid(color='0.7', linestyle='--', linewidth=1)
    #plt.tick_params(axis ='both', which ='both', length = 2, width= 0.5, color = '0.7', labelsize=9)
    #plt.gca().set_frame_on(True)
    #fig.axes.get_xaxis().set_visible(True)
    #plt.axis('on')
    #plt.axhline(linewidth=2, color="0.7") 
    #plt.axvline(linewidth=2, color="0.7") 
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(0.5)
        ax.spines[axis].set_color('0.7')

    ax.set_facecolor('0.92')

    sub_ax = inset_axes(
        parent_axes=ax,
        width="10%",
        height="50%",
        borderpad=1  # padding between parent and inset axes
    )

# add content inside inset plot
    sub_ax.bar(
            ['usage (PB)'],
            [summary['total_kb_used']/1000000000000],
            color='red',
            alpha=0.5
    )

    sub_ax.bar(
            ['usage (PB)'],
            [summary['total_kb']/1000000000000 - summary['total_kb_used']/1000000000000],
            bottom = [summary['total_kb_used']/1000000000000],
            color='blue',
            alpha=0.5
    )
    plt.ylim(0,180)
    plt.grid(color='0.9', linestyle='--', linewidth=1)


    plt.gcf().set_size_inches(1920.0/300.0,1080.0/300.0)
    plt.savefig(savePath, dpi=300, bbox_inches='tight')
    plt.close()
    arrPrev=utilArr
    summary = summaryPrev
    filename=filename+1
