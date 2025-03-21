clc;
clear all;
close all;

% โหลดชื่อชีตทั้งหมดจากไฟล์ Excel
filePath = 'C:\Users\KUNG_LOBSTER69\Documents\GitHub\WORK\Windows\CODE_BME\ResultRecord_DataIMU\Result IMU.xlsx';
sheetList = sheetnames(filePath);

% รายชื่อประเภทการทดลอง
trialTypes = {"Normal", "ACcut", "AC_CCcut", "Repair_CCloop", "Repair_DoubleButton", "Repair_SingleButton"};
% รายชื่อท่าทาง
motions = {"ForwardFlexion", "Abduction", "Adduction"};
% องศาที่ต้องอ่านของแต่ละท่าทาง
degreesMap.ForwardFlexion = [30, 60, 90, 120, 150];
degreesMap.Abduction = [30, 60, 90, 120, 150];
degreesMap.Adduction = [30, 60];

% คอลัมน์ที่ใช้
columns.Sternoclavicular = {'J','O'};
columns.Scapulothoracic = {'P','U'};

% แถวเริ่มต้นของแต่ละประเภทและท่าทาง
rowBase.Normal.ForwardFlexion = 30;
rowBase.ACcut.ForwardFlexion = 49;
rowBase.AC_CCcut.ForwardFlexion = 68;
rowBase.Repair_CCloop.ForwardFlexion = 87;
rowBase.Repair_DoubleButton.ForwardFlexion = 106;
rowBase.Repair_SingleButton.ForwardFlexion = 125;

rowBase.Normal.Abduction = 37;
rowBase.ACcut.Abduction = 56;
rowBase.AC_CCcut.Abduction = 75;
rowBase.Repair_CCloop.Abduction = 94;
rowBase.Repair_DoubleButton.Abduction = 113;
rowBase.Repair_SingleButton.Abduction = 132;

rowBase.Normal.Adduction = 44;
rowBase.ACcut.Adduction = 63;
rowBase.AC_CCcut.Adduction = 82;
rowBase.Repair_CCloop.Adduction = 101;
rowBase.Repair_DoubleButton.Adduction = 120;
rowBase.Repair_SingleButton.Adduction = 139;

% เตรียมตัวแปรสำหรับเก็บข้อมูล
AllData = struct();

% ลูปแต่ละชีต
for i = 3:length(sheetList)
    sheetName = sheetList{i};
    fieldName = matlab.lang.makeValidName(sheetName);

    for t = 1:length(trialTypes)
        trial = trialTypes{t};

        for m = 1:length(motions)
            motion = motions{m};
            baseRow = rowBase.(trial).(motion);
            degrees = degreesMap.(motion);

            for d = 1:length(degrees)
                deg = degrees(d);
                row = baseRow + d - 1;

                % สร้าง range string
                sternRange = sprintf('%s%d:%s%d', columns.Sternoclavicular{1}, row, columns.Sternoclavicular{2}, row);
                scapRange  = sprintf('%s%d:%s%d', columns.Scapulothoracic{1}, row, columns.Scapulothoracic{2}, row);

                % อ่านข้อมูล
                sternData = readmatrix(filePath, 'Sheet', sheetName, 'Range', sternRange);
                scapData = readmatrix(filePath, 'Sheet', sheetName, 'Range', scapRange);

                % เก็บข้อมูล
                AllData.(fieldName).(trial).(motion).Sternoclavicular.("deg"+deg) = sternData;
                AllData.(fieldName).(trial).(motion).Scapulothoracic.("deg"+deg) = scapData;
            end
        end
    end

    % แสดงชื่อชีต
    fprintf('==== Processing Sheet: %s ====\n', sheetName);
    disp(AllData.(fieldName));
end
