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

% พารามิเตอร์
percentClusters_ABNORMAL = 50; % ใช้ 10% ของข้อมูลเป็นจำนวนคลัสเตอร์
percentClusters_INTERMEDIATE = 50; % ใช้ 15% ของข้อมูลเป็นจำนวนคลัสเตอร์
percentClusters_NORMAL = 50; % ใช้ 20% ของข้อมูลเป็นจำนวนคลัสเตอร์
m = 2; % Fuzziness parameter
maxIter = 100; % จำนวนรอบสูงสุด
epsilon = 1e-5; % เกณฑ์การลู่เข้า

% GG Clustering สำหรับ ABNORMAL
disp('Processing ABNORMAL Dataset...');
[U_ABNORMAL, V_ABNORMAL, clusterLabels_ABNORMAL] = ...
    GGClustering(ABNORMAL, percentClusters_ABNORMAL, m, maxIter, epsilon);

% แสดงผล ABNORMAL
figure;
scatter3(ABNORMAL(:,1), ABNORMAL(:,2), ABNORMAL(:,3), 50, clusterLabels_ABNORMAL, 'filled');
hold on;
scatter3(V_ABNORMAL(:,1), V_ABNORMAL(:,2), V_ABNORMAL(:,3), 200, 'k', 'x', 'LineWidth', 3);
title('ABNORMAL Dataset (GG Clustering)');
xlabel('Feature 1');
ylabel('Feature 2');
zlabel('Feature 3');
grid on;

% GG Clustering สำหรับ INTERMEDIATE
disp('Processing INTERMEDIATE Dataset...');
[U_INTERMEDIATE, V_INTERMEDIATE, clusterLabels_INTERMEDIATE] = ...
    GGClustering(INTERMEDIATE, percentClusters_INTERMEDIATE, m, maxIter, epsilon);

% แสดงผล INTERMEDIATE
figure;
scatter3(INTERMEDIATE(:,1), INTERMEDIATE(:,2), INTERMEDIATE(:,3), 50, clusterLabels_INTERMEDIATE, 'filled');
hold on;
scatter3(V_INTERMEDIATE(:,1), V_INTERMEDIATE(:,2), V_INTERMEDIATE(:,3), 200, 'k', 'x', 'LineWidth', 3);
title('INTERMEDIATE Dataset (GG Clustering)');
xlabel('Feature 1');
ylabel('Feature 2');
zlabel('Feature 3');
grid on;

% GG Clustering สำหรับ NORMAL
disp('Processing NORMAL Dataset...');
[U_NORMAL, V_NORMAL, clusterLabels_NORMAL] = ...
    GGClustering(NORMAL, percentClusters_NORMAL, m, maxIter, epsilon);

% แสดงผล NORMAL
figure;
scatter3(NORMAL(:,1), NORMAL(:,2), NORMAL(:,3), 50, clusterLabels_NORMAL, 'filled');
hold on;
scatter3(V_NORMAL(:,1), V_NORMAL(:,2), V_NORMAL(:,3), 200, 'k', 'x', 'LineWidth', 3);
title('NORMAL Dataset (GG Clustering)');
xlabel('Feature 1');
ylabel('Feature 2');
zlabel('Feature 3');
grid on;