from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tqdm import tqdm

from PIL import UnidentifiedImageError
import os
import numpy as np

def safe_img_load(image_path, target_size=(224, 224)):
    try:
        img = load_img(image_path, target_size=target_size)
        img = img_to_array(img)
        img = np.expand_dims(img, axis=0)
        return img
    except (UnidentifiedImageError, IOError):
        print(f"Could not process img at: {image_path}!")
        return None
    
def clean_dir(dir):
    for root, dirs, files in os.walk(dir):
        for file in tqdm(files):
            if safe_img_load(os.path.join(root, file)) is None:
                os.remove(os.path.join(root, file))
                print(f"Removed img at {os.path.join(root, file)}!")

clean_dir('/Users/leviharris/Desktop/shot-quality-estimation/ex_img_only/finetune_vgg/dataset/train')
clean_dir('/Users/leviharris/Desktop/shot-quality-estimation/ex_img_only/finetune_vgg/dataset/val')
