import cv2
import model_inference
import getopt
import sys

# For moving average
queue = []
window_size = 0

model = model_inference.Model("model.tflite", "dict.txt")

video_file_path = sys.argv[1]
capture = cv2.VideoCapture(video_file_path)

count = 0
fin = 0
while capture.isOpened():

    ret, frame = capture.read()
    fin += 1

    if not ret:
        break

    # Run inference on the model
    results_raw_frame = model.classify(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), None, None)

    if len(results_raw_frame) > 0:

        if len(queue) < window_size:
            queue.append(results_raw_frame[0])
        else:

            queue.insert(0, results_raw_frame[0])
            print(queue)

            confidence = {}
            total = 0
            for res in queue:
                if res[0] in confidence:
                    confidence[res[0]] += res[1]
                else:
                    confidence[res[0]] = res[1]

            max_confidence = -1.0
            max_room = ""
            queue.pop()
            for room in confidence:
                result = confidence[room] 
                if result > max_confidence:
                    max_confidence = result
                    max_room = room

            text_to_show = ""
            text_to_show = str(fin) + " " +max_room + ", " + "{:.0f}%".format(max_confidence * 100)
            font = cv2.FONT_HERSHEY_PLAIN
            org = (20, 100)
            fontScale = 3
            color = (255, 255, 255)
            thickness = 4
            line_type = cv2.LINE_8
            final_frame = cv2.putText(frame, str(text_to_show), org, font, fontScale, color, thickness, line_type)

    count += 1

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
