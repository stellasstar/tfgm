from django import template

from transport.models import Waypoint
from geopy.distance import distance


register = template.Library()


def calc_distance(value, arg, unit="km"):

    if not isinstance(value, Waypoint.location):
        raise TypeError("First value is not a location")
    if not isinstance(arg, Waypoint.location):
        raise TypeError("Argument is not a location")

    if unit == "km":
        return distance(value.get_lat_long(), arg.get_lat_long()).km
    elif unit == "mi":
        return distance(value.get_lat_long(), arg.get_lat_long()).mi


def mi_to(value, arg):
    return calc_distance(value, arg, unit="mi")

register.filter('km_to', calc_distance)
register.filter('mi_to', mi_to)
