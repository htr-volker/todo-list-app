import unittest
from flask import url_for
from flask_testing import TestCase

from application import app, db
from application.models import Tasks

class TestBase(TestCase):
    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI="sqlite:///",
            WTF_CSRF_ENABLED=False, 
            DEBUG=True
        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """
        db.create_all()

        task1 = Tasks(description="My First Task")

        db.session.add(task1)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """
        db.session.remove()
        db.drop_all()

class TestViews(TestBase):
    def test_home_get(self):
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code,200)

    def test_update_get(self):
        response = self.client.get(url_for('update', id=1))
        self.assertEqual(response.status_code,200)

    def test_delete_get(self):
        response = self.client.get(url_for('delete', id=1), follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def test_create_get(self):
        response = self.client.get(url_for('create'))
        self.assertEqual(response.status_code,200)

class TestAdd(TestBase):
    def test_add_post(self):
        response = self.client.post(
            url_for('create'),
            data = dict(description="New task"),
            follow_redirects = True
        )
        self.assertIn(b'New task',response.data)

class TestUpdate(TestBase):
    def test_update_post(self):
        response = self.client.post(
            url_for('update', id=1),
            data = dict(description="Updated task"),
            follow_redirects=True
        )
        self.assertIn(b'Updated task',response.data)
    
    def test_complete_get(self):
        response = self.client.get(
            url_for('complete', id=1),
            follow_redirects=True
        )
        task = Tasks.query.filter_by(id=1).first()
        self.assertEqual(task.completed,True)

    def test_incomplete_get(self):
        response = self.client.get(
            url_for('incomplete', id=1),
            follow_redirects=True
        )
        task = Tasks.query.filter_by(id=1).first()
        self.assertEqual(task.completed,False)

class TestDelete(TestBase):
    def test_delete_post(self):
        response = self.client.get(
            url_for('delete', id=1),
            follow_redirects=True
        )
        self.assertNotIn(b'New task',response.data)