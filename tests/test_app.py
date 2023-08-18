import unittest
from app import app

class AstrologyAppTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Введите данные для расчета', response.data.decode())

    def test_valid_form_submission(self):
        response = self.client.post('/', data={
            'date': '2023-08-18',
            'time': '12:00',
            'location': 'New York, USA'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Результаты', response.data.decode())
        self.assertIn('Градусы планет', response.data.decode())
        self.assertIn('Градусы домов (Placidus)', response.data.decode())
        # Добавьте проверки для других систем домов

    def test_invalid_location_submission(self):
        response = self.client.post('/', data={
            'date': '2023-08-18',
            'time': '12:00',
            'location': 'Nonexistent Location'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Место не найдено', response.data.decode())

if __name__ == '__main__':
    unittest.main()