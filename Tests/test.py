"""
test.py

This module contains unit tests for the Flask-specific functions.
It tests the functionality of the Flask app, including routes and filtering by actor and genre.
"""
import unittest
from app import app, get_filtered_by_actor

class FlaskAppTestCase(unittest.TestCase):
    """Test class for the Flask app."""

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_homepage(self):
        """Test the home page returns status 200 and expected instructions."""
        response = self.app.get('/')
        self.assertIn(b'Welcome to Streaming Media', response.data)

    def test_valid_actor(self):
        """Standard: Test filtering by a valid actor name returns expected results."""
        response = self.app.get('/actor/Brendan Gleeson')
        self.assertIn(b'Results for actor: Brendan Gleeson', response.data)
        self.assertIn(b'The Grand Seduction', response.data)

    def test_invalid_actor(self):
        """Edge case: actor not in dataset should return specific message."""
        response = self.app.get('/actor/Nonexistent Actor')
        self.assertIn(b'No entries found', response.data)

    def test_actor_case_insensitive(self):
        """Edge case: actor name matching should be case-insensitive."""
        results_upper = get_filtered_by_actor("BRENDAN GLEESON")
        results_lower = get_filtered_by_actor("brendan gleeson")
        self.assertEqual(results_upper.keys(), results_lower.keys())

    def test_filter_by_genre(self):
        """Standard: Test filtering by a valid genre returns expected results."""
        response = self.app.get('/genre/Crime')
        self.assertIn(b'Silent Night', response.data)
    
    def test_invalid_genre(self):
        """Edge case: genre not in dataset should return specific message."""
        response = self.app.get('/genre/Nonexistent')
        self.assertIn(b'No entries found', response.data)

if __name__ == '__main__':
    unittest.main()
