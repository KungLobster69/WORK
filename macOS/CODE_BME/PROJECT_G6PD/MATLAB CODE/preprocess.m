addpath('D:\G6PD\Dataset1\')
clear, clc
close all
areas = zeros(59,10);

for i=1:59
RGB = imread([num2str(i) '-5.png']);
[m,n,p] = size(RGB);
RGB_crop = imcrop(RGB,[n*.25 m*.25 800-1 350-1]);
RGB2 = imadjust(rgb2gray(RGB_crop));
% RGB2 = histeq(rgb2gray(RGB_crop),255);

YIQ = rgb2ntsc(RGB_crop);
YIQ_chanel = YIQ(:,:,1);
YIQ_pros = RGB2;

Lab = rgb2lab(RGB_crop);
Lab_chanel = Lab(:,:,1);
Lab_pros = Lab_chanel;

HSV = rgb2hsv(RGB_crop);
HSV_pros = HSV(:,:,3);

% ycbcr = rgb2ycbcr(RGB_crop);
% ycbcr_tm = ycbcr(:,:,3);
% % figure,imshow(ycbcr(:,:,3))
% img_cmyk = rgb2cmyk(RGB_crop);

% BW = ~(gray < 0.045); %Threshold for Y of YIQ color space
% BW = ~(gray < 0.1); %Threshold for Q of YIQ color space

% To seperate background and forground
% BW = ~(Lab_pros < 6); %Threshold for L of Lab color space
BW = ~(HSV_pros < 0.3); %Threshold for L of Lab color space

se = strel('disk',4);
BW = imclose(BW,se);
se = strel('cube',5);
BW = imclose(BW,se);
L = bwlabel(BW,4);
stats = regionprops(L,'Area','Centroid');
figure,subplot(3,2,2),imshow(BW,[]),title('forground'),hold on
for k=1:length(stats)
    if stats(k).Area < size(BW,1)*size(BW,2)*0.3
        BW(L==k) = 0;
    else
        areas(i,k) = stats(k).Area;
        
        plot(stats(k).Centroid(1),stats(k).Centroid(2),'rx')
    end

end

% now select only forground area
YIQ_pros(BW==0) = 0;
HSV_pros(BW==0) = 0;

%split paper into 2 pieces
[control_img,test_img] = split_paper(YIQ_pros,areas(i,:),stats);
%find adative threshold
TC = adaptive_threshold(control_img); 
TT = adaptive_threshold(test_img);

control_img(control_img ~= 0 & control_img < TC) = 255;
test_img(test_img ~= 0 & test_img > TT) = 255;


subplot(3,2,3),imshow(control_img,[]),title('YIQ control paper') 
subplot(3,2,4),imshow(test_img,[]),title('YIQ test paper')


subplot(3,2,1),imshow(RGB2,[]),title('Original')

[control_img1,test_img1] = split_paper(HSV_pros,areas(i,:),stats);
%find adative threshold
TC1 = adaptive_threshold(control_img1); 
TT1 = adaptive_threshold(test_img1);

control_img1(control_img1 ~= 0 & control_img1 < TC1) = 1;
test_img1(test_img1 ~=0 & test_img1 > TT1) = 1;

subplot(3,2,5),imshow(control_img1),title('HSV control paper') 
subplot(3,2,6),imshow(test_img1),title('HSV test paper')

end
