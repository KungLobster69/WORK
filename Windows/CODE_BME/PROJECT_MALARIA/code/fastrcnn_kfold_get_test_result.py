import numpy as np
import pandas as pd
import json
import traceback
import sys

import matplotlib.pyplot as plt
from matplotlib import patches as patches
import cv2
import os
import shutil as sh

from pathlib import Path
import re
from tqdm import tqdm

import torch
import gc


import warnings 
warnings.simplefilter("ignore")

import seaborn as sns
import sys
sys.path.insert(0, "malaria/weightedboxesfusion/")
from ensemble_boxes import *

import joblib as jl

from PIL import Image

import albumentations as A
from albumentations.pytorch.transforms import ToTensorV2

import torch
import torchvision

from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection import FasterRCNN
from torchvision.models.detection.rpn import AnchorGenerator

from torch.utils.data import DataLoader, Dataset
from torch.utils.data.sampler import SequentialSampler

from sklearn.model_selection import train_test_split

import io
import base64

import time
from IPython.display import clear_output
import joblib as jl



custom_colors = ['#35FCFF', '#FF355A', '#96C503', '#C5035B', '#28B463', '#35FFAF', '#8000FF', '#F400FF']
hex2rgb = lambda hx: (int(hx[1:3],16),int(hx[3:5],16),int(hx[5:7],16))
rgbcolors = list(map(hex2rgb, custom_colors))[1:]
# Albumentations
def get_train_transform():
    return A.Compose([
        A.Flip(0.5),
        ToTensorV2(p=1.0)
    ], bbox_params={'format': 'pascal_voc', 'label_fields': ['labels']})

def get_valid_transform():
    return A.Compose([
        ToTensorV2(p=1.0)
    ], bbox_params={'format': 'pascal_voc', 'label_fields': ['labels']})


def collate_fn(batch):
    return tuple(zip(*batch))

def extract_nested_list(it):
    if isinstance(it, list):
        for sub_it in it:
            yield from extract_nested_list(sub_it)
    elif isinstance(it, dict):
        for value in it.values():
            yield from extract_nested_list(value)
    else:
        yield it
        
def format_prediction(boxes, scores, labels):
    result = np.zeros((len(boxes), 6))

    for i, (j) in enumerate(zip(scores, boxes, labels)):
        result[i, 0] = j[0]
        result[i, 1] = j[1][0]
        result[i, 2] = j[1][1]
        result[i, 3] = j[1][2]
        result[i, 4] = j[1][3]
        result[i, 5] = j[2]

    return result

class MalariaDataset(Dataset):

    def __init__(self, dataframe, root_dir, transforms=None):
        super().__init__()

        self.image_ids = dataframe['pathname'].unique()
        self.df = dataframe
        self.root_dir = root_dir
        self.transforms = transforms

    def __getitem__(self, index: int):

        image_id = self.image_ids[index]
        records = self.df[self.df['pathname'] == image_id]

        image = cv2.imread(f'{self.root_dir}/{image_id}')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32)
        image /= 255.0

        boxes = records[['x_min', 'y_min', 'x_max', 'y_max']].values

        area = records['w'].values * records['h'].values
        area = torch.as_tensor(area, dtype=torch.float32)

        # there is only one class
        labels = records['label'].values
        labels = torch.as_tensor(labels, dtype=torch.int64)

        # suppose all instances are not crowd
        iscrowd = torch.zeros((records.shape[0],), dtype=torch.int64)
        
        target = {}
        target['boxes'] = boxes
        target['labels'] = labels
        # target['masks'] = None
        target['image_id'] = torch.tensor([index])
        target['area'] = area
        target['iscrowd'] = iscrowd

        if self.transforms:
            sample = {
                'image': image,
                'bboxes': target['boxes'],
                'labels': labels
            }
            sample = self.transforms(**sample)
            image = sample['image']
            
            target['boxes'] = torch.stack(tuple(map(torch.tensor, zip(*sample['bboxes'])))).permute(1, 0).float()
        return image, target, image_id

    def __len__(self):
        return self.image_ids.shape[0]


class GlobalConfig:
    def __init__(self, trainf='malaria/training2.json', testf='malaria/test120.json'):    
        self.root_dir = 'malaria/'
        self.train_json_path = trainf
        self.test_json_path = testf
        self.yolo_weights = 'malaria/yolov5x_malaria.pt'
        self.fasterrcnn_weights = 'malaria/fasterrcnn_resnet50_fpn.pth'
        self.seed = 33
        
        
def seed_everything(seed: int):
    np.random.seed(seed)
    torch.manual_seed(seed)
    #torch.cuda.manual_seed(seed)

    

class Averager:
    def __init__(self):
        self.current_total = 0.0
        self.iterations = 0.0

    def send(self, value):
        self.current_total += value
        self.iterations += 1

    @property
    def value(self):
        if self.iterations == 0:
            return 0
        else:
            return 1.0 * self.current_total / self.iterations

    def reset(self):
        self.current_total = 0.0
        self.iterations = 0.0
    
def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        print('directory {0} exists, double check if error or not? '.format(directory))

def main():    
    gc.collect()
    torch.cuda.empty_cache()
    list_of_arguments = sys.argv
    create_dir('kfold_mid_result')
    fold = list_of_arguments[1]
    print('list_of_arguments={0}'.format(list_of_arguments))
    pfold = 'kfold_mid_result/fold_{0}'.format(fold)
    create_dir(pfold)
    try:
        config = GlobalConfig()
        seed_everything(config.seed)

        train_df = pd.read_json(config.train_json_path)
        test_df = pd.read_json(config.test_json_path)
        print("train_df")
        print(train_df.head(3))
        print("test_df")
        print(test_df.head(3))
        print('train_df.shape={0}, test_df.shape={1}'.format(train_df.shape, test_df.shape) )

        train_df.head()
        df = pd.concat([train_df, test_df]).reset_index(drop=True)# 矩阵拼接
        df.head()

        #print(df['image'].sample().values, "\n",#
        #      df['objects'].sample().values)
        df["checksum"] = df['image'].apply(lambda x: x["checksum"])
        df["pathname"] = df['image'].apply(lambda x: x["pathname"][1:])
        df["shape"] = df['image'].apply(lambda x: x["shape"])

        df = pd.DataFrame(
            [
             dict(pathname=row['pathname'], 
                  shape=row['shape'],
                  checksum=row['checksum'],
                  **bb_info) 
             for _, row in df.iterrows() 
             for bb_info in row['objects']
             ]
             )


        df['x_min'] = -1
        df['y_min'] = -1
        df['x_max'] = -1
        df['y_max'] = -1

        df[['y_min', 'x_min', 'y_max', 'x_max']] = np.stack(df['bounding_box'].apply(lambda x: np.array(list(extract_nested_list(x)))))
        df.drop(columns=['bounding_box'], inplace=True)
        df['x_min'] = df['x_min'].astype(np.float)
        df['y_min'] = df['y_min'].astype(np.float)
        df['x_max'] = df['x_max'].astype(np.float)
        df['y_max'] = df['y_max'].astype(np.float)

        df['w'] = df['x_max'] - df['x_min']
        df['h'] = df['y_max'] - df['y_min']

        df['x_center'] = df['x_min'] + df['w'] / 2
        df['y_center'] = df['y_min'] + df['h'] / 2

        df['img_width'] = -1
        df['img_height'] = -1
        df['channels'] = -1
        df['pixels'] = -1

        df[['img_height','img_width', 'channels']] = np.stack(df['shape'].apply(lambda x: np.array(list(extract_nested_list(x)))))
        df.drop(columns=['shape'], inplace=True)
        df['pixels'] = df['img_width'] * df['img_height'] * df['channels']

        cat_dict = {v:k for k,v in enumerate(df['category'].value_counts().index, 0)}
        df["label"] = df["category"].map(cat_dict)

        df['w_yolo'] = df[['w', 'img_width']].apply(lambda x: x[0] / x[1], axis=1)
        df['h_yolo'] = df[['h', 'img_height']].apply(lambda x: x[0] / x[1], axis=1)
        df['x_center_yolo'] = df[['x_center', 'img_width']].apply(lambda x: x[0] / x[1], axis=1)
        df['y_center_yolo'] = df[['y_center', 'img_height']].apply(lambda x: x[0] / x[1], axis=1)

        yolov5_df = df.copy()
        yolov5_df = yolov5_df[yolov5_df["pathname"].apply(lambda x: x[-4:] == '.png')].reset_index(drop=True)
        yolov5_df["name"] = yolov5_df["pathname"].apply(lambda x: x.split("/")[-1].split(".")[0])



        index = list(set(yolov5_df.name))

        source = "images"
        if True:
            for fold in [0]:
                val_index = index[len(index)*fold//5:len(index)*(fold+1)//5]
                for name, mini in tqdm(yolov5_df.groupby('name')):
                    if name in val_index:
                        path2save = 'val2017/'
                        #print("val")
                    else:
                        path2save = 'train2017/'
                    if not os.path.exists('convertor/fold{}/labels/'.format(fold)+path2save):
                        os.makedirs('convertor/fold{}/labels/'.format(fold)+path2save)
                    with open('convertor/fold{}/labels/'.format(fold)+path2save+name+".txt", 'w+') as f:
                        row = mini[['label','x_center_yolo', 'y_center_yolo', 'w_yolo', 'h_yolo']].astype(float).values
                        #print(row)
                        #row = row[0:]/1024
                        row = row.astype(str)
                        for j in range(len(row)):
                            text = ' '.join(row[j])
                            f.write(text)
                            f.write("\n")
                    if not os.path.exists('convertor/fold{}/images/{}'.format(fold,path2save)):
                        os.makedirs('convertor/fold{}/images/{}'.format(fold,path2save))
                    sh.copy("malaria/{}/{}.png".format(source,name),'convertor/fold{}/images/{}/{}.png'.format(fold,path2save,name))

        fastercnn_df = df[['pathname','x_min', 'y_min', 'x_max', 'y_max','w', 'h', 'label', 'category']].copy()
        remap_labels = {0:1, 1:2, 2:3, 3:4, 4:5, 5:6, 6:7}
        remap_category = {v:k for v,k in enumerate(fastercnn_df['category'].value_counts().index, 1)} 
        fastercnn_df['label'] = fastercnn_df['label'].apply(lambda x: remap_labels[x])      # remap because 0 its bg
        fastercnn_df['category'] = fastercnn_df['label'].apply(lambda x: remap_category[x]) # remap because 0 its bg

        image_ids = fastercnn_df['pathname'].unique()
        train_ids, valid_ids = train_test_split(image_ids,test_size=0.12, shuffle=True, random_state=22)

        valid_df = fastercnn_df[fastercnn_df['pathname'].isin(valid_ids)].reset_index(drop=True)
        train_df = fastercnn_df[fastercnn_df['pathname'].isin(train_ids)].reset_index(drop=True)



        train_dataset = MalariaDataset(train_df, config.root_dir, get_train_transform())
        valid_dataset = MalariaDataset(valid_df, config.root_dir, get_valid_transform())


        # split the dataset in train and test set
        indices = torch.randperm(len(train_dataset)).tolist()

        train_data_loader = DataLoader(
            train_dataset,
            batch_size=12,
            shuffle=False,
            num_workers=4,
            collate_fn=collate_fn
        )

        valid_data_loader = DataLoader(
            valid_dataset,
            batch_size=8,
            shuffle=False,
            num_workers=4,
            collate_fn=collate_fn
        )

        images, targets, ids = next(iter(train_data_loader))

        label2rgb = {k:v for k, v in 
                       zip(fastercnn_df['label'].value_counts().index.tolist(), rgbcolors)}

        label2category = dict(zip(fastercnn_df['label'].value_counts().index.values, 
                                  fastercnn_df['category'].value_counts().index.values))

        model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=False)

        num_classes = 8  # 7 classes + background

        # get number of input features for the classifier
        in_features = model.roi_heads.box_predictor.cls_score.in_features

        # replace the pre-trained head with a new one
        model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

        # Load the trained weights
        #model.load_state_dict(torch.load('/content/drive/My Drive/fasterrcnn_resnet50_fpn_80_epoch.pth'))

        model.to('cuda')
        params = [p for p in model.parameters() if p.requires_grad]
        optimizer = torch.optim.SGD(params, lr=0.004, momentum=0.9, weight_decay=0.0005)
        lr_scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="min",
                                                   patience=3, verbose=True)
        #lr_scheduler = None

        num_epochs = 1

        loss_hist = Averager()
        itr = 1
        device= 'cuda'
        for epoch in range(num_epochs):
            loss_hist.reset()

            for images, targets, image_ids in train_data_loader:

                images = list(image.to(device) for image in images)
                targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

                loss_dict = model(images, targets)

                losses = sum(loss for loss in loss_dict.values())
                loss_value = losses.item()

                loss_hist.send(loss_value)

                optimizer.zero_grad()
                losses.backward()
                optimizer.step()

                if itr % 50 == 0:
                    print(f"Iteration #{itr} loss: {loss_value}")

                itr += 1

            # update the learning rate
            if lr_scheduler is not None:
                lr_scheduler.step(loss_hist.value)

            print(f"Epoch #{epoch} loss: {loss_hist.value}")

        jl.dump(model, os.path.join(pfold, 'model_fastrcnn_ep_{0}.jl'.format(num_epochs)))

        torch.save(model.state_dict(), config.fasterrcnn_weights)


        # Load the trained weights
        model.load_state_dict(torch.load(config.fasterrcnn_weights))
        model.eval()

        detection_threshold = 0.5
        results = []
        ids = []
        device = 'cuda'
        model.to(device)
        for images, targets, image_ids in valid_data_loader:

            images = list(image.to(device) for image in images)
            outputs = model(images)

            for i, image in enumerate(images):

                boxes = outputs[i]['boxes'].data.cpu().numpy()
                scores = outputs[i]['scores'].data.cpu().numpy()
                labels = outputs[i]['labels'].data.cpu().numpy()

                boxes = boxes[scores >= detection_threshold].astype(np.int32)
                scores = scores[scores >= detection_threshold]
                image_id = image_ids[i]

                result = format_prediction(boxes, scores, labels)
                id_ = [image_id] * result.shape[0]

                results.append(result)
                ids.append(id_)

        test_df = pd.DataFrame(np.concatenate(results, axis=0), columns=['score', "x_min", "y_min", "x_max", "y_max", 'label'])
        test_df['pathname'] = sum(ids, [])
        test_df['category'] = test_df['label'].apply(lambda x: label2category[x])


        jl.dump(test_df, os.path.join(pfold,'test_df_fastrcnn.jl'))
        jl.dump(valid_df,os.path.join(pfold,'valid_df_fastrcnn.jl'))

        hex2rgb = lambda hx: (int(hx[1:3],16),int(hx[3:5],16),int(hx[5:7],16))
        label2rgb = list(map(hex2rgb, custom_colors))[1:]
        label2rgb = {k:v for k, v in 
                       zip(fastercnn_df['category'].value_counts().index.tolist(), label2rgb)}
        label2hex = {k:v for k, v in 
                       zip(fastercnn_df['category'].value_counts().index.tolist(), custom_colors[1:])}


        test_df_fastrcn = jl.load( os.path.join(pfold,'test_df_fastrcnn.jl') )
        valid_df_fastrcnn = jl.load( os.path.join(pfold,'valid_df_fastrcnn.jl') )

        test_df_fastrcn.to_excel( os.path.join(pfold,'test_df_fastrcnn.jl.xlsx') )
        valid_df_fastrcnn.to_excel( os.path.join(pfold,'valid_df_fastrcnn.jl.xlsx') )
        gc.collect()
        torch.cuda.empty_cache()
    except Exception as e:
        gc.collect()
        torch.cuda.empty_cache()
        msg = traceback.format_exc()
        print( 'exception here: {0}'.format(msg) )

        
if __name__=='__main__':
    main()
        
        
        
        
        
        
        
        
        