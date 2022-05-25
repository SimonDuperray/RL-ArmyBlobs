import numpy as np, matplotlib.pyplot as plt

SIZE = 10

arr = np.full((SIZE+1, SIZE+1), -1)
arr[0, 0] = 100

arr = arr[::-1]

print(arr)