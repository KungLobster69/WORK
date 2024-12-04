function [U, V, clusterLabels] = fuzzyCMeans(data, numClusters, m, maxIter, epsilon)
    % Fuzzy C-Means Clustering Algorithm
    % Inputs:
    %   data        - Dataset (n x d matrix, where n = number of data points, d = dimensions)
    %   numClusters - Number of clusters
    %   m           - Fuzziness parameter (must be > 1)
    %   maxIter     - Maximum number of iterations
    %   epsilon     - Convergence threshold
    % Outputs:
    %   U           - Final membership matrix (numClusters x n)
    %   V           - Final cluster centers (numClusters x d)
    %   clusterLabels - Cluster assignment based on highest membership value
    
    % Number of data points
    n = size(data, 1);
    
    % Initialize membership matrix
    U = rand(numClusters, n);
    U = U ./ sum(U, 1); % Normalize membership values

    % Initialize cluster centers
    V = zeros(numClusters, size(data, 2));

    % Fuzzy C-Means Clustering
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
                denominator = sum((norm(data(i, :) - V(j, :)) / norm(data(i, :) - V)) .^ (2 / (m - 1)));
                U_new(j, i) = 1 / denominator;
            end
        end

        % Check for convergence
        if max(abs(U_new - U), [], 'all') < epsilon
            break;
        end

        U = U_new; % Update U for the next iteration
    end

    % Assign data to clusters
    [~, clusterLabels] = max(U, [], 1);
end
