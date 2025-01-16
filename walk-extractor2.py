import csv
import cv2
import math
import numpy as np
import os
import re
import sys
import Common

csv_file = sys.argv[1]
video_file = sys.argv[2]
model_id = sys.argv[3]
output_file = sys.argv[4]

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
csv_output = csv.writer( open(output_file, 'w', newline=''), delimiter='\t')
csv_output.writerow(['time', 'label'] + m.labels)

for (begin,end,label) in times:
  _, f = v.next_frame()
  first_frame = v.current_frame
  label_f_count = 0
  while True:
    if v.current_time < end:
      label_f_count += 1
      f = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
      p = m.predict(f)
      csv_output.writerow([v.current_time, label] + list(p))
      _, f = v.next_frame()
    else:
        print(label, '[',begin, end,'] <-> [', first_frame, v.current_frame - 1,']',  label_f_count)
        break


