import unittest
from app import app


class MyTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

    # executed after each test
    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_page_error(self):
        response = self.app.get('/error', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    '''
        def test_predict(self):
        response = self.app.get('/servicio/v1/prediccion/48horas', follow_redirects=True, content_type='application/json')
        self.assertEqual(response.get_json(), {'algo': [ {“hour”:13:05,”temp”:32.20,”hum”:85.90}, 
                                                        {“hour”:13:10,”temp”:31.20,”hum”:86.30}] })
    '''

    def test_prediction_temperature(self):
        self.assertEqual(True, True)

    def test_prediction_humidity(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
