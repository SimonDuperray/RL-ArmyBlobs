import unittest, sys
sys.path[0]+="\\.."
from classes.Warzone import Warzone

ENV_SIZE = 20

class TestWarzone(unittest.TestCase):
   def are_lists_equivalents(self, a, b):
      return all(elem in a for elem in b) and all(elem in b for elem in a)


   def one_wall(self):
      warzone = Warzone(size=ENV_SIZE)
      self.assertEqual(warzone.size, ENV_SIZE)
      warzone.build_wall((2, 3), 4, 2)
      pts = [(2, 3), (2, 4), (2, 5), (3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5), (6, 3), (6, 4), (6, 5)]
      self.assertTrue(self.are_lists_equivalents(warzone.get_walls(), pts))

   def two_walls(self):
      warzone = Warzone(size=ENV_SIZE)
      self.assertEqual(warzone.size, ENV_SIZE)
      warzone.build_wall((0, 14), 5, 6)
      warzone.build_wall((5, 9), 2, 5)
      pts = [(5, 9), (5, 10), (5, 11), (5, 12), (5, 13), (5, 14), (6, 9), (6, 10), (6, 11), (6, 12), (6, 13), (6, 14), (6, 9), (6, 10), (6, 11), (6, 12), (6, 13), (6, 14)]
      self.assertTrue(self.are_lists_equivalents(warzone.get_walls(), pts))

if __name__ == "__main__":
   unittest.main()