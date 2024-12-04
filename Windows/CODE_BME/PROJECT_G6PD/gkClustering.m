function [U, V, clusterLabels] = GKClustering(data, percentClusters, m, maxIter, epsilon)
    % Gustafson and Kessel (GK) Clustering Algorithm with Percent-Based Cluster Count
    % Inputs:
    %   data            - Dataset (n x d matrix)
    %   percentClusters - Percentage of clusters relative to data size (0-100)
    %   m               - Fuzziness parameter (must be > 1)
    %   maxIter         - Maximum number of iterations
    %   epsilon         - Convergence threshold
    % Outputs:
    %   U               - Final membership matrix
    %   V               - Final cluster centers
    %   clusterLabels   - Cluster assignment based on highest membership value

    % Validate percentClusters
    if percentClusters <= 0 || percentClusters > 100
        error('Percent of clusters must be in the range (0, 100]');
    end

    % Calculate number of clusters based on percentClusters
    totalData = size(data, 1);
    numClusters = max(1, round(totalData * (percentClusters / 100)));

    % Number of data points and dimensions
    n = size(data, 1);
    d = size(data, 2);

    % Initialize membership matrix
    rng(1); % Seed for reproducibility
    U = rand(numClusters, n);
    U = U ./ sum(U, 1); % Normalize

    % Initialize cluster centers
    V = zeros(numClusters, d);

    % Initialize covariance matrices
    A = repmat(eye(d), [1, 1, numClusters]); % Identity matrices

    % GK Clustering Algorithm
    for iter = 1:maxIter
        % Update cluster centers (V)
        for j = 1:numClusters
            numerator = sum((U(j, :) .^ m)' .* data);
            denominator = sum(U(j, :) .^ m);
            V(j, :) = numerator / denominator;
        end

        % Update covariance matrices (A)
        for j = 1:numClusters
            numerator = zeros(d, d);
            denominator = 0;
            for i = 1:n
                diff = (data(i, :) - V(j, :))';
                numerator = numerator + (U(j, i) .^ m) * (diff * diff');
                denominator = denominator + U(j, i) .^ m;
            end
            A(:, :, j) = numerator / denominator;

            % Regularization: Add small value to diagonal elements
            A(:, :, j) = A(:, :, j) + eye(d) * 1e-5; % Regularize to ensure positive definiteness
        end

        % Normalize covariance matrices
        for j = 1:numClusters
            detA = det(A(:, :, j));
            if detA <= 0 || isnan(detA) || isinf(detA)
                warning('Covariance matrix adjusted to ensure positive-definiteness');
                A(:, :, j) = A(:, :, j) + eye(d) * 1e-5;
            else
                A(:, :, j) = (detA^(1 / d)) * inv(A(:, :, j));
            end
        end

        % Update membership matrix (U)
        U_new = zeros(size(U));
        for j = 1:numClusters
            for i = 1:n
                diff = (data(i, :) - V(j, :))';
                d_ij = diff' * A(:, :, j) * diff; % Mahalanobis distance
                if d_ij == 0
                    U_new(j, i) = 1;
                    continue;
                end
                denominator = sum((d_ij ./ (sum((data(i, :) - V) .^ 2, 2))).^(1 / (m - 1)));
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