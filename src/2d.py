import numpy as np
from typing import List, Container
from turtle import Turtle
import turtle as t
from random import random
from math import sin, cos, pi
from time import sleep


def make_points(num_points: int, *, max_x: int = 100, max_y: int = 100) -> List[Turtle]:
    out = []
    for _ in range(num_points):
        turt = Turtle(shape="circle")
        turt.pu()
        turt.setpos(random() * max_x * 2 - max_x, random() * max_y * 2 - max_y)
        out.append(turt)
    return out


def rotate_points(
    points: List[Turtle], rotations: int, *, speed: float = 1, delay: float = 0
) -> None:
    speed = speed / 180 * pi
    R = np.asarray([[cos(speed), -sin(speed)], [sin(speed), cos(speed)]])
    rot_num = 0
    while rot_num != rotations:
        sleep(delay)
        rot_num += 1
        for turt in points:
            turt.setpos(tuple(np.matmul(R, turt.pos())))


if __name__ == "__main__":
    num_points = 100
    t.tracer(num_points)
    points = make_points(num_points, max_x=300, max_y=300)
    rotate_points(points, -1, speed=.5)
