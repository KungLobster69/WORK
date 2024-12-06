function [U, V, clusterLabels] = fuzzyCMeans(data, clusterInput, m, maxIter, epsilon)
    % Fuzzy C-Means Clustering Algorithm with Flexible Cluster Input
    % Inputs:
    %   data          - Dataset (n x d matrix)
    %   clusterInput  - Either percentage of clusters (0-100) or the exact number of clusters
    %   m             - Fuzziness parameter (must be > 1)
    %   maxIter       - Maximum number of iterations
    %   epsilon       - Convergence threshold
    % Outputs:
    %   U             - Final membership matrix
    %   V             - Final cluster centers
    %   clusterLabels - Cluster assignment based on highest membership value

    % Determine the number of clusters
    totalData = size(data, 1);
    if clusterInput <= 1 % If input is a percentage (e.g., 0.5 for 50%)
        percentClusters = clusterInput * 100;
        if percentClusters <= 0 || percentClusters > 100
            error('Percentage of clusters must be in the range (0, 100].');
        end
        numClusters = max(1, round(totalData * (percentClusters / 100)));
    else % If input is a direct number of clusters
        numClusters = round(clusterInput);
        if numClusters <= 0 || numClusters > totalData
            error('Number of clusters must be in the range (1, total data points).');
        end
    end

    % Initialize membership matrix
    [n, d] = size(data); % Number of data points and dimensions
    rng(1); % Seed for reproducibility
    U = rand(numClusters, n);
    U = U ./ sum(U, 1); % Normalize

    % Initialize cluster centers
    V = zeros(numClusters, d);

    % Fuzzy C-Means Algorithm
    for iter = 1:maxIter
        % Update cluster centers (V)
        for j = 1:numClusters
            Uj_m = U(j, :) .^ m;
            numerator = sum((Uj_m') .* data, 1);
            denominator = sum(Uj_m);
            if denominator == 0
                warning('Cluster %d has no members; skipping update', j);
                continue;
            end
            V(j, :) = numerator / denominator;
        end

        % Update membership matrix (U)
        U_new = zeros(size(U));
        for j = 1:numClusters
            for i = 1:n
                distances = vecnorm(data(i, :) - V, 2, 2) + 1e-8; % Regularization
                if distances(j) == 0
                    U_new(j, i) = 1;
                    continue;
                end
                denominator = sum((distances(j) ./ distances) .^ (2 / (m - 1)));
                U_new(j, i) = 1 / denominator;
            end
        end

        % Check for convergence
        delta = max(abs(U_new - U), [], 'all');
        if delta < epsilon
            fprintf('Converged at iteration %d with delta = %.6f\n', iter, delta);
            break;
        end

        U = U_new; % Update U
    end

    % Assign data to clusters
    [~, clusterLabels] = max(U, [], 1);
end