function [U, V, clusterLabels] = fuzzyCMeans(data, percentClusters, m, maxIter, epsilon)
    % Fuzzy C-Means Clustering Algorithm with Percent-Based Cluster Count
    % Inputs:
    %   data           - Dataset (n x d matrix)
    %   percentClusters - Percentage of clusters relative to data size (0-100)
    %   m              - Fuzziness parameter (must be > 1)
    %   maxIter        - Maximum number of iterations
    %   epsilon        - Convergence threshold
    % Outputs:
    %   U              - Final membership matrix
    %   V              - Final cluster centers
    %   clusterLabels  - Cluster assignment based on highest membership value

    % Validate percentClusters
    if percentClusters <= 0 || percentClusters > 100
        error('Percent of clusters must be in the range (0, 100]');
    end

    % Determine the number of clusters based on percentClusters
    totalData = size(data, 1);
    numClusters = max(1, round(totalData * (percentClusters / 100)));

    % Initialize membership matrix
    n = totalData; % Number of data points
    d = size(data, 2); % Number of dimensions
    rng(1); % Seed for reproducibility
    U = rand(numClusters, n);
    U = U ./ sum(U, 1); % Normalize

    % Initialize cluster centers
    V = zeros(numClusters, d);

    % Fuzzy C-Means Algorithm
    for iter = 1:maxIter
        % Compute cluster centers
        for j = 1:numClusters
            numerator = sum((U(j, :) .^ m)' .* data);
            denominator = sum(U(j, :) .^ m);
            V(j, :) = numerator / denominator;
        end

        % Update membership matrix
        U_new = zeros(size(U));
        for j = 1:numClusters
            for i = 1:n
                distances = vecnorm(data(i, :) - V, 2, 2); % Euclidean distances
                if distances(j) == 0
                    U_new(j, i) = 1; % Handle zero distance
                    continue;
                end
                denominator = sum((distances(j) ./ distances) .^ (2 / (m - 1)));
                U_new(j, i) = 1 / denominator;
            end
        end

        % Check for convergence
        if max(abs(U_new - U), [], 'all') < epsilon
            break;
        end

        U = U_new; % Update U
    end

    % Assign data to clusters
    [~, clusterLabels] = max(U, [], 1);
end