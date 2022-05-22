# import the necessary packages
from findObjectAlgorithm.centroidtracker import CentroidTracker
from findObjectAlgorithm.trackableobject import TrackableObject
import numpy as np
import time
import dlib
import cv2
import sys

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
prototxt = 'MobileNetSSD_deploy.prototxt'
caffemodel = 'MobileNetSSD_deploy.caffemodel'

print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(prototxt, caffemodel)
cap = cv2.VideoCapture('t2.mp4')

if not cap.isOpened():
    print('Video Open Failed')
    sys.exit()
    
time.sleep(2.0)
 
writer = None
W = None
H = None

ct = CentroidTracker(maxDisappeared=40, maxDistance=50)
trackers = []
trackableObjects = {}
totalFrames = 0
totalDown = 0
totalUp = 0

while True:
	frame = cap.read()
	frame = frame[1]

	frame = cv2.resize(frame, (600, 800), interpolation=cv2.INTER_AREA)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	if W is None or H is None:
		(H, W) = frame.shape[:2]

	status = "Waiting"
	rects = []
 
	if totalFrames % 30 == 0:
		status = "Detecting"
		trackers = []
    
		blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
		net.setInput(blob)
		detections = net.forward()

		for i in np.arange(0, detections.shape[2]):
			confidence = detections[0, 0, i, 2]
			if confidence > 0.4:
				idx = int(detections[0, 0, i, 1])

				if CLASSES[idx] != "person":
					continue
				box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
				(startX, startY, endX, endY) = box.astype("int")

				tracker = dlib.correlation_tracker()
				rect = dlib.rectangle(startX, startY, endX, endY)
				tracker.start_track(rgb, rect)
				trackers.append(tracker)
	else:
		for tracker in trackers:
			status = "Tracking"
			tracker.update(rgb)
			pos = tracker.get_position()
			startX = int(pos.left())
			startY = int(pos.top())
			endX = int(pos.right())
			endY = int(pos.bottom())   
			rects.append((startX, startY, endX, endY))

	cv2.line(frame, (0, int(H * 0.6)), (W, int(H * 0.6)), (0, 255, 255), 2)
	objects = ct.update(rects)

	for (objectID, centroid) in objects.items():
		to = trackableObjects.get(objectID, None)
		if to is None:
			to = TrackableObject(objectID, centroid)
		else:
			y = [c[1] for c in to.centroids]
			direction = centroid[1] - np.mean(y)
			to.centroids.append(centroid)
			if not to.counted:
				if direction < 0 and centroid[1] < int(H * 0.6):
					totalUp += 1
					to.counted = True
				elif direction > 0 and centroid[1] > int(H * 0.6):
					totalDown += 1
					to.counted = True
		trackableObjects[objectID] = to

		text = "ID {}".format(objectID)
		cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
	info = [
		("Up", totalUp),
		("Down", totalDown),
		("Status", status),
	]
	for (i, (k, v)) in enumerate(info):
		text = "{}: {}".format(k, v)
		cv2.putText(frame, text, (10, H - ((i * 20) + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

	if writer is not None:
		writer.write(frame)
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1)
	if key == ord("q"):
		break
	totalFrames += 1

if writer is not None:
	writer.release()
if not cap.isOpened():
	cap.stop()
else:
	cap.release()
cv2.destroyAllWindows()