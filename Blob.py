import numpy as np

class Blob:
   def __init__(self, env_size, type, x=None, y=None, range=None):
      self.env_size = env_size
      self.type = type
      if x is not None:
         self.x = x
      else:
         self.x = np.random.randint(0, self.env_size)
      if y is not None:
         self.y = y
      else:
         self.y = np.random.randint(0, self.env_size)
      if range is not None:
         self.range = range
      else:
         self.range = None

   def __str__(self):
      pass