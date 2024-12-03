addpath('D:\G6PD\Dataset1\')
clear, clc
close all
areas = zeros(59,10);

for i=1:59
RGB = imread([num2str(i) '-5.png']);
[m,n,p] = size(RGB);
RGB_crop = imcrop(RGB,[n*.25 m*.25 800-1 350-1]);
% RGB2 = imadjust(rgb2gray(RGB_crop));
% RGB2 = histeq(rgb2gray(RGB_crop),255);

YIQ = rgb2ntsc(RGB_crop);
YIQ_chanel = YIQ(:,:,3); %use Q of YIQ
YIQ_pros = YIQ_chanel;
% YIQ_pros = imadjust(YIQ_pros);
Green_pros = RGB_crop(:,:,2);

% figure,
% subplot(2,2,1),imshow(RGB_crop),title(['Patient' num2str(i) ' 5 minutes'])
% subplot(2,2,2),imshow(RGB_crop1),title(['Patient' num2str(i) ' 5 minutes'])
% subplot(2,2,3),imshow(RGB_crop(:,:,2)),title(['Patient' num2str(i) ' 5 minutes'])
% subplot(2,2,4),imshow(RGB_crop1(:,:,2)),title(['Patient' num2str(i) ' 15 minutes'])

%BG Segment
HSV = rgb2hsv(RGB_crop);
HSV_pros = HSV(:,:,3);
BW = ~(HSV_pros < 0.3); %Threshold for L of Lab color space
se = strel('disk',4);
BW = imclose(BW,se);
se = strel('cube',5);
BW = imclose(BW,se);
L = bwlabel(BW,4);
stats = regionprops(L,'Area','Centroid');
figure,subplot(3,2,2),imshow(BW),title('forground'),hold on
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
Green_pros(BW==0) = 0;

%split paper into 2 pieces
[control_img,test_img] = split_paper(YIQ_pros,areas(i,:),stats);
[control_area, test_area] = split_paper(Green_pros,areas(i,:),stats);

%adjust image
control_img = imadjust(control_img);
test_img = imadjust(test_img);

%find adative threshold
TC = adaptive_threshold(control_img); 
TT = adaptive_threshold(test_img);

%select only blood areas
% control_img(control_img ~= 0 & control_img < TC) = 255;
% test_img(test_img ~= 0 & test_img > TT) = 255;
control_img(control_img ~= 0 & control_img < TC) = 1;
control_img(control_img ~= 1) = 0;
test_img(test_img ~= 0 & test_img < TT) = 1;
test_img(test_img ~= 1) = 0;

subplot(3,2,3),imshow(control_img,[]),title('YIQ control paper') 
subplot(3,2,4),imshow(test_img,[]),title('YIQ test paper')
subplot(3,2,1),imshow(YIQ_pros),title(['patient ' num2str(i)] )

% Morphology on blood control
% se = strel('line',10,90);
se = strel('cube',5);
BW_control = imdilate(control_img,se);
se = strel('diamond',5);
BW_control = imerode(BW_control,se);
% se = strel("line",len,deg) 

% select the biggest area by assumption that is the blood control area
L = bwlabel(control_img,4);
stats = regionprops(L,'Area','Centroid');
struct2cell(stats);
[I,idx]=max(cell2mat(ans(1,:)));
control_img(L~=idx) = 0;

% for k=1:length(stats)
%     if stats(k).Area < size(control_img,1)*size(control_img,2)*0.1
%         control_img(L==k) = 0;
%     end
% end
subplot(3,2,5),imshow(control_img),title('morphology control paper') 


% Morphology on blood test
se = strel('disk',4);
BW_test = imclose(test_img,se);
se = strel('cube',5);
BW_test = imerode(BW_test,se);

% select the biggest area by assumption that is the blood test area
L = bwlabel(test_img,4);
stats = regionprops(L,'Area','Centroid');
struct2cell(stats);
[I,idx]=max(cell2mat(ans(1,:)));
test_img(L~=idx) = 0;


subplot(3,2,6),imshow(test_img),title('morphology test paper')

nCT = find(control_img~=0);
control_img(nCT) = control_area(nCT);

nTT = find(test_img~=0);
test_img(nTT) = test_area(nTT);

Mean_control = sum(sum(control_img(nCT)))/length(nCT);
var_control = std(control_img(nCT));
Mean_test = sum(sum(test_img(nTT)))/length(nTT);
var_test = std(test_img(nTT));
results(i,:) = [Mean_control,var_control,Mean_test,var_test];

end
