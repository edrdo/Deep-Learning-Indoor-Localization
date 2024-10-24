import cv2
import tensorflow as tf
import numpy as np
import PIL 
import os
import sys

class VideoInput:
    def __init__(self, video_file):
        self.video_file = video_file
        self.handle = v =  cv2.VideoCapture(video_file)
        self.frame_count = int(v.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width = v.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = v.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.fps = v.get(cv2.CAP_PROP_FPS)
        self.frame_step = 1.0 / self.fps
        self.current_time = 0
        self.current_frame = -1

    def next_frame(self):
        r,f = self.handle.read()
        self.current_frame += 1
        self.current_time += self.frame_step
        return r,f

def load_image(image):
    if type(image) != PIL.Image.Image:
        if type(image) == np.ndarray:
            image = PIL.Image.fromarray(image).convert('RGB')
        else:
            image = PIL.Image.open(image).convert('RGB')
    return image

class Model:

    def __init__(self, path):
        dict_file = os.path.join(path, 'dict.txt')
        model_file = os.path.join(path, 'model.tflite')
        with open(dict_file, 'r') as f:
            self.labels = [line.strip() for line in f.readlines()]
        self.interpreter = tf.lite.Interpreter(model_path=model_file)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.floating_model = self.input_details[0]['dtype'] == np.float32
        self.height = self.input_details[0]['shape'][1]
        self.width = self.input_details[0]['shape'][2]
    def classify(self, image, max_results, min_confidence):
        with load_image(image).resize((self.width, self.height)) as img:
            input_data = np.expand_dims(img, axis=0)
            if self.floating_model:
                input_data = (np.float32(input_data) - 127.5) / 127.5
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            self.interpreter.invoke()
            output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
            results = np.squeeze(output_data)
            top_categories = results.argsort()[::-1]
            if max_results != None:
                top_categories = top_categories[:max_results]
            # print("==> %s <==" % file)
            final_results = []
            used_labels = set()
            for i in top_categories:
                if self.floating_model:
                    r = float(results[i])
                else:
                    r = float(results[i] / 255.0)
                if min_confidence != None and r < min_confidence:
                    break
                if self.labels[i] not in used_labels:
                    res = (self.labels[i], r)
                    final_results.append(res)
                    used_labels.add(self.labels[i])
            return final_results