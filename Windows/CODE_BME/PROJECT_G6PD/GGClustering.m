function [U, V, clusterLabels] = GGClustering(data, percentClusters, m, maxIter, epsilon)
    % Gath-Geva Clustering Algorithm with Percent-Based Cluster Count
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
    Sigma = repmat(eye(d), [1, 1, numClusters]); % Identity matrices

    % Gath-Geva Clustering Algorithm
    for iter = 1:maxIter
        % Update cluster centers (V)
        for j = 1:numClusters
            numerator = sum((U(j, :) .^ m)' .* data);
            denominator = sum(U(j, :) .^ m);
            V(j, :) = numerator / denominator;
        end

        % Update covariance matrices (Sigma)
        for j = 1:numClusters
            numerator = zeros(d, d);
            denominator = 0;
            for i = 1:n
                diff = (data(i, :) - V(j, :))';
                numerator = numerator + (U(j, i) .^ m) * (diff * diff');
                denominator = denominator + U(j, i) .^ m;
            end
            Sigma(:, :, j) = numerator / denominator;

            % Regularization: Add small value to diagonal elements
            Sigma(:, :, j) = Sigma(:, :, j) + eye(d) * 1e-5; % Regularize
        end

        % Update membership matrix (U)
        U_new = zeros(size(U));
        for j = 1:numClusters
            for i = 1:n
                diff = (data(i, :) - V(j, :))';
                mahalDist = diff' / Sigma(:, :, j) * diff; % Mahalanobis distance
                detSigma = det(Sigma(:, :, j));
                if detSigma <= 0
                    warning('Determinant of covariance matrix is non-positive');
                    detSigma = 1e-5; % Regularize determinant
                end
                likelihood = exp(-0.5 * mahalDist) / sqrt((2 * pi)^d * detSigma);
                if likelihood == 0
                    likelihood = 1e-5; % Avoid zero likelihood
                end
                U_new(j, i) = likelihood;
            end
        end

        % Normalize U to sum to 1 for each data point
        U_new = U_new ./ sum(U_new, 1);

        % Check for convergence
        if max(abs(U_new - U), [], 'all') < epsilon
            break;
        end
        U = U_new; % Update U
    end

    % Assign data to clusters
    [~, clusterLabels] = max(U, [], 1);
end