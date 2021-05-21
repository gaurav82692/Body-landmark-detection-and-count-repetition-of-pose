import cv2
import mediapipe as mp
import math



class PoseDetector():
	def __init__(self,
	static_image_mode=False,
	upper_body_only=False,
	smooth_landmarks=True,
	min_detection_confidence=0.5,
	min_tracking_confidence=0.5):
		self.static_image_mode = static_image_mode
		self.upper_body_only = upper_body_only
		self.smooth_landmarks = smooth_landmarks
		self.min_detection_confidence = min_detection_confidence
		self.min_tracking_confidence = min_tracking_confidence
		# Create a Pose Objects are used to detect human posture 
		self.pose = mp.solutions.pose.Pose(self.static_image_mode, self.upper_body_only, self.smooth_landmarks,
		self.min_detection_confidence, self.min_tracking_confidence)
	def find_pose(self, img, draw=True):
		imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		self.results = self.pose.process(imgRGB)
		if self.results.pose_landmarks:
			if draw:
				mp.solutions.drawing_utils.draw_landmarks(img, self.results.pose_landmarks,
						mp.solutions.pose.POSE_CONNECTIONS)
		return img
	def find_positions(self, img):
		self.lmslist = []
		if self.results.pose_landmarks:
			for id, lm in enumerate(self.results.pose_landmarks.landmark):
				h, w, c = img.shape
				cx, cy = int(lm.x * w), int(lm.y * h)
				self.lmslist.append([id, cx, cy])
		return self.lmslist
	def find_angle(self, img, p1, p2, p3, draw=True):
		x1, y1 = self.lmslist[p1][1], self.lmslist[p1][2]
		x2, y2 = self.lmslist[p2][1], self.lmslist[p2][2]
		x3, y3 = self.lmslist[p3][1], self.lmslist[p3][2]
		angle = int(math.degrees(math.atan2(y1 - y2, x1 - x2) - math.atan2(y3 - y2, x3 - x2)))
		if angle < 0:
			angle = angle + 360
		if angle > 180:
			angle = 360 - angle
		if draw:
			cv2.circle(img, (x1, y1), 20, (0, 0, 0), cv2.FILLED)
			cv2.circle(img, (x2, y2), 30, (255, 0, 255), cv2.FILLED)
			cv2.circle(img, (x3, y3), 20, (0, 255, 255), cv2.FILLED)
			cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255, 3))
			cv2.line(img, (x2, y2), (x3, y3), (255, 255, 255, 3))
			cv2.putText(img, str(angle), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 2)
		return angle