clc
clear
close all

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

filename = "C:\Users\KUNG_LOBSTER69\Documents\GitHub\WORK\Windows\CODE_BME\ResultRecord_DataIMU\Result IMU.xlsx";

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

dataIdx_all   = [1:2, 4:6, 13:15, 16:18, 19:21, 22:24, 25:27, 28:30];
dataIdx_left  = [1:2, 13:15, 19:21, 25:27];
dataIdx_right = [4:6, 16:18, 22:24, 28:30];


dataIdx = dataIdx_all;
% dataIdx = dataIdx_left;
% dataIdx = dataIdx_right;

angle = zeros(size(dataIdx,2),1);

y.FF_clavicle(1:6)=struct("x",zeros(size(dataIdx,2),1), "y",zeros(size(dataIdx,2),1), "z",zeros(size(dataIdx,2),1));
y.AB_clavicle(1:6)=struct("x",zeros(size(dataIdx,2),1), "y",zeros(size(dataIdx,2),1), "z",zeros(size(dataIdx,2),1));
y.AD_clavicle(1:6)=struct("x",zeros(size(dataIdx,2),1), "y",zeros(size(dataIdx,2),1), "z",zeros(size(dataIdx,2),1));
y.FF_scapula(1:6)=struct("x",zeros(size(dataIdx,2),1), "y",zeros(size(dataIdx,2),1), "z",zeros(size(dataIdx,2),1));
y.AB_scapula(1:6)=struct("x",zeros(size(dataIdx,2),1), "y",zeros(size(dataIdx,2),1), "z",zeros(size(dataIdx,2),1));
y.AD_scapula(1:6)=struct("x",zeros(size(dataIdx,2),1), "y",zeros(size(dataIdx,2),1), "z",zeros(size(dataIdx,2),1));

for(k=[1:5])
    angle = [angle, k*30*ones(size(dataIdx,2),1)];
    axis = axis_x;
    y.FF_clavicle(1).x = [y.FF_clavicle(1).x, Condition(cond_Normal).FF(k).clavicleXYZ(dataIdx, axis)];
    y.FF_clavicle(2).x = [y.FF_clavicle(2).x, Condition(cond_ACcut).FF(k).clavicleXYZ(dataIdx, axis)];
    y.FF_clavicle(3).x = [y.FF_clavicle(3).x, Condition(cond_ACCCcut).FF(k).clavicleXYZ(dataIdx, axis)];
    y.FF_clavicle(4).x = [y.FF_clavicle(4).x, Condition(cond_RepairCC).FF(k).clavicleXYZ(dataIdx, axis)];
    y.FF_clavicle(5).x = [y.FF_clavicle(5).x, Condition(cond_RepairDouble).FF(k).clavicleXYZ(dataIdx, axis)];
    y.FF_clavicle(6).x = [y.FF_clavicle(6).x, Condition(cond_RepairSingle).FF(k).clavicleXYZ(dataIdx, axis)];
    axis = axis_y;
    y.FF_clavicle(1).y = [y.FF_clavicle(1).y, Condition(cond_Normal).FF(k).clavicleXYZ(dataIdx, axis)];
    y.FF_clavicle(2).y = [y.FF_clavicle(2).y, Condition(cond_ACcut).FF(k).clavicleXYZ(dataIdx, axis)];
    y.FF_clavicle(3).y = [y.FF_clavicle(3).y, Condition(cond_ACCCcut).FF(k).clavicleXYZ(dataIdx, axis)];
    y.FF_clavicle(4).y = [y.FF_clavicle(4).y, Condition(cond_RepairCC).FF(k).clavicleXYZ(dataIdx, axis)];
    y.FF_clavicle(5).y = [y.FF_clavicle(5).y, Condition(cond_RepairDouble).FF(k).clavicleXYZ(dataIdx, axis)];
    y.FF_clavicle(6).y = [y.FF_clavicle(6).y, Condition(cond_RepairSingle).FF(k).clavicleXYZ(dataIdx, axis)];
    axis = axis_z;
    y.FF_clavicle(1).z = [y.FF_clavicle(1).z, Condition(cond_Normal).FF(k).clavicleXYZ(dataIdx, axis)];
    y.FF_clavicle(2).z = [y.FF_clavicle(2).z, Condition(cond_ACcut).FF(k).clavicleXYZ(dataIdx, axis)];
    y.FF_clavicle(3).z = [y.FF_clavicle(3).z, Condition(cond_ACCCcut).FF(k).clavicleXYZ(dataIdx, axis)];
    y.FF_clavicle(4).z = [y.FF_clavicle(4).z, Condition(cond_RepairCC).FF(k).clavicleXYZ(dataIdx, axis)];
    y.FF_clavicle(5).z = [y.FF_clavicle(5).z, Condition(cond_RepairDouble).FF(k).clavicleXYZ(dataIdx, axis)];
    y.FF_clavicle(6).z = [y.FF_clavicle(6).z, Condition(cond_RepairSingle).FF(k).clavicleXYZ(dataIdx, axis)];

    axis = axis_x;
    y.FF_scapula(1).x = [y.FF_scapula(1).x, Condition(cond_Normal).FF(k).scapulaXYZ(dataIdx, axis)];
    y.FF_scapula(2).x = [y.FF_scapula(2).x, Condition(cond_ACcut).FF(k).scapulaXYZ(dataIdx, axis)];
    y.FF_scapula(3).x = [y.FF_scapula(3).x, Condition(cond_ACCCcut).FF(k).scapulaXYZ(dataIdx, axis)];
    y.FF_scapula(4).x = [y.FF_scapula(4).x, Condition(cond_RepairCC).FF(k).scapulaXYZ(dataIdx, axis)];
    y.FF_scapula(5).x = [y.FF_scapula(5).x, Condition(cond_RepairDouble).FF(k).scapulaXYZ(dataIdx, axis)];
    y.FF_scapula(6).x = [y.FF_scapula(6).x, Condition(cond_RepairSingle).FF(k).scapulaXYZ(dataIdx, axis)];
    axis = axis_y;
    y.FF_scapula(1).y = [y.FF_scapula(1).y, Condition(cond_Normal).FF(k).scapulaXYZ(dataIdx, axis)];
    y.FF_scapula(2).y = [y.FF_scapula(2).y, Condition(cond_ACcut).FF(k).scapulaXYZ(dataIdx, axis)];
    y.FF_scapula(3).y = [y.FF_scapula(3).y, Condition(cond_ACCCcut).FF(k).scapulaXYZ(dataIdx, axis)];
    y.FF_scapula(4).y = [y.FF_scapula(4).y, Condition(cond_RepairCC).FF(k).scapulaXYZ(dataIdx, axis)];
    y.FF_scapula(5).y = [y.FF_scapula(5).y, Condition(cond_RepairDouble).FF(k).scapulaXYZ(dataIdx, axis)];
    y.FF_scapula(6).y = [y.FF_scapula(6).y, Condition(cond_RepairSingle).FF(k).scapulaXYZ(dataIdx, axis)];
    axis = axis_z;
    y.FF_scapula(1).z = [y.FF_scapula(1).z, Condition(cond_Normal).FF(k).scapulaXYZ(dataIdx, axis)];
    y.FF_scapula(2).z = [y.FF_scapula(2).z, Condition(cond_ACcut).FF(k).scapulaXYZ(dataIdx, axis)];
    y.FF_scapula(3).z = [y.FF_scapula(3).z, Condition(cond_ACCCcut).FF(k).scapulaXYZ(dataIdx, axis)];
    y.FF_scapula(4).z = [y.FF_scapula(4).z, Condition(cond_RepairCC).FF(k).scapulaXYZ(dataIdx, axis)];
    y.FF_scapula(5).z = [y.FF_scapula(5).z, Condition(cond_RepairDouble).FF(k).scapulaXYZ(dataIdx, axis)];
    y.FF_scapula(6).z = [y.FF_scapula(6).z, Condition(cond_RepairSingle).FF(k).scapulaXYZ(dataIdx, axis)];

    axis = axis_x;
    y.AB_clavicle(1).x = [y.AB_clavicle(1).x, Condition(cond_Normal).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AB_clavicle(2).x = [y.AB_clavicle(2).x, Condition(cond_ACcut).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AB_clavicle(3).x = [y.AB_clavicle(3).x, Condition(cond_ACCCcut).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AB_clavicle(4).x = [y.AB_clavicle(4).x, Condition(cond_RepairCC).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AB_clavicle(5).x = [y.AB_clavicle(5).x, Condition(cond_RepairDouble).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AB_clavicle(6).x = [y.AB_clavicle(6).x, Condition(cond_RepairSingle).FF(k).clavicleXYZ(dataIdx, axis)];
    axis = axis_y;
    y.AB_clavicle(1).y = [y.AB_clavicle(1).y, Condition(cond_Normal).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AB_clavicle(2).y = [y.AB_clavicle(2).y, Condition(cond_ACcut).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AB_clavicle(3).y = [y.AB_clavicle(3).y, Condition(cond_ACCCcut).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AB_clavicle(4).y = [y.AB_clavicle(4).y, Condition(cond_RepairCC).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AB_clavicle(5).y = [y.AB_clavicle(5).y, Condition(cond_RepairDouble).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AB_clavicle(6).y = [y.AB_clavicle(6).y, Condition(cond_RepairSingle).FF(k).clavicleXYZ(dataIdx, axis)];
    axis = axis_z;
    y.AB_clavicle(1).z = [y.AB_clavicle(1).z, Condition(cond_Normal).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AB_clavicle(2).z = [y.AB_clavicle(2).z, Condition(cond_ACcut).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AB_clavicle(3).z = [y.AB_clavicle(3).z, Condition(cond_ACCCcut).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AB_clavicle(4).z = [y.AB_clavicle(4).z, Condition(cond_RepairCC).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AB_clavicle(5).z = [y.AB_clavicle(5).z, Condition(cond_RepairDouble).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AB_clavicle(6).z = [y.AB_clavicle(6).z, Condition(cond_RepairSingle).FF(k).clavicleXYZ(dataIdx, axis)];

    axis = axis_x;
    y.AB_scapula(1).x = [y.AB_scapula(1).x, Condition(cond_Normal).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AB_scapula(2).x = [y.AB_scapula(2).x, Condition(cond_ACcut).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AB_scapula(3).x = [y.AB_scapula(3).x, Condition(cond_ACCCcut).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AB_scapula(4).x = [y.AB_scapula(4).x, Condition(cond_RepairCC).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AB_scapula(5).x = [y.AB_scapula(5).x, Condition(cond_RepairDouble).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AB_scapula(6).x = [y.AB_scapula(6).x, Condition(cond_RepairSingle).FF(k).scapulaXYZ(dataIdx, axis)];
    axis = axis_y;
    y.AB_scapula(1).y = [y.AB_scapula(1).y, Condition(cond_Normal).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AB_scapula(2).y = [y.AB_scapula(2).y, Condition(cond_ACcut).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AB_scapula(3).y = [y.AB_scapula(3).y, Condition(cond_ACCCcut).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AB_scapula(4).y = [y.AB_scapula(4).y, Condition(cond_RepairCC).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AB_scapula(5).y = [y.AB_scapula(5).y, Condition(cond_RepairDouble).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AB_scapula(6).y = [y.AB_scapula(6).y, Condition(cond_RepairSingle).FF(k).scapulaXYZ(dataIdx, axis)];
    axis = axis_z;
    y.AB_scapula(1).z = [y.AB_scapula(1).z, Condition(cond_Normal).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AB_scapula(2).z = [y.AB_scapula(2).z, Condition(cond_ACcut).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AB_scapula(3).z = [y.AB_scapula(3).z, Condition(cond_ACCCcut).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AB_scapula(4).z = [y.AB_scapula(4).z, Condition(cond_RepairCC).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AB_scapula(5).z = [y.AB_scapula(5).z, Condition(cond_RepairDouble).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AB_scapula(6).z = [y.AB_scapula(6).z, Condition(cond_RepairSingle).FF(k).scapulaXYZ(dataIdx, axis)];

    axis = axis_x;
    y.AD_clavicle(1).x = [y.AD_clavicle(1).x, Condition(cond_Normal).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AD_clavicle(2).x = [y.AD_clavicle(2).x, Condition(cond_ACcut).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AD_clavicle(3).x = [y.AD_clavicle(3).x, Condition(cond_ACCCcut).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AD_clavicle(4).x = [y.AD_clavicle(4).x, Condition(cond_RepairCC).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AD_clavicle(5).x = [y.AD_clavicle(5).x, Condition(cond_RepairDouble).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AD_clavicle(6).x = [y.AD_clavicle(6).x, Condition(cond_RepairSingle).FF(k).clavicleXYZ(dataIdx, axis)];
    axis = axis_y;
    y.AD_clavicle(1).y = [y.AD_clavicle(1).y, Condition(cond_Normal).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AD_clavicle(2).y = [y.AD_clavicle(2).y, Condition(cond_ACcut).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AD_clavicle(3).y = [y.AD_clavicle(3).y, Condition(cond_ACCCcut).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AD_clavicle(4).y = [y.AD_clavicle(4).y, Condition(cond_RepairCC).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AD_clavicle(5).y = [y.AD_clavicle(5).y, Condition(cond_RepairDouble).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AD_clavicle(6).y = [y.AD_clavicle(6).y, Condition(cond_RepairSingle).FF(k).clavicleXYZ(dataIdx, axis)];
    axis = axis_z;
    y.AD_clavicle(1).z = [y.AD_clavicle(1).z, Condition(cond_Normal).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AD_clavicle(2).z = [y.AD_clavicle(2).z, Condition(cond_ACcut).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AD_clavicle(3).z = [y.AD_clavicle(3).z, Condition(cond_ACCCcut).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AD_clavicle(4).z = [y.AD_clavicle(4).z, Condition(cond_RepairCC).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AD_clavicle(5).z = [y.AD_clavicle(5).z, Condition(cond_RepairDouble).FF(k).clavicleXYZ(dataIdx, axis)];
    y.AD_clavicle(6).z = [y.AD_clavicle(6).z, Condition(cond_RepairSingle).FF(k).clavicleXYZ(dataIdx, axis)];

    axis = axis_x;
    y.AD_scapula(1).x = [y.AD_scapula(1).x, Condition(cond_Normal).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AD_scapula(2).x = [y.AD_scapula(2).x, Condition(cond_ACcut).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AD_scapula(3).x = [y.AD_scapula(3).x, Condition(cond_ACCCcut).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AD_scapula(4).x = [y.AD_scapula(4).x, Condition(cond_RepairCC).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AD_scapula(5).x = [y.AD_scapula(5).x, Condition(cond_RepairDouble).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AD_scapula(6).x = [y.AD_scapula(6).x, Condition(cond_RepairSingle).FF(k).scapulaXYZ(dataIdx, axis)];
    axis = axis_y;
    y.AD_scapula(1).y = [y.AD_scapula(1).y, Condition(cond_Normal).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AD_scapula(2).y = [y.AD_scapula(2).y, Condition(cond_ACcut).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AD_scapula(3).y = [y.AD_scapula(3).y, Condition(cond_ACCCcut).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AD_scapula(4).y = [y.AD_scapula(4).y, Condition(cond_RepairCC).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AD_scapula(5).y = [y.AD_scapula(5).y, Condition(cond_RepairDouble).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AD_scapula(6).y = [y.AD_scapula(6).y, Condition(cond_RepairSingle).FF(k).scapulaXYZ(dataIdx, axis)];
    axis = axis_z;
    y.AD_scapula(1).z = [y.AD_scapula(1).z, Condition(cond_Normal).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AD_scapula(2).z = [y.AD_scapula(2).z, Condition(cond_ACcut).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AD_scapula(3).z = [y.AD_scapula(3).z, Condition(cond_ACCCcut).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AD_scapula(4).z = [y.AD_scapula(4).z, Condition(cond_RepairCC).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AD_scapula(5).z = [y.AD_scapula(5).z, Condition(cond_RepairDouble).FF(k).scapulaXYZ(dataIdx, axis)];
    y.AD_scapula(6).z = [y.AD_scapula(6).z, Condition(cond_RepairSingle).FF(k).scapulaXYZ(dataIdx, axis)];
end
return;

%% -<Plot Result>- %%
clc;
close all;

nameplot = { "Normal", "AC cut", "AC+CC cut", "Repair CC", "Repair Double", "Repair Single" };
motionTypes = { "FF", "AB", "AD" };
boneTypes = { "clavicle", "scapula" };
anglelim = [-50, 50];
Linewidth = 2;
xRange = 0:150;

for m = 1:length(motionTypes)
    for b = 1:length(boneTypes)
        motion = motionTypes{m};
        bone = boneTypes{b};
        fieldName = sprintf('%s_%s', motion, bone);

        % เตรียม array สำหรับเก็บ curve
        clear yCurve_x yCurve_y yCurve_z
        
        for typeExp = 1:6
            Ax_data = y.(fieldName)(typeExp).x;
            Ay_data = y.(fieldName)(typeExp).y;
            Az_data = y.(fieldName)(typeExp).z;

            xFit = reshape(angle, [], 1);
            yFit_x = reshape(Ax_data, [], 1);
            yFit_y = reshape(Ay_data, [], 1);
            yFit_z = reshape(Az_data, [], 1);

            fitobject_x = fit(xFit, yFit_x, 'poly3');
            fitobject_y = fit(xFit, yFit_y, 'poly3');
            fitobject_z = fit(xFit, yFit_z, 'poly3');

            yCurve_x(typeExp,:) = fitobject_x(xRange)';
            yCurve_y(typeExp,:) = fitobject_y(xRange)';
            yCurve_z(typeExp,:) = fitobject_z(xRange)';
        end

        % Plot แยกรูปต่อแกน
        for axisName = ["X", "Y", "Z"]
            figure('Name', sprintf('%s - %s - Axis %s', motion, bone, axisName), 'NumberTitle', 'off');
            hold on;
            for i = 1:6
                switch axisName
                    case "X"
                        plot(xRange, yCurve_x(i,:), 'Color', colorRGB(i,:), 'LineWidth', Linewidth);
                    case "Y"
                        plot(xRange, yCurve_y(i,:), 'Color', colorRGB(i,:), 'LineWidth', Linewidth);
                    case "Z"
                        plot(xRange, yCurve_z(i,:), 'Color', colorRGB(i,:), 'LineWidth', Linewidth);
                end
            end
            title(sprintf('%s - %s - Axis %s', motion, bone, axisName));
            legend(nameplot, 'Location', 'southeast');
            ylim(anglelim);
            hold off;
        end
    end
end
