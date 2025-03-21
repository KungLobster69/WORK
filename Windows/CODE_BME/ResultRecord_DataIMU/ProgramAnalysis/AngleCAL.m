clc
clear all
close all


% example >> https://www.andre-gaschler.com/rotationconverter/



%% Include Library

%addpath('ximu_matlab_library');	% include x-IMU MATLAB library
addpath('quaternion_library');	% include quatenrion library

%% Import data


importdata = 1;
if(importdata)
    clear('all');
    
    samplePeriod = 1/100; %(unit:sec)

    time = 0;
    gyr0 = struct('x',0,'y',0,'z',0);
    gyr1 = struct('x',0,'y',0,'z',0);
    gyr2 = struct('x',0,'y',0,'z',0);
    gyr3 = struct('x',0,'y',0,'z',0);
    
    acc0 = struct('x',0,'y',0,'z',0);
    acc1 = struct('x',0,'y',0,'z',0);
    acc2 = struct('x',0,'y',0,'z',0);
    acc3 = struct('x',0,'y',0,'z',0);
    
    mag0 = struct('x',0,'y',0,'z',0);
    mag1 = struct('x',0,'y',0,'z',0);
    mag2 = struct('x',0,'y',0,'z',0);
    mag3 = struct('x',0,'y',0,'z',0);

    lia0 = struct('x',0,'y',0,'z',0);
    lia1 = struct('x',0,'y',0,'z',0);
    lia2 = struct('x',0,'y',0,'z',0);
    lia3 = struct('x',0,'y',0,'z',0);
    
    quat0 = struct('w',0,'x',0,'y',0,'z',0);
    quat1 = struct('w',0,'x',0,'y',0,'z',0);
    quat2 = struct('w',0,'x',0,'y',0,'z',0);
    quat3 = struct('w',0,'x',0,'y',0,'z',0);
    
    
    fclose('all');
    filepath = "C:\Users\BMEI CMU\Documents\GitHub\WORK\Windows\CODE_BME\ResultRecord_DataIMU\";
%      filepath = filepath + "TestData20241223Left\"; % No1 
    %filepath = filepath + "TestData20241223Right\"; % No2
%      filepath = filepath + "TestData20250217Left\"; % No3
%     filepath = filepath + "TestData20250217Right\"; % No4
%      filepath = filepath + "TestData20250224Left\"; % No5
    filepath = filepath + "TestData20250224Right\"; % No6
%      filepath = filepath + "TestData20250225Left\"; % No7
%     filepath = filepath + "TestData20250225Right\"; % No8
%      filepath = filepath + "TestData20250226Left\"; % No9
%     filepath = filepath + "TestData20250226Right\"; % No10
    
    typepath = "Normal\";
%     typepath = "ACcut\";
%     typepath = "AC+CCcut\";
%     typepath = "RepairCCloop\";
%     typepath = "RepairDoubleButton\";
%     typepath = "RepairSingleButton\";
    
% %     openfile = "IMURecord_FF_0.csv";
    openfile = "IMURecord_FF_30.csv";
%     openfile = "IMURecord_FF_60.csv";
%     openfile = "IMURecord_FF_90.csv";
%     openfile = "IMURecord_FF_120.csv";
%     openfile = "IMURecord_FF_150.csv";
% %     openfile = "IMURecord_AB_0.csv";
%     openfile = "IMURecord_AB_30.csv";
%     openfile = "IMURecord_AB_60.csv";
%     openfile = "IMURecord_AB_90.csv";
%     openfile = "IMURecord_AB_120.csv";
%     openfile = "IMURecord_AB_150.csv";
% %     openfile = "IMURecord_AD_0.csv";
%     openfile = "IMURecord_AD_30.csv";
%     openfile = "IMURecord_AD_60.csv";


    fileID = fopen(filepath + typepath + openfile);
    headerline = fgetl(fileID); %header
    unitline = fgetl(fileID); %unit
    
    dataindex = 0;
    while(1)
        dataline = fgetl(fileID);
        dataindex = dataindex+1;
        %fprintf("read data %s[ %d ]\n", openfile, dataindex);
        
        C = strsplit(dataline,',');
        
        time(dataindex) = str2double(C{1});
        gyr0.x(dataindex) = str2double(C{2});
        gyr0.y(dataindex) = str2double(C{3});
        gyr0.z(dataindex) = str2double(C{4});
        acc0.x(dataindex) = str2double(C{5});
        acc0.y(dataindex) = str2double(C{6});
        acc0.z(dataindex) = str2double(C{7});
        mag0.x(dataindex) = str2double(C{8});
        mag0.y(dataindex) = str2double(C{9});
        mag0.z(dataindex) = str2double(C{10});
        lia0.x(dataindex) = str2double(C{11});
        lia0.y(dataindex) = str2double(C{12});
        lia0.z(dataindex) = str2double(C{13});
        quat0.w(dataindex) = str2double(C{14});
        quat0.x(dataindex) = str2double(C{15});
        quat0.y(dataindex) = str2double(C{16});
        quat0.z(dataindex) = str2double(C{17});
        
        gyr1.x(dataindex) = str2double(C{18});
        gyr1.y(dataindex) = str2double(C{19});
        gyr1.z(dataindex) = str2double(C{20});
        acc1.x(dataindex) = str2double(C{21});
        acc1.y(dataindex) = str2double(C{22});
        acc1.z(dataindex) = str2double(C{23});
        mag1.x(dataindex) = str2double(C{24});
        mag1.y(dataindex) = str2double(C{25});
        mag1.z(dataindex) = str2double(C{26});
        lia1.x(dataindex) = str2double(C{27});
        lia1.y(dataindex) = str2double(C{28});
        lia1.z(dataindex) = str2double(C{29});
        quat1.w(dataindex) = str2double(C{30});
        quat1.x(dataindex) = str2double(C{31});
        quat1.y(dataindex) = str2double(C{32});
        quat1.z(dataindex) = str2double(C{33});
        
        gyr2.x(dataindex) = str2double(C{34});
        gyr2.y(dataindex) = str2double(C{35});
        gyr2.z(dataindex) = str2double(C{36});
        acc2.x(dataindex) = str2double(C{37});
        acc2.y(dataindex) = str2double(C{38});
        acc2.z(dataindex) = str2double(C{39});
        mag2.x(dataindex) = str2double(C{40});
        mag2.y(dataindex) = str2double(C{41});
        mag2.z(dataindex) = str2double(C{42});
        lia2.x(dataindex) = str2double(C{43});
        lia2.y(dataindex) = str2double(C{44});
        lia2.z(dataindex) = str2double(C{45});
        quat2.w(dataindex) = str2double(C{46});
        quat2.x(dataindex) = str2double(C{47});
        quat2.y(dataindex) = str2double(C{48});
        quat2.z(dataindex) = str2double(C{49});
        
        gyr3.x(dataindex) = str2double(C{50});
        gyr3.y(dataindex) = str2double(C{51});
        gyr3.z(dataindex) = str2double(C{52});
        acc3.x(dataindex) = str2double(C{53});
        acc3.y(dataindex) = str2double(C{54});
        acc3.z(dataindex) = str2double(C{55});
        mag3.x(dataindex) = str2double(C{56});
        mag3.y(dataindex) = str2double(C{57});
        mag3.z(dataindex) = str2double(C{58});
        lia3.x(dataindex) = str2double(C{59});
        lia3.y(dataindex) = str2double(C{60});
        lia3.z(dataindex) = str2double(C{61});
        quat3.w(dataindex) = str2double(C{62});
        quat3.x(dataindex) = str2double(C{63});
        quat3.y(dataindex) = str2double(C{64});
        quat3.z(dataindex) = str2double(C{65});

        if(feof(fileID))
            fprintf("read data %s%s[ %d ]\n", typepath,openfile, dataindex);
            break;
        end
    end
    fclose(fileID);
    
    time = time - time(1);
    framesize = size(time',1);
    
    
    
    %<=>%Debug plot
%     figure("Name","Debug plot (Raw Data)");
%     hold('on');
%     plot(time,gyr0.x, time,gyr0.y, time,gyr0.z);
%     plot(time,acc0.x, time,acc0.y, time,acc0.z);
%     %plot(time,lia0.x, time,lia0.y, time,lia0.z);
%     %plot(time,quat0.w, time,quat0.x, time,quat0.y, time,quat0.z);
%     plot(time,gyr1.x, time,gyr1.y, time,gyr1.z);
%     plot(time,acc1.x, time,acc1.y, time,acc1.z);
%     %plot(time,lia1.x, time,lia1.y, time,lia1.z);
%     %plot(time,quat1.w, time,quat1.x, time,quat1.y, time,quat1.z);
%     plot(time,gyr2.x, time,gyr2.y, time,gyr2.z);
%     plot(time,acc2.x, time,acc2.y, time,acc2.z);
%     %plot(time,lia2.x, time,lia2.y, time,lia2.z);
%     %plot(time,quat2.w, time,quat2.x, time,quat2.y, time,quat2.z);
%     plot(time,gyr3.x, time,gyr3.y, time,gyr3.z);
%     plot(time,acc3.x, time,acc3.y, time,acc3.z);
%     %plot(time,lia3.x, time,lia3.y, time,lia3.z);
%     %plot(time,quat3.w, time,quat3.x, time,quat3.y, time,quat3.z);
%     hold('off');
    
end

%% Quaternion to Rotation Matrix
 %-%quaternion to its conjugate
 
rotm0 = quatern2rotMat([quat0.w',quat0.x',quat0.y',quat0.z']);
rotm1 = quatern2rotMat([quat1.w',quat1.x',quat1.y',quat1.z']);
rotm2 = quatern2rotMat([quat2.w',quat2.x',quat2.y',quat2.z']);
rotm3 = quatern2rotMat([quat3.w',quat3.x',quat3.y',quat3.z']);

% fprintf("rotm0[%d]\n", size(rotm0,3));
% fprintf("rotm1[%d]\n", size(rotm1,3));
% fprintf("rotm2[%d]\n", size(rotm2,3));
% fprintf("rotm3[%d]\n", size(rotm3,3));

%% Offset Rotation Matrix

x1 = [1, 0, 0];
y1 = [0, 1, 0];
z1 = [0, 0, 1];

x0 = [ rotm0(1,1,1), rotm0(2,1,1), rotm0(3,1,1) ];
y0 = [ rotm0(1,2,1), rotm0(2,2,1), rotm0(3,2,1) ];
z0 = [ rotm0(1,3,1), rotm0(2,3,1) ,rotm0(3,3,1) ];
R0_01 = [dot(x1,x0),dot(y1,x0),dot(z1,x0);
         dot(x1,y0),dot(y1,y0),dot(z1,y0);
         dot(x1,z0),dot(y1,z0),dot(z1,z0)];
     
x0 = [ rotm1(1,1,1), rotm1(2,1,1), rotm1(3,1,1) ];
y0 = [ rotm1(1,2,1), rotm1(2,2,1), rotm1(3,2,1) ];
z0 = [ rotm1(1,3,1), rotm1(2,3,1) ,rotm1(3,3,1) ];
R1_01 = [dot(x1,x0), dot(y1,x0), dot(z1,x0);
         dot(x1,y0), dot(y1,y0), dot(z1,y0);
         dot(x1,z0), dot(y1,z0), dot(z1,z0)];

x0 = [ rotm2(1,1,1), rotm2(2,1,1), rotm2(3,1,1) ];
y0 = [ rotm2(1,2,1), rotm2(2,2,1), rotm2(3,2,1) ];
z0 = [ rotm2(1,3,1), rotm2(2,3,1) ,rotm2(3,3,1) ];
R2_01 = [dot(x1,x0), dot(y1,x0), dot(z1,x0);
         dot(x1,y0), dot(y1,y0), dot(z1,y0);
         dot(x1,z0), dot(y1,z0), dot(z1,z0)];

x0 = [ rotm3(1,1,1), rotm3(2,1,1), rotm3(3,1,1) ];
y0 = [ rotm3(1,2,1), rotm3(2,2,1), rotm3(3,2,1) ];
z0 = [ rotm3(1,3,1), rotm3(2,3,1) ,rotm3(3,3,1) ];
R3_01 = [dot(x1,x0), dot(y1,x0), dot(z1,x0);
         dot(x1,y0), dot(y1,y0), dot(z1,y0);
         dot(x1,z0), dot(y1,z0), dot(z1,z0)];

for(n = [1:size(time',1)])   
rotm0(:,:,n) = R0_01*rotm0(:,:,n);   
rotm1(:,:,n) = R1_01*rotm1(:,:,n);  
rotm2(:,:,n) = R2_01*rotm2(:,:,n);  
rotm3(:,:,n) = R3_01*rotm3(:,:,n);
end





%% Setup figure and plot

simulation = 0;
if(simulation)
o0 = [0 0 0];
o1 = [-0.5 0.5 0];
o2 = [0 1 0];
o3 = [0.5 0.5 0];

% Create figure
fig = figure('NumberTitle', 'off', 'Name', '6DOF Animation');
ax = axes(fig);

hold("on");
framei = framesize-1;
qXhandle(1) = quiver3(o0(1),o0(2),o0(3), rotm0(1,1,framei),rotm0(2,1,framei),rotm0(3,1,framei), "r-");
qYhandle(1) = quiver3(o0(1),o0(2),o0(3), rotm0(1,2,framei),rotm0(2,2,framei),rotm0(3,2,framei), "g-");
qZhandle(1) = quiver3(o0(1),o0(2),o0(3), rotm0(1,3,framei),rotm0(2,3,framei),rotm0(3,3,framei), "b-");
qXhandle(2) = quiver3(o1(1),o1(2),o1(3), rotm1(1,1,framei),rotm1(2,1,framei),rotm1(3,1,framei), "r:");
qYhandle(2) = quiver3(o1(1),o1(2),o1(3), rotm1(1,2,framei),rotm1(2,2,framei),rotm1(3,2,framei), "g:");
qZhandle(2) = quiver3(o1(1),o1(2),o1(3), rotm1(1,3,framei),rotm1(2,3,framei),rotm1(3,3,framei), "b:");
qXhandle(3) = quiver3(o2(1),o2(2),o2(3), rotm2(1,1,framei),rotm2(2,1,framei),rotm2(3,1,framei), "r--");
qYhandle(3) = quiver3(o2(1),o2(2),o2(3), rotm2(1,2,framei),rotm2(2,2,framei),rotm2(3,2,framei), "g--");
qZhandle(3) = quiver3(o2(1),o2(2),o2(3), rotm2(1,3,framei),rotm2(2,3,framei),rotm2(3,3,framei), "b--");
qXhandle(4) = quiver3(o3(1),o3(2),o3(3), rotm3(1,1,framei),rotm3(2,1,framei),rotm3(3,1,framei), "r-.");
qYhandle(4) = quiver3(o3(1),o3(2),o3(3), rotm3(1,2,framei),rotm3(2,2,framei),rotm3(3,2,framei), "g-.");
qZhandle(4) = quiver3(o3(1),o3(2),o3(3), rotm3(1,3,framei),rotm3(2,3,framei),rotm3(3,3,framei), "b-.");
hold("off");

view([1 1 1]);
axis("equal");
grid("on");


Xlim = [-2, 2];
Ylim = [-2, 2];
Zlim = [-2, 2];
set(gca, 'Xlim', Xlim, 'Ylim', Ylim, 'Zlim', Zlim);



SamplePlotFreq = 20;
for(i = [1:SamplePlotFreq:framesize])
    titleText = sprintf("Sample %i of %i", i, framesize);
    title(titleText);
    
    set(qXhandle(1), 'XData',o0(1),'YData',o0(2),'ZData',o0(3), 'UData',rotm0(1,1,i), 'VData',rotm0(2,1,i), 'WData',rotm0(3,1,i));
    set(qYhandle(1), 'XData',o0(1),'YData',o0(2),'ZData',o0(3), 'UData',rotm0(1,2,i), 'VData',rotm0(2,2,i), 'WData',rotm0(3,2,i));
    set(qZhandle(1), 'XData',o0(1),'YData',o0(2),'ZData',o0(3), 'UData',rotm0(1,3,i), 'VData',rotm0(2,3,i), 'WData',rotm0(3,3,i));
    
    set(qXhandle(2), 'XData',o1(1),'YData',o1(2),'ZData',o1(3), 'UData',rotm1(1,1,i), 'VData',rotm1(2,1,i), 'WData',rotm1(3,1,i));
    set(qYhandle(2), 'XData',o1(1),'YData',o1(2),'ZData',o1(3), 'UData',rotm1(1,2,i), 'VData',rotm1(2,2,i), 'WData',rotm1(3,2,i));
    set(qZhandle(2), 'XData',o1(1),'YData',o1(2),'ZData',o1(3), 'UData',rotm1(1,3,i), 'VData',rotm1(2,3,i), 'WData',rotm1(3,3,i));
    
    set(qXhandle(3), 'XData',o2(1),'YData',o2(2),'ZData',o2(3), 'UData',rotm2(1,1,i), 'VData',rotm2(2,1,i), 'WData',rotm2(3,1,i));
    set(qYhandle(3), 'XData',o2(1),'YData',o2(2),'ZData',o2(3), 'UData',rotm2(1,2,i), 'VData',rotm2(2,2,i), 'WData',rotm2(3,2,i));
    set(qZhandle(3), 'XData',o2(1),'YData',o2(2),'ZData',o2(3), 'UData',rotm2(1,3,i), 'VData',rotm2(2,3,i), 'WData',rotm2(3,3,i));
        
    set(qXhandle(4), 'XData',o3(1),'YData',o3(2),'ZData',o3(3), 'UData',rotm3(1,1,i), 'VData',rotm3(2,1,i), 'WData',rotm3(3,1,i));
    set(qYhandle(4), 'XData',o3(1),'YData',o3(2),'ZData',o3(3), 'UData',rotm3(1,2,i), 'VData',rotm3(2,2,i), 'WData',rotm3(3,2,i));
    set(qZhandle(4), 'XData',o3(1),'YData',o3(2),'ZData',o3(3), 'UData',rotm3(1,3,i), 'VData',rotm3(2,3,i), 'WData',rotm3(3,3,i));
    
    drawnow;
    %pause(0.1);
end
end





%% Calculation angle plane
result_anglePlot = 1;
if(result_anglePlot)
%-%note 0 : Spin
%       1 : Clavicle
%       2 : Humerus
%       3 : Scapula bone

eul0 = rotm2eul(rotm0,"XYZ");
eul1 = rotm2eul(rotm1,"XYZ");
eul2 = rotm2eul(rotm2,"XYZ");
eul3 = rotm2eul(rotm3,"XYZ");

% eul0 = rotm2eul(rotm0,"ZYX");
% eul1 = rotm2eul(rotm1,"ZYX");
% eul2 = rotm2eul(rotm2,"ZYX");
% eul3 = rotm2eul(rotm3,"ZYX");

eul0 = rad2deg(eul0);
eul1 = rad2deg(eul1);
eul2 = rad2deg(eul2);
eul3 = rad2deg(eul3);




global selectedAction sheet xlRange;
selectedAction = typepath;

fliename = strsplit(filepath,'\');
fliename = fliename{end-1};
switch fliename
    case("TestData20241223Left")
        sheet = "No1 20241223Left";
        disp(sheet);
    case("TestData20241223Right") 
        sheet = "No2 20241223Right";
        disp(sheet);
    case("TestData20250217Left") 
        sheet = "No3 20250217Left";
        disp(sheet);
    case("TestData20250217Right") 
        sheet = "No4 20250217Right";
        disp(sheet);
    case("TestData20250224Left") 
        sheet = "No5 20250224Left";
        disp(sheet);
    case("TestData20250224Right") 
        sheet = "No6 20250224Right";
        disp(sheet);
    case("TestData20250225Left") 
        sheet = "No7 20250225Left";
        disp(sheet);
    case("TestData20250225Right") 
        sheet = "No8 20250225Right";
        disp(sheet);
    case("TestData20250226Left") 
        sheet = "No9 20250226Left";
        disp(sheet);
    case("TestData20250226Right") 
        sheet = "No10 20250226Right";
        disp(sheet);
end





fig0 = figure('NumberTitle', 'off', 'Name', 'Reference', 'Position', [50, 50, 800, 600]);
ax0 = axes('Parent', fig0);
plot(ax0, time,eul0(:,1),'r', time,eul0(:,2),'g', time,eul0(:,3),'b')

fig1 = figure('NumberTitle', 'off', 'Name', 'Clavicle');
ax1 = axes('Parent', fig1);
plot(time,eul1(:,1),'r', time,eul1(:,2),'g', time,eul1(:,3),'b')

fig2 = figure('NumberTitle', 'off', 'Name', 'Humerus');
ax2 = axes('Parent', fig2);
plot(time,eul2(:,1),'r', time,eul2(:,2),'g', time,eul2(:,3),'b')

fig3 = figure('NumberTitle', 'off', 'Name', 'Scapula');
ax3 = axes('Parent', fig3);
plot(time,eul3(:,1),'r', time,eul3(:,2),'g', time,eul3(:,3),'b')



interactive_signal_picker(fig0);
interactive_signal_picker(fig1);
interactive_signal_picker(fig2);
interactive_signal_picker(fig3);

end




