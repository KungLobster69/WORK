function T = adaptive_threshold(img,min_intensity,max_intensity)
    if nargin == 1
        idx = find(img~=0);
        max_intensity = max(img(idx));
        % idx1 = find(img(idx) > 0.3 & img(idx) <= 0.4)
        min_intensity = min(img(idx));
    end
    
    r = min_intensity + (max_intensity-min_intensity)*rand(1,1);
    T = r;
    newT = 9999;
    k = 0;
    while k~=500
        G1 = img(img <= T);
        nG1 = length(find(G1~=0));
        M1 = sum(G1)/nG1;
        G2 = img(img > T);
        M2 = sum(G2)/length(G2);
        if isnan(M2)
            M2 = 0;
        end
        newT = (M1+M2)/2;
        if(T==newT)
            break
        else
            T = newT;
        end
        k = k+1;
    end
end