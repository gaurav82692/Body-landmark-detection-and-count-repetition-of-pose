# Import opencv tool kit 
import cv2
# Import numpy
import numpy as np
# Import pose recognizer 
from poseutil import PoseDetector
# Open video file 
cap = cv2.VideoCapture("pushup.mp4")
# Gesture recognizer 
detector = PoseDetector()
# Direction and number 
dir = 0 # 0 For the next ,1 For the sake of 
count = 0
# Video width height 
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# Recording video settings 
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('videos/pushupoutput.mp4', fourcc, 30.0, (width, height))
while True:
	success, img = cap.read()
	if success:
		h, w, c = img.shape
		img = detector.find_pose(img, draw=True)
		positions = detector.find_positions(img)
		if positions:
			angle1 = detector.find_angle(img, 12, 24, 26)
			angle2 = detector.find_angle(img, 12, 14, 16)
			bar = np.interp(angle2, (45, 150), (w // 2 - 100, w // 2 + 100))
			cv2.rectangle(img, (w // 2 - 100, h - 150), (int(bar), h - 100), (0, 255, 0), cv2.FILLED)
			if angle2 <= 50 and angle1 >= 165 and angle1 <= 175:
				if dir == 0:
					count = count + 0.5
					dir = 1
			if angle2 >= 125 and angle1 >= 165 and angle1 <= 175:
				if dir == 1:
					count = count + 0.5
					dir = 0
		cv2.putText(img, str(int(count)), (w // 2, h // 2), cv2.FONT_HERSHEY_SIMPLEX, 10, (255, 255, 255), 20, cv2.LINE_AA)
		cv2.imshow('Image', img)
		out.write(img)
	else:
# End of video exit 
		break
# If you press q key , Program exit 
	key = cv2.waitKey(1)
	if key == ord('q'):
		break
# Close the video Saver 
out.release()
# Turn off camera 
cap.release()
# Close the program window 
cv2.destroyAllWindows()
