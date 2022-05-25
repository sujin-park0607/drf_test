# import django
# django.setup()

from requests import request
import requests
from .people_counter.findObjectAlgorithm.centroidtracker import CentroidTracker
from .people_counter.findObjectAlgorithm.trackableobject import TrackableObject
from rest_framework.parsers import JSONParser
from django.apps import AppConfig
# from .serializers import StaySerializer

import numpy as np
import os
import time
import dlib
import cv2

import sys
from pathlib import Path
from django.apps import AppConfig
 
# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wetyle_share.settings')
# import django
# django.setup()


BASE_DIR = Path(__file__).resolve().parent.parent


# class peopleCounter:
class PeopleCounter(AppConfig):
    name = 'api'

    # def counting(self, data):
        # data = JSONParser().parse(request)
        # serializer = StaySerializer(data=data)
        # if serializer.is_valid(): 
        #     serializer.save()

    # def people_counter(self, prototxt, caffemodel):
    def people_counter(self,prototxt,caffemodel):
        # 클래스 분류
        CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
            "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
            "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
            "sofa", "train", "tvmonitor"]

        # 모델 설정
        # prototxt = 'simple_object_tracker/MobileNetSSD_deploy.prototxt'
        # caffemodel = 'simple_object_tracker/MobileNetSSD_deploy.caffemodel'
        


        print("[INFO] loading model...")
        net = cv2.dnn.readNetFromCaffe(prototxt, caffemodel)

        cap = cv2.VideoCapture("http://203.252.230.244:8090/?action=stream")

        if not cap.isOpened():
            print('Video Open Failed')
            sys.exit()
            
        time.sleep(1.0)

        #f_w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        #f_h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        #fourcc = cv2.VideoWriter_fourcc(*"MP4V")
        #out = cv2.VideoWriter("output.mp4", fourcc, 30, (f_w, f_h), True)

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
            
            if not frame[0]:
                break
            
            original_frame = frame[1]
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
                    if confidence > 0.3:
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

            cv2.line(frame, (0, int(H * 0.55)), (W, int(H * 0.55)), (0, 255, 255), 2)
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
                        if direction < 0 and centroid[1] < int(H * 0.55):
                            totalUp += 1
                            data = {
                                'place' : 'Seongan-gil',
                                'inout' : 1
                            }
                            try:
                                hi = requests.get('https://localhost:8000/count/',json=data)
                                print(hi.status_code)
                            except:
                                print('error')
                            
                            time.sleep(2)
                            # self.counting(data)

                            to.counted = True
                        elif direction > 0 and centroid[1] > int(H * 0.55):
                            totalDown += 1
                            # data = {
                            #     'place' : 'Seongan-gil',
                            #     'inout' : 0
                            # }
                            # response = requests.get('https://localhost:8000/count/',json=data)
     
                    
                            # self.counting(data)
                            to.counted = True
                            
                trackableObjects[objectID] = to

                text = "ID {}".format(objectID)
                cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
            info = [
                ("Up", totalUp),
                ("Down", totalDown),
                ("Status", status),
            ]
            for (i, (k, v)) in enumerate(info):
                text = "{}: {}".format(k, v)
                cv2.putText(frame, text, (10, H - ((i * 20) + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
            #out.write(frame)
            cv2.imshow("Frame", frame)
            # cv2.imshow('Original_Frame', original_frame)
            key = cv2.waitKey(1)
            if key == ord("q"):
                break
            totalFrames += 1

        #out.release()
        cap.release()
        cv2.destroyAllWindows()
        
    def ready(self):
        prototxt = os.path.join(BASE_DIR,'api','people_counter','MobileNetSSD_deploy.prototxt')
        caffemodel = os.path.join(BASE_DIR,'api','people_counter','MobileNetSSD_deploy.caffemodel')
        self.people_counter(prototxt,caffemodel)