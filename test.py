import pyarchiver
import unittest
import tarfile

class pyArchiverTest(unittest.TestCase):
    tar_archive = 'tar_archive.tar.gz'
    zip_archive = 'zip_archive.zip'

    def test_filetype(self):
        self.assertEqual(pyarchiver.determine_filetype(self.tar_archive), "is_tar")
        self.assertEqual(pyarchiver.determine_filetype(self.zip_archive), "is_zip")

    def test_tar_file_list(self):
        test = [("", ["marples-black"]), ("marples-black", ["gtk-2.0", "gtk-3.0", "metacity-1", ".icon-theme.cache", "down transparent.png", "index.theme", "panelbg.png", "up transparent.png"])]
        with tarfile.open(self.tar_archive) as file:
            self.assertEqual(pyarchiver.tar_file_list(file, ""), ["marples-black"])
            self.assertEqual(pyarchiver.tar_file_list(file, "marples-black"), ["gtk-2.0", "gtk-3.0", "metacity-1", ".icon-theme.cache", "down transparent.png", "index.theme", "panelbg.png", "up transparent.png"])

if __name__ == '__main__':
    unittest.main()
