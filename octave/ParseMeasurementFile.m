function [x,y,z,xStep,yStep,xLim,yLim,zLim,DateTime] = ParseMeasurementFile (fileName)
  fid = fopen('test.txt');
  zLim =-1;
  %% read date and Time
  line_1_DateTime = fgetl(fid);
  pat_1 = '[#]+';
  [s, e, te, m, t, nm, sp] = regexp (line_1_DateTime, pat_1);
  DateTime = sp{2};
  
  %% read limits from secound line
  line_2_ConFig = fgetl(fid);
  str_2 = 'step size(xStep:30,yStep:26) xlim:(10,275), ylim:(13,200)';
  pat_2 = '\d+';
  match = regexp (line_2_ConFig, pat_2,'match');
  [xStep,yStep,xlim,ylim] = match{:};
  xStep = str2double(xStep);
  yStep = str2double(yStep);
  xLim = str2double(xlim);
  yLim = str2double(ylim);
  
  %read all x,y and z values
  tline = fgetl(fid);
  [xStep,yStep,xlim,ylim] = match{:};
  look4Numbers = '[-+.\d]+.';% look for floating points
  x=[];
  y=[];
  z=[]; 
  while ischar(tline)  
    %disp(tline)
    xyz = regexp (tline, look4Numbers,'match');
    x = [x,str2double(xyz(1))];
    y = [y,str2double(xyz(2))];
    z = [z,str2double(xyz(3))];
    tline = fgetl(fid);  
  end
  fclose(fid);
endfunction
