import json

from django.test import TestCase
from django.test.client import RequestFactory

from .middleware import GeoMiddleware
from .views import geoip


class BaseGeoMiddlewareTest(TestCase):

    def setUp(self):
        self.geo_middleware = GeoMiddleware()

    def test_real_request(self):
        request = RequestFactory(REMOTE_ADDR='173.194.113.110')  # Google IP
        request = request.get("/")

        self.geo_middleware.process_request(request)

        geo_google = {
            'city': u'Mountain View',
            'continent_code': u'NA',
            'region': u'CA',
            'charset': 0,
            'area_code': 650,
            'longitude': -122.05740356445312,
            'country_code3': u'USA',
            'latitude': 37.4192008972168,
            'postal_code': u'94043',
            'dma_code': 807,
            'country_code': u'US',
            'country_name': u'United States'
        }

        self.assertIsInstance(request.GEO, dict)
        self.assertEqual(request.GEO, geo_google)

    def test_local_request(self):
        request = RequestFactory()  # default address is 127.0.0.1
        request = request.get("/")

        self.geo_middleware.process_request(request)

        self.assertEqual(request.GEO, None)


class GeoIPBaseTest(TestCase):

    def test_google_request(self):
        request = RequestFactory(HTTP_X_FORWARDED_FOR='173.194.113.110').get('/')
        response = geoip(request)

        google_json = {
            "City": "Mountain View",
            "IP": "173.194.113.110",
            "Country Code": "US",
            "Proxy": "No",
            "Country": "United States",
            "Latitude": 37.4192008972168,
            "Longitude": -122.05740356445312,
        }

        self.assertEquals(google_json, json.loads(response.content.decode()))
