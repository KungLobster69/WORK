import os
import json
import sys

K = 10


# iterate each fold
for i in range(K):
    print('start {0} of {1}'.format(i, K))
    
    
    # train model 
    os.system("python train.py  --img 512 --batch 12 --epochs 1 --data /home/project2/malaria/malaria_conf.yaml --cfg /home/project2/malaria/yolov5x.yaml --name yolov5x_malaria ")
    print('end {0} of {1}'.format(i, K))