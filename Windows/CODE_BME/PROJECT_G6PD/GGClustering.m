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

    % Calculate number of clusters
    totalData = size(data, 1);
    numClusters = max(1, round(totalData * (percentClusters / 100)));

    % Number of data points and dimensions
    [n, d] = size(data);

    % Initialize membership matrix
    rng(1); % Seed for reproducibility
    U = rand(numClusters, n);
    U = U ./ sum(U, 1); % Normalize

    % Initialize cluster centers and covariance matrices
    V = zeros(numClusters, d);
    Sigma = repmat(eye(d), [1, 1, numClusters]); % Identity matrices

    % Gath-Geva Clustering Algorithm
    for iter = 1:maxIter
        % Update cluster centers (V)
        for j = 1:numClusters
            Uj_m = U(j, :) .^ m; % Membership values raised to power m
            numerator = sum((Uj_m') .* data, 1); % Weighted sum of data points
            denominator = sum(Uj_m); % Sum of weights
            V(j, :) = numerator / denominator; % Update cluster center
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
            Sigma(:, :, j) = numerator / denominator + eye(d) * 1e-5; % Regularization
        end

        % Update membership matrix (U)
        U_new = zeros(size(U));
        for j = 1:numClusters
            for i = 1:n
                diff = (data(i, :) - V(j, :))';
                mahalDist = diff' / Sigma(:, :, j) * diff; % Mahalanobis distance
                detSigma = det(Sigma(:, :, j));
                % Ensure determinant is positive and avoid NaN/Inf
                if detSigma <= 0 || isnan(detSigma) || isinf(detSigma)
                    warning('Covariance matrix determinant adjusted to positive value');
                    detSigma = max(detSigma, 1e-5);
                end
                likelihood = exp(-0.5 * mahalDist) / sqrt((2 * pi)^d * detSigma);
                % Avoid zero likelihood
                if isnan(likelihood) || isinf(likelihood) || likelihood <= 0
                    warning('Likelihood adjusted to avoid NaN, Inf, or zero');
                    likelihood = 1e-5;
                end
                U_new(j, i) = likelihood;
            end
        end

        % Normalize U to sum to 1 for each data point
        U_new = U_new ./ sum(U_new, 1);

        % Check for convergence
        delta = max(abs(U_new - U), [], 'all');
        if delta < epsilon
            fprintf('Converged at iteration %d with delta = %.6f\n', iter, delta);
            break;
        end
        U = U_new; % Update U
    end

    % Assign data to clusters based on highest membership
    [~, clusterLabels] = max(U, [], 1);
end