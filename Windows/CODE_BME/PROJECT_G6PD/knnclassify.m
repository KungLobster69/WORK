function predictedLabels = knnclassify(testData, trainData, trainLabels, k)
    % KNNCLASSIFY - Custom implementation using Euclidean distance via pdist2
    % Inputs:
    %   testData - n_test x d matrix (test data points)
    %   trainData - n_train x d matrix (training data points)
    %   trainLabels - n_train x 1 vector (training labels)
    %   k - number of nearest neighbors
    % Output:
    %   predictedLabels - n_test x 1 vector (predicted labels for test data)

    % Calculate Euclidean distances
    distances = pdist2(testData, trainData, 'euclidean');

    % Sort distances and get indices of k nearest neighbors
    [~, sortedIdx] = sort(distances, 2); % Sort rows (test points)
    nearestNeighbors = trainLabels(sortedIdx(:, 1:k)); % Get labels of k neighbors

    % Assign the most common label among neighbors
    predictedLabels = mode(nearestNeighbors, 2); % Find mode along rows
end
