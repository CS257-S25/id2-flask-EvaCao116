"""
test.py

This module contains unit tests for the Flask-specific functions.
"""
import unittest
from app import app, get_filtered_by_actor

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_homepage(self):
        """Test the home page returns status 200 and expected instructions."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Streaming Media', response.data)

    def test_valid_actor(self):
        """Test filtering by a valid actor name returns expected results."""
        response = self.app.get('/actor/Brendan Gleeson')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Results for actor: Brendan Gleeson', response.data)

    def test_invalid_actor(self):
        """Edge case: actor not in dataset should return 404."""
        response = self.app.get('/actor/Nonexistent Actor')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'No entries found for actor', response.data)

    def test_actor_case_insensitive(self):
        """Edge case: actor name matching should be case-insensitive."""
        results_upper = get_filtered_by_actor("BRENDAN GLEESON")
        results_lower = get_filtered_by_actor("brendan gleeson")
        self.assertEqual(results_upper.keys(), results_lower.keys())

    def test_empty_actor(self):
        """Edge case: empty actor string should return all or none based on logic."""
        results = get_filtered_by_actor("")
        self.assertEqual(len(results), 0)  # or > 0 if your logic handles empty as 'no filter'

if __name__ == '__main__':
    unittest.main()
