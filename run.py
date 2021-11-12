import cv2
import face_recognition
import os
import time
import serial
import dlib
import numpy.core._dtype_ctypes


class FaceRecognition:
	def __init__(self):
		self.path = "face"  # 存放人脸文件夹
		self.known_face_encodings = []  # 已知人脸编码列表
		self.number = 0  # true的次数
		self.cap = cv2.VideoCapture(1)  # 默认摄像头
		self.serialPort = "COM3"  # Arduino串口
		self.baudRate = 9600  # Arduino波特率
		dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

	def make_dir(self):  # 判断路径是否存在
		if not os.path.exists(self.path):
			os.makedirs(self.path)

	def known_encoding_face(self):  # 已知人脸编码
		for face in os.listdir(self.path):
			if face.endswith(".jpg") or face.endswith(".png"):
				load = face_recognition.load_image_file(self.path + "/" + face)
				load_encoding = face_recognition.face_encodings(load)
				self.known_face_encodings.append(load_encoding)

	def cream(self):  # 摄像头识别
		ser = serial.Serial(self.serialPort, self.baudRate, timeout=0.5)  # 串口通信
		while True:
			ret, frame = self.cap.read()
			try:
				small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
				# 开始计时算帧数
				start = time.time()
				# 翻转通道
				rgb_frame = small_frame[:, :, ::-1]
				# 定位人脸,画框
				face_locations = face_recognition.face_locations(rgb_frame)
				for face_location in face_locations:
					top, right, bottom, left = face_location
					top *= 4
					right *= 4
					bottom *= 4
					left *= 4
					cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
				# 对实时画面编码并对比
				face_encodings = face_recognition.face_encodings(rgb_frame)
				for face_encoding in face_encodings:
					for known_face_encoding in self.known_face_encodings:
						match = face_recognition.compare_faces(known_face_encoding, face_encoding, tolerance=0.6)
						# 如果为true,计数+1
						if match[0]:
							self.number += 1
							# 如果为10,给arduino发信号,且清除计数

							if self.number == 5:
								self.number = 0
								ser.write("1".encode())
								time.sleep(20)

				# 计时结束算帧率
				end = time.time()
				fps = 1 / (end - start)
				# 写出fps和窗口标题
				cv2.putText(frame, "FPS: {}".format(fps), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
				cv2.imshow('Video', frame)
				# 按下q退出
				if cv2.waitKey(1) == ord('q'):
					break
			except:
				pass
		# 释放资源
		self.cap.release()


def main():
	run = FaceRecognition()
	run.make_dir()
	run.known_encoding_face()
	run.cream()


if __name__ == "__main__":
	main()