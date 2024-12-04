addpath('C:\Users\BMEI CMU\Documents\G6PD\Dataset\GT\')
addpath('C:\Users\BMEI CMU\Documents\G6PD\Dataset\')
clear, clc
close all
areas = zeros(59,10);
results = zeros(59,4);
for i=1%:59
    %% read image amd do some pre-process
    GT1 = imread([num2str(i) '-15.tif']); %rgb with ground truth
    RGB = imread([num2str(i) '-15.png']); %rgb without ground truth
    
    Color = rgb2ntsc(RGB); %xform 
    % Color = rgb2lab(RGB); %xform
    Color_channel = Color(:,:,1);
    % Color_channel = imadjust(Color_channel);

    [m,n,p] = size(RGB);
    GT1_crop = imcrop(GT1,[n*.25 m*.25 800-1 350-1]); %crop rgb with ground truth
    Color_crop = imcrop(Color_channel,[n*.25 m*.25 800-1 350-1]); %crop rgb without ground truth
    RGB_crop = imcrop(RGB,[n*.25 m*.25 800-1 350-1]); %crop rgb without ground truth
    canvas1 = zeros(size(GT1_crop,1),size(GT1_crop,2));

    %% Segment background out of others
    HSV = rgb2hsv(RGB_crop);
    HSV_pros = HSV(:,:,3);
    BW = ~(HSV_pros < 0.3); %Threshold for L of Lab color space
    se = strel('disk',4);
    BW = imclose(BW,se);
    se = strel('cube',5);
    BW = imclose(BW,se);
    L = bwlabel(BW,4);
    stats = regionprops(L,'Area','Centroid');
    % figure,subplot(3,2,2),imshow(BW,[]),title('forground'),hold on
    for k=1:length(stats)
        if stats(k).Area < size(BW,1)*size(BW,2)*0.3
            BW(L==k) = 0;
        else
            areas(i,k) = stats(k).Area;
            % plot(stats(k).Centroid(1),stats(k).Centroid(2),'rx')
        end
    end

    %% Segment GT Areas
    canvas1(GT1_crop(:,:,1) == 0 & GT1_crop(:,:,2) == 0 & GT1_crop(:,:,3) == 0) = 1;
    L = bwlabel(canvas1,4);
    statsGT = regionprops(L,'Area','Centroid');
    for k=1:length(statsGT)
        if statsGT(k).Area < 5000
            canvas1(L==k) = 0;
        end

    end
    canvas1(canvas1==1) = Color_crop(canvas1==1);
    
    %% split paper into 2 pieces
    [control_img,test_img] = split_paper(canvas1,areas(i,:),stats);

     nCT = find(control_img~=0);
     Mean_control = sum(sum(control_img))/length(nCT);
     var_control = var(control_img(nCT));

     nTT = find(test_img~=0);
     Mean_test = sum(sum(test_img))/length(nTT);
     var_test = var(test_img(nTT));
     results(i,:) = [Mean_control,var_control,Mean_test,var_test];


    figure,subplot(1,2,1),imshow(control_img,[]),title(num2str(Mean_control))
    % subplot(1,2,2),imshow(test_img,[]),title(num2str(Mean_test))
end