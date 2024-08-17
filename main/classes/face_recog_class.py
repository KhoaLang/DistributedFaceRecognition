#!/usr/bin/env python3

import time
import cv2
import face_recognition
import cv2
import numpy as np
import time
import pickle

class Face_Recog():
    def __init__(self, ref_name_url="./ref_name.pkl", ref_embed_url="./ref_embed.pkl"):
        # *********************Initialize************************
        f=open(ref_name_url,"rb")
        self.ref_dictt=pickle.load(f)         #ref_dict=ref vs name //dictionary contain name of user with id as key
        f.close()

        f=open(ref_embed_url,"rb")
        self.embed_dictt=pickle.load(f) #embed_dict- ref  vs embedding 
        f.close()

        self.known_face_encodings = []  #encodingd of faces
        self.known_face_names = []	   #ref_id of faces
        #############################################################frame capturing from camera and face recognition
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True
        self.nameFlag = ""

        for ref_id , embed_list in self.embed_dictt.items():
            for embed in embed_list:
                self.known_face_encodings +=[embed]
                self.known_face_names += [ref_id]

    def draw_ident_box(self, frame, fps = None):
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            if fps is not None:
                cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30), font, 1.0, (255, 255, 255), 1)  
            if name != "Unknown":
                cv2.putText(frame, f'{self.ref_dictt[name]}', (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            else:
                cv2.putText(frame, "Unknown", (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        font = cv2.FONT_HERSHEY_DUPLEX
        return frame

    def recognition(self, frame, rgb_small_frame)->tuple:
        # Only process every other frame of video to save time
        if self.process_this_frame:
            self.face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)
            for face_encoding in self.face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index] # name variable is the id of the user
                    # ****Call API to update the enter/leave time****
                    if self.nameFlag != name: # Compare the id of this frame with the prev frame to determin whether is it nessary to call the API
                        self.nameFlag = name
                        # res = requests.post("http://localhost:3002/api/timestamp/{}".format(name), data={"enterTime": arrow.now().format("YYYY/MM/DD HH:mm:ss"), "leaveTime": None})
                    # ****************************************************************
                    self.face_names.append(name)
        self.process_this_frame = not self.process_this_frame
        self.end_time = time.time()
        fps = 1 / (self.end_time - self.start_time)
        with open(f"./log/fps_log_{self.stream_key}.txt", "a") as f:
            f.write(f"{str(fps)}\n")
        frame = self.draw_ident_box(frame = frame, fps=fps)

        return (self.nameFlag, frame) #{"data": self.nameFlag, "frame": compressed_frame}

    def publish_video(self, frame, stream_key):    
        self.start_time = time.time()
        self.stream_key = stream_key
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
        rgb_small_frame = np.ascontiguousarray(small_frame[:, :, (0, 1, 2)])    
        
        self.nameFlag, frame = self.recognition(frame, rgb_small_frame)

        return frame
    
    def __str__(self):
        return "This is Face Recog class"
        

