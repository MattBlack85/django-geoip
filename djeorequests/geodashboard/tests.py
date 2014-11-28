from django.test import TestCase
from django.test.client import RequestFactory

from djeorequests.geo_middleware.middleware import GeoMiddleware

from .models import Visits


class BaseVisitTest(TestCase):

    def test_request_saved(self):
        request = RequestFactory(REMOTE_ADDR='173.194.113.110')
        request = request.get("/")

        self.assertEquals(Visits.objects.count(), 0)

        gm = GeoMiddleware()
        gm.process_request(request)

        self.assertEquals(Visits.objects.count(), 1)