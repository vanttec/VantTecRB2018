filePath = fullfile(fileparts(which('PathPlanningExample')),'data','exampleMaps.mat');
load(filePath)
map = robotics.BinaryOccupancyGrid(50,10,30);
xy = [3 2; 8 5; 13 7; 20 1; 25 8; 32 6; 38 3; 40 9; 42 4; 23 2; 28 5; 33 7];
setOccupancy(map, xy, 1);
robotRadius = 0.5;
mapInflated = copy(map);
inflate(mapInflated,0.3);
prm = robotics.PRM
prm.Map = mapInflated;
startLocation = [3 3];
endLocation = [47 7];
prm.NumNodes = 25;

% Search for a solution between start and end location.
path = findpath(prm, startLocation, endLocation);
while isempty(path)
    prm.NumNodes = prm.NumNodes + 1;
    update(prm);
    path = findpath(prm, startLocation, endLocation);
end

% Display path
path
figure(1)
show(prm)

[r c] = size(path)

d = input(' initial data = [v0, ac0, v1, ac1, t0, tf] = ')
tf = 0;
dt = 0;

for y = 0:(r-2)
   x1 = path(y+1,1);
   x2 = path(y+2,1);
   y1 = path(y+1,2);
   y2 = path(y+2,2);
   dr = sqrt((x2-x1)^2 + (y2-y1)^2);
   dt = dt + dr;
end

for x = 0:(r-2)

q0x = path(x+1,1); v0 = d(1); ac0 = d(2);
q1x = path(x+2,1); v1 = d(3); ac1 = d(4);
q0y = path(x+1,2); 
q1y = path(x+2,2);
dq = sqrt((q1x-q0x)^2 + (q1y-q0y)^2);
t0 = d(5)+tf; tf = ((d(6))*dq/dt) + tf;
t = linspace(t0,tf);
c = ones(size(t));
M = [ 1 t0 t0^2 t0^3 t0^4 t0^5;
    0 1 2*t0 3*t0^2 4*t0^3 5*t0^4;
    0 0 2 6*t0 12*t0^2 20*t0^3;
    1 tf tf^2 tf^3 tf^4 tf^5;
    0 1 2*tf 3*tf^2 4*tf^3 5*tf^4;
    0 0 2 6*tf 12*tf^2 20*tf^3];
bx=[q0x;v0;ac0;q1x;v1;ac1];
by=[q0y;v0;ac0;q1y;v1;ac1];
ax=inv(M)*bx;
ay=inv(M)*by;
qx = ax(1).*c + ax(2).*t + ax(3).*t.^2 + ax(4).*t.^3 + ax(5).*t.^4 + ax(6).*t.^5;
figure(2)
plot(t, qx)
title('Position X')
hold on
qy = ay(1).*c + ay(2).*t + ay(3).*t.^2 + ay(4).*t.^3 + ay(5).*t.^4 + ay(6).*t.^5;
figure(3)
plot(t, qy)
title('Position Y')
hold on
vx = ax(2).*c + 2*ax(3).*t + 3*ax(4).*t.^2 + 4*ax(5).*t.^3 + 5*ax(6).*t.^4;
figure(4)
plot(t, vx)
title('Velocity X')
hold on
vy = ay(2).*c + 2*ay(3).*t + 3*ay(4).*t.^2 + 4*ay(5).*t.^3 + 5*ay(6).*t.^4;
figure(5)
plot(t, vy)
title('Velocity Y')
hold on
ax = 2*ax(3).*c + 6*ax(4).*t + 12*ax(5).*t.^2 + 20*ax(6).*t.^3;
figure(6)
plot(t, ax)
title('Acceleration X')
hold on
ay = 2*ay(3).*c + 6*ay(4).*t + 12*ay(5).*t.^2 + 20*ay(6).*t.^3;
figure(7)
plot(t, ay)
title('Acceleration Y')
hold on
figure(8)
plot(qx,qy)
title('XY')
hold on
end