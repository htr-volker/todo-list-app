import unittest
import time
from flask import url_for
from urllib.request import urlopen

from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from application import app, db
from application.models import Tasks
from os import getenv

class TestBase(LiveServerTestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = getenv("TEST_DATABASE_URI")
        app.config['SECRET_KEY'] = getenv("TEST_SECRET_KEY")
        app.config['LIVESERVER_PORT'] = 5001
        return app

    def setUp(self):
        """Setup the test driver and create test users"""
        print("--------------------------NEXT-TEST----------------------------------------------")
        chrome_options = Options()
        chrome_options.binary_location = "/usr/bin/chromium-browser"
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path="/home/jenkins/chromedriver/chromedriver", chrome_options=chrome_options)
        self.driver.get("http://localhost:5001")
        db.session.commit()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        self.driver.quit()
        print("--------------------------END-OF-TEST----------------------------------------------\n\n\n-------------------------UNIT-AND-SELENIUM-TESTS----------------------------------------------")

    def test_server_is_up_and_running(self):
        response = urlopen("http://localhost:5001")
        self.assertEqual(response.code, 200)

class TestCreateTask(TestBase):
    def test_create_task(self):
        self.driver.find_element_by_xpath("/html/body/a[2]").click()
        time.sleep(1)

        self.driver.find_element_by_xpath('//*[@id="description"]').send_keys("Teach integration testing")
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(1)

        assert url_for('home') in self.driver.current_url

if __name__ == '__main__':
    unittest.main(port=5001)
