import unittest
from unittest import mock
import boto3
from botocore.stub import Stubber

from main import get_user

class TestGetUser(unittest.TestCase):

    def test_get_user(self):
        client = boto3.client('cognito-idp')
        stubber = Stubber(client)
        stubber.add_response('admin_get_user', {
            'Username': 'user',
            'UserAttributes':
                [
                    {'Name': 'sub', 'Value': 'aa45403e-8ba5-42ab-ab27-78a6e9335b23'},
                    {'Name': 'email', 'Value': 'user@example.com'}
                ]
        })
        stubber.activate()
        with mock.patch('boto3.client', mock.MagicMock(return_value=client)):
            user = get_user('user')

        self.assertEqual(user,
                [
                    {'Name': 'sub', 'Value': 'aa45403e-8ba5-42ab-ab27-78a6e9335b23'},
                    {'Name': 'email', 'Value': 'user@example.com'}
                ]
        )

    def test_not_found_user(self):
        client = boto3.client('cognito-idp')
        stubber = Stubber(client)
        stubber.add_client_error('admin_get_user', 'UserNotFoundException')
        stubber.activate()
        with mock.patch('boto3.client', mock.MagicMock(return_value=client)):
            user = get_user('user')

        self.assertIsNone(user)

if __name__ == '__main__':
    unittest.main()
