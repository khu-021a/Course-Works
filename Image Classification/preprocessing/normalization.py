import os
import pickle
import numpy as np 
from PIL import Image


def get_mean_std(image_dir):
	files = os.listdir(image_dir)
	pixel_num = 0
	img_sum = 0
	for f in files:
		with Image.open(os.path.join(image_dir, f)) as img:
			w, h = img.size
			pixel_num += w * h
			img_sum += np.sum(np.asarray(img) / 255, axis=(0, 1))
	
	img_mean = img_sum / pixel_num

	img_nvar = 0
	for f in files:
		with Image.open(os.path.join(image_dir, f)) as img:
			w, h = img.size
			zero_mean = np.asarray(img) / 255 - np.repeat(np.repeat(img_mean.reshape((1, 1, 3)), w, axis=1), h, axis=0)
			img_nvar += np.sum(zero_mean ** 2, axis=(0, 1))
	
	img_std =  np.sqrt(img_nvar / (pixel_num - 1))
	return (img_mean, img_std)

def normalize(image_dir, target_dir, mean, std):
	files = os.listdir(image_dir)
	for f in files:
		with Image.open(os.path.join(image_dir, f)) as img:
			w, h = img.size
			mean_ndarr = np.repeat(np.repeat(mean.reshape((1, 1, 3)), w, axis=1), h, axis=0)
			std_ndarr = np.repeat(np.repeat(std.reshape((1, 1, 3)), w, axis=1), h, axis=0)
			normalized_img = (np.asarray(img) / 255 - mean_ndarr) / std_ndarr
			normalized_img.save(os.path.join(target_dir, f), 'PNG')
