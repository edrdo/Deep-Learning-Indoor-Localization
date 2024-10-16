import cv2
import math
import numpy as np
import os
import sys

def handle(video_file, frames_required):
  v =  cv2.VideoCapture(video_file)
  label = '_'.join(os.path.splitext(os.path.basename(video_file))[0].split('_')[1:])
  frame_count = int(v.get(cv2.CAP_PROP_FRAME_COUNT))
  step = math.floor(frame_count / frames_required)

  print('==> Video file', video_file)
  print('Label', label)
  print("Width", v.get(cv2.CAP_PROP_FRAME_WIDTH), "Height", v.get(cv2.CAP_PROP_FRAME_HEIGHT))
  print("FPS", v.get(cv2.CAP_PROP_FPS))
  print('# total frames:', frame_count)
  print('# required frames:', frames_required)
  print('# frame step:', step)
  
  
  fin = 0
  fout = 0
  csv_out = open("out/%s_%s.csv" % (prefix,label),"w")
  while fout < frames_required:
    more, frame = v.read()
    if not more:
      break
    if fin % step == 0:
      fout +=1
      fin += 1
      frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
      image_file = "%s_%s_%d_%d.jpeg" % (prefix,label,fout, fin)
      cv2.imwrite("out/" + image_file, frame)
      print("%s,%s,%s,%d" % (image_file,label,video_file,fin), file=csv_out)
    else:
     fin += 1 
  
  csv_out.close()
  print(fout, "frames written")

prefix = sys.argv[1]
frames_required = int(sys.argv[2])

for video_file in sys.argv[3:]:
  handle(video_file, frames_required)

