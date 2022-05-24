import unittest, sys
sys.path[0]+="\\.."
from sr.Blob import Blob
from sr.BlobTypes import BlobTypes

ENV_SIZE = 20

class TestBlob(unittest.TestCase):

   def test_empty_blob(self):
      blob = Blob(ENV_SIZE, BlobTypes.PLAYER)
      self.assertEqual(blob.env_size, ENV_SIZE)
      self.assertEqual(blob.blob_type, BlobTypes.PLAYER)
      self.assertTrue(blob.x>=0 and blob.x<ENV_SIZE)
      self.assertTrue(blob.y>=0 and blob.y<ENV_SIZE)
      self.assertIsNone(blob.range)
      self.assertEqual(blob.__str__(), f"Blob type: {BlobTypes.PLAYER} [r=None] - ({blob.x}, {blob.y})")

if __name__ == '__main__':
   unittest.main()