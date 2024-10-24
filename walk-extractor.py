import csv
import cv2
import math
import numpy as np
import os
import re
import sys
import Common

def handle(csv_file, video_file, model_id):
  time_re = re.compile('^(\d+):(\d+)$')
  times = []
  with open(csv_file, newline='') as csv_input:
    data = csv.reader(csv_input, delimiter='\t')
    for row in data:
      (begin,end,label) = row[1:4]
      print(begin,end,label)
      m = time_re.match(begin)
      begin = int(m.group(1)) * 60 + int(m.group(2))
      m = time_re.match(end)
      end = int(m.group(1)) * 60 + int(m.group(2))
      times.append((begin,end,label))      

  v =  Common.VideoInput(video_file)
  m = Common.Model('models/' + model_id)

  for (begin,end,label) in times:
    _, f = v.next_frame()
    first_frame = None
    label_f_count = 0
    label_p_count = 0
    while True:
      if v.current_time < end:
        label_f_count += 1
        r = m.classify(cv2.cvtColor(f, cv2.COLOR_BGR2RGB), max_results=1, min_confidence=0)
        if r[0][0] == label:
          label_p_count +=1 
        if not first_frame:
          first_frame = v.current_frame
        _, f = v.next_frame()
      else:
          print(label, '[',begin, end,'] <-> [', first_frame, v.current_frame - 1,']', label_p_count, label_f_count, label_p_count/label_f_count)
          first_frame = None
          break

csv_file = sys.argv[1]
video_file = sys.argv[2]
model_id = sys.argv[3]
handle(csv_file, video_file, model_id)

