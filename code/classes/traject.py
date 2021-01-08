class Traject():
    def __init__(self, uid):
        self.traject_id = uid
        self.stations = []

    def add_station(self, node):
        self.stations.append(node)

    def get_stations(self):
        return self.stations

    def get_traject_time(self):
        station1 = None
        traject_time = 0
        time = 0
        for station in self.stations:
            if station_1 is not None
                connections = station_1.get_connections
                time = connections[station]
            traject_time = traject_time + time
            station_1 = station

        return traject_time
