import argparse
import torch.backends.cudnn as cudnn
from models.experimental import *
from utils.datasets import *
from utils.utils import *

from flask import Flask, jsonify,request
import base64
import requests
import os
import json
import joblib as jl

models_path = 'weights/'

for f1 in os.listdir(models_path):
    f2 = os.path.join(models_path, f1)
    fold_num = int( f1.replace('last_yolov5x_malaria_','').replace('.pt','') )
    print(fold_num, f2)

    FOOD_CLASSES = ['gametocyte',
                    'red blood cell',
                    'ring',
                    'schizont',
                    'trophozoite',
                    'difficult', ]

    class_to_ind = dict(zip(FOOD_CLASSES, range(len(FOOD_CLASSES))))  # start from zero
    id_to_class = dict(zip(range(len(FOOD_CLASSES)), FOOD_CLASSES))

    conf_thres = 0.2
    iou_thres = 0.3


    out = 'outputs{0}'.format(fold_num)#'outputs'
    os.mkdir(out)
    source = 'convertor/fold{0}/images/val2017/'.format(fold_num)#'Test_img'
    weights = f2#'detect_weights/epoch_195.pt'
    imgsz = 640

    print('load img')

    with torch.no_grad():
        print('start detecting')

        # Initialize
        device = torch_utils.select_device('')

        half = device.type != 'cpu'  # half precision only supported on CUDA

        # Load model
        model = attempt_load(weights, map_location=device)  # load FP32 model
        imgsz = check_img_size(imgsz, s=model.stride.max())  # check img_size
        if half:
            model.half()  # to FP16

        # Second-stage classifier
        classify = True
        if classify:

            modelc = torch.load('classify_weights/cells_cls_v2.pt')
            modelc.to(device).eval()
            print('load done')
        #
        # Set Dataloader
        vid_path, vid_writer = None, None

        save_img = True
        dataset = LoadImages(source, img_size=imgsz)

        # Get names and colors

        names = id_to_class
        colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]

        # Run inference
        t0 = time.time()
        img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
        _ = model(img.half() if half else img) if device.type != 'cpu' else None  # run once

        image_to_cells_pred = {}
        for path, img, im0s, vid_cap in dataset:
            base_name = os.path.basename(path)
            image_to_cells_pred[base_name] = []

            img = torch.from_numpy(img).to(device)
            img = img.half() if half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # Inference
            pred = model(img)[0]
            print('pred={0}'.format(pred))
            # Apply NMS
            pred = non_max_suppression(pred, conf_thres, iou_thres)

            # Apply Classifier
            if classify:
                label_out = apply_classifier(pred, modelc, img, im0s)

                label_out = label_out.tolist()

            cnt_all_box = 0
            # Process detections
            for i, det in enumerate(pred):  # detections per image

                p, s, im0 = path, '', im0s

                save_path = str(Path(out) / Path(p).name)
                txt_path = str(Path(out) / Path(p).stem) + ('_%g' % dataset.frame if dataset.mode == 'video' else '')
                s += '%gx%g ' % img.shape[2:]  # print string
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                if det is not None and len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                    # Print results
                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        s += '%g %ss, ' % (n, id_to_class[int(c)])  # add to string

                        # Write results
                        # for *xyxy, conf, cls in det:
                        for k, (*xyxy, conf, cls) in enumerate(det):
                            print('cls={0}'.format(cls))
                            label = '%s %.2f' % (id_to_class[int(label_out[k])], conf)
                            cnt_all_box += 1
                            plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=3)
                            c1, c2 = (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3]))
                            #print("左上点的坐标为：(" + str(c1[0]) + "," + str(c1[1]) + ")，右下点的坐标为(" + str(c2[0]) + "," + str(c2[1]) + ")")
                            image_to_cells_pred[base_name].append( (c1[0],c1[1],c2[0],c2[1]) )

                    # Save results (image with detections)
                    if save_img:
                        cv2.imwrite(save_path, im0)


        jl.dump(image_to_cells_pred,'image_to_cells_pred_{0}.jl'.format(fold_num))

    print(cnt_all_box)    