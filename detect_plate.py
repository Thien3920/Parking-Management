import cv2
import time
import threading
from Plate.class_CNN import NeuralNetwork
from Plate.class_PlateDetection import PlateDetector
from Plate.utils.average_plate import *
from Plate.utils.find_best_quality_images import get_best_images

########### INIT ###########
# Initialize the plate detector
plateDetector = PlateDetector(type_of_plate='RECT_PLATE',
                              minPlateArea=4100,
                              maxPlateArea=15000)




# Initialize the Neural Network
myNetwork = NeuralNetwork(modelFile="./Plate/model/binary_128_0.50_ver3.pb",
                          labelFile="./Plate/model/binary_128_0.50_labels_ver2.txt")

list_char_on_plate = []  # contains an array of the segmented characters in each frame
countPlates = 0  # count the number of same plates
recog_plate = ''
coordinates = (0, 0)
num_frame_without_plates = 0
countPlates_threshold = 11  # the maximum number of images of the same plate to get

recog_plate_copy = None
###########################


def recognized_plate(list_char_on_plate, size):
    """
    input is a list that contains a images of the same plate
    get the best images in the list
    calculates the average plate
    """
    global recog_plate

    t0 = time.time()
    plates_value = []
    plates_length = []

    list_char_on_plate = get_best_images(list_char_on_plate, num_img_return=7)  # get the best images

    for segmented_characters in list_char_on_plate:
        plate, len_plate = myNetwork.label_image_list(segmented_characters[1], size)
        plates_value.append(plate)
        plates_length.append(len_plate)

    final_plate = get_average_plate_value(plates_value, plates_length)  # calculates the average plate
    if len(final_plate) > 7:
        if (final_plate[2] == '8'):
            final_plate = final_plate[:2] + 'B' + final_plate[3:]
        elif (final_plate[2] == '0'):
            final_plate = final_plate[:2] + 'D' + final_plate[3:]
    recog_plate = final_plate

    # print("recognized plate: " + final_plate)
    # print("threading time: " + str(time.time() - t0))


cap = cv2.VideoCapture('/home/thien/Desktop/BaiDuXeThongMinh/Plate/test_videos/test.MOV')  # video path

def predict(image,initial=False):
    global num_frame_without_plates
    global countPlates
    global coordinates
    global list_char_on_plate
    global recog_plate_copy
    global recog_plate
    if initial:
        num_frame_without_plates = 0
        countPlates = 0
        coordinates = (0,0)
        list_char_on_plate = []
        recog_plate_copy = None
        recog_plate = ""
    #     print(initial)
    #
    # print(num_frame_without_plates,countPlates,coordinates,len(list_char_on_plate))

    _frame = cv2.resize(image, (960, 540))  # resize the frame to fit the screen
    frame_height, frame_width = image.shape[:2]
    _frame_height, _frame_width = _frame.shape[:2]
    cropped_frame = image[int(frame_height * 0.3):frame_height, 0:int(frame_width * 0.8)]  # crop the ROI
    cv2.rectangle(_frame, (0, int(_frame_height * 0.3)), (int(_frame_width * 0.8), _frame_height), (255, 0, 0),
                  2)  # draw a
    # rectangle to locate the ROI


    # out.write(_frame)
    # cv2.imshow('video', _frame)

    possible_plates = plateDetector.find_possible_plates(cropped_frame)
    # cv2.imshow('morphed', plateDetector.after_preprocess)
    if possible_plates is not None:
        num_frame_without_plates = 0
        distance = tracking(coordinates,
                            plateDetector.corresponding_area[0])  # calculates the distance between two plates
        coordinates = plateDetector.corresponding_area[0]  # get the coordinate of the detected plate
        if (distance < 100):
            if (countPlates < countPlates_threshold):
                # cv2.imshow('Plate', possible_plates[0])
                temp = []
                temp.append(possible_plates[0])
                temp.append(
                    plateDetector.char_on_plate[0])  # temp = [image of plate, segmented characters on plate]

                list_char_on_plate.append(temp)
                countPlates += 1
            elif (countPlates == countPlates_threshold):
                # create a new thread for image recognition
                threading.Thread(target=recognized_plate, args=(list_char_on_plate, 128)).start()
                countPlates += 1
        else:
            countPlates = 0
            list_char_on_plate = []

    # the program will try to catch 11 images of the same plate and then pick the top 7 best
    # quality images out of 11. However, if the program cannot catch enough images, after
    # num_frame_without_plates frames without plates, it will process the and calculate the
    # final plate
    if (possible_plates == None):
        num_frame_without_plates += 1
        if (countPlates <= countPlates_threshold and countPlates > 0 and num_frame_without_plates > 5):
            threading.Thread(target=recognized_plate, args=(list_char_on_plate, 128)).start()
            countPlates = 0
    result = None
    if recog_plate_copy == recog_plate:
        result = None
    else:
        result = recog_plate
    recog_plate_copy = recog_plate

    # print the result
    cv2.rectangle(_frame, (0, 0), (190, 40), (0, 0, 0), -1)
    cv2.putText(_frame, result, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    return _frame,result

if __name__ == "__main__":
    while (cap.isOpened()):
        ret, frame = cap.read()
        if (frame is None):
            print("[INFO] End of Video")
            break

        # print(predict(frame))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
