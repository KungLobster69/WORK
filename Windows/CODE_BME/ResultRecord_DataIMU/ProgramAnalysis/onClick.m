    function txt = onClick(~, event)
        % Get clicked position (time)
        clickedTime = event.Position(1);
        
        % Find the closest index in the time array
        idx = find(event.Target.XData == clickedTime);

        % Retrieve corresponding values from all signals
        timePoint = clickedTime;
        amp1 = fig.CurrentAxes.Children(1).YData(idx);
        amp2 = fig.CurrentAxes.Children(2).YData(idx);
        amp3 = fig.CurrentAxes.Children(3).YData(idx);

        % Store data point
        collectedData = [collectedData; timePoint, amp1, amp2, amp3];

        % Display selected data in console
        %fprintf('Selected Time: %.3f sec\n', timePoint);
        %fprintf('Signal 1: %.3f, Signal 2: %.3f, Signal 3: %.3f\n\n', amp1, amp2, amp3);

        % Update cursor text
        txt = {sprintf('Time: %.2f', timePoint), ...
               sprintf('b: %.2f', amp1), ...
               sprintf('g: %.2f', amp2), ...
               sprintf('r: %.2f', amp3)};
    end