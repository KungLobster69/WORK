import os
import json
import sys
import yaml
import shutil

K = 10

# manually delete convertor/folder1~10 firstly (rm -rf convertor/folder1)

# read images and labels
fid_to_image_path = {}
fid_to_label_path = {}
p1 = 'convertor/fold0/images/train2017'
for f in os.listdir(p1):
    fid = f.split('.')[0]
    image_path = os.path.join(p1,f)
    fid_to_image_path[fid] = image_path
p2 = 'convertor/fold0/images/val2017'
for f in os.listdir(p2):
    fid = f.split('.')[0]
    image_path = os.path.join(p2,f)
    fid_to_image_path[fid] = image_path
p3 = 'convertor/fold0/labels/train2017'
for f in os.listdir(p3):
    fid = f.split('.')[0]
    label_path = os.path.join(p3,f)
    fid_to_label_path[fid] = label_path
p4 = 'convertor/fold0/labels/val2017'
for f in os.listdir(p4):
    fid = f.split('.')[0]
    label_path = os.path.join(p4,f)
    fid_to_label_path[fid] = label_path
print(  'fid_to_image_path={0}'.format(len(fid_to_image_path)    ))
print(  'fid_to_label_path={0}'.format(len(fid_to_label_path)    ))
fid_list = []
for k in fid_to_image_path:
    fid_list.append( k )


batch = len(fid_list)//K    

# cut images/labels to kfold: TBD

# prepare data
#   mkdir
#   copy files to each folder : TBD
p1 = 'convertor/'
for i in range(K):
    if i<K-1:
        sub_fid_list_for_train = fid_list[(i+1)*batch:]
        if i>0:
            sub_fid_list_for_train = fid_list[:i*batch]+sub_fid_list_for_train
        sub_fid_list_for_test = fid_list[i*batch:(i+1)*batch]
    else:
        sub_fid_list_for_train = fid_list[:i*batch]
        sub_fid_list_for_test = fid_list[i*batch:]
    j = i+1
    print('fold{0}, sub_fid_list_for_train = {1}'.format(j, len(sub_fid_list_for_train)))
    print('fold{0}, sub_fid_list_for_test = {1}'.format(j, len(sub_fid_list_for_test)))
    p2 = os.path.join(p1, 'fold{0}'.format(j))
    for p3 in ['images/train2017', 'images/val2017', 'labels/train2017', 'labels/val2017']:
        p4 = os.path.join(p2,p3)
        os.makedirs(p4)
        print('successful mkdir path = {0}'.format(p4))
    # modify yaml file and copy to each folder
    with open('malaria/malaria_conf.yaml', 'r') as file:
        yaml_obj = yaml.safe_load(file)
    yaml_obj['train'] = yaml_obj['train'].replace('fold0', 'fold{0}'.format(j))
    yaml_obj['val'] = yaml_obj['val'].replace('fold0', 'fold{0}'.format(j))
    with open('convertor/fold{0}/malaria_conf.yaml'.format(j), 'w') as file:
        yaml.dump(yaml_obj, file)
    # copy image and label to each folder
    for fid in sub_fid_list_for_test:  
        src = fid_to_image_path[fid]
        dst = src.replace('fold0', 'fold{0}'.format(j))
        shutil.copy(src, dst)
        src = fid_to_label_path[fid]
        dst = src.replace('fold0', 'fold{0}'.format(j))
        shutil.copy(src, dst)
    for fid in sub_fid_list_for_train:  
        src = fid_to_image_path[fid]
        dst = src.replace('fold0', 'fold{0}'.format(j))
        shutil.copy(src, dst)
        src = fid_to_label_path[fid]
        dst = src.replace('fold0', 'fold{0}'.format(j))
        shutil.copy(src, dst)
    
    # fid_to_image_path
    

# iterate each fold
for i in range(K):
    j = i+1
    print('start {0} of {1}'.format(i, K))
    
    
    # train model 
    os.system("python train.py  --img 512 --batch 12 --epochs 5 --data /home/ubuntu/project2/convertor/fold{0}/malaria_conf.yaml --cfg /home/ubuntu/project2/malaria/yolov5x.yaml --name yolov5x_malaria ".format(j))
    print('end {0} of {1}'.format(i, K))