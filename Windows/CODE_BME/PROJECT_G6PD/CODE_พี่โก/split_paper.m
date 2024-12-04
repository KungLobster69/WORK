function [control_img,test_img] = split_paper(imgFG,areas,stats)
    k = find(areas~=0);
    s = stats(k);

    if length(k) == 2
        cutoff = round((s(1).Centroid + s(2).Centroid)/2);
    else
        cutoff = round(s(1).Centroid);
    end
    control_img = imcrop(imgFG,[1,1,cutoff(1),size(imgFG,1)]); %[xmin ymin width height]
    test_img = imcrop(imgFG,[cutoff(1)+1,1,size(imgFG,2)-cutoff(1),size(imgFG,1)]); %[xmin ymin width height]
end