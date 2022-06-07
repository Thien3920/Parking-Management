import cv2
import numpy as np
import insightface
from insightface.model_zoo.retinaface import RetinaFace
from insightface.app import FaceAnalysis
from insightface.model_zoo.arcface_onnx import ArcFaceONNX
# from insightface.data import get_image as ins_get_image

# app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
# app.prepare(ctx_id=0, det_size=(640, 640))
# img = ins_get_image('t1')

# faces = app.get(img)
# rimg = app.draw_on(img, faces)
# cv2.imwrite("./t1_output.jpg", rimg)
# cv2.imwrite("/home/thien/Desktop/t1_output.jpg", rimg)

detector = RetinaFace(model_file='/home/thien/.insightface/models/buffalo_l/det_10g.onnx')
recognizer = ArcFaceONNX(model_file='/home/thien/.insightface/models/buffalo_l/w600k_r50.onnx')

img = cv2.imread('/home/thien/Pictures/Screenshot from 2022-05-24 14-47-59.png')
faces, kpss = detector.detect(img, input_size =(640, 640))
feat_face_1 = recognizer.get(img, kpss[0])

img = cv2.imread('/home/thien/Pictures/Screenshot from 2022-06-06 21-50-29.png')
faces, kpss = detector.detect(img, input_size =(640, 640))
feat_face_2 = recognizer.get(img, kpss[0])



print(feat_face_1.shape)
print(feat_face_2.shape)


distance = recognizer.compute_sim(feat_face_1,feat_face_2)

print("disstance:",distance)


# print(faces)
# print(kpss)
