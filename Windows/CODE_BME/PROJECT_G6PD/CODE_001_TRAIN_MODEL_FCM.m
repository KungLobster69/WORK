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
percentClusters_ABNORMAL = 50;
percentClusters_INTERMEDIATE = 50;
percentClusters_NORMAL = 50;
m = 2; % Fuzziness parameter
maxIter = 100; % จำนวนรอบสูงสุด
epsilon = 1e-5; % เกณฑการลู่เข้า

% เรียกใช้ Fuzzy C-Means สำหรับ ABNORMAL
disp('Processing ABNORMAL Dataset...');
[U_ABNORMAL, V_ABNORMAL, clusterLabels_ABNORMAL] = ...
fuzzyCMeans(ABNORMAL, percentClusters_ABNORMAL, m, maxIter, epsilon);

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
    fuzzyCMeans(INTERMEDIATE, percentClusters_INTERMEDIATE, m, maxIter, epsilon);

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
    fuzzyCMeans(NORMAL, percentClusters_NORMAL, m, maxIter, epsilon);

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
k_values = 1:19; % ค่า K ตั้งแต่ 1 ถึง 19
accuracy_KNN = zeros(length(k_values), 1); % เก็บผล Accuracy สำหรับ K-NN
accuracy_FuzzyKNN = zeros(length(k_values), 1); % เก็บผล Accuracy สำหรับ Fuzzy K-NN
predicted_KNN_all = cell(length(k_values), 1); % เก็บ Predicted Labels สำหรับ K-NN
predicted_FuzzyKNN_all = cell(length(k_values), 1); % เก็บ Predicted Labels สำหรับ Fuzzy K-NN

% พารามิเตอร์สำหรับ Fuzzy K-NN
m = 2; % Fuzziness parameter

for k = k_values
    % K-NN Classification
    predictedLabels_KNN = knnclassify(testData, trainData, trainLabels, k);
    accuracy_KNN(k) = sum(predictedLabels_KNN == testLabels) / length(testLabels) * 100;
    predicted_KNN_all{k} = predictedLabels_KNN; % เก็บ Predicted Labels
    
    % Fuzzy K-NN Classification
    predictedLabels_FuzzyKNN = fuzzyKNN(testData, trainData, trainLabels, k, m);
    accuracy_FuzzyKNN(k) = sum(predictedLabels_FuzzyKNN == testLabels) / length(testLabels) * 100;
    predicted_FuzzyKNN_all{k} = predictedLabels_FuzzyKNN; % เก็บ Predicted Labels
    
    % แสดงผล Predicted Labels สำหรับแต่ละ K
    disp(['For K = ', num2str(k), ':']);
    disp('K-NN Predicted Labels:');
    disp(predictedLabels_KNN');
    disp('Fuzzy K-NN Predicted Labels:');
    disp(predictedLabels_FuzzyKNN');
end

% Plot results
figure;
plot(k_values, accuracy_KNN, '-o', 'LineWidth', 1.5, 'DisplayName', 'K-NN Accuracy');
hold on;
plot(k_values, accuracy_FuzzyKNN, '-s', 'LineWidth', 1.5, 'DisplayName', 'Fuzzy K-NN Accuracy');
grid on;
xlabel('Number of Neighbors (K)');
ylabel('Accuracy (%)');
title('Accuracy vs K for K-NN and Fuzzy K-NN');
legend('show', 'Location', 'Best');