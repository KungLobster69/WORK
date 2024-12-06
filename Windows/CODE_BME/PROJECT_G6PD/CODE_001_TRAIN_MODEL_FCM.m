clc
clear
close all

load('C:\Users\BMEI CMU\Documents\G6PD\YGH.mat');

% สร้างตัวแปรสำหรับเก็บ mean และ variance
meanValues = zeros(1, size(YGH_Color, 2));
varianceValues = zeros(1, size(YGH_Color, 2));

% คำนวณ mean และ variance พร้อมสร้าง YGH_NORMALIZE
for SIZE_CUL = 1:size(YGH_Color, 2)
    meanValues(SIZE_CUL) = mean(YGH_Color(:, SIZE_CUL)); 
    varianceValues(SIZE_CUL) = var(YGH_Color(:, SIZE_CUL)); 
    
    for SIZE_ROW = 1:size(YGH_Color, 1)
        YGH_NORMALIZE(SIZE_ROW, SIZE_CUL) = ...
            (YGH_Color(SIZE_ROW, SIZE_CUL) - meanValues(SIZE_CUL)) / varianceValues(SIZE_CUL);
    end
end

ABNORMAL = YGH_NORMALIZE(1:11,:);
INTERMEDIATE = YGH_NORMALIZE(12:17,:);
NORMAL = YGH_NORMALIZE(17:59,:);

% พารามิเตอร
Clusters_ABNORMAL = 6;
Clusters_INTERMEDIATE = 6;
Clusters_NORMAL = 6;
m = 2; % Fuzziness parameter
maxIter = 100; % จำนวนรอบสูงสุด
epsilon = 1e-5; % เกณฑการลู่เข้า

% เรียกใช้ Fuzzy C-Means สำหรับ ABNORMAL
disp('Processing ABNORMAL Dataset...');
[U_ABNORMAL, V_ABNORMAL, clusterLabels_ABNORMAL] = ...
fuzzyCMeans(ABNORMAL, Clusters_ABNORMAL, m, maxIter, epsilon);

% % แสดงผล ABNORMAL
% figure;
% scatter3(ABNORMAL(:,1), ABNORMAL(:,2), ABNORMAL(:,3), 50, clusterLabels_ABNORMAL, 'filled');
% hold on;
% % ปรับขนาดของกากบาทให้เล็กลง
% scatter3(V_ABNORMAL(:,1), V_ABNORMAL(:,2), V_ABNORMAL(:,3), 50, 'k', 'x', 'LineWidth', 1.5);
% title('ABNORMAL Dataset');
% xlabel('Feature 1');
% ylabel('Feature 2');
% zlabel('Feature 3');
% grid on;


% เรียกใช้ Fuzzy C-Means สำหรับ INTERMEDIATE
disp('Processing INTERMEDIATE Dataset...');
[U_INTERMEDIATE, V_INTERMEDIATE, clusterLabels_INTERMEDIATE] = ...
    fuzzyCMeans(INTERMEDIATE, Clusters_INTERMEDIATE, m, maxIter, epsilon);

% % แสดงผล INTERMEDIATE
% figure;
% scatter3(INTERMEDIATE(:,1), INTERMEDIATE(:,2), INTERMEDIATE(:,3), 50, clusterLabels_INTERMEDIATE, 'filled');
% hold on;
% % ปรับขนาดของกากบาทให้เล็กลง
% scatter3(V_INTERMEDIATE(:,1), V_INTERMEDIATE(:,2), V_INTERMEDIATE(:,3), 50, 'k', 'x', 'LineWidth', 1.5);
% title('INTERMEDIATE Dataset');
% xlabel('Feature 1');
% ylabel('Feature 2');
% zlabel('Feature 3');
% grid on;

% เรียกใช้ Fuzzy C-Means สำหรับ NORMAL
disp('Processing NORMAL Dataset...');
[U_NORMAL, V_NORMAL, clusterLabels_NORMAL] = ...
    fuzzyCMeans(NORMAL, Clusters_NORMAL, m, maxIter, epsilon);

% % แสดงผล NORMAL
% figure;
% scatter3(NORMAL(:,1), NORMAL(:,2), NORMAL(:,3), 50, clusterLabels_NORMAL, 'filled');
% hold on;
% % ปรับขนาดของกากบาทให้เล็กลง
% scatter3(V_NORMAL(:,1), V_NORMAL(:,2), V_NORMAL(:,3), 50, 'k', 'x', 'LineWidth', 1.5);
% title('NORMAL Dataset');
% xlabel('Feature 1');
% ylabel('Feature 2');
% zlabel('Feature 3');
% grid on;

% สร้าง labels สำหรับ ABNORMAL
label_ABNORMAL = ones(size(V_ABNORMAL, 1), 1); % กำหนด label = 1

% สร้าง labels สำหรับ INTERMEDIATE
label_INTERMEDIATE = 2 * ones(size(V_INTERMEDIATE, 1), 1); % กำหนด label = 2

% สร้าง labels สำหรับ NORMAL
label_NORMAL = 3 * ones(size(V_NORMAL, 1), 1); % กำหนด label = 3

% รวม labels ทั้งหมด (หากต้องการ)
all_labels = [label_ABNORMAL; label_INTERMEDIATE; label_NORMAL];
all_Models = [V_ABNORMAL; V_INTERMEDIATE; V_NORMAL];

% TEST Models
load('C:\Users\BMEI CMU\Documents\G6PD\YGH_TEST.mat');

% ตรวจสอบว่าข้อมูลที่โหลดมามีขนาดตรงกับ meanValues และ varianceValues หรือไม่
if size(YGHTEST, 2) ~= length(meanValues)
    error('The number of columns in YGH_TEST does not match the number of columns in YGH_Color.');
end

% ทำการ Normalize ข้อมูล YGH_TEST
YGHTEST_NORMALIZE = zeros(size(YGHTEST)); % เตรียมเมทริกซ์สำหรับเก็บผลลัพธ์
for SIZE_CUL = 1:size(YGHTEST, 2)
    for SIZE_ROW = 1:size(YGHTEST, 1)
        YGHTEST_NORMALIZE(SIZE_ROW, SIZE_CUL) = ...
            (YGHTEST(SIZE_ROW, SIZE_CUL) - meanValues(SIZE_CUL)) / varianceValues(SIZE_CUL);
    end
end

% สร้าง label สำหรับ YGH_TEST_NORMALIZE
labels_YGHTEST = zeros(size(YGHTEST_NORMALIZE, 1), 1); 

% กำหนด label ตามช่วงแถว
labels_YGHTEST(1:11) = 1;
labels_YGHTEST(12:17) = 2;
labels_YGHTEST(18:end) = 3;

% Preparing the data
trainData = all_Models;          % ข้อมูล train
trainLabels = all_labels;        % label ของ train
testData = YGHTEST_NORMALIZE;   % ข้อมูล test
testLabels = labels_YGHTEST;    % label ของ test

% สร้างตัวแปรสำหรับเก็บค่า Accuracy และ Predicted Labels
k_values = 1:2:9; % ค่า K ตั้งแต่ 1 ถึง 9
accuracy_KNN = zeros(length(k_values), 1); % เก็บผล Accuracy สำหรับ K-NN
accuracy_FuzzyKNN = zeros(length(k_values), 1); % เก็บผล Accuracy สำหรับ Fuzzy K-NN

% พารามิเตอร์สำหรับ Fuzzy K-NN
m = 2; % Fuzziness parameter

for k_idx = 1:length(k_values)
    k = k_values(k_idx);
    
    % K-NN Classification
    predictedLabels_KNN = knnclassify(testData, trainData, trainLabels, k);
    cm_KNN = confusionmat(testLabels, predictedLabels_KNN); % Confusion Matrix
    accuracy_KNN(k_idx) = sum(diag(cm_KNN)) / sum(cm_KNN(:)) * 100; % Accuracy
    
    % Fuzzy K-NN Classification
    predictedLabels_FuzzyKNN = fuzzyKNN(testData, trainData, trainLabels, k, m);
    cm_FuzzyKNN = confusionmat(testLabels, predictedLabels_FuzzyKNN); % Confusion Matrix
    accuracy_FuzzyKNN(k_idx) = sum(diag(cm_FuzzyKNN)) / sum(cm_FuzzyKNN(:)) * 100; % Accuracy
end
% แสดงผลลัพธ์
fprintf('Accuracy for K-NN (k = %s):\n', mat2str(k_values));
disp(accuracy_KNN);

fprintf('Accuracy for Fuzzy K-NN (k = %s):\n', mat2str(k_values));
disp(accuracy_FuzzyKNN);