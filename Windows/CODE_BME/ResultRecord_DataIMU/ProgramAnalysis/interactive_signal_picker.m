function interactive_signal_picker(fig)
    global collectedData;
    collectedData = [];  

    % เปิด Data Cursor Mode
    dcm = datacursormode(fig);
    dcm.Enable = 'on';
    dcm.SnapToDataVertex = 'on';  % ให้เลือกเฉพาะจุดที่มีข้อมูลพอดี

    % ปุ่ม Save Data
    btnSave = uicontrol('Parent', fig, 'Style', 'pushbutton', 'String', 'Save Data', ...
        'Position', [350, 100, 100, 30], 'Callback', @saveData);
    
    % ปุ่ม Extract Data เพื่อดึงค่าที่เลือกแน่นอนแล้ว
    btnExtract = uicontrol('Parent', fig, 'Style', 'pushbutton', 'String', 'Extract Data', ...
        'Position', [350, 140, 100, 30], 'Callback', @extractCursorData);
    
    function extractCursorData(~, ~)
        % ดึงข้อมูลที่ถูกเลือก
        cursorInfo = getCursorInfo(dcm);
        
        % ตรวจสอบว่ามีข้อมูลหรือไม่
        if isempty(cursorInfo)
            disp('No data points selected.');
            return;
        end

        % เคลียร์ค่าเก่าแล้วเก็บค่าใหม่
        collectedData = [];

        % เรียงลำดับเส้นให้ตรงกับที่แสดงบนกราฟ
        lines = flip(fig.CurrentAxes.Children); % MATLAB อาจเก็บเส้นกราฟสลับกัน

        % วนลูปดึงค่าที่ถูกเลือก
        for i = 1:length(cursorInfo)
            x = cursorInfo(i).Position(1);  % ค่าเวลา (Time)

            % หา index ของ X ที่ใกล้ที่สุด
            [~, idx] = min(abs(lines(1).XData - x));

            % ดึงค่าจากทั้ง 3 เส้น
            amp1 = lines(1).YData(idx);  % น้ำเงิน (b)
            amp2 = lines(2).YData(idx);  % เขียว (g)
            amp3 = lines(3).YData(idx);  % แดง (r)

            % เพิ่มค่าที่เลือกลงใน collectedData
            collectedData = [collectedData; x, amp1, amp2, amp3];
        end
        
        % แสดงค่าที่เลือกใน Command Window
        fprintf('Final Selected Points:\n');
        disp(array2table(collectedData, 'VariableNames', {'Time', 'น้ำเงิน', 'เขียว', 'แดง'}));
    end
end
 