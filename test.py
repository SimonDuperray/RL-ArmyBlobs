import math

circle = ((3, 2), 2)
p = (4, 4)

def is_inside_circle(c, p):
   return round(math.dist(c[0], p), 2)<float(circle[1])

print(math.dist((2, 2), (1, 1)))