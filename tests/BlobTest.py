import unittest, sys
sys.path[0]+="\\.."
from classes.Blob import Blob
from classes.BlobTypes import BlobTypes

ENV_SIZE = 20

class TestBlob(unittest.TestCase):

   def test_empty_player(self):
      blob = Blob(ENV_SIZE, BlobTypes.PLAYER)
      self.assertEqual(blob.env_size, ENV_SIZE)
      self.assertEqual(blob.blob_type, BlobTypes.PLAYER)
      self.assertTrue(blob.x>=0 and blob.x<ENV_SIZE)
      self.assertTrue(blob.y>=0 and blob.y<ENV_SIZE)
      self.assertIsNone(blob.range)
      self.assertEqual(blob.__str__(), f"Blob type: {BlobTypes.PLAYER} [r=None] - ({blob.x}, {blob.y})")

   def test_parameterized_player(self):
      blob1 = Blob(ENV_SIZE, BlobTypes.PLAYER, x=10, y=10)
      self.assertEqual(blob1.env_size, ENV_SIZE)
      self.assertEqual(blob1.blob_type, BlobTypes.PLAYER)
      self.assertEqual(blob1.x, 10)
      self.assertEqual(blob1.y, 10)
      self.assertIsNone(blob1.range)
      self.assertEqual(blob1.__str__(), f"Blob type: {BlobTypes.PLAYER} [r=None] - ({blob1.x}, {blob1.y})")

      blob2 = Blob(ENV_SIZE, BlobTypes.PLAYER, x=ENV_SIZE+5, y=ENV_SIZE+5)
      self.assertEqual(blob2.env_size, ENV_SIZE)
      self.assertEqual(blob2.blob_type, BlobTypes.PLAYER)
      self.assertTrue(blob2.x>=0 and blob2.x<ENV_SIZE)
      self.assertTrue(blob2.y>=0 and blob2.y<ENV_SIZE)

   def test_enemy(self):
      blob = Blob(ENV_SIZE, BlobTypes.ENEMY)
      self.assertEqual(blob.env_size, ENV_SIZE)
      self.assertEqual(blob.blob_type, BlobTypes.ENEMY)
      self.assertTrue(blob.x>=0 and blob.x<ENV_SIZE)
      self.assertTrue(blob.y>=0 and blob.y<ENV_SIZE)
      self.assertIsNone(blob.range)

      blob2 = Blob(ENV_SIZE, BlobTypes.ENEMY, x=5, y=5)
      self.assertEqual(blob2.env_size, ENV_SIZE)
      self.assertEqual(blob2.blob_type, BlobTypes.ENEMY)
      self.assertEqual(blob2.x, 5)
      self.assertEqual(blob2.y, 5)
      self.assertIsNone(blob2.range)

      blob3 = Blob(ENV_SIZE, BlobTypes.ENEMY, x=5, y=5, range=2)
      self.assertEqual(blob3.env_size, ENV_SIZE)
      self.assertEqual(blob3.blob_type, BlobTypes.ENEMY)
      self.assertEqual(blob3.x, 5)
      self.assertEqual(blob3.y, 5)
      self.assertEqual(blob3.range, 2)
      
if __name__ == '__main__':
   unittest.main()