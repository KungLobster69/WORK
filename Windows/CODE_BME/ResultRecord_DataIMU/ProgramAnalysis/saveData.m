function saveData(~, ~)
    global collectedData;

    if isempty(collectedData)
        disp('No data collected!');
        return;
    end

    % แสดงข้อมูลที่เลือกไว้แน่นอน
    disp('Saving final selected data:');
    disp(array2table(collectedData, 'VariableNames', {'Time', 'Signal1', 'Signal2', 'Signal3'}));

    % บันทึกข้อมูลลงไฟล์ CSV
    writematrix(collectedData, 'selected_points.csv');
    disp('Data saved to selected_points.csv');
end
