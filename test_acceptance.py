import unittest
from selenium import webdriver
from threading import Thread
from app import app

class TestAcceptance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server_thread = Thread(target=app.run, kwargs={'port': 8943, 'debug': False, 'use_reloader': False})
        cls.server_thread.setDaemon(True)
        cls.server_thread.start()
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        # To stop the Flask server you may need to use another method depending on your environment.

    def test_index(self):
        self.driver.get('http://127.0.0.1:8943/')
        self.assertIn("Tournament Results", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
