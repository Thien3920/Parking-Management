import os 
import cv2
import time
import numpy as np
import plate.tools.predict_system as predict_sys
import plate.tools.predict_lpd as predict_lpd
from PIL import Image, ImageFont, ImageDraw
import re
import time
import threading
from collections import Counter
import math





class ALPR():
    def __init__(self, out_dir ='./outputs') -> None:
        self.text_system = predict_sys.TextSystem()
        self.lp_detector = predict_lpd.LisencePlateDetector()
        self.output_directory = out_dir
        self.previous_bbox = [0,0,2,2]
        self.list_images = []
        self.countPlates = 0
        self.countPlates_threshold = 11
        self.num_frame_without_plates = 0
        self.recog_plate = ''
        self.checkup =''
        self.checkdown = ''
        

    def detect_lp(self,path: str, Bbox : bool, save : bool, show : bool):
        
        img = cv2.imread(path)
        Name = os.path.basename(path).split('.')[0]
        bbox, _, _, _ = self.lp_detector(img)
        if len(bbox):
            pts = bbox[0]
            if Bbox:
                xmin = int(min(pts[0]))
                ymin = int(min(pts[1]))
                xmax = int(max(pts[0]))
                ymax = int(max(pts[1]))
                cv2.rectangle(img, (xmin,ymin),(xmax,ymax), (0, 255, 0), 2)
            else:
                pt1 = [int(pts[0][0]),int(pts[1][0])]
                pt2 = [int(pts[0][1]),int(pts[1][1])]
                pt3 = [int(pts[0][2]),int(pts[1][2])]
                pt4 = [int(pts[0][3]),int(pts[1][3])]
                ptslist = np.array([[pt1,pt2,pt3,pt4]],dtype=np.int32)
                cv2.drawContours(img, ptslist, -1, (0, 255, 0), 2)
            
            if save:
                cv2.imwrite('%s/%s_lpd.png' % (self.output_directory, Name), img)

            if show:
                cv2.imshow(Name,img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
        
        else:
            print('No License Plates Detected')
    
    def blur_lp(self,path: str, save : bool, show : bool):
        
        img = cv2.imread(path)
        Name = os.path.basename(path).split('.')[0]
        max_len = max(img.shape[0],img.shape[1])
        w_k = int(0.2*max_len)
        if w_k%2 == 0:
            w_k = w_k+1
        blurred_img = cv2.GaussianBlur(img, (w_k,w_k), 0)
        mask = np.zeros(img.shape, dtype=np.uint8)
        bbox, _, _, _ = self.lp_detector(img)
        if len(bbox):
            pts = bbox[0]
            
            pt1 = [int(pts[0][0]),int(pts[1][0])]
            pt2 = [int(pts[0][1]),int(pts[1][1])]
            pt3 = [int(pts[0][2]),int(pts[1][2])]
            pt4 = [int(pts[0][3]),int(pts[1][3])]
            ptslist = np.array([[pt1,pt2,pt3,pt4]],dtype=np.int32)
            mask = cv2.fillPoly(mask,ptslist,(255,255,255))
            img = np.where(mask==0, img, blurred_img)
            
            # if save:
            #     cv2.imwrite('%s/%s_blurred.png' % (self.output_directory, Name), img)

            if show:
                cv2.imshow('Name',img)
                cv2.waitKey(1)
                cv2.destroyAllWindows()
        
        else:
            print('No License Plates Detected')
        
    
    
    def find_possible_plates(self, input_img,f_scale=1.0):
        bbox, _,  LlpImg, _ = self.lp_detector(input_img)
        if len(bbox):
            pts = bbox[0]
            xmin = int(min(pts[0]))
            ymin = int(min(pts[1]))
            xmax = int(max(pts[0]))
            ymax = int(max(pts[1]))
            bbox=[xmin,ymin,xmax,ymax]
            return bbox,LlpImg
        return None,LlpImg
    
    def getDistance(self,pointA, pointB):
        return math.sqrt(math.pow((pointA[0] - pointB[0]), 2) + math.pow((pointA[1] - pointB[1]), 2))
    
    def tracking(self,previous_bbox,current_bbox):
        
        CenterA = ((previous_bbox[2]-previous_bbox[0])//2,(previous_bbox[3]-previous_bbox[1])//2)
        CenterB = ((current_bbox[2]-current_bbox[0])//2,(current_bbox[3]-current_bbox[1])//2)

        distance = self.getDistance(CenterA, CenterB)
        return distance
    def votting(self,ups,downs):
        if len(ups) > 7  and len(downs)> 7:
            A = Counter(ups)
            B = Counter(downs)
            up = A.most_common(1)[0][0]
            down = B.most_common(1)[0][0]
            up = up[0:2]+"-"+up[3:5]
            if len(down)==5:
                down =down[0:3]+"."+down[3:5]
            return up,down
        else:
            return None,None
            
    def recognized_plate(self,listimages):
        ups = []
        downs = []
        for LlpImg in listimages:
            Ilp = LlpImg[0]
            Ilp = cv2.cvtColor(Ilp, cv2.COLOR_BGR2GRAY)
            Ilp = cv2.cvtColor(Ilp, cv2.COLOR_GRAY2BGR)
            _, rec_res = self.text_system(Ilp*255.)
            try:
                ups.append(rec_res[0][0])
                downs.append(rec_res[1][0])
            except:
                pass
        up,down = self.votting(ups,downs)
        if up  is not None:
            if self.checkup != up and self.checkdown != down:
                self.recog_plate = up+"|"+down
            else:
                self.recog_plate = ''
            
            self.checkup = up
            self.checkdown = down
        else:
            self.recog_plate = ''
        print('--------------------------------')
        print(self.recog_plate)
        print('--------------------------------')
    
    def default(self):
        self.previous_bbox = [0,0,2,2]
        self.list_images = []
        self.countPlates = 0
        self.countPlates_threshold = 11
        self.num_frame_without_plates = 0
        self.recog_plate = ''
        self.checkup =''
        self.checkdown = ''

    
    def predict(self,img,initial = False):
        if initial:
            self.default()

        cv2.rectangle(img,(15,50),(315,328),(0,255,255),1,cv2.FONT_HERSHEY_PLAIN)
        roi = img[50:328,15:315]
        # roi = img
        bbox,LlpImg = self.find_possible_plates(roi)
        
        if bbox is not None:
            self.num_frame_without_plates = 0
            distance = self.tracking(self.previous_bbox,bbox)
            self.previous_bbox = bbox
        

            if distance < 4:
                if(self.countPlates < self.countPlates_threshold):
                    
                    # try:
                    #     lpimg = roi[bbox[1]:bbox[3],bbox[0]:bbox[2]]
                    #     cv2.imshow('plate',lpimg)
                    # except:
                    #     pass
                    self.list_images.append(LlpImg)
                    self.countPlates += 1
                elif(self.countPlates == self.countPlates_threshold):
                    threading.Thread(target=self.recognized_plate, args=(self.list_images,)).start()
                    self.countPlates += 1
            
            else:
                self.countPlates = 0
                self.list_images = []
            
        if (bbox == None):
            self.num_frame_without_plates += 1
            if (self.countPlates <= self.countPlates_threshold and self.countPlates > 0 and self.num_frame_without_plates > 5):
                threading.Thread(target=self.recognized_plate, args=(self.list_images, )).start()
                self.countPlates = 0
        
        
        return self.recog_plate




    def recognize_video(self, source: str, f_scale : float):
        if source == "0":
            source = 0

        cap = cv2.VideoCapture(source)
        while(True):
            ret, img = cap.read()
            cv2.rectangle(img,(15,50),(315,328),(0,255,255),1,cv2.FONT_HERSHEY_PLAIN)
            
            
            roi = img[50:328,15:315]
            # roi = img
            bbox,LlpImg = self.find_possible_plates(roi)
            
            if bbox is not None:
                self.num_frame_without_plates = 0
                distance = self.tracking(self.previous_bbox,bbox)
                self.previous_bbox = bbox
            

                if distance < 4:
                    if(self.countPlates < self.countPlates_threshold):
                        
                        try:
                            lpimg = roi[bbox[1]:bbox[3],bbox[0]:bbox[2]]
                            cv2.imshow('plate',lpimg)
                        except:
                            pass
                        self.list_images.append(LlpImg)
                        self.countPlates += 1
                    elif(self.countPlates == self.countPlates_threshold):
                        threading.Thread(target=self.recognized_plate, args=(self.list_images,)).start()
                        self.countPlates += 1
                
                else:
                    self.countPlates = 0
                    self.list_images = []
                
            if (bbox == None):
                self.num_frame_without_plates += 1
                if (self.countPlates <= self.countPlates_threshold and self.countPlates > 0 and self.num_frame_without_plates > 5):
                    threading.Thread(target=self.recognized_plate, args=(self.list_images, )).start()
                    self.countPlates = 0


            
            cv2.imshow('window',img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        

def draw_text(img, text,
          pos=(0, 0),
          font=cv2.FONT_HERSHEY_PLAIN,
          font_scale=3,
          text_color=(0, 0, 0),
          font_thickness=2,
          text_color_bg=(0, 0, 0)
          ):

    x, y = pos
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    cv2.rectangle(img, pos, (int(x + 1.1*text_w), y + 2*text_h), text_color_bg, -1)
    im_p = Image.fromarray(img)
    draw = ImageDraw.Draw(im_p)
    font = ImageFont.truetype("fonts/simfang.ttf",int(32*font_scale/1.5))
    draw.text((x, y ),text,text_color,font=font)
    result_o = np.array(im_p)
    # cv2.putText(img, text, (x, int(y + text_h + font_scale - 1)), font, font_scale, text_color, font_thickness)
    return result_o

def strip_chinese(string):
    en_list = re.findall(u'[^\u4E00-\u9FA5]', string)
    for c in string:
        if c not in en_list:
            string = string.replace(c, '')
    return string






if __name__ == "__main__":
    x = ALPR(out_dir='lpd_results')
    # print(x.tracking([0,0,2,2],[0,0,4,4]))
    x.recognize_video(source='/home/thien/Downloads/nhan-dien-bien-so-xe-may-dung-camera-cong-nghiep-xu-ly-anh-ftw2lbxa_LkJbuSf8.mp4',f_scale=1.0)