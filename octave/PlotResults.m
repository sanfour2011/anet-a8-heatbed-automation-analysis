clear all;
clc;
resultFile = fullfile(fileparts(mfilename('fullpath')), '..', 'results', 'data', '2021.07.25 - 18.28.50.txt');
[x,y,z,xStep,yStep,xLim,yLim,zLim,DateTime] = ParseMeasurementFile(resultFile);
tx = unique(x);
ty = unique(y);

tz = reshape(z,length(ty),length(tx));
tz(:,2:2:end) = flipud(tz(:,2:2:end));
offset = tz(1,1);

tz = tz-offset;


surf(tx,ty,tz)
title (DateTime)
xlabel "X-axis";
ylabel "Y-axis";
zlabel "Z-axis";
colormap winter

