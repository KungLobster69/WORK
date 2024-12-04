clc
clear
close all

load('C:\Users\BMEI CMU\Documents\G6PD\YGH.mat');

for SIZE_CUL = 1:size(YGH_Color,2)
    for SIZE_ROW = 1:size(YGH_Color,1)
        YGH_NORMALIZE(SIZE_ROW,SIZE_CUL) = (YGH_Color(SIZE_ROW,SIZE_CUL)-mean(YGH_Color(:,SIZE_CUL)))/var(YGH_Color(:,SIZE_CUL));
    end
end

ABNORMAL = YGH_NORMALIZE(1:11,:);
INTERMEDIATE = YGH_NORMALIZE(12:17,:);
NORMAL = YGH_NORMALIZE(17:59,:);

