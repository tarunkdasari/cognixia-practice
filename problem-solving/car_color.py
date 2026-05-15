class Car:
    def __init__(self, color):
        self.color = color

def find_car_by_color(cars):
    color_counts = {}
    for car in cars:
        if car.color not in color_counts:
            color_counts[car.color] = 0
        color_counts[car.color] += 1

    return color_counts


cars = [
    Car("red"),
    Car("blue"),
    Car("red"),
    Car("black"),
    Car("white"),
    Car("blue"),
    Car("green"),
    Car("black"),
    Car("yellow"),
    Car("red")
]

res = find_car_by_color(cars)
#print(res)
for color, count in res.items():
    print(f"{color}: {count}")