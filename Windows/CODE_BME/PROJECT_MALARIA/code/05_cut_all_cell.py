import json
import cv2
import os
from tqdm import *


row_th = 200
col_th = 200




# 1. load json
json_train = 'malaria/training.json'
with open(json_train, 'r') as fr:
    json_data_train = json.load(fr)
    
json_test = 'malaria/test.json'
with open(json_test, 'r') as fr:
    json_data_test = json.load(fr)

    
# 2. iteration
category_to_count = {}
image_path_root = 'malaria/images/'
dst = 'malaria/cell_data/'
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
                    
                    x_delta = (row_th-(x2-x1))//2
                    y_delta = (col_th-(y2-y1))//2
                    x1_new = x1-x_delta
                    x2_new = x2+x_delta
                    y1_new = y1-y_delta
                    y2_new = y2+y_delta
                    while x2_new-x1_new<row_th:
                        x2_new += 1
                    while y2_new-y1_new<col_th:
                        y2_new += 1

                    is_skip = False
                    if x1_new<0 or x2_new>img.shape[0] or y1_new<0 or y2_new>img.shape[1]:
                        is_skip = True
                    
                    if is_skip==False:
                        label = cell['category']
                        #print('cell, label={0}, position={1},{2},{3},{4}'.format(label,x1,x2,y1,y2))
                        filename = os.path.join(dst, image_name.split('.')[0]+'___'+str(cnt)+'___'+label.replace(' ', '_')+'.png')

                        subimg = img[x1_new:x2_new, y1_new:y2_new]
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
                    x_delta = (row_th-(x2-x1))//2
                    y_delta = (col_th-(y2-y1))//2
                    x1_new = x1-x_delta
                    x2_new = x2+x_delta
                    y1_new = y1-y_delta
                    y2_new = y2+y_delta
                    while x2_new-x1_new<row_th:
                        x2_new += 1
                    while y2_new-y1_new<col_th:
                        y2_new += 1

                    is_skip = False
                    if x1_new<0 or x2_new>img.shape[0] or y1_new<0 or y2_new>img.shape[1]:
                        is_skip = True
                    
                    if is_skip==False:
                        label = cell['category']
                        #print('cell, label={0}, position={1},{2},{3},{4}'.format(label,x1,x2,y1,y2))
                        filename = os.path.join(dst, image_name.split('.')[0]+'___'+str(cnt)+'___'+label.replace(' ', '_')+'.png')
                        subimg = img[x1_new:x2_new, y1_new:y2_new]
                        cv2.imwrite(filename, subimg)
                        if label not in category_to_count:
                            category_to_count[label] = 0
                        category_to_count[label]+=1

                    
print(category_to_count)                    
