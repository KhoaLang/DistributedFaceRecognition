import cv2 
import os
import face_recognition
import pickle

class TrainingEntry:
	def __init__(self, train_dataset_path):
		self.ref_dictt = None
		self.embed_dictt = None
		self.train_dataset_path = train_dataset_path

	def input(self, personName, personId):
		name = personName
		ref_id = personId
		try:
			f=open("ref_name.pkl","rb")
			self.ref_dictt=pickle.load(f)
			f.close()
		except:
			self.ref_dictt={}
			
		self.ref_dictt[ref_id]=name
		f=open("ref_name.pkl","wb")
		pickle.dump(self.ref_dictt,f)
		f.close()
		try:
			f=open("ref_embed.pkl","rb")
			self.embed_dictt=pickle.load(f)
			f.close()
		except:
			self.embed_dictt={}

	def process_image(self, path, ref_id):
		# print(path)
		try:
			frame = cv2.imread(path)
			small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
			rgb_small_frame = small_frame[:, :, ::-1]
			face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
			if face_locations != []:
				face_encoding = face_recognition.face_encodings(frame)[0]
				
				if ref_id in self.embed_dictt:
					self.embed_dictt[ref_id]+=[face_encoding] 
				else:
					self.embed_dictt[ref_id]=[face_encoding]  
			print("Taken this image!!")
		except Exception as e:
			print("Broken Image !!! Abort this image.")

	def execute(self):
		# find the path of the folder train_dataset
		folder_path = self.train_dataset_path
		
		# loop through every image in the folder
		for _, _, files in os.walk(folder_path):
			for file in files:
				personName = file.split("_")[1]
				personId = file.split("_")[0]
				print(f"####### Trainning {personName} images with index {file.split('_')[0]} #######")	
			
				print("...")
				print(f"{folder_path}/{file}")
				print("...")

				self.input(personName, personId)
				self.process_image(f"{folder_path}/{file}", personId)
				print(f"####### Done trainning {personName} images !!! #######")	

				f=open("ref_embed.pkl","wb")
				pickle.dump(self.embed_dictt,f)
				f.close()
				print("Trainning Complete")
		
if __name__ == "__main__":
	# ****Modiy the train dataset path as you need**** 
	train_entry = TrainingEntry('../train_dataset')
	train_entry.execute()