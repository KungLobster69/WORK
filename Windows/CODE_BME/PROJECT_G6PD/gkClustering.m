function [U, V, clusterLabels] = gkClustering(data, numClusters, m, maxIter, epsilon)
    % Gustafson-Kessel Clustering Algorithm
    % Inputs:
    %   data        - Dataset (n x d matrix)
    %   numClusters - Number of clusters
    %   m           - Fuzziness parameter (must be > 1)
    %   maxIter     - Maximum number of iterations
    %   epsilon     - Convergence threshold
    % Outputs:
    %   U           - Final membership matrix
    %   V           - Final cluster centers
    %   clusterLabels - Cluster assignment based on highest membership value

    % Initialize variables
    n = size(data, 1); % Number of data points
    d = size(data, 2); % Dimension of data
    rng(1); % Set seed for reproducibility
    U = rand(numClusters, n);
    U = U ./ sum(U, 1); % Normalize membership matrix
    V = zeros(numClusters, d); % Initialize cluster centers

    % GK Algorithm
    for iter = 1:maxIter
        % Update cluster centers
        for j = 1:numClusters
            numerator = sum((U(j, :) .^ m)' .* data);
            denominator = sum(U(j, :) .^ m);
            V(j, :) = numerator / denominator;
        end

        % Compute covariance matrix for each cluster
        S = cell(numClusters, 1); % Covariance matrices
        A = cell(numClusters, 1); % Adaptive matrices
        for j = 1:numClusters
            S{j} = zeros(d, d);
            for i = 1:n
                diff = (data(i, :) - V(j, :))';
                S{j} = S{j} + (U(j, i) ^ m) * (diff * diff');
            end
            S{j} = S{j} / sum(U(j, :) .^ m);
            detS = det(S{j});
            if detS > 0
                A{j} = (detS^(1/d)) * inv(S{j});
            else
                A{j} = eye(d); % Default to identity matrix if det(S) is zero
            end
        end

        % Update membership matrix
        U_new = zeros(size(U));
        for j = 1:numClusters
            for i = 1:n
                distances = zeros(numClusters, 1);
                for k = 1:numClusters
                    diff = (data(i, :) - V(k, :))';
                    distances(k) = sqrt(diff' * A{k} * diff);
                end
                U_new(j, i) = 1 / sum((distances(j) ./ distances) .^ (2 / (m - 1)));
            end
        end

        % Check convergence
        if max(abs(U_new - U), [], 'all') < epsilon
            break;
        end

        U = U_new; % Update U
    end

    % Assign data to clusters
    [~, clusterLabels] = max(U, [], 1);
end