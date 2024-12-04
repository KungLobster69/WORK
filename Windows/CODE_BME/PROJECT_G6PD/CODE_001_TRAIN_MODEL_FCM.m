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

% พารามิเตอร์สำหรับ Fuzzy C-Means
m = 2; % Fuzziness parameter
maxIter = 100; % จำนวนรอบสูงสุด
epsilon = 1e-5; % เกณฑ์การลู่เข้า

% เรียกใช้ Fuzzy C-Means สำหรับ ABNORMAL
disp('Processing ABNORMAL Dataset...');
percentClusters_ABNORMAL = 50; % กำหนดเป็นเปอร์เซ็นต์
[U_ABNORMAL, V_ABNORMAL, clusterLabels_ABNORMAL] = ...
fuzzyCMeans(ABNORMAL, percentClusters_ABNORMAL, m, maxIter, epsilon);

% เรียกใช้ Fuzzy C-Means สำหรับ INTERMEDIATE
disp('Processing INTERMEDIATE Dataset...');
percentClusters_INTERMEDIATE = 50; % กำหนดเป็นเปอร์เซ็นต์
[U_INTERMEDIATE, V_INTERMEDIATE, clusterLabels_INTERMEDIATE] = ...
    fuzzyCMeans(INTERMEDIATE, percentClusters_INTERMEDIATE, m, maxIter, epsilon);

% เรียกใช้ Fuzzy C-Means สำหรับ NORMAL
disp('Processing NORMAL Dataset...');
percentClusters_NORMAL = 50; % กำหนดเป็นเปอร์เซ็นต์
[U_NORMAL, V_NORMAL, clusterLabels_NORMAL] = ...
    fuzzyCMeans(NORMAL, percentClusters_NORMAL, m, maxIter, epsilon);

% แสดงผล ABNORMAL
figure;
scatter3(ABNORMAL(:,1), ABNORMAL(:,2), ABNORMAL(:,3), 50, clusterLabels_ABNORMAL, 'filled');
hold on;
scatter3(V_ABNORMAL(:,1), V_ABNORMAL(:,2), V_ABNORMAL(:,3), 200, 'k', 'x', 'LineWidth', 3);
title('ABNORMAL Dataset');
xlabel('Feature 1');
ylabel('Feature 2');
zlabel('Feature 3');
grid on;

% แสดงผล INTERMEDIATE
figure;
scatter3(INTERMEDIATE(:,1), INTERMEDIATE(:,2), INTERMEDIATE(:,3), 50, clusterLabels_INTERMEDIATE, 'filled');
hold on;
scatter3(V_INTERMEDIATE(:,1), V_INTERMEDIATE(:,2), V_INTERMEDIATE(:,3), 200, 'k', 'x', 'LineWidth', 3);
title('INTERMEDIATE Dataset');
xlabel('Feature 1');
ylabel('Feature 2');
zlabel('Feature 3');
grid on;

% แสดงผล NORMAL
figure;
scatter3(NORMAL(:,1), NORMAL(:,2), NORMAL(:,3), 50, clusterLabels_NORMAL, 'filled');
hold on;
scatter3(V_NORMAL(:,1), V_NORMAL(:,2), V_NORMAL(:,3), 200, 'k', 'x', 'LineWidth', 3);
title('NORMAL Dataset');
xlabel('Feature 1');
ylabel('Feature 2');
zlabel('Feature 3');
grid on;