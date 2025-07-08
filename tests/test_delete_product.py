import unittest
from unittest.mock import patch, MagicMock
from py_client.delete_product import delete_product

class TestDeleteProduct(unittest.TestCase):

    @patch('delete_product.requests.delete')
    def test_successful_delete(self, mock_delete):
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_delete.return_value = mock_response

        self.assertEqual(mock_delete.return_value.status_code, 204)

    @patch('delete_product.requests.delete')
    def test_not_found(self, mock_delete):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_delete.return_value = mock_response

        self.assertEqual(mock_delete.return_value.status_code, 404)