import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

cap=cv2.VideoCapture(0)
base_options = python.BaseOptions(model_asset_path=(r'model\hand_landmarker.task'))
options = vision.HandLandmarkerOptions(base_options=base_options,num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)

def hand_detection_and_label(image,detection):
    landmarks_list = detection.hand_landmarks
    image_height,image_width, image_channels = image.shape 
    for i,j in enumerate(landmarks_list):
        x = min([coord.x for coord in j])*image_width
        y = min([coord.y for coord in j])*image_height
        cv2.putText(image,f"{(detection.handedness[i][0].category_name)}",(int(x),int(y)),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,255,255),thickness=2, lineType=cv2.LINE_AA)


while True:
    success, frame=cap.read()

    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    detection_result = detector.detect(image)
    hand_detection_and_label(frame,detection_result)
    
    cv2.imshow("Hand Detection",frame)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
