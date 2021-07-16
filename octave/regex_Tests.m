clc;
clear all;
##str_1 = '###############07/12/2021, 19:38:32###############';
##%str_1 = "2.3";
##
##%pat_1 = "(?:^|\\s+)([a-zA-Z]+)(?=[,.]?(?:$|\\s))";
##pat_1 = '[#]+';
##[s, e, te, m, t, nm, sp] = regexp (str_1, pat_1);
##date = sp(2);
##
str_2 = 'step size(xStep:30,yStep:26) xlim:(10,275), ylim:(13,200)';
pat_2 = '\d+';
[s, e, te, m, t, nm, sp] = regexp (str_2, pat_2);
[xStep,yStep,xlim,ylim] = m{:}

##str_2 = '10	-65	-0.23';
##pat_2 = '[-+.\d]+.';
##match = regexp (str_2, pat_2,'match');
##[x,y,z] = match {:}
