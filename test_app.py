import unittest
import requests
from main import classify_products


class TestApp(unittest.TestCase):

    def test_api1(self):
        url = "https://master--chevignon.myvtex.com/api/catalog_system/pub/products/search/?_from=1&_to=50"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_api2(self):
        url = "https://master--pepeganga.myvtex.com/api/catalog_system/pub/products/search/?_from=1&_to=50"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_empty_input(self):
        products = []
        keyword = "test"
        result = classify_products(products, keyword)
        self.assertEqual(result, [])

    def test_one_product(self):
        products = [{"id": "1", "name": "Test Product", "description": "This is a test product"}]
        keyword = "test"
        result = classify_products(products, keyword)
        self.assertEqual(len(result), 1)
        self.assertIn("score", result[0])

    def test_multiple_products(self):
        products = [
            {"id": "1", "name": "Test Product 1", "description": "This is a test product 1"},
            {"id": "2", "name": "Test Product 2", "description": "This is a test product 2"},
            {"id": "3", "name": "Another Product", "description": "This is another product"}
        ]
        keyword = "test"
        result = classify_products(products, keyword)
        self.assertEqual(len(result), 2)
        self.assertIn("score", result[0])
        self.assertIn("score", result[1])
        self.assertGreater(result[0]["score"], result[1]["score"])


if __name__ == '__main__':
    unittest.main()
