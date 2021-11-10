# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestLikepassController(BaseTestCase):
    """LikepassController integration test stubs"""

    def test_like_or_pass(self):
        """Test case for like_or_pass

        Adds to the list of users this user has asked to connect with or ignore
        """
        response = self.client.open(
            '/crav12345/GoatBoat/{likepass}/{username}'.format(likepass=True, username='username_example'),
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
