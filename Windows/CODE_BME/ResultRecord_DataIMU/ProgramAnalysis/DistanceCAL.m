close("all");
clc;


% example >> https://www.andre-gaschler.com/rotationconverter/
% Kalman Filter for 1D Motion with Acceleration and Bias


%% Include Library

%addpath('ximu_matlab_library');	% include x-IMU MATLAB library
addpath('quaternion_library');	% include quatenrion library

%% Import data


importdata = 0;
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
    filepath = "F:\Working_BIOMED\022023_LoadingTester_DSom\ResultRecord_DataIMU\TestData20241223Left\";
    typepath = "Normal\";
    %typepath = "ACcut\";
    %typepath = "AC+CCcut\";
    %typepath = "RepairCCloop\";
    %typepath = "RepairDoubleButton\";
    %typepath = "RepairSingleButton\";
    
    %filename = {"IMURecord_FF_0.csv","IMURecord_FF_30.csv","IMURecord_FF_60.csv","IMURecord_FF_90t2.csv","IMURecord_FF_120.csv","IMURecord_FF_150.csv"};
    filename = {"IMURecord_AB_0.csv","IMURecord_AB_30.csv","IMURecord_AB_60.csv","IMURecord_AB_90.csv","IMURecord_AB_120.csv","IMURecord_AB_150.csv"};
    %filename = {"IMURecord_AD_0.csv","IMURecord_AD_30.csv","IMURecord_AD_60.csv"};

    openfile = filename{2}; %[2:6]------
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




%% Compute translational accelerations

%-% Rotate body accelerations to Earth frame
rotm0 = quatern2rotMat([quat0.w',quat0.x',quat0.y',quat0.z']);
rotm1 = quatern2rotMat([quat1.w',quat1.x',quat1.y',quat1.z']);
rotm2 = quatern2rotMat([quat2.w',quat2.x',quat2.y',quat2.z']);
rotm3 = quatern2rotMat([quat3.w',quat3.x',quat3.y',quat3.z']);
for(n = [1:size(time',1)])   
acc_0(n,:) = (rotm0(:,:,n)'*[acc0.x(n); acc0.y(n); acc0.z(n)])';
acc_1(n,:) = (rotm1(:,:,n)'*[acc1.x(n); acc1.y(n); acc1.z(n)])'; 
acc_2(n,:) = (rotm2(:,:,n)'*[acc2.x(n); acc2.y(n); acc2.z(n)])'; 
acc_3(n,:) = (rotm3(:,:,n)'*[acc3.x(n); acc3.y(n); acc3.z(n)])'; 
end

% acc_0 = quaternRotate([acc0.x', acc0.y', acc0.z'], ([quat0.w',quat0.x',quat0.y',quat0.z']));
% acc_1 = quaternRotate([acc1.x', acc1.y', acc1.z'], ([quat1.w',quat1.x',quat1.y',quat1.z']));
% acc_2 = quaternRotate([acc2.x', acc2.y', acc2.z'], ([quat2.w',quat2.x',quat2.y',quat2.z']));
% acc_3 = quaternRotate([acc3.x', acc3.y', acc3.z'], ([quat3.w',quat3.x',quat3.y',quat3.z']));

%-% Remove gravity from measurements
acc_0 = acc_0 - [0,0,1];
acc_1 = acc_1 - [0,0,1];
acc_2 = acc_2 - [0,0,1];
acc_3 = acc_3 - [0,0,1];

%-% Convert acceleration measurements to m/s/s
% acc_0 = acc_0*9.81;
% acc_1 = acc_1*9.81;
% acc_2 = acc_2*9.81;
% acc_3 = acc_3*9.81;


% figure('NumberTitle', 'off', 'Position', [0, 400, 400, 300]);
% subplot(2,1,1)
% plot(time,acc0.x,'r:', time,acc0.y,'g:', time,acc0.z,'b:');
% title("Acceleration (RAW) IMU0");
% legend('X', 'Y', 'Z');
% subplot(2,1,2)
% plot(time,acc_0(:,1),'r', time,acc_0(:,2),'g', time,acc_0(:,3),'b');
% title("Acceleration (-G) IMU0");
% legend('X', 'Y', 'Z');
% figure('NumberTitle', 'off', 'Position', [410, 400, 400, 300]);
% subplot(2,1,1)
% plot(time,acc1.x,'r:', time,acc1.y,'g:', time,acc1.z,'b:');
% title("Acceleration (RAW) IMU1");
% legend('X', 'Y', 'Z');
% subplot(2,1,2)
% plot(time,acc_1(:,1),'r', time,acc_1(:,2),'g', time,acc_1(:,3),'b');
% title("Acceleration (-G) IMU1");
% legend('X', 'Y', 'Z');
% figure('NumberTitle', 'off', 'Position', [820, 400, 400, 300]);
% subplot(2,1,1)
% plot(time,acc2.x,'r:', time,acc2.y,'g:', time,acc2.z,'b:');
% title("Acceleration (RAW) IMU2");
% legend('X', 'Y', 'Z');
% subplot(2,1,2)
% plot(time,acc_2(:,1),'r', time,acc_2(:,2),'g', time,acc_2(:,3),'b');
% title("Acceleration (-G) IMU2");
% legend('X', 'Y', 'Z');
% figure('NumberTitle', 'off', 'Position', [820, 20, 400, 300]);
% subplot(2,1,1)
% plot(time,acc3.x,'r:', time,acc3.y,'g:', time,acc3.z,'b:');
% title("Acceleration (RAW) IMU3");
% legend('X', 'Y', 'Z');
% subplot(2,1,2)
% plot(time,acc_3(:,1),'r', time,acc_3(:,2),'g', time,acc_3(:,3),'b');
% title("Acceleration (-G) IMU3");
% legend('X', 'Y', 'Z');



%% Detect stationary periods (Zero Velocity Potential Update : ZUPT )


%% Compute translational velocities

%-% Integrate acceleration to yield velocity
vel_0 = zeros(framesize,3);
vel_1 = zeros(framesize,3);
vel_2 = zeros(framesize,3);
vel_3 = zeros(framesize,3);
for(t = [2:framesize])
%     vel_0(t,:) = acc_0(t,:) * samplePeriod;
%     vel_1(t,:) = acc_1(t,:) * samplePeriod;
%     vel_2(t,:) = acc_2(t,:) * samplePeriod;
%     vel_3(t,:) = acc_3(t,:) * samplePeriod;
    
    vel_0(t,:) = vel_0(t-1,:) + acc_0(t,:) * samplePeriod;
    vel_1(t,:) = vel_1(t-1,:) + acc_1(t,:) * samplePeriod;
    vel_2(t,:) = vel_2(t-1,:) + acc_2(t,:) * samplePeriod;
    vel_3(t,:) = vel_3(t-1,:) + acc_3(t,:) * samplePeriod;

%     if(stationary0(t) == 1)
%         vel_0(t,:) = [0 0 0]; %-% force zero velocity when foot stationary
%     end
%     if(stationary1(t) == 1)
%         vel_1(t,:) = [0 0 0]; %-% force zero velocity when foot stationary
%     end
%     if(stationary2(t) == 1)
%         vel_2(t,:) = [0 0 0]; %-% force zero velocity when foot stationary
%     end
%     if(stationary3(t) == 1)
%         vel_3(t,:) = [0 0 0]; %-% force zero velocity when foot stationary
%     end
end

order = 1;
filtCutOff = 0.1;
[b, a] = butter(order, (2*filtCutOff)/(1/samplePeriod), 'high');
velFT_0 = filtfilt(b, a, vel_0);
velFT_1 = filtfilt(b, a, vel_1);
velFT_2 = filtfilt(b, a, vel_2);
velFT_3 = filtfilt(b, a, vel_3);




% figure('NumberTitle', 'off', 'Position', [0, 400, 400, 300]);
% subplot(2,1,1)
% plot(time,vel_0(:,1),'r', time,vel_0(:,2),'g', time,vel_0(:,3),'b');
% title("Velocity (RAW) IMU0");
% legend('X', 'Y', 'Z');
% subplot(2,1,2)
% plot(time,velFT_0(:,1),'r', time,velFT_0(:,2),'g', time,velFT_0(:,3),'b');
% title("Velocity (filter) IMU0");
% legend('X', 'Y', 'Z');
% figure('NumberTitle', 'off', 'Position', [410, 400, 400, 300]);
% subplot(2,1,1)
% plot(time,vel_1(:,1),'r', time,vel_1(:,2),'g', time,vel_1(:,3),'b');
% title("Acceleration (RAW) IMU1");
% legend('X', 'Y', 'Z');
% subplot(2,1,2)
% plot(time,velFT_1(:,1),'r', time,velFT_1(:,2),'g', time,velFT_1(:,3),'b');
% title("Velocity (filter) IMU1");
% legend('X', 'Y', 'Z');
% figure('NumberTitle', 'off', 'Position', [820, 400, 400, 300]);
% subplot(2,1,1)
% plot(time,vel_2(:,1),'r', time,vel_2(:,2),'g', time,vel_2(:,3),'b');
% title("Velocity (RAW) IMU2");
% legend('X', 'Y', 'Z');
% subplot(2,1,2)
% plot(time,velFT_2(:,1),'r', time,velFT_2(:,2),'g', time,velFT_2(:,3),'b');
% title("Velocity (filter) IMU2");
% legend('X', 'Y', 'Z');
% figure('NumberTitle', 'off', 'Position', [820, 20, 400, 300]);
% subplot(2,1,1)
% plot(time,vel_3(:,1),'r', time,vel_3(:,2),'g', time,vel_3(:,3),'b');
% title("Velocity (RAW) IMU3");
% legend('X', 'Y', 'Z');
% subplot(2,1,2)
% plot(time,velFT_3(:,1),'r', time,velFT_3(:,2),'g', time,velFT_3(:,3),'b');
% title("Velocity (filter) IMU3");
% legend('X', 'Y', 'Z');

%% Compute translational position
pos_0 = zeros(framesize,3);
pos_1 = zeros(framesize,3);
pos_2 = zeros(framesize,3);
pos_3 = zeros(framesize,3);

for (t = [2:framesize])
    pos_0(t,:) = pos_0(t-1,:) + vel_0(t,:)*samplePeriod + 0.5*acc_0(t,:)*samplePeriod*samplePeriod ;    % integrate velocity to yield position
    pos_1(t,:) = pos_1(t-1,:) + vel_1(t,:)*samplePeriod + 0.5*acc_1(t,:)*samplePeriod*samplePeriod ;    % integrate velocity to yield position
    pos_2(t,:) = pos_2(t-1,:) + vel_2(t,:)*samplePeriod + 0.5*acc_2(t,:)*samplePeriod*samplePeriod ;    % integrate velocity to yield position
    pos_3(t,:) = pos_3(t-1,:) + vel_3(t,:)*samplePeriod + 0.5*acc_3(t,:)*samplePeriod*samplePeriod ;    % integrate velocity to yield position
end

order = 1;
filtCutOff = 0.15;
[b, a] = butter(order, (2*filtCutOff)/(1/samplePeriod), 'high');
pos_0 = filtfilt(b, a, pos_0);
pos_1 = filtfilt(b, a, pos_1);
pos_2 = filtfilt(b, a, pos_2);
pos_3 = filtfilt(b, a, pos_3);

pos_0mm = (pos_0) * 1000; %convert unit
pos_1mm = (pos_1) * 1000; %convert unit
pos_2mm = (pos_2) * 1000; %convert unit
pos_3mm = (pos_3) * 1000; %convert unit







close('all');
figure('Name' , 'Position 0');
subplot(3,1,1)
plot(time,pos_0mm(:,1),'r');
subplot(3,1,2)
plot(time,pos_0mm(:,2),'g');
subplot(3,1,3)
plot(time,pos_0mm(:,3),'b');
figure('Name' , 'Position 1');
subplot(3,1,1)
plot(time,pos_1mm(:,1),'r');
subplot(3,1,2)
plot(time,pos_1mm(:,2),'g');
subplot(3,1,3)
plot(time,pos_1mm(:,3),'b');
figure('Name' , 'Position 2');
subplot(3,1,1)
plot(time,pos_2mm(:,1),'r');
subplot(3,1,2)
plot(time,pos_2mm(:,2),'g');
subplot(3,1,3)
plot(time,pos_2mm(:,3),'b');
figure('Name' , 'Position 3');
subplot(3,1,1)
plot(time,pos_3mm(:,1),'r');
subplot(3,1,2)
plot(time,pos_3mm(:,2),'g');
subplot(3,1,3)
plot(time,pos_3mm(:,3),'b');




