clear all;
clc;
resultFile = fullfile(fileparts(mfilename('fullpath')), '..', 'results', 'data', '2021.07.25 - 17.07.06.txt');
[x,y,z,xStep,yStep,xLim,yLim,zLim,DateTime] = ParseMeasurementFile(resultFile);

tx = unique(x);
ty = unique(y);

tz = reshape(z,length(ty),length(tx));
a1 = tz;

x = a1(:,1);
y = a1(:,2);
z = a1(:,3);
n = 9;
[X, Y] = meshgrid(linspace(min(x),max(x),n), linspace(min(y),max(y),n));
Z = griddata(x,y,z,X,Y);
%// Remove the NaNs for imshow:
Z(isnan(Z)) = 0;
m = min(Z(Z~=0));
M = max(Z(Z~=0));
imshow((Z-m)/(M-m));
colormap winter