function interactive_signal_picker()
    %close all figure
    close all 
    
    % Create figure and axes
    fig = figure('Name', 'Interactive Signal Picker', 'Position', [100, 100, 800, 600]);
    ax = axes('Parent', fig, 'Position', [0.1, 0.3, 0.8, 0.6]);
    hold(ax, 'on'); % Allow multiple signals to be plotted

    % Generate Sample Data
    t = linspace(0, 10, 500);  % Time from 0 to 10 seconds
    y1 = sin(2*pi*0.5*t);       % First signal
    y2 = cos(2*pi*0.7*t);       % Second signal
    y3 = sin(2*pi*1.2*t) + 0.5; % Third signal

    % Plot the signals
    plot1 = plot(ax, t, y1, 'r', 'DisplayName', 'Signal 1');
    plot2 = plot(ax, t, y2, 'g', 'DisplayName', 'Signal 2');
    plot3 = plot(ax, t, y3, 'b', 'DisplayName', 'Signal 3');
    legend(ax, 'show');
    xlabel(ax, 'Time (s)');
    ylabel(ax, 'Amplitude');
    title(ax, 'Click on any Signal to Pick Data from All Signals');

    % Enable data cursor
    dcm = datacursormode(fig);
    datacursormode on;

    % Store selected data
    collectedData = zeros(1,9);
    clickCount = 0;  % Click counter
    selectedAction = 'Normal';
    selectedMovement = 'Forward Flexion';

        % Create First Combo Box (One, Two, Three)
    uicontrol('Style', 'text', 'String', 'Conditions:', ...
        'Position', [50, 50, 100, 20], 'HorizontalAlignment', 'left');
    comboBox1 = uicontrol('Style', 'popupmenu', 'String', {'Normal', 'AC cut', 'AC CC cut',...
        'Repair CC loop','Repair Double Button','Repair Single Button'}, ...
        'Position', [150, 50, 100, 25], 'Callback', @comboBox1Callback);

    % Create Second Combo Box (X, Y, Z)
    uicontrol('Style', 'text', 'String', 'Movements:', ...
        'Position', [50, 20, 100, 20], 'HorizontalAlignment', 'left');
    comboBox2 = uicontrol('Style', 'popupmenu', 'String', {'Forward Flexion', 'Abduction', 'Adduction'}, ...
        'Position', [150, 20, 100, 25], 'Callback', @comboBox2Callback);

    % Create a button to save data
    btn = uicontrol('Style', 'pushbutton', 'String', 'Save Data', ...
        'Position', [350, 50, 100, 30], 'Callback', @saveData);

    % Set data cursor update function
    set(dcm, 'UpdateFcn', @onClick);

    function comboBox1Callback(source, ~)
        selectedAction = source.String{source.Value};
        fprintf('Combo Box 1 Selected: %s\n', selectedAction);
    end

    function comboBox2Callback(source, ~)
        selectedMovement = source.String{source.Value};
        fprintf('Combo Box 2 Selected: %s\n', selectedMovement);
    end

    function txt = onClick(~, event)
        % Get clicked position (time)
        clickedTime = event.Position(1);

        % Increment click count
        clickCount = clickCount + 1;

        % Find the closest index in the stop point of time array
        [~, idx] = min(abs(t - clickedTime));
        % Display selected data in console
        fprintf('Selected Time: %.3f sec\n', t(idx));
        fprintf('end point, Signal 1: %.3f, Signal 2: %.3f, Signal 3: %.3f\n\n', y1(idx), y2(idx), y3(idx));

        % Retrieve corresponding interval values from all signals
        timePoint = t(idx);
        amp1 = y1(idx);
        amp2 = y2(idx);
        amp3 = y3(idx);

        % Store data point
        if clickCount == 1
            collectedData(1) = amp1;
            collectedData(4) = amp2;
            collectedData(7) = amp3;
        elseif clickCount == 2
            collectedData(2) = amp1;
            collectedData(5) = amp2;
            collectedData(8) = amp3;
        elseif clickCount == 3
            collectedData(3) = amp1;
            collectedData(6) = amp2;
            collectedData(9) = amp3;
        end

        % Update cursor text
        txt = {sprintf('Time: %.3f', t(idx)), ...
               sprintf('S1: %.3f', y1(idx)), ...
               sprintf('S2: %.3f', y2(idx)), ...
               sprintf('S3: %.3f', y3(idx))};
    end

    function saveData(~, ~)
        fprintf(selectedAction);
        if isempty(collectedData)
            msgbox('No data collected!', 'Warning', 'warn');
        else
            filename = 'Result IMU.xlsx';
            sheet = 'No3 20250217Left';
            xlRange = 'J30';
            % save into excel
            xlswrite(filename,collectedData,sheet,xlRange)
            msgbox('Data saved successfully!', 'Success');
            %clear variables
            clickCount = 0;
            collectedData = zeros(1,9);
        end
    end
end