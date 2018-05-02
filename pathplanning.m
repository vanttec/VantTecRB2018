filePath = fullfile(fileparts(which('PathPlanningExample')),'data','exampleMaps.mat');
load(filePath)
map = robotics.OccupancyGrid(ternaryMap, 20)
robotRadius = 0.5;
mapInflated = copy(map);
inflate(mapInflated,robotRadius);
prm = robotics.PRM
prm.Map = mapInflated;
startLocation = [5 22];
endLocation = [20 5];
prm.NumNodes = 1;

% Search for a solution between start and end location.
path = findpath(prm, startLocation, endLocation);
while isempty(path)
    prm.NumNodes = prm.NumNodes + 1;
    update(prm);
    path = findpath(prm, startLocation, endLocation);
end

% Display path
path
show(prm)