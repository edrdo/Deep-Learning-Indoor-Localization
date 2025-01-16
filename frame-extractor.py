import cv2
import math
import numpy as np
import os
import sys
import Common

def handle(video_file, frames_required):
  label = '_'.join(os.path.splitext(os.path.basename(video_file))[0].split('_')[1:])
  LABEL_CONV = {
    "diversidade_de_formas" : "DF",
    "atrio_caes_principio_etico" : "AT_CA",
    "globo" : "GL",
    "teatro_dos_sentidos" : "TS",
    "atrio_a_que_cheira" : "AT_CH",
    "comer_e_nao_ser_comido" : "CN",
    "diversidade_genetica_incerteza" : "DG",
    "especiacao" : "ES",
    "atrio_ovos_principio_estetico" : "AT_O2",
    "selecao_sexual" : "SS",
    "terra_mar_ar" : "TMA",
    "atrio_ovo_esferico" : "AT_O1",
    "atrio_medicamentos_principio_cientifico" : "AT_M",
    "selecao_artificial" : "SA",
    "hall_primeiro_andar" : "HA",
    "selecao_natural" : "SN",
    "diversidade_de_cores" : "DC",
    "atrio_sementes_principio_economico" : "AT_S",
    "atrio_mamiferos_cadeira" : "AT_I2",
    "analogia_homologia" : "AH",
    "atrio_diluicao_como_espetaculo" : "AT_I1",
    "atrio" : "A"
  }
  label = LABEL_CONV.get(label, '')
  if label == '':
    print('*** IGNORING', video_file) 
    return
  print('==> Video file', video_file)
  print('Label', label)
  v =  Common.VideoInput(video_file)
  frame_count = int(v.frame_count)
  step = math.floor(frame_count / frames_required)


  print("Width", v.width, "Height", v.height)
  print("FPS", v.fps)
  print('# total frames:', v.frame_count)
  print('# required frames:', frames_required)
  print('# frame step:', step)
  

  fin = 0
  fout = 0
  csv_out = open("out/%s_%s.csv" % (prefix,label),"w")
  while fout < frames_required:
    more, frame = v.next_frame()
    if not more:
      break
    if fin % step == 0:
      fout +=1
      fin += 1
      frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
      image_file = "out/%s/%s_%04d_%04d.jpeg" % (label, prefix,fout, fin)
      os.makedirs('out/' + label,exist_ok=True)
      cv2.imwrite(image_file, frame)
      print("%s,%s,%s,%d" % (image_file,label,video_file,fin), file=csv_out)
    else:
     fin += 1 
  
  csv_out.close() 
  print(fout, "frames written")

prefix = sys.argv[1]
frames_required = int(sys.argv[2])

for video_file in sys.argv[3:]:
  handle(video_file, frames_required)

