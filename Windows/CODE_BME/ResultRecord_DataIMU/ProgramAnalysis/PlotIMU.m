clc
clear all
close all

cond_Normal   = 1;
cond_ACcut    = 2;
cond_ACCCcut  = 3;
cond_RepairCC = 4;
cond_RepairDouble = 5;
cond_RepairSingle = 6;

axis_x = 1;
axis_y = 2;
axis_z = 3;

angle_30 = 1;
angle_60 = 2;
angle_90 = 3;
angle_120 = 4;
angle_150 = 5;


colorRGB(1,:) = [0.0000,0.4470,0.7410];
colorRGB(2,:) = [0.8500,0.3250,0.0980];
colorRGB(3,:) = [0.9290,0.6940,0.1250];
colorRGB(4,:) = [0.4940,0.1840,0.5560];
colorRGB(5,:) = [0.4660,0.6740,0.1880];
colorRGB(6,:) = [0.3010,0.7450,0.9330];


importdata = 1;
if(importdata)
    for(cond=[1:6]) %=>[cond_Normal, cond_ACcut, cond_ACCCcut, cond_RepairCC, cond_RepairDouble, cond_RepairSingle]
        %-% angle 30
        Condition(cond).FF(1).humerus = [];
        Condition(cond).FF(1).clavicleXYZ = [];
        Condition(cond).FF(1).scapulaXYZ = [];
        %-% angle 60
        Condition(cond).FF(2).humerus = [];
        Condition(cond).FF(2).clavicleXYZ = [];
        Condition(cond).FF(2).scapulaXYZ = [];
        %-% angle 90
        Condition(cond).FF(3).humerus = [];
        Condition(cond).FF(3).clavicleXYZ = [];
        Condition(cond).FF(3).scapulaXYZ = [];
        %-% angle 120
        Condition(cond).FF(4).humerus = []';
        Condition(cond).FF(4).clavicleXYZ = [];
        Condition(cond).FF(4).scapulaXYZ = [];
        %-% angle 150
        Condition(cond).FF(5).humerus = [];
        Condition(cond).FF(5).clavicleXYZ = [];
        Condition(cond).FF(5).scapulaXYZ = [];

        %-% angle 30
        Condition(cond).AB(1).humerus = [];
        Condition(cond).AB(1).clavicleXYZ = [];
        Condition(cond).AB(1).scapulaXYZ = [];
        %-% angle 60
        Condition(cond).AB(2).humerus = [];
        Condition(cond).AB(2).clavicleXYZ = [];
        Condition(cond).AB(2).scapulaXYZ = [];
        %-% angle 90
        Condition(cond).AB(3).humerus = [];
        Condition(cond).AB(3).clavicleXYZ = [];
        Condition(cond).AB(3).scapulaXYZ = [];
        %-% angle 120
        Condition(cond).AB(4).humerus = [];
        Condition(cond).AB(4).clavicleXYZ = [];
        Condition(cond).AB(4).scapulaXYZ = [];
        %-% angle 150
        Condition(cond).AB(5).humerus = [];
        Condition(cond).AB(5).clavicleXYZ = [];
        Condition(cond).AB(5).scapulaXYZ = [];

        %-% angle 30
        Condition(cond).AD(1).humerus = [];
        Condition(cond).AD(1).clavicleXYZ = [];
        Condition(cond).AD(1).scapulaXYZ = [];
        %-% angle 60
        Condition(cond).AD(2).humerus = [];
        Condition(cond).AD(2).clavicleXYZ = [];
        Condition(cond).AD(2).scapulaXYZ = [];
    end

    filename = "C:\Users\BMEi\Documents\GitHub\WORK\Windows\CODE_BME\ResultRecord_DataIMU\Result IMU.xlsx";

    sheets{1} = "No1 20241223Left";
    sheets{2} = "No2 20241223Right";
    sheets{3} = "No3 20250217Left";
    sheets{4} = "No4 20250217Right";
    sheets{5} = "No5 20250224Left";
    sheets{6} = "No6 20250224Right";
    sheets{7} = "No7 20250225Left";
    sheets{8} = "No8 20250225Right";
    sheets{9} = "No9 20250226Left";
    sheets{10} = "No10 20250226Right";


    xlRanges{1,1} = "G29:AA34"; %Normal Forward Flexion
    xlRanges{1,2} = "G36:AA41"; %Normal Abduction
    xlRanges{1,3} = "G43:AA45"; %Normal Adduction

    xlRanges{2,1} = "G48:AA53"; %AC cut Forward Flexion
    xlRanges{2,2} = "G55:AA60"; %AC cut Abduction
    xlRanges{2,3} = "G62:AA64"; %AC cut Adduction

    xlRanges{3,1} = "G67:AA72"; %AC + CC cut Forward Flexion
    xlRanges{3,2} = "G74:AA79"; %AC + CC cut Abduction
    xlRanges{3,3} = "G81:AA83"; %AC + CC cut Adduction

    xlRanges{4,1} = "G86:AA91"; %Repair CC loop Forward Flexion
    xlRanges{4,2} = "G93:AA98"; %Repair CC loop Abduction
    xlRanges{4,3} = "G100:AA102"; %Repair CC loop Adduction

    xlRanges{5,1} = "G105:AA110"; %Repair Double Button Forward Flexion
    xlRanges{5,2} = "G112:AA117"; %Repair Double Button Abduction
    xlRanges{5,3} = "G119:AA121"; %Repair Double Button Adduction

    xlRanges{6,1} = "G124:AA129"; %Repair Single Button Forward Flexion
    xlRanges{6,2} = "G131:AA136"; %Repair Single Button Abduction
    xlRanges{6,3} = "G138:AA140"; %Repair Single Button Adduction

    for(sheetI = [1:10])
        sheet = sheets{sheetI};
        disp(sheet);

        for(xlRangeI=[1:6])

            %-%Forward Flexion
            xlRange = xlRanges{xlRangeI,1};
            [num,txt,raw1]=xlsread(filename, sheet, xlRange);
            num1 = cell2mat(raw1);
            for(k=[1:5])
                Condition(xlRangeI).FF(k).humerus = [Condition(xlRangeI).FF(k).humerus; num1(k+1,1:3)'];
                Condition(xlRangeI).FF(k).clavicleXYZ = [Condition(xlRangeI).FF(k).clavicleXYZ; [num1(k+1,10:12)', num1(k+1,7:9)', num1(k+1,4:6)']];
                Condition(xlRangeI).FF(k).scapulaXYZ = [Condition(xlRangeI).FF(k).scapulaXYZ; [num1(k+1,19:21)', num1(k+1,16:18)', num1(k+1,13:15)']];
            end



            %-%Abduction
            xlRange = xlRanges{xlRangeI,2};
            [num,txt,raw2]=xlsread(filename, sheet, xlRange);
            num2 = cell2mat(raw2);
            for(k=[1:5])
                Condition(xlRangeI).AB(k).humerus = [Condition(xlRangeI).AB(k).humerus; num2(k+1,1:3)'];
                Condition(xlRangeI).AB(k).clavicleXYZ = [Condition(xlRangeI).AB(k).clavicleXYZ; [num2(k+1,10:12)', num2(k+1,7:9)', num2(k+1,4:6)']];
                Condition(xlRangeI).AB(k).scapulaXYZ = [Condition(xlRangeI).AB(k).scapulaXYZ; [num2(k+1,19:21)', num2(k+1,16:18)', num2(k+1,13:15)']];
            end


            %-%Adduction
            xlRange = xlRanges{xlRangeI,3};
            [num,txt,raw3]=xlsread(filename, sheet, xlRange);
            num3 = cell2mat(raw3);
            for(k=[1:2])
                Condition(xlRangeI).AD(k).humerus = [Condition(xlRangeI).AD(k).humerus; num3(k+1,1:3)'];
                Condition(xlRangeI).AD(k).clavicleXYZ = [Condition(xlRangeI).AD(k).clavicleXYZ; [num3(k+1,10:12)', num3(k+1,7:9)', num3(k+1,4:6)']];
                Condition(xlRangeI).AD(k).scapulaXYZ = [Condition(xlRangeI).AD(k).scapulaXYZ; [num3(k+1,19:21)', num3(k+1,16:18)', num3(k+1,13:15)']];
            end
        end
    end

end


% return



%                % No1| No2| No3| No4|   No5|   No6|   No7|   No8|   No9|   No10
% dataIdx_all   = [1:3, 4:6, 7:9, 10:12, 13:15, 16:18, 19:21, 22:24, 25:27, 28:30];
% No1| No2| No5|   No6|   No7|   No8|   No9|   No10
dataIdx_all   = [1:2, 4:6, 13:15, 16:18, 19:21, 22:24, 25:27, 28:30];
dataIdx_left  = [1:2, 13:15, 19:21, 25:27];
dataIdx_right = [4:6, 16:18, 22:24, 28:30];


dataIdx = dataIdx_all;
% dataIdx = dataIdx_left;
% dataIdx = dataIdx_right;

angle_six = zeros(size(dataIdx,2),1);
angle_three = zeros(size(dataIdx,2),1);

y.FF_clavicle(1:6)=struct("x",zeros(size(dataIdx,2),1), "y",zeros(size(dataIdx,2),1), "z",zeros(size(dataIdx,2),1));
y.AB_clavicle(1:6)=struct("x",zeros(size(dataIdx,2),1), "y",zeros(size(dataIdx,2),1), "z",zeros(size(dataIdx,2),1));
y.AD_clavicle(1:6)=struct("x",zeros(size(dataIdx,2),1), "y",zeros(size(dataIdx,2),1), "z",zeros(size(dataIdx,2),1));
y.FF_scapula(1:6)=struct("x",zeros(size(dataIdx,2),1), "y",zeros(size(dataIdx,2),1), "z",zeros(size(dataIdx,2),1));
y.AB_scapula(1:6)=struct("x",zeros(size(dataIdx,2),1), "y",zeros(size(dataIdx,2),1), "z",zeros(size(dataIdx,2),1));
y.AD_scapula(1:6)=struct("x",zeros(size(dataIdx,2),1), "y",zeros(size(dataIdx,2),1), "z",zeros(size(dataIdx,2),1));

motionList = {'FF', 'AB', 'AD'};
segmentList = {'clavicle', 'scapula'};
axisList = {'x', 'y', 'z'};

for k = 1:5  % มุม 30 ถึง 150 องศา
    for m = 1:length(motionList)
        motion = motionList{m};
        for s = 1:length(segmentList)
            segment = segmentList{s};

            % ยกเว้น AD ที่มีแค่ 2 มุม
            if strcmp(motion, 'AD') && k > 2
                continue;
            end

            % เพิ่มมุมให้กับ angle_six หรือ angle_three
            if strcmp(motion, 'AD')
                angle_three = [angle_three, k*30*ones(size(dataIdx,2),1)];
            else
                angle_six = [angle_six, k*30*ones(size(dataIdx,2),1)];
            end

            % วนในแต่ละ condition
            for condIdx = 1:6
                for a = 1:length(axisList)
                    axisName = axisList{a};
                    axisNum = eval(['axis_' axisName]); % ใช้ตัวแปร axis_x, axis_y, axis_z

                    y.(motion + "_" + segment)(condIdx).(axisName) = ...
                        [y.(motion + "_" + segment)(condIdx).(axisName), ...
                         Condition(condIdx).(motion)(k).([segment 'XYZ'])(dataIdx, axisNum)];
                end
            end
        end
    end
end


% figure('Name', "Axis X");
% hold('on');
% for(exp=[1:size(dataIdx,2)])
% plot(angle(exp,:), y(1).x(exp,:), "Color",  colorRGB(1,:));
% plot(angle(exp,:), y(2).x(exp,:), "Color",  colorRGB(2,:));
% plot(angle(exp,:), y(3).x(exp,:), "Color",  colorRGB(3,:));
% plot(angle(exp,:), y(4).x(exp,:), "Color",  colorRGB(4,:));
% plot(angle(exp,:), y(5).x(exp,:), "Color",  colorRGB(5,:));
% plot(angle(exp,:), y(6).x(exp,:), "Color",  colorRGB(6,:));
% end
% fill([0,30,60,90,120,150,150,120,90,60,30,0],[min(y(1).x),fliplr(max(y(1).x))], colorRGB(1,:), "FaceAlpha",0.1, "EdgeColor","none");
% fill([0,30,60,90,120,150,150,120,90,60,30,0],[min(y(2).x),fliplr(max(y(2).x))], colorRGB(2,:), "FaceAlpha",0.1, "EdgeColor","none");
% hold('off');
% legend(nameplot, 'Location','eastoutside');
% title(nameplot{1});


% figure('Name', "Axis Y");
% hold('on');
% for(exp=[1:size(dataIdx,2)])
% plot(angle(exp,:), y(1).y(exp,:), "Color",  colorRGB(1,:));
% plot(angle(exp,:), y(2).y(exp,:), "Color",  colorRGB(2,:));
% plot(angle(exp,:), y(3).y(exp,:), "Color",  colorRGB(3,:));
% % plot(angle(exp,:), y(4).y(exp,:), "Color",  colorRGB(4,:));
% % plot(angle(exp,:), y(5).y(exp,:), "Color",  colorRGB(5,:));
% % plot(angle(exp,:), y(6).y(exp,:), "Color",  colorRGB(6,:));
% end
% hold('off');


% figure('Name', "Axis Z");
% hold('on');
% for(exp=[1:size(dataIdx,2)])
% plot(angle(exp,:), y(1).z(exp,:), "Color",  colorRGB(1,:));
% plot(angle(exp,:), y(2).z(exp,:), "Color",  colorRGB(2,:));
% plot(angle(exp,:), y(3).z(exp,:), "Color",  colorRGB(3,:));
% % plot(angle(exp,:), y(4).z(exp,:), "Color",  colorRGB(4,:));
% % plot(angle(exp,:), y(5).z(exp,:), "Color",  colorRGB(5,:));
% % plot(angle(exp,:), y(6).z(exp,:), "Color",  colorRGB(6,:));
% end
% hold('off');


return;

%% -<Plot Result>- %%
close all;

% กำหนดชื่อกลุ่มการทดลอง และ mapping กับตัวแปร cond_*
nameplot = { "Normal", "AC cut", "AC+CC cut", "Repair CC", "Repair Double", "Repair Single" };
typeExpList = [cond_Normal, cond_ACcut, cond_ACCCcut, cond_RepairCC, cond_RepairDouble, cond_RepairSingle];

anglelim = [-50 , 50];
Linewidth = 2;

motions = {'FF', 'AB', 'AD'};
segments = {'clavicle', 'scapula'};
axesList = {'x', 'y', 'z'};

for m = 1:length(motions)
    motion = motions{m};
    
    % เลือกมุมที่ใช้กับ motion นั้น ๆ
    if strcmp(motion, 'AD')
        angle = angle_three;
    else
        angle = angle_six;
    end
    
    for s = 1:length(segments)
        segment = segments{s};
        yCurve = struct('x', [], 'y', [], 'z', []);

        for a = 1:length(axesList)
            ax = axesList{a};

            for i = 1:length(typeExpList)
                typeExp = typeExpList(i);
                yData = y.(motion + "_" + segment)(typeExp).(ax);

                xFit = reshape(angle, [], 1);
                yFit = reshape(yData, [], 1);

                % เช็คขนาดข้อมูลก่อนใช้งาน
                if length(xFit) ~= length(yFit)
                    warning('%s - %s - Axis %s - Condition %d: angle (%d) ≠ yData (%d)', ...
                        motion, segment, ax, typeExp, length(xFit), length(yFit));
                    yCurve.(ax)(i, :) = nan(1, 151);
                    continue;
                end

                % กรอง NaN ออก
                validIdx = ~isnan(xFit) & ~isnan(yFit);
                xFit_valid = xFit(validIdx);
                yFit_valid = yFit(validIdx);

                % เช็คว่าข้อมูลพอสำหรับ poly3
                if numel(xFit_valid) >= 4
                    fitObject = fit(xFit_valid, yFit_valid, 'poly3');
                    yCurve.(ax)(i, :) = fitObject(0:150);
                else
                    yCurve.(ax)(i, :) = nan(1, 151);
                    warning('%s - %s - Axis %s - Condition %d: insufficient data for fitting', ...
                        motion, segment, ax, typeExp);
                end
            end

            % วาดกราฟของแกนนี้
            figure('Name', [motion, ' - ', segment, ' - Axis ', upper(ax)]);
            hold on;
            for i = 1:length(typeExpList)
                plot(0:150, yCurve.(ax)(i, :), ...
                    'Color', colorRGB(i,:), 'LineWidth', Linewidth);
            end
            hold off;
            title({motion, segment, ['Axis ', upper(ax)]});
            legend(nameplot(typeExpList), 'Location', 'eastoutside');
            ylim(anglelim);
        end
    end
end
