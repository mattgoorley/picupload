from app import app
import os
import unittest
import tempfile
import shutil
import io

class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        shutil.rmtree(app.config['UPLOAD_FOLDER'])

    def test_image(self):
        response = self.app.post(
            '/', data=dict(picture=(io.BytesIO(b'test'), 'test_file.jpg'),
            follow_redirects=True,
            content_type='multipart/form-data'
        ), follow_redirects=False)
        self.assertIn(b'test_file.jpg', response.data)

if __name__ == '__main__':
    unittest.main()
