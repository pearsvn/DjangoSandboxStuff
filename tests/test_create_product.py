import unittest
from unittest.mock import patch, MagicMock
import os

from py_client.create_product import create_product

class TestCreateProduct(unittest.TestCase):

    @patch('py_client.create_product.requests.post')
    def test_successful_product_creation(self, mock_post):
        # Mock response setup
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'id': 1, 'title': 'Item'}
        mock_post.return_value = mock_response

        result = create_product()

        # Assert the post was called correctly
        mock_post.assert_called_once()
        self.assertIn('Authorization', result['headers'])
        self.assertEqual(result['status'], 201)
        self.assertEqual(result['response'], {'id': 1, 'title': 'Item'})

    @patch('py_client.create_product.requests.post')
    def test_non_json_response(self, mock_post):
        # Mock response setup
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.side_effect = ValueError("Non-JSON response")
        mock_response.text = 'Bad Request'
        mock_post.return_value = mock_response

        result = create_product()

        self.assertEqual(result['status'], 400)
        self.assertEqual(result['response'], 'Bad Request')
        self.assertTrue(result.get('non_json', False))

    @patch('py_client.create_product.requests.post')
    def test_correct_headers_and_payload(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'id': 2, 'title': 'Item'}
        mock_post.return_value = mock_response

        result = create_product()

        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['json'], {'title': 'Item', 'content': 'Content', 'price': 1.99})
        self.assertIn('Authorization', kwargs['headers'])

if __name__ == '__main__':
    unittest.main()