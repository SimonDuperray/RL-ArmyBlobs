import numpy as np

class Blob:
   def __init__(self, env_size, blob_type, x=None, y=None, range=None):
      self.env_size = env_size
      self.blob_type = blob_type
      if x is not None:
         if x<=self.env_size and x>=0:
            self.x = x
         else:
            self.x = np.random.randint(0, self.env_size)
      else:
         self.x = np.random.randint(0, self.env_size)
      if y is not None:
         if y<=self.env_size and y>=0:
            self.y = y
         else:
            self.y = np.random.randint(0, self.env_size)
      else:
         self.y = np.random.randint(0, self.env_size)
      if range is not None:
         self.range = range
      else:
         self.range = None

   def __str__(self):
      return f"Blob type: {self.blob_type} [r={self.range if self.range is not None else None}] - ({self.x}, {self.y})"

   def __sub__(self, blob):
      return (self.x-blob.x, self.y-blob.y)

   def action(self, choice):
      if choice==0:
         self.moove(x=1, y=1)
      elif choice==1:
         self.moove(x=-1, y=-1)
      elif choice==2:
         self.moove(x=-1, y=1)
      elif choice==3:
         self.moove(x=1, y=-1)
      else:
         print(f"Error: Unknown choice: {choice}")

   def moove(self, x=None, y=None):
      if x is not None:
         self.x = x
      else:
         self.x = np.random.randint(-1, 2)
      if y is not None:
         self.y = y
      else:
         self.y = np.random.randint(-1, 2)

      if self.x<0:
         self.x = 0
      elif self.x>self.size-1:
         self.x = self.size-1
      if self.y<0:
         self.y = 0
      elif self.y>self.size-1:
         self.y=self.size-1