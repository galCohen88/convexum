import geopy.distance


class GeoEntity:

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.coords = (latitude, longitude)

    def update_position(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def calculate_distance_from_object(self, geo_instance):
        geo_instance_coords = (geo_instance.latitude, geo_instance.longitude)
        return geopy.distance.vincenty(self.coords, geo_instance_coords).m
