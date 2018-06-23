import matlab.engine
from communications.boat_nav.gpsNavigation import GPSNavigation

class path_nav:
    def __init__(self, imu):
        self.eng = matlab.engine.start_matlab()
        self.navigation = GPSNavigation(imu)
        self.imu = imu
        self.path = []
        self.path2 = []

    def nav_set_waypoints(self, path, boat_x, boat_y):
        '''
        Navegacion por cierta cantidad de Waypoints
        '''
        for i in range(0,len(self.path)):
            x = self.path[i][0]             #Obtiene coordenada x y de la matriz regresada por matlab para el camino de ida
            y = self.path[i][1]
            coords = self.imu.get_obstacle_gps_coords(boat_x, boat_y, x, y ) # convierte la coordenada a latitud / longitud            
            self.navigation.update_nav(coords['latitude'], coords['longitud']) # le da la orden de navegar hacia el punto dado

    def path_planning(self):
        '''
        Metodo encargado de tomar los paths en x y, y modificarlos a lat lon para poderlos meter
        al metodo navigate del objeto navigation
        '''
        self.path,self.path2 = self.eng.FindThePath()#ARGUMENTOS QUE ME VA A PASAR JAVI
        print(type(self.path))
        print(type(self.path2))
        self.nav_set_waypoints(self.path,boat_x, boat_y)
        self.nav_set_waypoints(self.path2, boat_x, boat_y)

    def end_matlab(self):
        '''
        Cerrar el engine de Matlab
        '''
        self.eng.quit()

