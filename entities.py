import random
import geopy.distance
from drone.consts import SENSOR_MODE_PASSIVE_DETECTING, SENSOR_MODE_PASSIVE_TRACKING, SENSOR_MODE_ACTIVE
from drone.geo_base import GeoEntity
from drone.utils import random_str
import math


class Drone(GeoEntity):
    def __init__(self, latitude, longitude, sample_time):
        GeoEntity.__init__(self, latitude, longitude)
        self.sample_time = sample_time
        self.id = random_str()


class Sensor(GeoEntity):
    def __init__(self,  latitude, longitude, mode=SENSOR_MODE_PASSIVE_DETECTING):
        GeoEntity.__init__(self, latitude, longitude)
        self.mode = mode
        self.id = random_str()
        self.tracked_drone_movement = []
        self.velocity_vector = None

    def alter_mode(self, new_mode):
        self.mode = new_mode

    def scan_perimeter(self):
        while 'nothing is seen':
            pass

        while 'drone detected':
            self.mode = SENSOR_MODE_PASSIVE_TRACKING
            # event of drone detection - random position..

            sample_time = random.uniform(0, 50.0)
            lat1 = random.uniform(0, 50.0)
            lon1 = random.uniform(0, 50.0)

            drone = Drone(lat1, lon1, sample_time)
            self.tracked_drone_movement.append(drone)
            if len(self.tracked_drone_movement) > 1:
                self._update_velocity_vector()

    def _update_velocity_vector(self):
        last_position = self.tracked_drone_movement[-1]
        previous_position = self.tracked_drone_movement[-2]
        time_delta = last_position.sample_time - previous_position.sample_time
        self.velocity_vector = VelocityVector(previous_position.latitude, previous_position.longitude,
                                              last_position.latitude, last_position.longitude, time_delta)

    def land_drone(self):
        self.mode = SENSOR_MODE_ACTIVE
        # do magic


class LandingSite(GeoEntity):
    def __init__(self,  latitude, longitude):
        GeoEntity.__init__(self, latitude, longitude)


class VelocityVector:
    def __init__(self, lat1, lon1, lat2, lon2, sample_time):
        self.lat1 = lat1
        self.lat2 = lat2
        self.lon1 = lon1
        self.lon2 = lon2
        self.sample_time = sample_time

        self.velocity = geopy.distance.vincenty((lat1, lon1), (lat2, lon2)).m / sample_time
        self.bearing = self.calc_bearing()

    def calc_bearing(self):
        d_lon = self.lon2 - self.lon1
        y = math.sin(d_lon) * math.cos(self.lat2)
        x = math.cos(self.lat1)*math.sin(self.lat2) - math.sin(self.lat1)*math.cos(self.lat2)*math.cos(d_lon)
        return math.cos(math.atan2(y, x))
