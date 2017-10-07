import random

from drone.consts import SENSOR_MODE_PASSIVE_TRACKING
from drone.entities import Sensor
from drone import geo_base


def listen():
    sensor1 = Sensor(1, 2)
    sensor2 = Sensor(3, 4)
    sensor3 = Sensor(6, 10)
    landing_site = LandingSite(0, 0)

    # detached..
    sensor1.scan_perimeter()
    sensor2.scan_perimeter()
    sensor3.scan_perimeter()

    while True:
        sensors = [sensor1, sensor2, sensor3]
        detection_sensors = [i for i, x in enumerate(sensors) if x.mode == SENSOR_MODE_PASSIVE_TRACKING]
        possible_sensors_for_handling = []
        threat_detected = False
        for idx in detection_sensors:
            possible_sensors_for_handling.append(sensors[idx])
            if is_a_threat(sensors[idx]):
                threat_detected = True
        if threat_detected:
            handle_threat(choose_sensor(possible_sensors_for_handling, landing_site))


def handle_threat(sensor):
    sensor.land_drone()


def choose_sensor(possible_sensors_for_handling, landing_site):
    # based on the shortest path from drone to destination - choose the closest sensor to middle of path
    middle_of_route_post = calculate_drone_to_landing_site_path_middle_coordinates(possible_sensors_for_handling.
                                                                                   tracked_drone_movement[:-1], landing_site)
    distances_from_sensors_to_middle_of_path = []
    for sensor in possible_sensors_for_handling:
        distances_from_sensors_to_middle_of_path.append(sensor.calculate_distance_from_object(middle_of_route_post))
    minimum_distance = min(distances_from_sensors_to_middle_of_path)
    minimum_idx = distances_from_sensors_to_middle_of_path.index(minimum_distance)
    return possible_sensors_for_handling[minimum_idx]


def calculate_drone_to_landing_site_path_middle_coordinates(drone, landing_site):
    middle_lat = ((drone.latitude - landing_site.latitude) / 2) + landing_site.latitude
    middle_lon = ((drone.longitude - landing_site.longitude) / 2) + drone.longitude
    return geo_base.GeoEntity(middle_lat, middle_lon)


def is_a_threat(sensor):
    # return True if distance & speed & bearing is calculated to threat on compound

    drone_distance_from_sensor = sensor.calculate_distance_from_object(sensor.tracked_drone_movement[-1])
    velocity_vector = sensor.velocity_vector

    if 'bearing, speed and distance considered a threat':
        return True
    return False
