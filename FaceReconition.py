from Yolo.detect import Y5Detect
from pymongo import MongoClient
import face_recognition
import cv2

model = Y5Detect(weights="./Yolo/weights/best.pt")


uri = "mongodb://localhost:27017/"
Client = MongoClient(uri)
DataBase = Client["Thien"]
UserCollection = DataBase["User"]





def RegFace(Codes,TestImage,bboxes,thresh=0.6):
    Name = None
    Id = None

    if len(bboxes)> 0:
        x0, y0, x1, y1 = [int(_) for _ in bboxes[0]][:4]
        img = TestImage[y0-10:y1+10, x0-10:x1+10]
        if img.shape[0]>0 and img.shape[1]>0:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            EncodeTest = face_recognition.face_encodings(img)
            if len(EncodeTest)>0:
                EncodeTest = EncodeTest[0]
                for i in range(len(Codes)):
                    result = face_recognition.compare_faces([Codes[i]], EncodeTest,tolerance=thresh)
                    if result[0] == True:
                        User = UserCollection.find_one({"Code": Codes[i]})
                        Id = User['_id']
                        Name = User['Name']
                        # cv2.putText(TestImage, "Name:{} id {}".format(Name, id ), (x0, y0), 0, 5e-3 * 130, (0, 255, 255), 2)

    return TestImage,Name,Id

def DrawFace(image=None, boxes=None,labels=None, scores=0):

    FaceBoxes  = []
    FaceScores = []
    for i in range(len(labels)):
        W = boxes[i][2] - boxes[i][0]
        H = boxes[i][3] - boxes[i][1]
        if (labels[i] =="withmask" or labels[i] =="withoutmask") and W > 100 and H >100:
            FaceBoxes.append(boxes[i])
            FaceScores.append(scores[i])
    color = [0,255,0]

    FaceBbox = []



    if len(FaceBoxes) > 0:
        FaceBbox.append(FaceBoxes[0])
        label = "Face: {:.2f}".format(FaceScores[0])
        xmin, ymin, xmax, ymax = FaceBoxes[0]

        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, 1) #cv2.FONT_HERSHEY_SIMPLEX

        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 1, cv2.LINE_AA)
        cv2.rectangle(image, (xmin, ymin - h), (xmin + w, ymin), color, -1, cv2.LINE_AA)
        cv2.putText(image, label, (xmin, ymin), cv2.FONT_HERSHEY_COMPLEX_SMALL ,0.8, (255,255,255),1,cv2.LINE_AA)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image,FaceBbox


def DetectFace(image):
    img = image.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    bboxs,labels,scores = model.predict(img)
    img ,bbox = DrawFace(img , bboxs,labels,scores)

    D = 0 
    if len(bbox) > 0:
            x0, y0, x1, y1 = [int(_) for _ in bbox[0]][:4]
            W = x1 - x0
            H = y1 - y0
            D = W*H
    if D < 40000:
        bbox = []
        img = image
    return img,bbox





# if __name__ == "__main__":
#     source = 0
#     cap = cv2.VideoCapture(source)
#
#     while True:
#
#         ret, image_bgr  = cap.read()
#
#         if ret == 0:
#             break
#         img = image_bgr.copy()
#
#
#         image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         IMG, BBOX = DetectFace(image)
#
#
#         cv2.imshow('person', IMG)
#         k = cv2.waitKey(1) & 0xff
#         if k == ord('q') or k == 27:
#             break
#
#     # When everything done, release the capture
#     cap.release()
#     cv2.destroyAllWindows()