from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

def randrange(n, vmin, vmax):
    '''
    Helper function to make an array of random numbers having shape (n, )
    with each number distributed Uniform(vmin, vmax).
    '''
    return (vmax - vmin)*np.random.rand(n) + vmin

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

n = 100
xs = randrange(n, 23, 32)
ys = randrange(n, 0, 100)
zs = randrange(n, np.min(xs), np.max(ys))
# plt.xlim(-1, 51)
# plt.ylim(-1, 101)
ax.plot([2, 2], [3, 3], [4, 4], color="red")

for x, y, z in zip(xs, ys, zs):
   ax.scatter(x, y, z, color='blue')
   plt.pause(.5)


