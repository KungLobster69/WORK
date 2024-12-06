function predictedLabels = fuzzyKNN(testData, trainData, trainLabels, k, m)
    % FUZZYKNN - Implementation of Fuzzy K-Nearest Neighbors using Euclidean Distance
    % Inputs:
    %   testData - n_test x d matrix (test data points)
    %   trainData - n_train x d matrix (training data points)
    %   trainLabels - n_train x 1 vector (training labels)
    %   k - number of nearest neighbors
    %   m - fuzziness parameter
    % Output:
    %   predictedLabels - n_test x 1 vector (predicted labels for test data)

    numTest = size(testData, 1); % Number of test samples
    predictedLabels = zeros(numTest, 1); % Initialize predicted labels

    % Calculate Euclidean distances
    distances = pdist2(testData, trainData, 'euclidean');

    for i = 1:numTest
        % Get the indices of k nearest neighbors
        [~, sortedIdx] = sort(distances(i, :)); % Sort distances for the i-th test sample
        nearestNeighbors = sortedIdx(1:k);

        % Calculate membership weights for k neighbors
        weights = 1 ./ (distances(i, nearestNeighbors).^m + eps); % Avoid division by zero
        weights = weights / sum(weights); % Normalize weights

        % Aggregate the weights by class
        uniqueClasses = unique(trainLabels);
        classScores = zeros(length(uniqueClasses), 1);
        for j = 1:length(uniqueClasses)
            classScores(j) = sum(weights(trainLabels(nearestNeighbors) == uniqueClasses(j)));
        end

        % Assign the class with the highest score
        [~, maxIdx] = max(classScores);
        predictedLabels(i) = uniqueClasses(maxIdx);
    end
end
