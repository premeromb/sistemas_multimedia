# import the opencv library
import cv2
from dt_apriltags import Detector
import numpy as np
import time

at_detector = Detector(families='tag16h5',
                       nthreads=1,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)

camera_params = (336.7755634193813, 336.02729840829176,
                 333.3575643300718, 212.77376312080065)

capture_duration = 8

# define a video capture object
vid = cv2.VideoCapture(0)

# Check if camera opened successfully
if (vid.isOpened() == False):
  print("Error opening video  file")


def checkForTags():

  start_time = time.time()

  captured = []

  while int(time.time() - start_time) < capture_duration:

      # Capture the video frame
      ret, frame = vid.read()
      grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

      # Display the resulting frame
      cv2.imshow('frame', grayFrame)

      tags = at_detector.detect(grayFrame, True, camera_params, 0.2)

      tag_ids = [tag.tag_id for tag in tags]

      color_img = cv2.cvtColor(grayFrame, cv2.COLOR_GRAY2RGB)

      for tag in tags:
          if tag.decision_margin > 55:

              for idx in range(len(tag.corners)):
                  cv2.line(color_img, tuple(
                      tag.corners[idx-1, :].astype(int)), tuple(tag.corners[idx, :].astype(int)), (0, 255, 0))

                  cv2.putText(color_img, str(tag.tag_id),
                              org=(tag.corners[0, 0].astype(
                                  int)+10, tag.corners[0, 1].astype(int)+10),
                              fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                              fontScale=0.8,
                              color=(0, 0, 255))

              if tag.tag_id not in captured:
                captured.append(tag.tag_id)
              
      cv2.imshow('Detected tags for ', color_img)

  return captured

print(checkForTags())

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()