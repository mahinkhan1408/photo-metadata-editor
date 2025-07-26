import random
from geopy.distance import distance
from geopy.point import Point
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime, timedelta
import csv

def generate_random_coordinates(center_lat, center_lon, diameter_meters, n_points):
    center = Point(center_lat, center_lon)
    radius = diameter_meters / 2

    coords = []
    for _ in range(n_points):
        bearing = random.uniform(0, 360)
        dist = random.uniform(0, radius)
        destination = distance(meters=dist).destination(center, bearing)
        coords.append((destination.latitude, destination.longitude))
    return coords

def generate_serial_datetimes(date_str, start_time_str, end_time_str, n_points):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        start_dt = datetime.strptime(start_time_str, "%H:%M").time()
        end_dt = datetime.strptime(end_time_str, "%H:%M").time()
    except ValueError:
        raise ValueError("Incorrect date/time format")

    start_datetime = datetime.combine(date_obj, start_dt)
    end_datetime = datetime.combine(date_obj, end_dt)

    if start_datetime >= end_datetime:
        raise ValueError("Start time must be before end time")

    total_seconds = (end_datetime - start_datetime).total_seconds()
    interval = total_seconds / max(n_points - 1, 1)

    datetimes = []
    for i in range(n_points):
        dt = start_datetime + timedelta(seconds=i * interval)
        datetimes.append(dt.s
