clc
clear all
close all

importdata = 1;
if(importdata)
    clear('all');

    for(cond=[1:6])
        for i = 1:5
            ConditionLeft(cond).FF(i).humerus = [];
            ConditionLeft(cond).FF(i).clavicleXYZ = [];
            ConditionLeft(cond).FF(i).scapulaXYZ = [];

            ConditionRight(cond).FF(i).humerus = [];
            ConditionRight(cond).FF(i).clavicleXYZ = [];
            ConditionRight(cond).FF(i).scapulaXYZ = [];

            ConditionLeft(cond).AB(i).humerus = [];
            ConditionLeft(cond).AB(i).clavicleXYZ = [];
            ConditionLeft(cond).AB(i).scapulaXYZ = [];

            ConditionRight(cond).AB(i).humerus = [];
            ConditionRight(cond).AB(i).clavicleXYZ = [];
            ConditionRight(cond).AB(i).scapulaXYZ = [];
        end

        for i = 1:2
            ConditionLeft(cond).AD(i).humerus = [];
            ConditionLeft(cond).AD(i).clavicleXYZ = [];
            ConditionLeft(cond).AD(i).scapulaXYZ = [];

            ConditionRight(cond).AD(i).humerus = [];
            ConditionRight(cond).AD(i).clavicleXYZ = [];
            ConditionRight(cond).AD(i).scapulaXYZ = [];
        end
    end

    filename = "C:\Users\BMEI CMU\Documents\GitHub\WORK\Windows\CODE_BME\ResultRecord_DataIMU\Result IMU.xlsx";

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

    xlRanges{1,1} = "G29:AA34";
    xlRanges{1,2} = "G36:AA41";
    xlRanges{1,3} = "G43:AA45";

    xlRanges{2,1} = "G48:AA53";
    xlRanges{2,2} = "G55:AA60";
    xlRanges{2,3} = "G62:AA64";

    xlRanges{3,1} = "G67:AA72";
    xlRanges{3,2} = "G74:AA79";
    xlRanges{3,3} = "G81:AA83";

    xlRanges{4,1} = "G86:AA91";
    xlRanges{4,2} = "G93:AA98";
    xlRanges{4,3} = "G100:AA102";

    xlRanges{5,1} = "G105:AA110";
    xlRanges{5,2} = "G112:AA117";
    xlRanges{5,3} = "G119:AA121";

    xlRanges{6,1} = "G124:AA129";
    xlRanges{6,2} = "G131:AA136";
    xlRanges{6,3} = "G138:AA140";

    for(sheetI = [1:10])
        sheet = sheets{sheetI};
        disp(sheet);

        if contains(sheet, 'Left')
            side = 'Left';
        else
            side = 'Right';
        end

        for(xlRangeI=[1:6])
            % Forward Flexion
            xlRange = xlRanges{xlRangeI,1};
            [~,~,raw1]=xlsread(filename, sheet, xlRange);
            num1 = cell2mat(raw1);
            for(k=[1:5])
                if strcmp(side, 'Left')
                    ConditionLeft(xlRangeI).FF(k).humerus = [ConditionLeft(xlRangeI).FF(k).humerus; num1(k+1,1:3)'];
                    ConditionLeft(xlRangeI).FF(k).clavicleXYZ = [ConditionLeft(xlRangeI).FF(k).clavicleXYZ; [num1(k+1,10:12)', num1(k+1,7:9)', num1(k+1,4:6)']];
                    ConditionLeft(xlRangeI).FF(k).scapulaXYZ = [ConditionLeft(xlRangeI).FF(k).scapulaXYZ; [num1(k+1,19:21)', num1(k+1,16:18)', num1(k+1,13:15)']];
                else
                    ConditionRight(xlRangeI).FF(k).humerus = [ConditionRight(xlRangeI).FF(k).humerus; num1(k+1,1:3)'];
                    ConditionRight(xlRangeI).FF(k).clavicleXYZ = [ConditionRight(xlRangeI).FF(k).clavicleXYZ; [num1(k+1,10:12)', num1(k+1,7:9)', num1(k+1,4:6)']];
                    ConditionRight(xlRangeI).FF(k).scapulaXYZ = [ConditionRight(xlRangeI).FF(k).scapulaXYZ; [num1(k+1,19:21)', num1(k+1,16:18)', num1(k+1,13:15)']];
                end
            end

            % Abduction
            xlRange = xlRanges{xlRangeI,2};
            [~,~,raw2]=xlsread(filename, sheet, xlRange);
            num2 = cell2mat(raw2);
            for(k=[1:5])
                if strcmp(side, 'Left')
                    ConditionLeft(xlRangeI).AB(k).humerus = [ConditionLeft(xlRangeI).AB(k).humerus; num2(k+1,1:3)'];
                    ConditionLeft(xlRangeI).AB(k).clavicleXYZ = [ConditionLeft(xlRangeI).AB(k).clavicleXYZ; [num2(k+1,10:12)', num2(k+1,7:9)', num2(k+1,4:6)']];
                    ConditionLeft(xlRangeI).AB(k).scapulaXYZ = [ConditionLeft(xlRangeI).AB(k).scapulaXYZ; [num2(k+1,19:21)', num2(k+1,16:18)', num2(k+1,13:15)']];
                else
                    ConditionRight(xlRangeI).AB(k).humerus = [ConditionRight(xlRangeI).AB(k).humerus; num2(k+1,1:3)'];
                    ConditionRight(xlRangeI).AB(k).clavicleXYZ = [ConditionRight(xlRangeI).AB(k).clavicleXYZ; [num2(k+1,10:12)', num2(k+1,7:9)', num2(k+1,4:6)']];
                    ConditionRight(xlRangeI).AB(k).scapulaXYZ = [ConditionRight(xlRangeI).AB(k).scapulaXYZ; [num2(k+1,19:21)', num2(k+1,16:18)', num2(k+1,13:15)']];
                end
            end

            % Adduction
            xlRange = xlRanges{xlRangeI,3};
            [~,~,raw3]=xlsread(filename, sheet, xlRange);
            num3 = cell2mat(raw3);
            for(k=[1:2])
                if strcmp(side, 'Left')
                    ConditionLeft(xlRangeI).AD(k).humerus = [ConditionLeft(xlRangeI).AD(k).humerus; num3(k+1,1:3)'];
                    ConditionLeft(xlRangeI).AD(k).clavicleXYZ = [ConditionLeft(xlRangeI).AD(k).clavicleXYZ; [num3(k+1,10:12)', num3(k+1,7:9)', num3(k+1,4:6)']];
                    ConditionLeft(xlRangeI).AD(k).scapulaXYZ = [ConditionLeft(xlRangeI).AD(k).scapulaXYZ; [num3(k+1,19:21)', num3(k+1,16:18)', num3(k+1,13:15)']];
                else
                    ConditionRight(xlRangeI).AD(k).humerus = [ConditionRight(xlRangeI).AD(k).humerus; num3(k+1,1:3)'];
                    ConditionRight(xlRangeI).AD(k).clavicleXYZ = [ConditionRight(xlRangeI).AD(k).clavicleXYZ; [num3(k+1,10:12)', num3(k+1,7:9)', num3(k+1,4:6)']];
                    ConditionRight(xlRangeI).AD(k).scapulaXYZ = [ConditionRight(xlRangeI).AD(k).scapulaXYZ; [num3(k+1,19:21)', num3(k+1,16:18)', num3(k+1,13:15)']];
                end
            end
        end
    end
end

close all;

nameplot{1} = "Normal";
nameplot{2} = "AC cut";
nameplot{3} = "AC+CC cut";
nameplot{4} = "Repair CC loop";
nameplot{5} = "Repair Double Button";
nameplot{6} = "Repair Single Button";

%--- Plot LEFT
for(cond = 1:6)
    figure('Name', ['Left - ' char(nameplot{cond})]);
    hold on;
    for(k = 1:5)
        angle = k * 30;
        n = size(ConditionLeft(cond).FF(k).scapulaXYZ, 1);
        scatter(angle * ones(n,1), ConditionLeft(cond).FF(k).scapulaXYZ(:,1), 'r');
        scatter(angle * ones(n,1), ConditionLeft(cond).FF(k).scapulaXYZ(:,2), 'g');
        scatter(angle * ones(n,1), ConditionLeft(cond).FF(k).scapulaXYZ(:,3), 'b');
    end
    title(['Left scapulaXYZ - ' char(nameplot{cond})]);
end

%--- Plot RIGHT
for(cond = 1:6)
    figure('Name', ['Right - ' char(nameplot{cond})]);
    hold on;
    for(k = 1:5)
        angle = k * 30;
        n = size(ConditionRight(cond).FF(k).scapulaXYZ, 1);
        scatter(angle * ones(n,1), ConditionRight(cond).FF(k).scapulaXYZ(:,1), 'r');
        scatter(angle * ones(n,1), ConditionRight(cond).FF(k).scapulaXYZ(:,2), 'g');
        scatter(angle * ones(n,1), ConditionRight(cond).FF(k).scapulaXYZ(:,3), 'b');
    end
    title(['Right scapulaXYZ - ' char(nameplot{cond})]);
end
