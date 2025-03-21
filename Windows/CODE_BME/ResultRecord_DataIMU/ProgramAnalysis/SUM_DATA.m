clc;
clear all;
close all;

% โหลดชื่อชีตทั้งหมดจากไฟล์ Excel
filePath = 'C:\Users\BMEI CMU\Documents\GitHub\WORK\Windows\CODE_BME\ResultRecord_DataIMU\Result IMU.xlsx';
sheetList = sheetnames(filePath);

% เตรียมตัวแปรสำหรับเก็บข้อมูล
NormalData = struct();
ACcutData = struct();

% ลูปตั้งแต่ชีตที่ 3 เป็นต้นไป
for i = 3%:length(sheetList)
    sheetName = sheetList{i};
    fieldName = matlab.lang.makeValidName(sheetName);

    % อ่านข้อมูล Normal: คอลัมน์ J ถึง O แถว 30 ถึง 34
    normalMatrix = readmatrix(filePath, 'Sheet', sheetName, 'Range', 'J30:O34');
    NormalData.(fieldName) = normalMatrix;

    % อ่านข้อมูล AC cut: คอลัมน์ J ถึง O แถว 49 ถึง 53
    accutMatrix = readmatrix(filePath, 'Sheet', sheetName, 'Range', 'J49:O53');
    ACcutData.(fieldName) = accutMatrix;

    % แสดงชื่อชีต
    fprintf('==== Processing Sheet: %s ====', sheetName);

    % แสดงข้อมูล Normal
    disp('Normal Data (J30:O34):');
    disp(normalMatrix);

    % แสดงข้อมูล AC cut
    disp('AC Cut Data (J49:O53):');
    disp(accutMatrix);
end
