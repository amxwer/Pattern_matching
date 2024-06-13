import io
import unittest
from unittest.mock import patch

from PIL import Image

from image_matching.main import load_images_from_directory, compute_image_hash, find_duplicates_by_hash, \
    find_duplicates_in_single_folder, find_duplicates_between_folders


class TestImageProcessing(unittest.TestCase):
    def setUp(self):
        self.image1 = Image.new('RGB', (100, 100), color='red')
        self.image2 = Image.new('RGB', (100, 100), color='blue')
        self.image3 = Image.new('RGB', (100, 100), color='red')

        self.image1_bytes = io.BytesIO()
        self.image1.save(self.image1_bytes, format='JPEG')

        self.image2_bytes = io.BytesIO()
        self.image2.save(self.image2_bytes, format='JPEG')

        self.image3_bytes = io.BytesIO()
        self.image3.save(self.image3_bytes, format='JPEG')

        self.image1_bytes.seek(0)
        self.image2_bytes.seek(0)
        self.image3_bytes.seek(0)

    @patch('os.walk')
    @patch('PIL.Image.open')
    def test_load_images_from_directory(self, mock_image_open, mock_os_walk):
        mock_os_walk.return_value = [
            ('/fake_directory', ('subdir',), ('image1.jpg', 'image2.jpg')),
        ]

        mock_image_open.side_effect = [Image.open(self.image1_bytes), Image.open(self.image2_bytes)]

        images, paths = load_images_from_directory('/fake_directory')

        self.assertEqual(len(images), 2)
        self.assertEqual(paths, ['/fake_directory/image1.jpg', '/fake_directory/image2.jpg'])

    def test_compute_image_hash(self):
        hash1 = compute_image_hash(self.image1)
        hash2 = compute_image_hash(self.image2)
        hash3 = compute_image_hash(self.image3)

        self.assertEqual(hash1, hash3)
        self.assertNotEqual(hash1, hash2)

    def test_find_duplicates_by_hash(self):
        images = [self.image1, self.image2, self.image3]
        paths = ['path/image1.jpg', 'path/image2.jpg', 'path/image3.jpg']

        duplicates = find_duplicates_by_hash(images, paths)

        self.assertEqual(len(duplicates), 1)
        self.assertEqual(duplicates[0], ('path/image3.jpg', 'path/image1.jpg'))

    @patch('main_module.load_images_from_directory')
    def test_find_duplicates_in_single_folder(self, mock_load_images):
        mock_load_images.return_value = (
        [self.image1, self.image2, self.image3], ['path/image1.jpg', 'path/image2.jpg', 'path/image3.jpg'])

        duplicates = find_duplicates_in_single_folder('/fake_directory')

        self.assertEqual(len(duplicates), 1)
        self.assertEqual(duplicates[0], ('path/image3.jpg', 'path/image1.jpg'))

    @patch('main_module.load_images_from_directory')
    def test_find_duplicates_between_folders(self, mock_load_images):
        mock_load_images.side_effect = [
            ([self.image1, self.image2], ['dir1/image1.jpg', 'dir1/image2.jpg']),
            ([self.image3], ['dir2/image3.jpg'])
        ]

        duplicates = find_duplicates_between_folders('/dir1', '/dir2')

        self.assertEqual(len(duplicates), 1)
        self.assertEqual(duplicates[0], ('dir2/image3.jpg', 'dir1/image1.jpg'))


if __name__ == "__main__":
    unittest.main()