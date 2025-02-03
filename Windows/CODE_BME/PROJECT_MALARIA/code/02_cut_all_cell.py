import json
import cv2
import os
from tqdm import *



# 1. load json
json_train = '../malaria_small/training.json'
with open(json_train, 'r') as fr:
    json_data_train = json.load(fr)
    
json_test = '../malaria_small/test.json'
with open(json_test, 'r') as fr:
    json_data_test = json.load(fr)

    
# 2. iteration
category_to_count = {}
image_path_root = '../malaria_small/images/'
dst = '../malaria_small/cell_data/'
for image_name in tqdm( os.listdir(image_path_root) ):
    image_path_real = os.path.join(image_path_root, image_name)
    img = cv2.imread(image_path_real, cv2.IMREAD_COLOR)# IMREAD_GRAYSCALE, IMREAD_COLOR

    # training data
    for d in json_data_train:
        if image_name in d['image']['pathname']:
            json1 = d
            if 'objects' in json1:
                cnt = 0
                for cell in json1['objects']:
                    cnt+=1
                    x1 = cell['bounding_box']['minimum']['r']
                    x2 = cell['bounding_box']['maximum']['r']
                    y1 = cell['bounding_box']['minimum']['c']
                    y2 = cell['bounding_box']['maximum']['c']
                    label = cell['category']
                    #print('cell, label={0}, position={1},{2},{3},{4}'.format(label,x1,x2,y1,y2))
                    filename = os.path.join(dst, image_name.split('.')[0]+'___'+str(cnt)+'___'+label.replace(' ', '_')+'.png')
                    subimg = img[x1:x2, y1:y2]
                    cv2.imwrite(filename, subimg)
                    if label not in category_to_count:
                        category_to_count[label] = 0
                    category_to_count[label]+=1
    # testing data
    for d in json_data_test:
        if image_name in d['image']['pathname']:
            json1 = d
            if 'objects' in json1:
                cnt = 0
                for cell in json1['objects']:
                    cnt+=1
                    x1 = cell['bounding_box']['minimum']['r']
                    x2 = cell['bounding_box']['maximum']['r']
                    y1 = cell['bounding_box']['minimum']['c']
                    y2 = cell['bounding_box']['maximum']['c']
                    label = cell['category']
                    #print('cell, label={0}, position={1},{2},{3},{4}'.format(label,x1,x2,y1,y2))
                    filename = os.path.join(dst, image_name.split('.')[0]+'___'+str(cnt)+'___'+label.replace(' ', '_')+'.png')
                    subimg = img[x1:x2, y1:y2]
                    cv2.imwrite(filename, subimg)
                    if label not in category_to_count:
                        category_to_count[label] = 0
                    category_to_count[label]+=1

                    
print(category_to_count)                    
